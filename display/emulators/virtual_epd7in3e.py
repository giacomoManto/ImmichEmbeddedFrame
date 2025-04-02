from display.base_display_manager import BaseDisplayManager
import os
import cv2
import time
import queue
import numpy as np
from utils.logging_setup import setup_logger
import threading
logger = setup_logger(__name__)

class Virtual7in3e(BaseDisplayManager):
    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height
        self.windowName = "Virtual EPD 7in3e"
        self.image = np.ones((height, self.width, 3), dtype=np.uint8) * 0
        self.thread = None
        self.shutdown_thread = False
        self.queue = queue.Queue()
        
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
    
    def init(self):
        logger.info("Initializing Virtual EPD 7in3e")
        if self.thread is None:
            self.thread = threading.Thread(target=self._display_loop, daemon=True)
            self.shutdown_thread = False
            self.thread.start()
    
    def _display_loop(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_KEEPRATIO)
        logger.info("Starting display loop for Virtual EPD 7in3e")
        image = np.ones((self.height, self.width, 3), dtype=np.uint8) * 0
        while not self.shutdown_thread:
            if not self.queue.empty():
                image = self.queue.get()
            cv2.imshow(self.windowName, image)
            if cv2.waitKey(50) & 0xFF == ord('q'):  # Press 'q' to quit
                self.shutdown_thread = True
                cv2.destroyAllWindows()
                logger.warning("Display loop for Virtual EPD 7in3e interrupted by user shutting down virtual display.")
        cv2.destroyAllWindows()
        logger.info("Shut down display loop for Virtual EPD 7in3e")
    
    def clear(self):
        logger.info("Clearing Virtual EPD 7in3e display. Taking 12 seconds to simulate hardware.")
        self.display_helper(np.ones((self.height, self.width, 3), dtype=np.uint8) * 255, 12)

    
    def display(self, imagePath):
        logger.info(f"Displaying image {imagePath}. Taking 5 seconds to simulate hardware.")
        self.display_helper(cv2.imread(imagePath), 5)
    
    def display_helper(self, imageArray, timeSeconds):
        stepsPerSecond = 5
        start = self.image
        end = imageArray
        steps = timeSeconds * stepsPerSecond
        transition_arrays = [((1 - t) * start + t * end) for t in np.linspace(0, 1, steps)]
        transition_arrays = [arr.astype(np.uint8) for arr in transition_arrays]
        for i, arr in enumerate(transition_arrays):
            self.image = arr
            self.queue.put(arr)
            time.sleep(1 / stepsPerSecond)
    
    def sleep(self):
        logger.info("Virtual EPD 7in3e 'sleeping' closing thread")
        self.shutdown_thread = True

    
    def get_act_path(self) -> str:
        return None
