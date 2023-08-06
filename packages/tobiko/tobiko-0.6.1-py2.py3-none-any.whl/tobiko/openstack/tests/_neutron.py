from __future__ import absolute_import

import collections
import functools
import json
import re
import typing

from keystoneauth1 import exceptions
import netaddr
from oslo_log import log

import tobiko
from tobiko.openstack import neutron
from tobiko.openstack import topology
from tobiko.shell import ip
from tobiko.shell import sh
from tobiko.tripleo import pacemaker

LOG = log.getLogger(__name__)


# Supported OVN DB service models
RAFT = 'RAFT'
HA = 'HA'
# Supported OVN databases
OVNDBS = ('nb', 'sb')
DBNAMES = {'nb': 'OVN_Northbound', 'sb': 'OVN_Southbound'}


def build_ovn_db_show_dict(ovn_db_show_str):
    # returns a dictionary with OVN NB or OVN SB DB information
    # each dict key is a section from the OVN DB command output
    # each dict value is a list of strings
    ovn_master_db_dict = {}
    for line in ovn_db_show_str.splitlines():
        if not re.match(r'^\s+', line):
            # if line does not start with a space char, a new section will be
            # started, i.e. a new dict entry
            current_ovn_section = line.strip()
            ovn_master_db_dict[current_ovn_section] = []
        else:
            ovn_master_db_dict[current_ovn_section].append(line.strip())

    for section in ovn_master_db_dict:
        ovn_master_db_dict[section].sort()
    return ovn_master_db_dict


def test_neutron_agents_are_alive(timeout=300., interval=5.) \
        -> tobiko.Selection[neutron.NeutronAgentType]:
    for attempt in tobiko.retry(timeout=timeout, interval=interval):
        LOG.debug("Look for unhealthy Neutron agents...")
        try:
            # get Neutron agent list
            agents = neutron.list_agents()
        except (neutron.ServiceUnavailable,
                neutron.NeutronClientException,
                exceptions.connection.ConnectFailure) as ex:
            if attempt.is_last:
                raise
            else:
                # retry because Neutron server could still be unavailable
                # after a disruption
                LOG.debug(f"Waiting for neutron service... ({ex})")
                continue  # Let retry

        dead_agents = agents.with_items(alive=False)
        if dead_agents:
            dead_agents_details = json.dumps(agents, indent=4, sort_keys=True)
            if attempt.is_last:
                tobiko.fail("Unhealthy agent(s) found:\n"
                            f"{dead_agents_details}\n")
            else:
                # retry because some Neutron agent could still be unavailable
                # after a disruption
                LOG.debug("Waiting for Neutron agents to get alive...\n"
                          f"{dead_agents_details}")
                continue

        LOG.debug(f"All {len(agents)} Neutron agents are alive.")
        break
    else:
        raise RuntimeError("Retry loop broken")

    return agents


def ovn_dbs_vip_bindings(test_case):
    ovn_conn_str = get_ovn_db_connections()
    db_service_model = get_ovn_db_service_model()
    # ovn db sockets might be centrillized or distributed
    # that depends on the openstack version under test
    sockets_centrallized = topology.verify_osp_version('14.0', lower=True)
    for db in OVNDBS:
        found_centralized = False
        addrs, port = parse_ips_from_db_connections(ovn_conn_str[db])
        if db_service_model == RAFT:
            addrs.append(netaddr.IPAddress('0.0.0.0'))
        for node in topology.list_openstack_nodes(group='controller'):
            socs = get_ovn_db_socket_info(node.hostname, port)
            if sockets_centrallized and not socs:
                continue
            test_case.assertEqual(1, len(socs))
            test_case.assertIn(socs[0]['addr'], addrs)
            test_case.assertEqual(socs[0]['process'], 'ovsdb-server')
            if sockets_centrallized:
                test_case.assertFalse(found_centralized)
                found_centralized = True
        if sockets_centrallized:
            test_case.assertTrue(found_centralized)


def get_ovn_db_connections():
    """Fetches OVN DB connection strings from ml2_conf.ini file

    In HA environments there is a single IP address in the connection
    string <PROTO>:<ADDR>:<PORT>. There is always cluster virtual IP
    address.
        tcp:172.17.1.95:6641
        ssl:172.17.1.95:6641
        tcp:[fd00:fd00:fd00:2000::356]:6641

    In RAFT environments there are separate IP address for each cluster
    member divided by comma. Protocols and ports should be similar in such
    a configuration.
        tcp:172.17.1.24:6641,tcp:172.17.1.90:6641,tcp:172.17.1.115:6641
    """
    ml2_conf = topology.get_config_file_path('ml2_conf.ini')
    ctl_ssh = topology.list_openstack_nodes(group='controller')[0].ssh_client
    con_strs = {}
    for db in OVNDBS:
        cmd = 'crudini --get {} ovn ovn_{}_connection'.format(ml2_conf, db)
        output = sh.execute(cmd, ssh_client=ctl_ssh, sudo=True).stdout
        con_strs[db] = output.splitlines()[0]
    LOG.debug('OVN DB connection string fetched from {} file: {}'.format(
        ml2_conf, con_strs))
    return con_strs


class InvalidDBConnString(tobiko.TobikoException):
    pass


def parse_ips_from_db_connections(con_str):
    """Parse OVN DB connection string to get IP addresses

    In HA environments there is a single IP address in the connection
    string <PROTO>:<ADDR>:<PORT>. There is always cluster virtual IP
    address.
        tcp:172.17.1.95:6641
        ssl:172.17.1.95:6641
        tcp:[fd00:fd00:fd00:2000::356]:6641

    In RAFT environments there are separate IP address for each cluster
    member divided by comma. Protocols and ports should be similar in such
    a configuration.
        tcp:172.17.1.24:6641,tcp:172.17.1.90:6641,tcp:172.17.1.115:6641
    """
    addrs = []
    ref_port = ''
    ref_protocol = ''
    for substr in con_str.split(','):
        try:
            protocol, con = substr.split(':', 1)
            tmp_addr, port = con.rsplit(':', 1)
        except (ValueError, AttributeError) as ex:
            msg = 'Fail to parse "{}" substring of "{}" OVN DB connection '\
                    'string'.format(substr, con_str)
            LOG.error(msg)
            raise InvalidDBConnString(message=msg) from ex
        if not ref_port:
            ref_port = port
        if not ref_protocol:
            ref_protocol = protocol
        if protocol != ref_protocol or port != ref_port:
            msg = 'Ports or protocols are not identical for OVN DB'\
                    'connections: {}'.format(con_str)
            LOG.error(msg)
            raise InvalidDBConnString(message=msg)
        try:
            addr = netaddr.IPAddress(tmp_addr.strip(']['))
        except ValueError as ex:
            msg = 'Invalid IP address "{}" in "{}"'.format(addr, con_str)
            LOG.error(msg)
            raise InvalidDBConnString(message=msg) from ex
        addrs.append(addr)
    LOG.debug('Addresses are parsed from OVN DB connection string: {}'.format(
        addrs))
    return addrs, ref_port


class ParsingError(tobiko.TobikoException):
    pass


def get_ovn_db_socket_info(hostname, port):
    """Parse SS output for details about open port"""
    socs = []
    cmd = 'ss -Hp state listening sport = {}'.format(port)
    node_ssh = topology.get_openstack_node(hostname=hostname).ssh_client
    output = sh.execute(cmd, ssh_client=node_ssh, sudo=True).stdout
    for soc_details in output.splitlines():
        try:
            _, _, _, con_tuple, _, process_info = soc_details.split()
            addr = netaddr.IPAddress(con_tuple.split(':')[0])
            proc = process_info.split('"')[1]
        except (ValueError, AttributeError, IndexError) as ex:
            msg = 'Fail getting socket infornation from "{}"'.format(
                    soc_details)
            LOG.error(msg)
            raise ParsingError(message=msg) from ex
        LOG.debug('Parsed "{}" ip address and "{}" process name from "{}"'.
                  format(addr, proc, soc_details))
        socs.append({'addr': addr, 'process': proc})
    return socs


def ovn_dbs_are_synchronized(test_case):
    """Check that OVN DBs are syncronized across all controller nodes"""
    db_model = get_ovn_db_service_model()
    db_sync_status = get_ovn_db_sync_status()
    if db_model == HA:
        # In Active-Backup service model we expect the same controller to be
        # active for both databases. This controller node should be configured
        # for virtual IP in pacemaker. Other controllers should be in backup
        # state
        ovn_master_node_name = pacemaker.get_ovn_db_master_node()
        test_case.assertEqual(1, len(ovn_master_node_name))
        ovn_master_node = topology.get_openstack_node(ovn_master_node_name[0])
        LOG.debug("OVN DB master node hostname is: {}".format(
            ovn_master_node.hostname))
        for db in OVNDBS:
            for controller, state in db_sync_status[db]:
                if controller == ovn_master_node.hostname:
                    test_case.assertEqual('active', state)
                else:
                    test_case.assertEqual('backup', state)
    elif db_model == RAFT:
        # In clustered database service model we expect all databases to be
        # active
        for db in OVNDBS:
            for _, state in db_sync_status[db]:
                test_case.assertEqual('active', state)
    dumps = dump_ovn_databases()
    for db in OVNDBS:
        if len(dumps[db]) <= 1:
            # Database from a single node is available
            # so there is nothing to compare it with
            continue
        for i in range(1, len(dumps[db])):
            test_case.assertEqual(dumps[db][0][1], dumps[db][i][1])
            LOG.debug('OVN {} databases are equal on {} and {}'.format(
                db, dumps[db][0][0], dumps[db][i][0]))


def find_ovn_db_sockets():
    """Search for OVN DB sockets

    Unix sockets are useful in case there is a need to check the local
    database.
    """
    node_ssh = topology.list_openstack_nodes(group='controller')[0].ssh_client
    socs = sh.execute('ss -ax state listening', ssh_client=node_ssh, sudo=True)
    sockets = {}
    for db in OVNDBS:
        pattern = '[^ ]*ovn{}_db.sock'.format(db)
        sockets[db] = re.search(pattern, socs.stdout, re.MULTILINE).group()
    LOG.debug('OVN DB socket files found: {}'.format(sockets))
    return sockets


def dump_ovn_databases():
    """Dump NB and SB on each controller node"""
    from tobiko.tripleo import containers
    runtime_name = containers.get_container_runtime_name()
    sockets = find_ovn_db_sockets()
    db_mode = get_ovn_db_service_model()
    # To be able to connect to local database in RAFT environment
    # --no-leader-only parameter should be specified
    no_leader = (' --no-leader-only' if db_mode == 'RAFT' else '')
    dumps = {}
    for node in topology.list_openstack_nodes(group='controller'):
        for db in OVNDBS:
            connection = '--db=unix:{}{}'.format(sockets[db], no_leader)
            cmd = '{} exec -uroot ovn_controller ovn-{}ctl {} show'.format(
                    runtime_name, db, connection)
            LOG.debug('Dump {} database on {} with following command: {}'.
                      format(db, node.hostname, cmd))
            output = sh.execute(cmd, ssh_client=node.ssh_client, sudo=True)
            dumps.setdefault(db, [])
            dumps[db].append(
                    [node.hostname, build_ovn_db_show_dict(output.stdout)])
    return dumps


def find_ovn_db_ctl_files():
    """Search for ovnsb_db.ctl and ovnnb_db.ctl files"""
    node = topology.list_openstack_nodes(group='controller')[0]
    ctl_files = {}
    for db in OVNDBS:
        cmd = 'find /var/ -name ovn{}_db.ctl'.format(db)
        found = sh.execute(cmd, ssh_client=node.ssh_client, sudo=True).stdout
        ctl_files[db] = found.strip()
    LOG.debug('OVN DB ctl files found: {}'.format(ctl_files))
    return ctl_files


def get_ovn_db_sync_status():
    """Query sync status for NB and SB for each controller node"""
    db_sync_status = {}
    ctl_files = find_ovn_db_ctl_files()
    for node in topology.list_openstack_nodes(group='controller'):
        for db in OVNDBS:
            ctl_file = ctl_files[db]
            cmd = 'ovs-appctl -t {} ovsdb-server/sync-status'.format(ctl_file)
            output = sh.execute(cmd, ssh_client=node.ssh_client, sudo=True)
            db_status = output.stdout
            if 'state: active' in db_status:
                status = 'active'
            elif 'state: backup' in db_status:
                status = 'backup'
            else:
                status = 'unknown'
            db_sync_status.setdefault(db, [])
            db_sync_status[db].append([node.hostname, status])
    LOG.debug('OVN DB status for all controllers: {}'.format(db_sync_status))
    return db_sync_status


class InvalidDBServiceModel(tobiko.TobikoException):
    message = "Database service model is not supported:\n{db_string}"


@functools.lru_cache()
def get_ovn_db_service_model():
    """Show in which mode OVN databases are configured

    There are two modes currently supported:
     - RAFT aka clustered service model (default starting OSP17.0)
     - HA aka Active-Backup service model (default for pre-OSP17.0 versions)

    For more information:
    https://docs.openvswitch.org/en/latest/ref/ovsdb.7/#service-models
    """
    controller0 = topology.list_openstack_nodes(group='controller')[0]
    db_info = sh.execute('find / -name ovnnb_db.db | xargs sudo head -n 1',
                         ssh_client=controller0.ssh_client, sudo=True)
    if 'CLUSTER' in db_info.stdout:
        return RAFT
    elif 'JSON' in db_info.stdout:
        return HA
    else:
        LOG.error('Only RAFT and HA database service models are supported')
        raise InvalidDBServiceModel(db_string=db_info.stdout)


def test_ovn_dbs_validations():
    if not neutron.has_ovn():
        LOG.debug('OVN not configured. OVN DB sync validations skipped')
        return

    test_case = tobiko.get_test_case()

    ovn_dbs_are_synchronized(test_case)
    ovn_dbs_vip_bindings(test_case)


class RAFTStatusError(tobiko.TobikoException):
    pass


def get_raft_cluster_details(hostname, database):
    """Return RAFT cluster details from specific node as dictionary"""
    if database not in OVNDBS:
        raise ValueError('{} database is not in the list {}'.format(
            database, OVNDBS))
    ctl_files = find_ovn_db_ctl_files()
    cmd = 'ovs-appctl -t {} cluster/status {}'.format(ctl_files[database],
                                                      DBNAMES[database])
    node_ssh = topology.get_openstack_node(hostname=hostname).ssh_client
    output = sh.execute(cmd, ssh_client=node_ssh, sudo=True).stdout
    cluster_status = {}
    for line in output.splitlines():
        if not re.match(r'^\s+', line):
            line_data = line.strip().split(':', 1)
            if len(line_data) == 1:
                continue
            section, data = line_data
            if not data.strip():
                cluster_status[section] = []
                continue
            cluster_status[section] = data.strip()
        else:
            cluster_status[section].append(line.strip())
    return cluster_status


def collect_raft_cluster_details(database):
    """Collect RAFT cluster details from all controllers

    Data collection should be restarted if one of the nodes has `candidate`
    role as it means that there is leader election in progress
    """
    for _ in tobiko.retry(timeout=30, interval=1):
        restart_collection = False
        cluster_details = []
        for node in topology.list_openstack_nodes(group='controller'):
            details = get_raft_cluster_details(node.hostname, database)
            if details['Role'].lower() == 'candidate':
                LOG.warning('Cluster not stable. Leader election in progress')
                LOG.debug('Cluster details from {} node:\n{}'.format(
                    node.hostname, details))
                restart_collection = True
                break
            cluster_details.append(details)
        if not restart_collection:
            break
    return cluster_details


def check_raft_timers(node_details):
    election_timer = int(node_details['Election timer'])
    leader_id = node_details['Leader']
    for srv_str in node_details['Servers']:
        if 'self' in srv_str:
            continue
        if node_details['Role'] == 'follower' and \
                not srv_str.startswith(leader_id):
            # There is no active connection between followers
            continue
        timer = re.findall(r'last msg [0-9]+ ms ago', srv_str)
        if len(timer) != 1:
            msg = 'Failed to parse connection timer from "{}"'.format(srv_str)
            LOG.error(msg)
            LOG.debug(node_details)
            raise RAFTStatusError(message=msg)
        if election_timer < int(timer[0].split()[2]):
            msg = 'Cluster communication time {} is higher then election'\
                  ' timer {}'.format(int(timer.split()[2]), election_timer)
            LOG.error(msg)
            LOG.debug(node_details)
            raise RAFTStatusError(message=msg)


def get_raft_ports():
    node = topology.list_openstack_nodes(group='controller')[0]
    ports = {}
    for db in OVNDBS:
        cluster_details = get_raft_cluster_details(node.hostname, db)
        _, port = parse_ips_from_db_connections(cluster_details['Address'])
        ports[db] = port
    return ports


def test_raft_cluster():
    if get_ovn_db_service_model() != RAFT:
        return
    test_case = tobiko.get_test_case()
    cluster_ports = get_raft_ports()
    for db in OVNDBS:
        cluster_details = collect_raft_cluster_details(db)
        leader_found = False
        for node_details in cluster_details:
            check_raft_timers(node_details)
            if node_details['Role'] == 'leader':
                test_case.assertFalse(leader_found)
                leader_found = True
        test_case.assertTrue(leader_found)
        for node in topology.list_openstack_nodes(group='controller'):
            node_ips = ip.list_ip_addresses(ssh_client=node.ssh_client)
            socs = get_ovn_db_socket_info(node.hostname, cluster_ports[db])
            test_case.assertEqual(1, len(socs))
            test_case.assertIn(socs[0]['addr'], node_ips)
            test_case.assertEqual(socs[0]['process'], 'ovsdb-server')


def test_ovs_bridges_mac_table_size():
    test_case = tobiko.get_test_case()
    expected_mac_table_size = '50000'
    get_mac_table_size_cmd = ('ovs-vsctl get bridge {br_name} '
                              'other-config:mac-table-size')
    if neutron.has_ovn():
        get_br_mappings_cmd = ('ovs-vsctl get Open_vSwitch . '
                               'external_ids:ovn-bridge-mappings')
    else:
        get_br_mappings_cmd = (
            'crudini --get /var/lib/config-data/puppet-generated/neutron/'
            'etc/neutron/plugins/ml2/openvswitch_agent.ini '
            'ovs bridge_mappings')
    for node in topology.list_openstack_nodes(group='overcloud'):
        try:
            br_mappings_str = sh.execute(get_br_mappings_cmd,
                                         ssh_client=node.ssh_client,
                                         sudo=True).stdout.splitlines()[0]
        except sh.ShellCommandFailed:
            LOG.debug(f"bridge mappings not configured on node '{node.name}'",
                      exc_info=1)
            continue
        br_list = [br_mapping.split(':')[1] for br_mapping in
                   br_mappings_str.replace('"', '').split(',')]
        for br_name in br_list:
            mac_table_size = sh.execute(
                get_mac_table_size_cmd.format(br_name=br_name),
                ssh_client=node.ssh_client, sudo=True).stdout.splitlines()[0]
            test_case.assertEqual(mac_table_size.replace('"', ''),
                                  expected_mac_table_size)


OPENSTACK_NODE_GROUP = re.compile(r'(compute|controller|overcloud)')
OVS_NAMESPACE = re.compile(r'(qrouter.*|qdhcp.*|snat.*|fip.*)')


def test_ovs_namespaces_are_absent(
        group: typing.Pattern[str] = OPENSTACK_NODE_GROUP,
        namespace: typing.Pattern[str] = OVS_NAMESPACE):
    nodes = topology.list_openstack_nodes(group=group)

    namespaces: typing.Dict[str, typing.List[str]] = (
        collections.defaultdict(list))
    for node in nodes:
        for node_namespace in ip.list_network_namespaces(
                ssh_client=node.ssh_client, sudo=True):
            if namespace.match(node_namespace):
                namespaces[node.name].append(node_namespace)
    namespaces = dict(namespaces)

    test_case = tobiko.get_test_case()
    test_case.assertEqual(
        {}, dict(namespaces),
        f"OVS namespace(s) found on OpenStack nodes: {namespaces}")


OVS_INTERFACE = re.compile(r'(qvo.*|qvb.*|qbr.*|qr.*|qg.*|fg.*|sg.*)')


def test_ovs_interfaces_are_absent(
        group: typing.Pattern[str] = OPENSTACK_NODE_GROUP,
        interface: typing.Pattern[str] = OVS_INTERFACE):
    nodes = topology.list_openstack_nodes(group=group)

    interfaces: typing.Dict[str, typing.List[str]] = (
        collections.defaultdict(list))
    for node in nodes:
        for node_interface in ip.list_network_interfaces(
                ssh_client=node.ssh_client, sudo=True):
            if interface.match(node_interface):
                interfaces[node.name].append(node_interface)
    interfaces = dict(interfaces)

    test_case = tobiko.get_test_case()
    test_case.assertEqual(
        {}, interfaces,
        f"OVS interface(s) found on OpenStack nodes: {interfaces}")
