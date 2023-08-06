from unittest import TestCase
from unittest.mock import MagicMock
from pydigitalenergy.models import Result
from pydigitalenergy.cloudbroker import models
from pydigitalenergy.digitalenergy import DigitalEnergyApi


class TestCloudbrokerApi(TestCase):

    required_test_settings = {
        'hostname': 'localhost',
        'client_id': 'test',
        'client_secret': 'test',
        'token': 'test-jwt-key',
    } 

    def setUp(self) -> None:
        self.api = DigitalEnergyApi(**self.required_test_settings)
        self.api._adapter.get = MagicMock()
        self.api._adapter.post = MagicMock()

    data_compute = {
        'id': 1, 
        'name': 'vm', 
        'gid': 1, 
        'accountId': 1, 
        'accountName': 'test', 
        'rgId': 1,
        'rgName': 'test', 
        'stackId': 1, 
        'status': 'enabled',
        'techStatus': 'started'
    }

    def test_computes_get_returns_one_compute(self):
        self.api._adapter.post.return_value = Result(200, headers={}, data=self.data_compute)
        compute = self.api.cloudbroker.computes.get(1)
        self.assertIsInstance(compute, models.Compute)

    def test_computes_list_returns_list_of_compute(self):
        self.api._adapter.post.return_value = Result(200, headers={}, data=[self.data_compute for i in range(2)])
        compute_list = self.api.cloudbroker.computes.list()
        self.assertIsInstance(compute_list, list)
        self.assertTrue(len(compute_list), 2)
        self.assertIsInstance(compute_list[0], models.Compute)
