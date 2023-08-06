from typing import List
from pydigitalenergy.system import models
from pydigitalenergy.system.endpoints import API_PATH
from pydigitalenergy.adapter import RestAdapter
from pydigitalenergy.basegroup import BaseGroup
from pydigitalenergy.exceptions import DigitalEnergyApiException


class System:
    def __init__(self, adapter: RestAdapter):
        self.grids = GridGroup(adapter)
        self.data_centers = DataCenterGroup(adapter)


class GridGroup(BaseGroup):
    """
    System Grid Group
    """

    def list(self) -> List[models.Grid]:
        """
        Get list of system grid instances

        :return: 
            List of Grid objects
        """
        endpoint = API_PATH['grid_list']
        result = self._adapter.get(endpoint)
        return [models.Grid(**grid) for grid in result.data]

    def get(self, grid_id: int) -> models.Grid:
        """
        Get information about system grid instance

        :param grid_id: 
            Grid instance identifier

        :return: 
            Grid object
        """
        for grid in self.list():
            if grid.id == grid_id:
                return grid
        raise DigitalEnergyApiException('404: Not Found')


class DataCenterGroup(GridGroup):
    """
    System Data Center Group 
    It is an alias for System Grid Group
    """
    pass