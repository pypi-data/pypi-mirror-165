from pydigitalenergy.adapter import RestAdapter


class BaseGroup:
    def __init__(self, adapter: RestAdapter):
        """
        Base class for all Digital Energy API Groups

        :param adapter: 
            Low-lever adapter for Digital Energy API
        """
        self._adapter = adapter
