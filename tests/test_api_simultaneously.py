import pytest
import random

from restMethods.petsApi import petsApi
from typing import Dict, List
from constants.constants import *


@pytest.fixture(autouse=True)
def apis():
    return petsApi()

@pytest.fixture
def add_pets_siml(apis):
    mypet_list = [
        'Dog', 'Cat', 'Horse', 'Rabbit', 'Mouse', 'Snake'
    ]
    ntimes = 100
    return apis.addPetsSimultaneously(mypet_list, ntimes=ntimes)

@pytest.fixture
def list_pets_siml(apis):
    return apis.listPetsSimultaneously()

@pytest.fixture
def petlength(apis):
    resp = apis.listPets()
    return len(resp.json())

@pytest.fixture
def get_pet_siml(apis):
    return apis.findByIdSimultaneously()

def test_add_pet_simultaneously(apis):
    """ 
        Testing Add pets rest API while running simultaneously.
        Validating the pets after threads are completed.
    """

    mypet_list = [
        'Dog', 'Cat', 'Horse', 'Rabbit', 'Mouse', 'Snake'
    ]
    ntimes = 100
    apis.addPetsSimultaneously(mypet_list, ntimes=ntimes)
    
    resp = apis.listPets()
    # Length before starting the test
    initial_len = len(resp.json())

    apis.addPetsSimultaneously(mypet_list, ntimes=ntimes)
    resp = apis.listPets()
    
    # Length after adding the pets 
    after_len = len(resp.json())

    # Validating the length after adding number of pets simultaneously
    assert after_len  == initial_len + ntimes

def test_adding_pets_while_other_apis_running(
    apis, petlength, add_pets_siml, list_pets_siml, get_pet_siml
):
    """
        Testing Adding Pets API while other APIs also running at same time.
        Validating that Pets added successfully.
    """
    resp = apis.listPets()
    npets = 100
    assert len(resp.json()) == petlength+ npets

def test_delete_pet_simultaneously(apis):
    """
        Testing Delete APIs simultaneously.
        Validating that all pets are cleaned up.
    """
    apis.deletePetSimultaneously()
    resp = apis.listPets()
    # Length before starting the test
    assert resp.json() == None
