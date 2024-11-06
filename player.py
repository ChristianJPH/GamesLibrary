import os

class Player:
    
    def play_game(self, sender, app_data, user_data):
        os.startfile(user_data["executable"])

    def install_game(self, sender, app_data, user_data):
        os.startfile(user_data["installer"])   