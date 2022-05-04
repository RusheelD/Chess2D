import pyglet
from UI import UI as UI
from UIAI import UI as UiAi
from UISynchronic import UI as UiSynchronic

def main():
    ui = UI()
    pyglet.app.run()
    ui.game.store_history()

if __name__ == '__main__':
    main()