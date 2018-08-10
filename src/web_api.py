import requests
import json
from config import authDetails
from torrent_data import Torrent

class MyWebApi():
    WEB_API_URL = "http://localhost:8112/json"
    headers_to_use = {
        'content-type': 'application/json',
        'accept':'application/json'
    }

    def __init__(self, URL):
        self.url = URL
        self.session = requests.session()
        self.session.headers = MyWebApi.headers_to_use
        self.downloading_torrents = []

    def login(self):
        payload = {
            "id": 3,
            "method": "auth.login",
            "params": [authDetails["password"]]
        }

        response = self.session.post(MyWebApi.WEB_API_URL, data=json.dumps(payload))
        self.session.cookies = response.cookies
        print(self.session.cookies)

    def list_all_torrents(self, filter = None):
        payload = {
            "id": 3,
            "method": "webapi.get_torrents",
            "params": []
        }

        response = self.session.post(MyWebApi.WEB_API_URL, data=json.dumps(payload))
        json_response = json.loads(response.text)


        if response.status_code == 200:
            torrents = json_response["result"]["torrents"]
            if len(self.downloading_torrents) > 0:
                self.downloading_torrents = []
            for torrent in torrents:
                self.downloading_torrents.append(Torrent(name=torrent["name"],hash_to_remove=torrent["hash"]))
            return json_response["result"]["torrents"]
        


    def add_torrent(self, magnet_link):
        payload = {
            "id": 3,
            "method": "webapi.add_torrent",
            "params": [magnet_link]
        }
        print(payload)
        response = self.session.post(MyWebApi.WEB_API_URL, data=json.dumps(payload))
        if response.status_code == 200:
            print(response.text)
            return True, ""
        
        return False, response.text
    
    def delete_torrent(self, hash, remove_data = False):
        payload = {
            "id": 3,
            "method": "webapi.remove_torrent",
            "params": [hash, remove_data]
        }

        response = self.session.post(MyWebApi.WEB_API_URL, data=json.dumps(payload))
        print(response.text)
        if response.status_code == 200:
            return True, ""
        
        return False, response.text
        

