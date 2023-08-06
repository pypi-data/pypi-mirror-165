from typing import Optional, Union, Any, List, Dict


from dataclasses import dataclass
import datetime
import ipaddress


@dataclass
class DeviceData:
    ACTIVITY_UPDATE_BY: int
    AZIMUT: int
    BASECODE: int
    CABLELEN: int
    CODE: int
    COLCOL: str
    COM_LOGIN: str
    COM_PASS: str
    COM_PRIVATE: str
    COM_PUBLIC: str
    CUSTOM_IFACE_LIST: str
    DATEADD: Optional[datetime.datetime]
    DATEPELENG: Optional[datetime.datetime]
    DATE_CABLETEST: Optional[datetime.datetime]
    DATE_IFERR: Optional[datetime.datetime]
    DATE_LAST_ACTIVITY: datetime.datetime
    DEVTYPER: int
    DNPORT: List
    FDPVER: int
    FLAG_CUSTOM_COORD: int
    HASH_PORT2: str
    HOSTNAME: str
    ID: int
    IPABON: int
    IPPORT: str
    ISMAILSEND: int
    ISSMSSEND: int
    IS_ALWAYS_ON_MAP: Optional[Any]
    IS_MESENGER_NOTIFY_ENABLE: int
    IS_MESENGER_NOTIFY_SEND: int
    IS_PELENG: int
    LATITUDE: str
    LEVEL_MAX: int
    LEVEL_MIN: int
    LOCATION: str
    LOG_STATUS: int
    LONGITUDE: str
    NAZV: str
    ONMAIL: int
    ONSMS: int
    OPIS: str
    OPTIONS: str
    PORT: int
    PROFILE: int
    PROSHIVKA: str
    PROSHIVKA_DATE: Optional[datetime.datetime]
    ROTATION: int
    SECTCOORD: str
    SFP_ATT_LIST: str
    SKLADCODE: int
    SNMPVER: int
    SNMP_DONTASK: int
    SNMP_PORT: int
    SNMP_V3_AUTH_PASSPHRASE: str
    SNMP_V3_AUTH_PROTOCOL: str
    SNMP_V3_PRIV_PASSPHRASE: str
    SNMP_V3_PRIV_PROTOCOL: str
    SNMP_V3_SECURITY_NAME: str
    SNMP_V3_SEC_LEVEL: str
    TELNET_ENABLE_PASSWORD: str
    UPPORT: List
    USERCODE: int
    UZELCODE: int
    VALUEMEMO: str
    X1: int
    Y1: int
    _LASTACT: str
    _lastact: str
    activity_time: Optional[datetime.datetime]
    activity_update_by: int
    azimut: int
    basecode: int
    cablelen: str
    code: int
    colcol: str
    com_login: str
    com_pass: str
    com_private: str
    com_public: str
    comment: str
    custom_iface_list: str
    date_cabletest: Optional[datetime.datetime]
    date_iferr: Optional[datetime.datetime]
    date_last_activity: Optional[datetime.datetime]
    dateadd: Optional[datetime.datetime]
    datepeleng: Optional[datetime.datetime]
    devtyper: int
    dnlink_iface: List
    dnlink_iface_array: List
    dnport: List
    entrance: int
    fdpver: int
    flag_custom_coord: int
    hash_port2: str
    host: str
    hostname: str
    id: int
    interfaces: int
    inventory_id: int
    ip: ipaddress.IPv4Address
    ipabon: str
    ipport: str
    is_always_on_map: Optional[Any]
    is_mesenger_notify_enable: int
    is_mesenger_notify_send: int
    is_online: int
    is_peleng: int
    ismailsend: int
    issmssend: int
    latitude: str
    level_max: int
    level_min: int
    location: str
    log_status: int
    longitude: str
    mac: str
    name: str
    nazv: str
    node_id: int
    onmail: int
    onsms: int
    opis: str
    options: str
    podezd: int
    port: int
    profile: int
    proshivka: str
    proshivka_date: Optional[datetime.datetime]
    rotation: int
    sectcoord: str
    sfp_att_list: str
    skladcode: int
    snmp_community_ro: str
    snmp_community_rw: str
    snmp_dontask: int
    snmp_port: int
    snmp_proto: int
    snmp_v3_auth_passphrase: str
    snmp_v3_auth_protocol: str
    snmp_v3_priv_passphrase: str
    snmp_v3_priv_protocol: str
    snmp_v3_sec_level: str
    snmp_v3_security_name: str
    snmpver: int
    telnet_enable_password: str
    telnet_login: str
    telnet_pass: str
    type_id: int
    uplink_iface: List
    uplink_iface_array: List
    upport: List
    usercode: int
    uzelcode: int
    valuememo: str
    x1: int
    y1: int

    def __post_init__(self):
        if isinstance(self.date_cabletest, str):
            self.date_cabletest = datetime.datetime.strptime(self.date_cabletest, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.DATEADD, str):
            self.DATEADD = datetime.datetime.strptime(self.DATEADD, '%Y-%m-%d')
        if isinstance(self.DATEPELENG, str):
            self.DATEPELENG = datetime.datetime.strptime(self.DATEPELENG, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.DATE_CABLETEST, str):
            self.DATE_CABLETEST = datetime.datetime.strptime(self.DATE_CABLETEST, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.DATE_IFERR, str):
            self.DATE_IFERR = datetime.datetime.strptime(self.DATE_IFERR, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.DATE_LAST_ACTIVITY, int):
            self.DATE_LAST_ACTIVITY = datetime.datetime.fromtimestamp(self.DATE_LAST_ACTIVITY)
        if isinstance(self.PROSHIVKA_DATE, str):
            self.PROSHIVKA_DATE = datetime.datetime.strptime(self.PROSHIVKA_DATE, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.activity_time, str):
            self.activity_time = datetime.datetime.strptime(self.activity_time, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.date_cabletest, str):
            self.date_cabletest = datetime.datetime.strptime(self.date_cabletest, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.date_iferr, str):
            self.date_iferr = datetime.datetime.strptime(self.date_iferr, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.date_last_activity, int):
            self.date_last_activity = datetime.datetime.fromtimestamp(self.date_last_activity)
        if isinstance(self.dateadd, str):
            self.dateadd = datetime.datetime.strptime(self.dateadd, '%Y-%m-%d')
        if isinstance(self.datepeleng, str):
            self.datepeleng = datetime.datetime.strptime(self.datepeleng, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.proshivka_date, str):
            self.proshivka_date = datetime.datetime.strptime(self.proshivka_date, '%Y-%m-%d %H:%M:%S')
        if isinstance(self.ip, str):
            self.ip = ipaddress.ip_address(int(self.ip))
        if isinstance(self.dnport, str):
            self.dnport = [port for port in self.dnport.split(',') if port]
        if isinstance(self.dnlink_iface, str):
            self.dnlink_iface = [port for port in self.dnlink_iface.split(',') if port]
        if isinstance(self.dnlink_iface_array, dict):
            self.dnlink_iface_array = list(self.dnlink_iface_array.keys())
        if isinstance(self.upport, str):
            self.upport = [port for port in self.upport.split(',') if port]
        if isinstance(self.uplink_iface, str):
            self.uplink_iface = [port for port in self.uplink_iface.split(',') if port]
        if isinstance(self.uplink_iface_array, dict):
            self.uplink_iface_array = list(self.uplink_iface_array.keys())
        if isinstance(self.UPPORT, str):
            self.UPPORT = [port for port in self.UPPORT.split(',') if port]
        if isinstance(self.DNPORT, str):
            self.DNPORT = [port for port in self.DNPORT.split(',') if port]


@dataclass
class DeviceDataWithIfaces(DeviceData):
    ifaces: Optional[Dict[str, Dict[str, Union[str, int]]]]
