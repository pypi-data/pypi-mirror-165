from typing import Optional, List, Dict, Union, Any


class DiskDelQueue:
    def __init__(self, purge_attempts_threshold: Optional[int] = None, **kwargs):
        self.purge_attempts_threshold = purge_attempts_threshold
        self.__dict__.update(kwargs)


class HousekeepingSettings:
    def __init__(self, disk_del_queue: Optional[Union[DiskDelQueue, dict]] = None, **kwargs):
        self.disk_del_queue = DiskDelQueue(**disk_del_queue) if isinstance(disk_del_queue, dict) else disk_del_queue
        self.__dict__.update(kwargs)


class StoragePool:
    def __init__(self, id: int, snapshot_pool_id: int, name: str, clone_technology: Optional[str] = '', maxLdevId: Optional[int] = None, minLdevId: Optional[int] = None, snapshotable: Optional[bool] = None, types: Optional[List[str]] = [], usage_limit: Optional[int] = None, **kwargs):
        self.id = id
        self.snapshot_pool_id = snapshot_pool_id
        self.name = name
        self.clone_technology = clone_technology
        self.max_ldev_id = maxLdevId
        self.min_ldev_id = minLdevId
        self.snapshotable = snapshotable
        self.types = types
        self.usage_limit = usage_limit
        self.__dict__.update(kwargs)


class StorageConfig:
    def __init__(self, model: str, protocol: str, ssl_verify: bool, SN: int, disk_max_size: int, API_URLs: Optional[List[str]] = [], format: Optional[str] = '', hostGroupNumMax: Optional[int] = None, hostGroupNumMin: Optional[int] = None, hostGroupNumber: Optional[int] = None, hosts: Optional[Dict[str, int]] = {}, housekeeping_settings: Optional[Union[HousekeepingSettings, dict]] = None, mgmt_password: Optional[str] = '', mgmt_user: Optional[str] = '', name_prefix: Optional[str] = '', pools: Optional[List[Union[StoragePool, dict]]] = [], ports: Optional[List[str]] = [], **kwargs):
        self.model = model
        self.protocol = protocol
        self.ssl_verify = ssl_verify
        self.serial_number = SN
        self.disk_max_size = disk_max_size
        self.api_urls = API_URLs
        self.format = format
        self.host_group_num_max = hostGroupNumMax
        self.host_group_num_min = hostGroupNumMin
        self.host_group_number = hostGroupNumber
        self.hosts = hosts
        self.housekeeping_settings = HousekeepingSettings(**housekeeping_settings) if isinstance(housekeeping_settings, dict) else housekeeping_settings
        self.mgmt_password = mgmt_password
        self.mgmt_user = mgmt_user
        self.name_prefix = name_prefix
        self.pools = [] if not pools else [StoragePool(**pool) for pool in pools]
        self.ports = ports
        self.__dict__.update(kwargs)


class StorageEndpoint:
    def __init__(self, id: int, gid: int, name: str, desc: str, type: str, objStatus: str, techStatus: str, config: Optional[Union[StorageConfig, dict]] = None, consumedBy: Optional[List[int]] = [], guid: Optional[int] = None, milestones: Optional[int] = None, providedBy: Optional[List[Any]] = [], _ckey: Optional[str] = '', _meta: Optional[List[Union[int, str]]] = [], **kwargs):
        self.id = id
        self.gid = gid
        self.name = name
        self.desc = desc
        self.type = type
        self.obj_status = objStatus
        self.tech_status = techStatus
        self.config = StorageConfig(**config) if isinstance(config, dict) else config
        self.consumed_by = consumedBy
        self.guid = guid
        self.milestones = milestones
        self.provided_by = providedBy
        self._ckey = _ckey
        self._meta = _meta
        self.__dict__.update(kwargs)
