from typing import Union, Optional, List, Any


class IOtune:
    def __init__(self, total_iops_sec: Optional[int], **kwargs):
        self.total_iops_sec = total_iops_sec
        self.__dict__.update(kwargs)


class Disk:
    def __init__(self, id: int, gid: int, name: str, accountId: Optional[int] = None, accountName: Optional[str] = '', acl: Optional[Any] = None, bootPartition: Optional[int] = None, createdTime: Optional[int] = None, deletedTime: Optional[int] = None, desc: Optional[str] = '', destructionTime: Optional[int] = None, devicename: Optional[str] = '', diskPath: Optional[str] = '', guid: Optional[int] = None, imageId: Optional[int] = None, images: Optional[List[Any]] = [], iotune: Optional[Union[IOtune, dict]] = None, iqn: Optional[str] = '', login: Optional[str] = '', milestones: Optional[int] = None, order: Optional[int] = None, params: Optional[str] = '', parentId: Optional[int] = None, passwd: Optional[str] = '', pciSlot: Optional[int] = None, pool: Optional[str] = '', purgeAttempts: Optional[int] = None, purgeTime: Optional[int] = None, realityDeviceNumber: Optional[int] = None, referenceId: Optional[str] = '', resId: Optional[int] = None, resName: Optional[str] = '', role: Optional[str] = '', sepId: Optional[int] = None, sepType: Optional[str] = '', sizeMax: Optional[int] = None, sizeUsed: Optional[int] = None, snapshots: Optional[List[Any]] = [], status: Optional[str] = '', techStatus: Optional[str] = '', type: Optional[str] = '', vmid: Optional[int] = None, **kwargs):
        self.id = id
        self.gid = gid
        self.name = name
        self.account_id = accountId
        self.account_name = accountName
        self.acl = acl
        self.boot_partition = bootPartition
        self.created_time = createdTime
        self.deleted_time = deletedTime
        self.desc = desc
        self.destruction_time = destructionTime
        self.device_name = devicename
        self.disk_path = diskPath
        self.guid = guid
        self.image_id = imageId
        self.images = images
        self.iotune = IOtune(**iotune) if isinstance(iotune, dict) else iotune
        self.iqn = iqn
        self.login = login
        self.milestones = milestones
        self.order = order
        self.params = params
        self.parent_id = parentId
        self.password = passwd
        self.pci_slot = pciSlot
        self.pool = pool
        self.purge_attempts = purgeAttempts
        self.purge_time = purgeTime
        self.reality_device_number = realityDeviceNumber
        self.reference_id = referenceId
        self.res_id = resId
        self.res_name = resName
        self.role = role
        self.sep_id = sepId
        self.sep_type = sepType
        self.size_max = sizeMax
        self.size_used = sizeUsed
        self.snapshots = snapshots
        self.status = status
        self.tech_status = techStatus
        self.type = type
        self.vmid = vmid
        self.__dict__.update(kwargs)