from typing import Optional, List, Union, Any


class Image:
    def __init__(self, id: int, name: str, type: str, version: str, status: str, techStatus: str, UNCPath: Optional[str] = '', accountId: Optional[int] = None, acl: Optional[List[Any]] = [], architecture: Optional[str] = '', bootType: Optional[str] = '', bootable: Optional[bool] = None, computeciId: Optional[int] = None, deletedTime: Optional[int] = None, desc: Optional[str] = '', drivers: Optional[List[str]] = [], enabled: Optional[bool] = None, gid: Optional[int] = None, guid: Optional[int] = None, history: Optional[List[Any]] = [], hotResize: Optional[bool] = None, lastModified: Optional[int] = None, linkTo: Optional[int] = None, milestones: Optional[int] = None, username: Optional[str] = '', password: Optional[str] = '', pool: Optional[str] = '', providername: Optional[str] = '', purgeAttempts: Optional[int] = None, referenceId: Optional[str] = '', resId: Optional[int] = None, resName: Optional[str] = '', rescuecd: Optional[bool] = None, sepId: Optional[int] = None, sharedWith: Optional[List[Any]] = [], size: Optional[int] = None, url: Optional[str] = '', virtual: Optional[bool] = None, _ckey: Optional[str] = '', _meta: Optional[List[Union[int, str]]] = [], **kwargs):
        self.id = id
        self.name = name
        self.type = type
        self.version = version
        self.status = status
        self.tech_status = techStatus
        self.unc_patch = UNCPath
        self.account_id = accountId
        self.acl = acl
        self.architecture = architecture
        self.boot_type = bootType
        self.bootable = bootable
        self.computeci_id = computeciId
        self.deleted_time = deletedTime
        self.desc = desc
        self.drivers = drivers
        self.enabled = enabled
        self.gid = gid
        self.guid = guid
        self.history = history
        self.hot_resize = hotResize
        self.last_modified = lastModified
        self.link_to = linkTo
        self.milestones = milestones
        self.password = password
        self.pool = pool
        self.provider_name = providername
        self.purge_attempts = purgeAttempts
        self.reference_id = referenceId
        self.res_id = resId
        self.res_name = resName
        self.rescuecd = rescuecd
        self.sep_id = sepId
        self.shared_with = sharedWith
        self.size = size
        self.url = url
        self.username = username
        self.virtual = virtual
        self._ckey = _ckey
        self._meta = _meta
        self.__dict__.update(kwargs)
