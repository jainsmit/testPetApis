import pytest
import random

from restMethods.petsApi import petsApi
from typing import Dict, List
from constants.constants import *


@pytest.fixture
def apis():
    return petsApi()

@pytest.fixture
def add_pet(apis):
    pname = "Rabbit"
    status = "Available"
    apis.addPet(pet_name=pname, status=status)
    resp = apis.listPets()
    return resp.json()[-1]['id']

def test_add_pets(apis):
    # Validate Add Pet API's
    pname = "Horse"
    status = "available"
    apis.addPet(pet_name=pname, status=status)

    # Listing pets after adding new pets
    resp = apis.listPets()
    id = resp.json()[-1]['id']

    # Validating the last added pet attributes
    resp = apis.findById(id)
    assert resp.json()['name'] == pname
    assert resp.json()['status'] == status

    # Validating duplicate pets
    status = "Pending"

    apis.addPet(pet_name=pname, status=status)

    # Listing pets after adding new pets
    resp = apis.listPets()
    id = resp.json()[-1]['id']

    # Validating the last added pet attributes
    resp = apis.findById(id)
    assert resp.json()['name'] == pname
    assert resp.json()['status'] == status


def test_delete_pets(apis, add_pet):
    # Add and Delete Pet
    apis.deletePet(add_pet)

    # Test to get pet by id which is deleted or doesn't exist
    resp = apis.findById(add_pet)

    # Expecting status code 404 (Not Found)
    assert resp.status_code == 404

    # Delete pet with id which doesn't exist
    id = random.randint(START_BIG_INT, END_BIG_INT)
    apis.deletePet(id)
    resp = apis.findById(id)

    # Expecting status code 404 (Not Found)
    assert resp.status_code == 404