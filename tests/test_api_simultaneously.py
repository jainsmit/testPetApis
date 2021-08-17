import pytest
import random

from restMethods.petsApi import petsApi
from typing import Dict, List
from constants.constants import *


@pytest.fixture
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
def get_pet_siml(apis):
    return apis.findByIdSimultaneously()

def test_add_pet_simultaneously(apis):
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

def test_adding_pets_while_other_apis_running(add_pets_siml, list_pets_siml):
    pass

#def test_getting_pet_simultaneously(get_pet_siml):
#    pass

def test_delete_pet_simultaneously(apis):
    apis.deletePetSimultaneously()
    resp = apis.listPets()
    # Length before starting the test
    assert resp.json() == None

