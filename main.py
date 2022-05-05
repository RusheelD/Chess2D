import pyglet
from GameMode import GameMode

def main():
    ui = GameMode().choose_mode('S')
    pyglet.app.run()
    ui.game.store_history()

if __name__ == '__main__':
    main()