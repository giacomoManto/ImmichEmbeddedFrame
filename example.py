import time
from utils.logging_setup import setup_logger
from config.config_handler import get_config, ConfigKeys
from display.get_display_manager import get_display_manager
from image_fetcher.mock_image_fetcher import MockImageFetcher
from image_fetcher.search_handlers.album_search_handler import AlbumSearchHandler
from photo_processing.ImageProcessor import ImageProcessor


class ImmichDisplayDaemon:
    def __init__(self):
        try:
            # Set up logging
            self.logger = setup_logger(__name__)
            
            # Set up socket path
            self.socket_path = "/tmp/immich-display"
            
            # Load Config
            self.config = get_config("example_config.yaml")
            
            # Set up Display
            self.display_manager = get_display_manager(self.config[ConfigKeys.DISPLAY_MANAGER.value])
            
            # Set Up Server Handling
            # self.server = Immich(
            #     x_api_key=self.config[ConfigKeys.X_API_KEY.value],
            #     url=self.config[ConfigKeys.SERVER_ADDRESS.value],
            #     backup_url=self.config[ConfigKeys.BACKUP_ADDRESS.value]
            # )
            self.search_handler = AlbumSearchHandler(
                album_name=self.config[ConfigKeys.ALBUM_NAME.value],
            )
            self.image_fetcher = MockImageFetcher(
                processor=ImageProcessor(
                    act_path=self.display_manager.get_act_path(),
                    width=self.display_manager.get_width(),
                    height=self.display_manager.get_height(),
                    rotate=False,
                ),                
                data_path=self.config[ConfigKeys.PHOTO_STORAGE.value],   
            )
            # Set up successful
            self.logger.info("ImmichDisplayDaemon initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing ImmichDisplayDaemon: {e}")
            raise        

def main():
    logger = setup_logger(__name__)
    test = ImmichDisplayDaemon()
    images = test.image_fetcher.download_and_process()
    logger.info("Press 'q' to close display.")
    test.display_manager.init()
    test.display_manager.clear()
    while True:
        for image in images:
            logger.info("Press 'q' to close display.")
            test.display_manager.display(image)
            time.sleep(20)
if __name__ == "__main__":
    main()