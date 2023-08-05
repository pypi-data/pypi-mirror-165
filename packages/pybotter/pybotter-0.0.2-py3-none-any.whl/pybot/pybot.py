from cv2 import resize, threshold
from .src.bothandler import BotHandler

class PyBot:
    def __init__(self, window_name, debug = None) -> None:
        self.debug = debug
        self.window_name = window_name
        self.bothandler = BotHandler(window_name, self.debug)
        print("Object PyBot created")

    def add_image(self, name, path):
        self.bothandler.add_image(name, path)

    def find_image(self, name, threshold = 0.5):
        self.bothandler.find_image(name, threshold)

    def show_window(self):
        self.bothandler.show_screenshot()


    def run(self, debug = None):
        self.bothandler.run(debug)


    def left_click(self, x, y, duration):
        self.bothandler.leftclick(x, y, duration)

    def resize(self, x, y):
        self.bothandler.resize(x, y)
        

    