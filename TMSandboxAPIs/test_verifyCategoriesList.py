"""''
This test case retrieves the categories available and verifies the count of categories and if certain categories are present.

''"""
import requests
import logging
import pytest
from TMSandboxAPIs.UtilityClass import UtilityClass

@pytest.mark.parametrize("valueToCheck", ['Antiques & collectables'])
def test_verifyCategoriesList(valueToCheck):
    logging.info("Checking if category " + valueToCheck + " exists")
    baseURL = "https://api.tmsandbox.co.nz/v1/Categories.json?depth=1"
    response = requests.request("GET", baseURL, headers={}, data={})
    logging.info("Status Code= " + str(response.status_code))
    assert response.status_code == 200
    responseJSON = response.json()
    subcategories = responseJSON['Subcategories']
    logging.info(str(len(subcategories)) + " Categories present")
    assert len(subcategories) == 27, "Categories count does not match"
    assert UtilityClass().checkIfKeyExists(subcategories, 'Name', valueToCheck), 'Category does not exist'
