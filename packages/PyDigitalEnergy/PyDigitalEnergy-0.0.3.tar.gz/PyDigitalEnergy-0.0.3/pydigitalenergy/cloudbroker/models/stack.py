from typing import Optional, List, Union


class Stack:
    def __init__(self, id: int, gid: int, name: str, status: str, type: str, referenceId: int, _ckey: Optional[str] = '', _meta: Optional[List[Union[int, str]]] = [], apiUrl: Optional[str] = '', apikey: Optional[str] = '', appId: Optional[str] = '', desc: Optional[str] = '', descr: Optional[str] = '', drivers: Optional[List[str]] = '', eco: Optional[str] = '', error: Optional[int] = None, guid: Optional[int] = None, images: Optional[List[int]] = [], login: Optional[str] = '', passwd: Optional[str] = '', **kwargs):
        self.id = id
        self.gid = gid
        self.name = name
        self.status = status
        self.type = type
        self.reference_id = int(referenceId) if referenceId.isdigit() else referenceId
        self.api_url = apiUrl
        self.api_key = apikey
        self.app_id = appId
        self.desc = desc
        self.descr = descr
        self.drivers = drivers
        self.eco = eco
        self.error = error
        self.guid = guid
        self.images = images
        self.login = login
        self.passwd = passwd
        self._ckey = _ckey
        self._meta = _meta
        self.__dict__.update(kwargs)

    def get_node(self):
        """
        Get node info for current stack
        """
        raise NotImplementedError

    def get_cluster(self):
        """
        Get cluster info for current stack
        It is an alias for get_node() method
        """
        return self.get_node()

    def get_storage(self):
        """
        Get storage endpoint for current stack
        """
        raise NotImplementedError
