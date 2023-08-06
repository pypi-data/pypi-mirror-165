import requests
import logging

logging.basicConfig(level=logging.CRITICAL)

from unittest import TestCase, mock
from requests.exceptions import RequestException
from pydigitalenergy.models import Result
from pydigitalenergy.adapter import RestAdapter
from pydigitalenergy.exceptions import DigitalEnergyApiException


class TestRestAdapter(TestCase):

    required_test_settings = {
        'hostname': 'localhost',
        'client_id': 'test',
        'client_secret': 'test',
        'token': 'test-jwt-key',
    } 

    def setUp(self) -> None:
        self.rest_adapter = RestAdapter(**self.required_test_settings)
        self.response = requests.Response()

    def test__make_request_good_request_returns_result(self):
        self.response.status_code = 200
        self.response._content = '{}'.encode()
        with mock.patch('requests.request', return_value=self.response):
            result = self.rest_adapter._make_request('GET', '')
            self.assertIsInstance(result, Result)

    def test__make_request_bad_request_raises_digitalenergyapi_exception(self):
        with mock.patch('requests.request', side_effect=RequestException):
            with self.assertRaises(DigitalEnergyApiException):
                self.rest_adapter._make_request('GET', '')

    def test__make_request_bad_json_raises_digitalenergyapi_exception(self):
        self.response._content = '{"some bad json": '
        with mock.patch('requests.request', return_value=self.response):
            with self.assertRaises(DigitalEnergyApiException):
                self.rest_adapter._make_request('GET', '')

    def test__make_request_300_or_higher_raises_digitalenergyapi_exception(self):
        self.response.status_code = 300
        with mock.patch('requests.request', return_value=self.response):
            with self.assertRaises(DigitalEnergyApiException):
                self.rest_adapter._make_request('GET', '')

    def test__make_request_199_or_lower_raises_digitalenergyapi_exception(self):
        self.response.status_code = 199
        with mock.patch('requests.request', return_value=self.response):
            with self.assertRaises(DigitalEnergyApiException):
                self.rest_adapter._make_request('GET', '')

    def test_get_method_passes_in_get(self):
        self.response.status_code = 200
        self.response._content = '{}'.encode()
        with mock.patch('requests.request', return_value=self.response) as request:
            self.rest_adapter.get('')
            self.assertTrue(request.method, 'GET')
