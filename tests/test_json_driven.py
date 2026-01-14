import pytest
import requests
from utils.data_reader import DataReader


@pytest.fixture(scope="module")
def api_test_data():
    return DataReader.read_json("data/api_test_data.json")


@pytest.mark.positive
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.read_json("data/api_test_data.json")["login_tests"])
def test_login_api_json(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    endpoint = test_data['endpoint']
    method = test_data['method']
    payload = test_data['payload']
    expected_status = test_data['expected_status']
    
    test_logger.info(f"Running {test_id} - {method} {endpoint}")
    
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url, json=payload)
    
    assert response.status_code == expected_status, f"{test_id} failed: Expected {expected_status}, got {response.status_code}"
    test_logger.info(f"{test_id} PASSED - Status: {response.status_code}")


@pytest.mark.positive
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.read_json("data/api_test_data.json")["register_tests"])
def test_register_api_json(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    endpoint = test_data['endpoint']
    method = test_data['method']
    payload = test_data['payload']
    expected_status = test_data['expected_status']
    
    test_logger.info(f"Running {test_id} - {method} {endpoint}")
    
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url, json=payload)
    
    assert response.status_code == expected_status, f"{test_id} failed: Expected {expected_status}, got {response.status_code}"
    test_logger.info(f"{test_id} PASSED - Status: {response.status_code}")


@pytest.mark.positive
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.read_json("data/api_test_data.json")["users_tests"])
def test_users_api_json(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    endpoint = test_data['endpoint']
    method = test_data['method']
    expected_status = test_data['expected_status']
    
    test_logger.info(f"Running {test_id} - {method} {endpoint}")
    
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url)
    
    assert response.status_code == expected_status, f"{test_id} failed: Expected {expected_status}, got {response.status_code}"
    test_logger.info(f"{test_id} PASSED - Status: {response.status_code}")
    