from display.drivers import epd7in3e
from ..base_display_manager import BaseDisplayManager
from utils.logging_setup import setup_logger

import os

class EPD7IN3E_MANAGER(BaseDisplayManager):
    def __init__(self):
        self.WIDTH = epd7in3e.EPD_WIDTH
        self.HEIGHT = epd7in3e.EPD_HEIGHT
        self.epd = epd7in3e.EPD()
        self.logger = setup_logger(__name__)
        
        
    def get_width(self):
        return self.WIDTH
    
    def get_height(self):
        return self.HEIGHT
    
    def init(self):
        self.logger.info("Initializing EPD7IN3E display")
        self.epd.init()
    
    def clear(self):
        self.logger.info("Clearing EPD7IN3E display")
        self.epd.Clear()
    
    def display(self, imagePath):
        self.logger.info(f"Displaying image {imagePath} on EPD7IN3E display")
        with open(imagePath, "rb") as file:
            image = file.read()
        self.epd.display(image)
    
    def sleep(self):
        self.logger.info("Sleeping EPD7IN3E display")
        self.epd.sleep()
        
    def get_act_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "act", "6-color.act")