import time
import os
import asyncio
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
            self.data_lock = asyncio.Lock()
            
            self._display_index = 0
            self._clear_time = 0
            self._display_time = 0
            
            # Set up successful
            self.logger.info("ImmichDisplayDaemon initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing ImmichDisplayDaemon: {e}")
            raise
        
    async def stop_threads(self):
            self.running = False
            self.logger.info("Setting stop flag")
            
    async def run(self):
        self.logger.info("Running first startup.")
        self.running = True
        
        loop = asyncio.get_event_loop()
        signal.signal(signal.SIGINT, lambda s, f: asyncio.run_coroutine_threadsafe(self.stop_threads(), loop))
        signal.signal(signal.SIGTERM, lambda s, f: asyncio.run_coroutine_threadsafe(self.stop_threads(), loop))
        
        
        await asyncio.gather(
            self.download_and_process(),
            self.display_loop(),
        )

        
    async def display_loop(self):
        self.display_manager.init()
        while self.running:
            clear = time.time() - self._clear_time > self.config[ConfigKeys.CLEAR_INTERVAL.value]
            next_image = time.time() - self._display_time > self.config[ConfigKeys.PHOTO_INTERVAL.value]
            
            if clear and next_image:
                try:
                    await asyncio.to_thread(self.display_manager.clear)
                    self._clear_time = time.time()
                except Exception as e:
                    self.logger.error(f"Error clearing display: {e}")
            
            if next_image:
                async with self.data_lock:
                    if len(self.images) == 0:
                        self.logger.warning("No images to display.")
                    else:
                        if self._display_index >= len(self.images):
                            self._display_index = 0
                        try:
                            await asyncio.to_thread(self.display_manager.display, self.images[self._display_index])
                            self._display_index += 1
                            self._display_time = time.time()
                        except Exception as e:
                            self.logger.error(f"Error displaying image: {e}")
            for a in range(self.config[ConfigKeys.PHOTO_INTERVAL.value]):
                if not self.running:
                    self.display_manager.sleep()
                    break
                await asyncio.sleep(1)
        
        
    async def download_and_process(self):
        while self.running:
            try:
                tempImages = await asyncio.to_thread(self.image_fetcher.download_and_process)
                async with self.data_lock:
                    self.images = tempImages
            except Exception as e:
                self.logger.error(f"Error downloading and processing images: {e}")
                raise
            for a in range(self.config[ConfigKeys.ALBUM_FETCH_INTERVAL.value]):
                if not self.running:
                    break
                await asyncio.sleep(1)
def main():
    daemon = ImmichDisplayDaemon()
    asyncio.run(daemon.run())

if __name__ == "__main__":
    main()