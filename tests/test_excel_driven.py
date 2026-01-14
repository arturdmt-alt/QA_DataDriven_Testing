import pytest
import requests
from utils.data_reader import DataReader


@pytest.mark.positive
@pytest.mark.data_driven
@pytest.mark.parametrize("test_data", DataReader.excel_to_list_of_dicts("data/user_registration.xlsx"))
def test_user_registration_excel(test_data, base_url, test_logger):
    test_id = test_data['test_id']
    email = test_data['email']
    password = test_data['password']
    expected = test_data['expected_result']
    test_type = test_data['test_type']
    
    test_logger.info(f"Running {test_id} - Type: {test_type}")
    
    payload = {}
    if email:
        payload['email'] = email
    if password:
        payload['password'] = password
    
    response = requests.post(f"{base_url}/register", json=payload)
    
    if expected == 'success':
        assert response.status_code == 200, f"{test_id} failed: Expected 200, got {response.status_code}"
        test_logger.info(f"{test_id} PASSED - Registration successful")
    else:
        assert response.status_code == 400, f"{test_id} failed: Expected 400, got {response.status_code}"
        test_logger.info(f"{test_id} PASSED - Invalid registration rejected")
        