import concurrent.futures
import json
import logging

from typing import List
from constants.endpoints import *
from constants.constants import *
from restMethods.user_session import UserSession

log = logging.getLogger('petsAPIs')

class petsApi(UserSession):
    """Class for Pets Store APIs."""

    def __init__(self):
        super().__init__(BASE_URL)
    
    def findById(self, id: int):
        """Find Pet By ID Method."""

        endpoint = FIND_PET_BY_ID(id)
        try:
            return self.get(endpoint)
        except Exception as exp:
            log.error(f'findById API failed with exception: {exp}')
            raise
    
    def addPet(self, pet_name: str, status: str = None, tags: List = []):
        """Add Pet Method"""

        payload = {
            "name": pet_name,
            "status": status,
            "tags": tags
        }

        try:
            return self.post(ADD_PET_ENDPOINT, payload)
        except Exception as exp:
            log.error(f'Add Pet API failed with exception: {exp}')
            raise

    def listPets(self):
        """List Pets Method."""
        try:
            return self.get(FIND_PET_ENDPOINT)
        except Exception as exp:
            log.error(f'findPets API failed with exception: {exp}')
            raise

    def deletePet(self, id: int):
        """Delete Pet Method."""

        endpoint = FIND_PET_BY_ID(id)
        try:
            return self.delete(endpoint)
        except Exception as exp:
            log.error(f'Delete Pet API failed with exception: {exp}')
        
    def addPetsSimultaneously(
        self, pet_list: List, ntimes: int = 100, status: str = "Available"):
        """Method to add pet simultaneously."""

        plen = len(pet_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future = {
                executor.submit(
                    self.addPet, pet_list[i % plen], status): i for i in range(ntimes) 
            }
            for f in concurrent.futures.as_completed(future):
                tid = future[f]
                try:
                    resp = f.result()
                    if resp.status_code != 200:
                        raise Exception(
                            f'Simultaneously adding pet failed with error: {resp.reason}'
                        )
                except Exception as exc:
                    raise exc
    
    def listPetsSimultaneously(self, ntimes: int = 100):
        """Method to list pet simultaneously."""

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future = { executor.submit(self.listPets): i for i in range(ntimes)}
            for f in concurrent.futures.as_completed(future):
                tid = future[f]
                try:
                    resp = f.result()
                    if resp.status_code != 200:
                        raise Exception(
                            f'Simultaneously adding pet failed with error: {resp.reason}'
                        )
                except Exception as exc:
                    raise exc

    def findByIdSimultaneously(self):
        """Method to get pet simultaneously."""
        resp = self.listPets()
        data_list = json.loads(resp.text)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future = { executor.submit(self.findById(r['id'])): r for r in data_list }
            for f in concurrent.futures.as_completed(future):
                try:
                    resp = f.result()
                    if resp.status_code != 200:
                        raise Exception(
                            f'Simultaneously getting pet failed with error: {resp.reason}'
                        )
                except Exception as exc:
                    #print("Exception: %s" % (exc))
                    pass

    def deletePetSimultaneously(self):
        """Method to delete pet simultaneously."""
        resp = self.listPets()
        data_list = json.loads(resp.text)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future = { executor.submit(self.deletePet(r['id'])): r for r in data_list }
            for f in concurrent.futures.as_completed(future):
                tid = future[f]
                try:
                    resp = f.result()
                    if resp.status_code != 200:
                        raise Exception(
                            f'Simultaneously deleting pet failed with error: {resp.reason}'
                        )
                except Exception as exc:
                    #print("Exception: %s" % (exc))
                    pass