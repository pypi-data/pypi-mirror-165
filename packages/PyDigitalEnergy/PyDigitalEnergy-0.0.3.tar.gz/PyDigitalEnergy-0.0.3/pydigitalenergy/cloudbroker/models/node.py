from typing import Union, Optional, List


class Consumed:
    def __init__(self, RAM: int, computes: int, routers: int, vCPU: int, **kwargs):
        self.ram = RAM
        self.computes = computes
        self.routers = routers
        self.vcpu = vCPU
        self.__dict__.update(kwargs)


class Storage:
    def __init__(self, RAM: int, **kwargs):
        self.ram = RAM
        self.__dict__.update(kwargs)


class Consumption:
    def __init__(self, consumed: Union[Consumed, dict], free: Union[Storage, dict], hostname: str, reserved: Union[Storage, dict], total: Union[Storage, dict], **kwargs):
        self.consumed = Consumed(**consumed) if isinstance(consumed, dict) else consumed
        self.free = Storage(**free) if isinstance(free, dict) else free
        self.hostname = hostname
        self.reserved = Storage(**reserved) if isinstance(reserved, dict) else reserved
        self.total = Storage(**total) if isinstance(total, dict) else total
        self.__dict__.update(kwargs)


class Node:
    def __init__(self, gid: int, id: int, name: str, status: Optional[str], version: Optional[str], consumption: Union[Consumption, dict] = None, roles: Optional[List[str]] = [], **kwargs):
        self.gid = gid
        self.id = id
        self.name = name
        self.status = status
        self.version = version
        self.consumption = Consumption(**consumption) if isinstance(consumption, dict) else consumption
        self.roles = roles
        self.__dict__.update(kwargs)
