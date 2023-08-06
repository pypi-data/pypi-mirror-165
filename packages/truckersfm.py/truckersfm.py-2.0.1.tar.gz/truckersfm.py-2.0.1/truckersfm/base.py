from typing import Union
import urllib3
import json
from .baseExceptions import ConnectionError, NotFoundError, RateLimitError

import requests

http = urllib3.PoolManager()


class TruckersFM:
    def __init__(self):
        self._root_url = "https://radiocloud.pro/api/public/v1/"
    
    
    def __checkError(self, errorCode) -> Union[bool, Exception]:
        if errorCode in [400, 401, 403, 502, 503, 504]:
            raise ConnectionError() 
        elif errorCode == 404:
            raise NotFoundError()
        elif errorCode == 429:
            raise RateLimitError()
    
    def __decode_data(self, req) -> dict:
        return json.loads(req.data.decode("utf-8"))   
    
    def currentSong(self):
        req = http.request("GET", f"{self._root_url}song/current")
        self.__checkError(req.status)

        return self.__decode_data(req)
    
    def currentSongTitle(self):
        req = requests.get(f"{self._root_url}song/current")
        self.__checkError(req.status_code)
        
        return req.json()["data"]["title"]
    
    def currentSongArtist(self):
        req = requests.get(f"{self._root_url}song/current")
        self.__checkError(req.status_code)
        
        return req.json()["data"]["artist"]
                   
    def currentPresenter(self):
        req = requests.get(f"{self._root_url}presenter/summary")
        self.__checkError(req.status_code)

        return req.json()["data"]["live"]["user"]
    
    def currentPresenterName(self):
        req = requests.get(f"{self._root_url}presenter/summary")
        self.__checkError(req.status_code)
        
        return req.json()["data"]["live"]["user"]["name"]
    
    def currentShow(self):
        req = requests.get(f"{self._root_url}presenter/summary")
        self.__checkError(req.status_code)
        
        return req.json()["data"]["live"]
    
    def currentShowTitle(self):
        req = requests.get(f"{self._root_url}presenter/summary")
        self.__checkError(req.status_code)
        
        return req.json()["data"]["live"]["description"]