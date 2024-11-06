import dearpygui.dearpygui as dpg
from program import Program

def main():
    program = Program("games.json")
    program.start()

main()