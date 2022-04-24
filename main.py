from config import Config
from gui.main_window import MainWindow
from gui.utils import show_error
from world import Map

if __name__ == '__main__':
    try:
        config = Config()

        map = Map(config)

        main_frame = MainWindow(config, map)
    except Exception as err:
        show_error(f'Error. {err}')
