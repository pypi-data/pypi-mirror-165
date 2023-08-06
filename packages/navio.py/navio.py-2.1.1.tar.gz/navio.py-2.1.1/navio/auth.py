from typing import Union
import requests 
from requests.structures import CaseInsensitiveDict
import json 
from .baseExceptions import ConnectionError, NotFoundError, RateLimitError, UnauthorisedError


# As this is intended to only be used internally, code may be simplified
class Auth:
    url = 'https://api.navio.app/v1/me'
    
    def __init__(self, token: str):
        self.token = token
    
    def __checkError(self, errorCode) -> Union[bool, Exception]:
        if errorCode in [400, 502, 503, 504]:
            raise ConnectionError() 
        elif errorCode in [401, 403]:
            raise UnauthorisedError()
        elif errorCode == 404:
            raise NotFoundError()
        elif errorCode == 429:
            raise RateLimitError()
    
    def authorise(self) -> str:
        url = self.url 
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"  
        resp = requests.get(url, headers=headers)
        self.__checkError(resp.status_code)
        return resp.status_code    
    