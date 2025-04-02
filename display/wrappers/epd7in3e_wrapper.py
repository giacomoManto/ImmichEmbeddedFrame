from display.drivers import epd7in3e
from ..base_display_manager import BaseDisplayManager

import os

class EPD7IN3E_MANAGER(BaseDisplayManager):
    def __init__(self):
        self.WIDTH = epd7in3e.EPD_WIDTH
        self.HEIGHT = epd7in3e.EPD_HEIGHT
        self.epd = epd7in3e.EPD()
        
        
    def get_width(self):
        return self.WIDTH
    
    def get_height(self):
        return self.HEIGHT
    
    def init(self):
        self.epd.init()
    
    def clear(self):
        self.epd.Clear()
    
    def display(self, imagePath):
        with open(imagePath, "rb") as file:
            image = file.read()
        self.epd.display(image)
    
    def sleep(self):
        self.epd.sleep()
        
    def get_act_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "act", "6-color.act")