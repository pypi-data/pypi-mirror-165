from logging import exception
from typing import List
from pydigitalenergy.cloudbroker import models
from pydigitalenergy.cloudbroker.endpoints import API_PATH
from pydigitalenergy.adapter import RestAdapter
from pydigitalenergy.basegroup import BaseGroup


class Cloudbroker:
    def __init__(self, adapter: RestAdapter):
        self.computes = ComputeGroup(adapter)
        self.virtual_machines = VirtualMachineGroup(adapter)
        self.stacks = StackGroup(adapter)
        self.hosts = HostGroup(adapter)
        self.nodes = NodeGroup(adapter)
        self.clusters = ClusterGroup(adapter)
        self.grids = GridGroup(adapter)
        self.data_centers = DataCenterGroup(adapter)
        self.storages = StorageEndpointGroup(adapter)
        self.images = IamgeGroup(adapter)
        self.disks = DiskGroup(adapter)
        self.networks = ExternalNetworkGroup(adapter)


class ComputeGroup(BaseGroup):
    """
    Compute Group
    """

    def list(self, include_deleted: bool = False, page: int = 0, size: int = 0) -> List[models.Compute]:
        """
        Get list of compute instances
        Page and size can be specified only together

        :param include_deleted: (optional)
            Whether add deleted compute instances or not
        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Compute objects
        """
        endpoint = API_PATH['compute_list']
        ep_params = {'includedeleted': include_deleted, 'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.Compute(**compute) for compute in result.data]

    def get(self, compute_id: int, reason: str = '') -> models.Compute:
        """
        Get information about compute instance

        :param compute_id: 
            Compute instance identifier
        :param reason: (optional)
            Reason of action
        
        :return: 
            Compute object
        """
        endpoint = API_PATH['compute_get']
        ep_params = {'computeId': compute_id, 'reason': reason}
        result = self._adapter.post(endpoint, ep_params)
        return models.Compute(**result.data)


class VirtualMachineGroup(ComputeGroup):
    """
    Virtual Machine Group 
    It is an alias for Compute Group
    """
    pass


class StackGroup(BaseGroup):
    """
    Stack Group
    """

    def list(self, enabled: bool = True, page: int = 0, size: int = 0) -> List[models.Stack]:
        """
        Get list of stack instances
        Page and size can be specified only together

        :param enabled: (optional)
            Whether to show only enabled stacks or all of them
        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Stack objects
        """
        endpoint = API_PATH['stack_list']
        ep_params = {'enabled': enabled, 'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.Stack(**stack) for stack in result.data]

    def get(self, stack_id: int) -> models.Stack:
        """
        Get information about stack instance

        :param stack_id: 
            Stack instance identifier

        :return: 
            Stack object
        """
        endpoint = API_PATH['stack_get']
        ep_params = {'stackId': stack_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.Stack(**result.data)


class HostGroup(StackGroup):
    """
    Host Group 
    It is an alias for Stack Group
    """
    pass


class NodeGroup(BaseGroup):
    """
    Node Group
    """

    def list(self, page: int = 0, size: int = 0) -> List[models.Node]:
        """
        Get list of node instances
        Page and size can be specified only together

        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Node objects
        """
        endpoint = API_PATH['node_list']
        ep_params = {'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.Node(**node) for node in result.data]

    def get(self, node_id: int) -> models.Node:
        """
        Get information about node instance

        :param node_id: 
            Node instance identifier

        :return: 
            Node object
        """
        endpoint = API_PATH['node_get']
        ep_params = {'nid': node_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.Node(**result.data)


class ClusterGroup(NodeGroup):
    """
    Cluster Group 
    It is an alias for Node Group
    """
    pass


class GridGroup(BaseGroup):
    """
    Grid Group
    """

    def list(self, page: int = 0, size: int = 0) -> List[models.Grid]:
        """
        Get list of grid instances
        Page and size can be specified only together

        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Grid objects
        """
        endpoint = API_PATH['grid_list']
        ep_params = {'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.Grid(**grid) for grid in result.data]

    def get(self, grid_id: int) -> models.Grid:
        """
        Get information about grid instance

        :param grid_id: 
            Grid instance identifier

        :return: 
            Grid object
        """
        endpoint = API_PATH['grid_get']
        ep_params = {'gridId': grid_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.Grid(**result.data)


class DataCenterGroup(GridGroup):
    """
    Data Center Group 
    It is an alias for Grid Group
    """
    pass


class StorageEndpointGroup(BaseGroup):
    """
    Storage Endpoint Group
    """

    def list(self, page: int = 0, size: int = 0) -> List[models.StorageEndpoint]:
        """
        Get list of Storage Endpoint instances
        Page and size can be specified only together

        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of StorageEndpoint objects
        """
        endpoint = API_PATH['sep_list']
        ep_params = {'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.StorageEndpoint(**sep) for sep in result.data]

    def get(self, sep_id: int) -> models.StorageEndpoint:
        """
        Get information about Storage Endpoint instance

        :param sep_id: 
            Storage Endpoint instance identifier

        :return: 
            StorageEndpoint object
        """
        endpoint = API_PATH['sep_get']
        ep_params = {'sep_id': sep_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.StorageEndpoint(**result.data)

    def get_config(self, sep_id: int) -> models.StorageConfig:
        """
        Get config of Storage Endpoint instance

        :param sep_id: 
            Storage Endpoint instance identifier

        :return: 
            StorageConfig object
        """
        endpoint = API_PATH['sep_get_config']
        ep_params = {'sep_id': sep_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.StorageConfig(**result.data)

    def get_pool(self, sep_id: int, pool_name: str) -> models.StoragePool:
        """
        Get pool of Storage Endpoint instance

        :param sep_id: 
            Storage Endpoint instance identifier
        :param pool_name: 
            Name of certain Storage Endpoint pool

        :return: 
            StoragePool object
        """
        endpoint = API_PATH['sep_get_pool']
        ep_params = {'sep_id': sep_id, 'pool_name': pool_name}
        result = self._adapter.post(endpoint, ep_params)
        return models.StoragePool(**result.data)


class IamgeGroup(BaseGroup):
    """
    Image Group
    """

    def list(self, sep_id: int = None, shared_with: int = None, page: int = 0, size: int = 0) -> List[models.Image]:
        """
        Get list of Image instances
        Page and size can be specified only together

        :param sep_id: (optional)
            Filter images based on Storage Endpoint instance identifier
        :param shared_with: (optional)
            Filter images based on Account identifier availability
        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Image objects
        """
        endpoint = API_PATH['image_list']
        ep_params = {'sepId': sep_id, 'sharedWith': shared_with, 'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.Image(**image) for image in result.data]

    def get(self, image_id: int) -> models.Image:
        """
        Get information about Image instance

        :param image_id: 
            Image instance identifier

        :return: 
            Image object
        """
        endpoint = API_PATH['image_get']
        ep_params = {'imageId': image_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.Image(**result.data)


class DiskGroup(BaseGroup):
    """
    Disk Group
    """

    def list(self, account_id: int = None, disk_type: str = None, page: int = 0, size: int = 0) -> List[models.Disk]:
        """
        Get list of Disk instances
        Page and size can be specified only together

        :param account_id: (optional)
            Filter disks based on their belonging to the Account
        :param disk_type: (optional)
            Filter disks based on their type mark
        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of Disk objects
        """
        endpoint = API_PATH['disks_list']
        ep_params = {'accountId': account_id, 'type': disk_type, 'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)

        # for disk in result.data:
        #     try:
        #         models.Disk(**disk)
        #     except Exception as e:
        #         print('data:', disk)
        #         print('e:', e)

        return [models.Disk(**disk) for disk in result.data]

    def get(self, disk_id: int) -> models.Disk:
        """
        Get information about Disk instance

        :param disk_id: 
            Disk instance identifier

        :return: 
            Disk object
        """
        endpoint = API_PATH['disks_get']
        ep_params = {'diskId': disk_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.Disk(**result.data)


class ExternalNetworkGroup(BaseGroup):
    """
    External Network Group
    """

    def list(self, account_id: int = None, page: int = 0, size: int = 0) -> List[models.ExternalNetwork]:
        """
        Get list of External Network instances
        Page and size can be specified only together

        :param account_id: (optional)
            Filter external networks based on their belonging to the Account
        :param page: (optional)
            Page number
        :param size: (optional)
            Amount of instances per page
        
        :return: 
            List of ExternalNetwork objects
        """
        endpoint = API_PATH['extnet_list']
        ep_params = {'accountId': account_id, 'page': page, 'size': size}
        result = self._adapter.post(endpoint, ep_params)
        return [models.ExternalNetwork(**sep) for sep in result.data]

    def get(self, net_id: int) -> models.ExternalNetwork:
        """
        Get information about External Network instance

        :param net_id: 
            External Network instance identifier

        :return: 
            ExternalNetwork object
        """
        endpoint = API_PATH['extnet_get']
        ep_params = {'net_id': net_id}
        result = self._adapter.post(endpoint, ep_params)
        return models.ExternalNetwork(**result.data)
