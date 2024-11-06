import json
import os
from pathlib import Path
from igdb_retriever import IGDBRetriever
import simple_image_download.simple_image_download as simp
from utils import read_games

class Adder:

    def __init__(self, games_path):
        self.games_path = games_path
        self.igdb_retriever = IGDBRetriever()
        self.game_data_path_key = "file_path_name"
        self.executable_extension = ".exe"
        self.installer_extensions = [".exe", ".iso"]
        self.image_extensions = [".png", ".jpg", ".jpeg"]
        self.game_banner_name = "banner"
    

    def gen_possible_image_filenames(self):
        filenames = []
        for extension in self.image_extensions:
            filenames.append("".join([self.game_banner_name, extension]))
        return filenames

    def find_game_installer(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(tuple(self.installer_extensions)):
                    return os.path.join(root, file)

    def find_game_banner(self, name, path):
        banner_path = os.path.join(path, "banner.jpg")
        self.igdb_retriever.download_image(name, banner_path)
        return banner_path

    def find_game_data(self, executable, path):
        game_data = {
            "executable": None,
            "banner": None
        }

        for root, dirs, files in os.walk(path):
            if executable in files:
                game_data["executable"] = os.path.join(root, executable)
            for file in files:
                if file in self.gen_possible_image_filenames():
                    game_data["banner"] = os.path.join(root, file)

        if game_data["executable"] == None:
            game_data["installer"] = self.find_game_installer(path)
        if game_data["banner"] == None:
            game_data["banner"] = self.find_game_banner(executable.split(".")[0], path)
        return game_data

    def add_game(self, game_data):
        self._games = read_games(self.games_path)
        game_path = Path(game_data[self.game_data_path_key])
        game_data = self.find_game_data(game_path.name + self.executable_extension, game_data[self.game_data_path_key])

        game = {
            game_path.name: {
                "name": game_path.name,
                "directory_path": str(game_path),
            }
        }
        game[game_path.name] = game[game_path.name] | game_data
        self._games = self._games | game
        print(self._games)
        self.write_game_data()
        return game[game_path.name]
    
    def write_game_data(self):
        with open(self.games_path, "w") as games_file:
            games_file.write(json.dumps(self._games))