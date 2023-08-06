from typing import Optional, Union, Any, List, Dict


from dataclasses import dataclass
import datetime
import ipaddress


@dataclass
class DeviceData:

    id: int
    type_id: int
    name: str
    entrance: int
    ip: ipaddress.IPv4Address
    host: str
    mac: str
    comment: str
    inventory_id: int
    location: str
    uplink_iface: list[int]
    dnlink_iface: list[int]
    node_id: int
    customer_id: int
    interfaces: int
    podezd: int
    activity_time: datetime.datetime
    uplink_iface_array: list[int]
    dnlink_iface_array: list[int]
    is_online: int
    snmp_proto: int
    snmp_community_ro: str
    snmp_community_rw: str
    snmp_port: int
    telnet_login: str
    telnet_pass: str

    def __post_init__(self):
        if isinstance(self.activity_time, str):
            self.activity_time = datetime.datetime.strptime(self.activity_time, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.ip, str):
            self.ip = ipaddress.ip_address(int(self.ip))
        if isinstance(self.uplink_iface, str):
            self.uplink_iface = [int(port) for port in self.uplink_iface.split(',') if port]
        if isinstance(self.dnlink_iface, str):
            self.dnlink_iface = [int(port) for port in self.dnlink_iface.split(',') if port]
        if isinstance(self.uplink_iface_array, dict):
            self.uplink_iface_array = list(self.uplink_iface_array.keys())
        if isinstance(self.dnlink_iface_array, dict):
            self.dnlink_iface_array = list(self.dnlink_iface_array.keys())


@dataclass
class DeviceDataWithIfaces(DeviceData):
    ifaces: Optional[Dict[str, Dict[str, Union[str, int]]]]
