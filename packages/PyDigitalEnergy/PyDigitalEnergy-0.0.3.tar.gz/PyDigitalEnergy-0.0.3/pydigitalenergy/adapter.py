import requests
import logging

from typing import Dict
from json import JSONDecodeError
from pydigitalenergy.exceptions import DigitalEnergyApiException
from pydigitalenergy.models import Result


class RestAdapter:
    def __init__(self, hostname: str, client_id: str, client_secret: str, auth_version: str = 'v1', auth_validity: int = 3600, ssl_verify: bool = True, logger: logging.Logger = None, token: str = ''):
        """
        Constructor for RestAdapter

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
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

        self.url = f'https://{hostname}/restmachine'
        self._hostname = hostname
        self._client_id = client_id
        self._client_secret = client_secret
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        self._token = token if token else self._get_new_token(auth_version, auth_validity)

    def _get_new_token(self, auth_version: str = 'v1', auth_validity: int = 3600) -> str:
        """
        Private method for getting new JSON Web Token (JWT)

        :param auth_version: 
            Auth version, default v1
        :param auth_validity: 
            Lifetime of JWT in seconds, default 3600 seconds or 1 hour
        
        :return: 
            Token string
        """
        auth_params = {
            'client_id': self._client_id,
            'client_secret': self._client_secret, 
            'validity': auth_validity,
            'grant_type': 'client_credentials', 
            'response_type': 'id_token'
        }
        auth_url = f'https://sso-{self._hostname}/{auth_version}/oauth/access_token'
        log_line_pre = f'method=POST, url={auth_url}'
        log_line_post = ', '.join((log_line_pre, 'success={}, status_code={}, message={}'))

        # Log HTTP params and perform an HTTP POST request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.post(url=auth_url, verify=self._ssl_verify, params=auth_params)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DigitalEnergyApiException('Request new JWT failed') from e

        # If status_code not in 200-299 range raise exception, otherwise return new JWT
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(is_success, response.status_code, response.reason)

        if not is_success:
            self._logger.error(msg=log_line)
            raise DigitalEnergyApiException(f'{response.status_code}: {response.reason}')

        self._logger.debug(msg=log_line)
        return response.content.decode('utf8')

    def _make_request(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Private method for get(), post(), delete(), etc. methods

        :param http_method: 
            GET, POST, DELETE, etc.
        :param endpoint: 
            URL Endpoint as a string
        :param ep_params: (Optional)
            Dictionary of Endpoint parameters
        :param data: (Optional)
            Dictionary of data to pass to DigitalEnergyApi
        
        :return: 
            Result object
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'bearer {self._token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        full_url = self.url + endpoint
        log_line_pre = f'method={http_method}, url={full_url}, params={ep_params}'
        log_line_post = ', success={}, status_code={}, message={}'

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify,
                                        headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DigitalEnergyApiException('Request failed') from e

        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_pre + log_line_post.format(False, None, e))
            raise DigitalEnergyApiException('Bad JSON in response') from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_pre + log_line_post.format(is_success, response.status_code, response.reason)

        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, headers=response.headers, message=response.reason, data=data_out)

        self._logger.error(msg=log_line)
        raise DigitalEnergyApiException(f'{response.status_code}: {response.reason}')

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """
        HTTP GET method

        :param endpoint: 
            URL Endpoint as a string
        :param ep_params: (Optional)
            Dictionary of Endpoint parameters
        :param data: (Optional)
            Dictionary of data to pass to DigitalEnergyApi
        
        :return: 
            Result object
        """
        return self._make_request(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        HTTP POST method

        :param endpoint: 
            URL Endpoint as a string
        :param ep_params: (Optional)
            Dictionary of Endpoint parameters
        :param data: (Optional)
            Dictionary of data to pass to DigitalEnergyApi
        
        :return: 
            Result object
        """
        return self._make_request(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
