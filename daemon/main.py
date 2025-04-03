import time
import os
import threading
from utils.logging_setup import setup_logger
from config.config_handler import get_config, ConfigKeys
from display.get_display_manager import get_display_manager
from image_fetcher.immich import Immich
from image_fetcher.image_fetcher import ImageFetcher
from image_fetcher.search_handlers.album_search_handler import AlbumSearchHandler
from photo_processing.ImageProcessor import ImageProcessor
import signal


class ImmichDisplayDaemon:
    def __init__(self):
        try:
            # Set up logging
            self.logger = setup_logger(__name__)
            
            # Set up socket path
            self.socket_path = "/tmp/immich-display"
            
            # Load Config
            self.config = get_config()
            
            # Set up Display
            self.display_manager = get_display_manager(self.config[ConfigKeys.DISPLAY_MANAGER.value])
            
            # Set Up Server Handling
            self.server = Immich(
                x_api_key=self.config[ConfigKeys.X_API_KEY.value],
                url=self.config[ConfigKeys.SERVER_ADDRESS.value],
                backup_url=self.config[ConfigKeys.BACKUP_ADDRESS.value]
            )
            self.search_handler = AlbumSearchHandler(
                album_name=self.config[ConfigKeys.ALBUM_NAME.value],
            )
            self.image_fetcher = ImageFetcher(
                search_handler=self.search_handler,
                processor=ImageProcessor(
                    act_path=self.display_manager.get_act_path(),
                    width=self.display_manager.get_width(),
                    height=self.display_manager.get_height(),
                    rotate=self.config[ConfigKeys.ROTATE.value],
                    ratio_mode=self.config[ConfigKeys.RATIO_MODE.value],
                ),
                data_path=self.config[ConfigKeys.PHOTO_STORAGE.value],
                server=self.server
            )
            
            # Initialize threading
            self.images = []
            self.data_lock = threading.Lock()
            
            self._display_index = 0
            self._clearTime = 0
            self._startTime = 0
            
            # Set up successful
            self.logger.info("ImmichDisplayDaemon initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing ImmichDisplayDaemon: {e}")
            raise
        
    def stop_threads(self):
            self.running = False
            self.logger.info("Setting stop flag")
            
    def run(self):
        self.logger.info("Running first startup.")
        self.running = True
        
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_threads())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_threads())
        
        threading.Thread(target=self.download_and_process).start()
        threading.Thread(target=self.display_loop).start()

        
    def display_loop(self):
        if not self.running:
            self.logger.info("Stopping display loop.")
            self.display_manager.sleep()
            return
        try:
            if time.time() - self._clearTime > self.config[ConfigKeys.CLEAR_INTERVAL.value]:
                self.display_manager.clear()
            self.data_lock.acquire()
            if len(self.images) == 0:
                self.logger.warning("No images to display.")
            else:
                if self._display_index >= len(self.images):
                    self._display_index = 0
                self.display_manager.display(self.images[self._display_index])
                self._display_index += 1
            self.data_lock.release()
        except Exception as e:
            self.logger.error(f"Error in display loop: {e}")
        threading.Timer(self.config[ConfigKeys.PHOTO_INTERVAL.value], self.display_loop).start()
        
        
    def download_and_process(self):
        if not self.running:
            self.logger.info("Stopping download and process.")
            return
        try:
            # Check config hash
            curHash = hash(frozenset(self.config))
            with open(os.path.join(ConfigKeys.PHOTO_STORAGE.value, "config_hash"), "w+") as f:
                oldHash = int(f.read())
                if curHash != oldHash:
                    f.write(str(curHash))
                    self.logger.info("Config hash changed, removing processed images.")
                    self.image_fetcher.purge_processed()
            tempImages = self.image_fetcher.download_and_process()
            self.data_lock.acquire()
            self.images = tempImages
            self.data_lock.release()
        except Exception as e:
            self.data_lock.release()
            self.logger.error(f"Error downloading and processing images: {e}")
            raise
        threading.Timer(self.config[ConfigKeys.ALBUM_FETCH_INTERVAL.value], self.download_and_process).start()
        
def main():
    test = ImmichDisplayDaemon()
    test.run()

if __name__ == "__main__":
    main()