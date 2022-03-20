from config import Config
from gui.main_window import MainWindow
from gui.utils import show_error
from world import World

if __name__ == '__main__':
    try:
        config = Config()

        world = World(config)

        main_frame = MainWindow(config, world)
    except Exception as err:
        show_error(f'Error. {err}')
