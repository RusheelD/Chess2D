import pyglet
from UIAI import UI

def main():
    ui = UI()
    pyglet.app.run()
    ui.game.store_history()

if __name__ == '__main__':
    main()