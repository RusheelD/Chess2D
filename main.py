import pyglet
from UI import UI

def main():
    ui = UI()
    pyglet.app.run()
    ui.game_main.store_history()

if __name__ == '__main__':
    main()