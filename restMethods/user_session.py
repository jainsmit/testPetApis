import json
import requests
import logging
from typing import Dict

log = logging.getLogger('user_session')


class UserSession:
    """User Session class for API Server Testing"""

    def __init__(self, base_url: str):
        self.url = base_url
        self.session = requests.Session()
        self.headers = self._header

    @property
    def _header(self):
        return {'Content-Type': 'application/json'}

    def get_url_and_json_params(self, endpoint:str, params: Dict = {}):
        full_url = self.url + endpoint
        return full_url, json.dumps(params)    

    def get(self, endpoint: str, params: Dict = {}):
        full_url, json_param = self.get_url_and_json_params(endpoint, params)
        log.info("Executing GET API: [%s]", full_url)

        try:
            resp = self.session.get(
                full_url, data=json_param, headers=self.headers, verify=False, cookies=""
            )
            return resp
        except Exception as exp:
            raise Exception(f'Get method failed with exception: {exp}')
        
    
    def post(self, endpoint: str, params: Dict):
        full_url, json_param = self.get_url_and_json_params(endpoint, params)
        try:
            resp = self.session.post(
                full_url, data=json_param, headers=self.headers, verify=False, cookies=""
            )
            return resp
        except Exception as exp:
            raise Exception(f'Post method failed with exception: {exp}')

    def delete(self, endpoint: str, params: Dict = {}):
        full_url, json_param = self.get_url_and_json_params(endpoint, params)
        try:
            resp = self.session.delete(
                full_url, data=json_param, headers=self.headers, verify=False, cookies=""
            )
            return resp
        except Exception as exp:
            raise Exception(f'Delete method failed with exception: {exp}')
        
    
    def close(self):
        self.session.close()

