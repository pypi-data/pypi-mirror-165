from typing import Union, Optional


class Stats:
    def __init__(self, cpu: int, disksize: int, extips: int, exttraffic: int, gpu: int, ram: int, **kwargs):
        self.cpu = cpu
        self.disksize = disksize
        self.extips = extips
        self.exttraffic = exttraffic
        self.gpu = gpu
        self.ram = ram
        self.__dict__.update(kwargs)


class Resource:
    def __init__(self, Current: Union[Stats, dict], Reserved: Union[Stats, dict], **kwargs):
        self.current = Stats(**Current) if isinstance(Current, dict) else Current
        self.reserved = Stats(**Reserved) if isinstance(Reserved, dict) else Reserved
        self.__dict__.update(kwargs)


class Grid:
    def __init__(self, id: int, name: str, gid: int, Resources: Union[Resource, dict], flag: Optional[str] = '', guid: Optional[int] = None, locationCode: Optional[str] = '', **kwargs):
        self.id = id
        self.name = name
        self.gid = gid
        self.Resources = Resource(**Resources) if isinstance(Resources, dict) else Resources
        self.flag = flag
        self.guid = guid
        self.locationCode = locationCode
        self.__dict__.update(kwargs)
