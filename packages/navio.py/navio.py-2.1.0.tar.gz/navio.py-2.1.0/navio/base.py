from typing import Union
import requests 
from requests.structures import CaseInsensitiveDict
import json 
from .baseExceptions import ConnectionError, NotFoundError, RateLimitError, UnauthorisedError


# As this is intended to only be used internally, code may be simplified
class Navio:
    
    def __init__(self, token: str):
        self.token = token
        self._root_url = 'https://api.navio.app/v1/'
    
    def __checkError(self, errorCode) -> Union[bool, Exception]:
        if errorCode in [400, 502, 503, 504]:
            raise ConnectionError() 
        elif errorCode in [401, 403]:
            raise UnauthorisedError()
        elif errorCode == 404:
            raise NotFoundError()
        elif errorCode == 429:
            raise RateLimitError()
    
    def drivers(self) -> str:
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"  
        req = requests.get(f"{self._root_url}drivers", headers=headers)
        self.__checkError(req.status_code)
        return req.status_code    
    
    def add_driver(self, steamID):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"  
        myobject = {
  "steam_id": f"{steamID}"
}
        req = requests.post(f"{self._root_url}drivers", headers=headers, json= myobject)
        self.__checkError(req.status_code)
        return req.json()
    