from logging import Logger
from pydigitalenergy.adapter import RestAdapter
from pydigitalenergy.cloudbroker.actors import Cloudbroker
from pydigitalenergy.system.actors import System


class DigitalEnergyApi:
    def __init__(self, hostname: str, client_id: str, client_secret: str, auth_version: str = 'v1', auth_validity: int = 3600, ssl_verify: bool = True, logger: Logger = None, token: str = ''):
        """
        The DigitalEnergyApi class provides convenient access to Digital Energy's API

        :param hostname: 
            DigitalEnergy API hostname. Something like, api.digitalenergy.online
        :param client_id: 
            String defined application identifier
        :param client_secret: 
            String defined application secret
        :param auth_version: 
            Auth version, default v1
        :param auth_validity: 
            Lifetime of JWT-key in seconds, default 3600 seconds or 1 hour
        :param ssl_verify: 
            Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional)
            If your app has a logger, pass it in here
        :param token: (optional)
            Your JWT-key to work with API, if not specified will be generated automatically
        """
        self._adapter = RestAdapter(hostname, client_id, client_secret, auth_version, auth_validity, ssl_verify, logger, token)
        self._logger = logger
        
        # Following actors are RESTfull API interfaces that are used to run backend tasks
        self.cloudapi = None
        self.cloudbroker = Cloudbroker(self._adapter)
        self.libcloud = None
        self.system = System(self._adapter)
