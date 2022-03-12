from config import Config
from gui.main_frame import MainFrame
from world import World

if __name__ == '__main__':
    config = Config()

    world = World(config)

    main_frame = MainFrame(world)
    main_frame.start_loop()
