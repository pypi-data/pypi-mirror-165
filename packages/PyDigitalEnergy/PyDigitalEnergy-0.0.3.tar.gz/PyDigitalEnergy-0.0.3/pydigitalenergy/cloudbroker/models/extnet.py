from typing import Optional, List, Union, Any


class DefaultQos:
    def __init__(self, guid: Optional[str] = '', eRate: Optional[int] = None, inBurst: Optional[int] = None, inRate: Optional[int] = None, **kwargs):
        self.guid = guid
        self.e_rate = eRate
        self.in_rate = inRate
        self.in_burst = inBurst
        self.__dict__.update(kwargs)


class Reservation:
    def __init__(self, vmId: int, ip: str, mac: str, type: str, clientType: Optional[str] = '', desc: Optional[str] = '', domainname: Optional[str] = '', hostname: Optional[str] = '', **kwargs): 
        self.vm_id = vmId
        self.ip = ip
        self.mac = mac
        self.type = type
        self.client_type = clientType
        self.desc = desc
        self.domain_name = domainname
        self.host_name = hostname
        self.__dict__.update(kwargs)


class VNFs:
    def __init__(self, dhcp: Optional[int] = None, **kwargs):
        self.dhcp = dhcp
        self.__dict__.update(kwargs)


class ExternalNetwork:
    def __init__(self, id: int, gid: int, name: str, status: str, ipcidr: str, gateway: str = '', network: str = '', networkId: int = None, checkIps: Optional[List[str]] = [], default: Optional[bool] = None, defaultQos: Optional[Union[DefaultQos, dict]] = None, desc: Optional[str] = '', dns: Optional[List[Any]] = [], excluded: Optional[List[Any]] = [], free_ips: Optional[int] = None, guid: Optional[int] = None, milestones: Optional[int] = None, preReservationsNum: Optional[int] = None, prefix: Optional[int] = None, priVnfDevId: Optional[int] = None, reservations: Optional[List[Reservation]] = [], sharedWith: Optional[List[Any]] = [], vlanId: Optional[int] = None, vnfs: Optional[Union[VNFs, dict]] = None, _ckey: Optional[str] = '', _meta: Optional[List[Union[int, str]]] = [], **kwargs):
        self.id = id
        self.gid = gid
        self.name = name
        self.status = status
        self.ipcidr = ipcidr
        self.gateway = gateway
        self.network = network
        self.network_id = networkId
        self.check_ips = checkIps
        self.default = default
        self.default_qos = DefaultQos(**defaultQos) if isinstance(defaultQos, dict) else defaultQos
        self.desc = desc
        self.dns = dns
        self.excluded = excluded
        self.free_ips = free_ips
        self.guid = guid
        self.milestones = milestones
        self.pre_reservations_num = preReservationsNum
        self.prefix = prefix
        self.pri_vnf_dev_id = priVnfDevId
        self.reservations = [] if not reservations else [Reservation(**reservation) for reservation in reservations]
        self.shared_with = sharedWith
        self.vlan_id = vlanId
        self.vnfs = VNFs(**vnfs) if isinstance(vnfs, dict) else vnfs
        self._ckey = _ckey
        self._meta = _meta
        self.__dict__.update(kwargs)
