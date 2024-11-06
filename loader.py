import dearpygui.dearpygui as dpg
import json

class Loader:
    
    def __init__(self, main_window):
        self._games_layout = "Games Layout"
        self._game_layout = "Game Layout"
        self._buttons_layout = "Buttons Layout"
        self._main_window = main_window
        self.game_idx = 0
        self.num_games_row = 5

    def load_banner(self, path, game_name, parent=None):
        width, height, channels, data = dpg.load_image(path)
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=game_name)
        if parent:
            dpg.add_image(game_name, parent=parent)

    def load_game_buttons(self, game_data, parent, callbacks):
        with dpg.group(label=self._buttons_layout, horizontal=True, parent=parent):
            if game_data["executable"] == None and game_data["installer"]:
                dpg.add_button(tag = "Install" + game_data["name"], label="Install", callback=callbacks["installer_callback"], user_data=game_data)
            elif game_data["executable"]:
                dpg.add_button(tag = "Play" + game_data["name"], label="Play", callback= callbacks["player_callback"], user_data=game_data)            
            dpg.add_button(tag = "Configure" + game_data["name"], label = "Configure")

    def load_game(self, game, callbacks):
        if self.game_idx % self.num_games_row == 0:
            self.group = dpg.add_group(label=self._games_layout + str(self.game_idx), horizontal=True, parent=self.games_window)
        dpg.push_container_stack(self.group)
        with dpg.group(label=self._game_layout, horizontal=False, parent=self.group):
            self.load_banner(game["banner"], game["name"], self._game_layout)
            self.load_game_buttons(game, self._game_layout, callbacks)
        self.game_idx += 1

    def load_games(self, games, callbacks, parent=None):
        self.games_window = dpg.add_child_window(tag=self._games_layout, horizontal_scrollbar=True, parent=self._main_window)
        self.horizontal_games_group = dpg.add_group(label=self._games_layout, horizontal=True, parent=self.games_window)
        self.group = self.horizontal_games_group
        for game in games.keys():
            self.load_game(games[game], callbacks)