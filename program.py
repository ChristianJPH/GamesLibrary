from adder import Adder
from loader import Loader
from player import Player
from igdb_retriever import IGDBRetriever
import dearpygui.dearpygui as dpg
from utils import read_games

class Program:
    
    def __init__(self, games_path):
        self.games_path = games_path
        self._main_window = "Main Window"
        self._games_adder = Adder(self.games_path)
        self._games_loader = Loader(self._main_window)
        self._games_player = Player()
        self._buttons_callbacks = {
            "installer_callback": self._games_player.install_game,
            "player_callback": self._games_player.play_game
        }
    
    def add_game(self, sender, app_data):
        game_data = self._games_adder.add_game(app_data)
        self._games_loader.load_game(game_data, self._buttons_callbacks)


    def directory_search(self):
        with dpg.file_dialog(directory_selector=True, show=False, callback=self.add_game, id="file_dialog_id", width=700 ,height=400):
            dpg.add_file_extension(".*")

    def load_games(self):
        self._games_loader.load_games(read_games(self.games_path), self._buttons_callbacks, self._main_window)

    def start(self):
        dpg.create_context()
        self.directory_search()
        with dpg.window(tag=self._main_window, autosize=True,no_resize=False, horizontal_scrollbar=True) as window:
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Add Game", callback=lambda: dpg.show_item("file_dialog_id"))
            self.load_games()
        dpg.create_viewport(title='Game Library', small_icon="./img/second-logo.ico", large_icon="./img/logo.ico", width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(self._main_window, True)
        dpg.start_dearpygui()
        dpg.destroy_context()