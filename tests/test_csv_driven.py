import pytest
import requests
from utils.data_reader import DataReader


@pytest.fixture(scope="module")
def login_data():
    return DataReader.csv_to_list_of_dicts("data/login_data.csv")


@pytest.mark.positive
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.csv_to_list_of_dicts("data/login_data.csv"))
def test_login_data_driven(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    username = test_data['username']
    password = test_data['password']
    expected = test_data['expected_result']
    test_type = test_data['test_type']
    
    test_logger.info(f"Running {test_id} - Type: {test_type}")
    
    if test_type == 'positive':
        assert username and password, f"{test_id}: Valid credentials required"
        test_logger.info(f"Positive test with username: {username}")
    elif test_type == 'negative':
        test_logger.info(f"Negative test - expecting error")
    
    payload = {}
    if username:
        payload['email'] = username
    if password:
        payload['password'] = password
    
    response = requests.post(f"{base_url}/login", json=payload)
    
    if expected == 'success':
        assert response.status_code == 200, f"{test_id} failed: Expected 200, got {response.status_code}"
        assert 'token' in response.json(), f"{test_id} failed: No token in response"
        test_logger.info(f"{test_id} PASSED - Status: {response.status_code}")
    else:
        assert response.status_code == 400, f"{test_id} failed: Expected 400, got {response.status_code}"
        assert 'error' in response.json(), f"{test_id} failed: No error in response"
        test_logger.info(f"{test_id} PASSED - Error handled correctly")


@pytest.mark.negative
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.csv_to_list_of_dicts("data/invalid_data.csv"))
def test_invalid_data(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    field = test_data['field']
    value = test_data['value']
    expected_error = test_data['expected_error']
    
    test_logger.info(f"Running {test_id} - Invalid {field}: {value}")
    
    payload = {field: value}
    response = requests.post(f"{base_url}/register", json=payload)
    
    assert response.status_code == 400, f"{test_id} failed: Expected 400, got {response.status_code}"
    test_logger.info(f"{test_id} PASSED - Invalid data rejected")
    