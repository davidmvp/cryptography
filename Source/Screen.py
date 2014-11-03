from abc import ABCMeta, abstractmethod

# need to pass something in?


class BaseState():

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    def render(self):
        pass

    def update(self, time):
        pass

    def event(self, event):
        pass


class Globals(object):

    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    WORLD = None
    CAMERA = None
    WALLS = None
    CURRENT_PLAYER = ['hi', 'he', 'him', 0]
if __name__ == "__main__":
    main()
