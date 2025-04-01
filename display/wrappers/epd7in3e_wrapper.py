from display.drivers import epd7in3e
from ..display_manager import DisplayManager

import os

class EPD7IN3E_MANAGER(DisplayManager):
    def __init__(self):
        self.WIDTH = epd7in3e.EPD_WIDTH
        self.HEIGHT = epd7in3e.EPD_HEIGHT
        self.epd = epd7in3e.EPD()
        
        
    def width(self):
        return self.WIDTH
    
    def height(self):
        return self.HEIGHT
    
    def init(self):
        self.epd.init()
    
    def clear(self):
        self.epd.Clear()
    
    def display(self, image):
        self.epd.display(image)
    
    def sleep(self):
        self.epd.sleep()
        
    def get_act_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "act", "6-color.act")