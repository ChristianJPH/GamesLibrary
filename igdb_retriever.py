from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult
import requests
import os
import json


class IGDBRetriever:
    
    def __init__(self):
        self.twitch_app_access_url =  "https://id.twitch.tv/oauth2/token"
        self.igdb_api_url = "https://api.igdb.com/v4/"
        self.covers_endpoint = "covers"
        self.games_endpoint = "games"
        self._base_image_url = "https://images.igdb.com/igdb/image/upload/"
        self.credentials_file = "credentials.json"
        self.load_credentials()
    
    def load_credentials(self):
        with(open(self.credentials_file, "r")) as credentials_file:
            credentials_json = json.load(credentials_file)
            self._client_id = credentials_json["client_id"]
            self._client_secret = credentials_json["client_secret"]

    def request_app_access(self):
        parameters = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "client_credentials"
        }

        twitch_app_access_request = requests.post(self.twitch_app_access_url, json=parameters)
        return twitch_app_access_request.json()["access_token"]

    def create_igdb_wrapper(self):
        return IGDBWrapper(self._client_id, self.request_app_access())

    def retrieve_image_data(self, game_id):
        wrapper = self.create_igdb_wrapper()
        byte_array = wrapper.api_request(
            "covers",
            "fields image_id, width; where game = " + str(game_id) + "; limit 1;"
          )
        return json.loads(byte_array)[0]
        
    def create_image_url(self, image_data, size="t_cover_big"):
        return self._base_image_url + size + "/" + image_data["image_id"] + ".jpg"

    def retrieve_game_data(self, game_name):
        wrapper = self.create_igdb_wrapper()
        byte_array = wrapper.api_request(
            "games",
            'search' + "\"" + game_name + "\"" + ";" + "fields name, created_at, genres; limit 1;"
          )
        return json.loads(byte_array)[0]

    def download_image(self, game_name, path):
        game_data = self.retrieve_game_data(game_name)
        image_data = self.retrieve_image_data(game_data["id"])
        image_url = self.create_image_url(image_data)
        img_data = requests.get(image_url).content
        with open(path, "wb") as file_handler:
            file_handler.write(img_data)
