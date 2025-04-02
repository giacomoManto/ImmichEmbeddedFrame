import os
from image_fetcher.immich import Immich
from utils.logging_setup import setup_logger

from pillow_heif import register_heif_opener
from photo_processing.ImageProcessor import ImageProcessor
from image_fetcher.base_search_handler import BaseSearchHandler

class ImageFetcher:
    def __init__(self, search_handler: BaseSearchHandler, processor: ImageProcessor, data_path, server: Immich):
        self.logger = setup_logger(__name__)
        self.server = server
        self.search_handler = search_handler
        self.processor = processor
        self.asset_ids_and_extensions = {}
        
        self.originals_path = os.path.join(data_path, "original")
        self.processed_path = os.path.join(data_path, "processed")
        
        register_heif_opener()

        os.makedirs(self.originals_path, exist_ok=True)
        os.makedirs(self.processed_path, exist_ok=True)
        
    def download_and_process(self) -> list[str]:
        self.download()
        self.purge_local()
        self.process()
        
        img_paths = []
        for photo in os.listdir(self.processed_path):
            img_paths.append(os.path.join(self.processed_path, photo))
        return img_paths
            
    
    def purge_local(self):
        keys = self.asset_ids_and_extensions.keys()
        for photo in os.listdir(self.originals_path):
            file_name, file_extension = os.path.splitext(photo)
            if file_name not in keys:
                try:
                    os.remove(os.path.join(self.originals_path, photo))
                    self.logger.debug(f"Removed {photo} from orignals")
                except Exception as e:
                    self.logger.error(f"Error removing file: {e}")
        for photo in os.listdir(self.processed_path):
            file_name, file_extension = os.path.splitext(photo)
            try:
                os.remove(os.path.join(self.processed_path, file_name + ".bmp"))
                self.logger.debug(f"Removed {file_name + '.bmp'} from processed")
            except Exception as e:
                self.logger.error(f"Error removing file: {e}")
                    
    def download(self):
        self.logger.info("Downloading assets from server")
        server_set = self.search_handler.search(self.server)
        for id, extension in server_set.items():
            if id not in self.asset_ids_and_extensions:
                with open(os.path.join(self.originals_path, id+extension), "wb+") as f:
                    f.write(self.server.downloadAsset(id))
                    self.logger.info(f"Downloaded {id} to {self.originals_path}")
        
        self.asset_ids_and_extensions = server_set
        self.logger.debug("Updated local asset IDs")

    def process(self):
        self.logger.info("Processing images")
        processed_photos = os.listdir(self.processed_path)
        for photo in os.listdir(self.originals_path):
            file_name, file_extension = os.path.splitext(photo)
            if file_name + ".bmp" not in processed_photos:
                self.processor.apply_act_palette(os.path.join(self.originals_path, photo), os.path.join(self.processed_path, file_name + ".bmp"))
                self.logger.info(f"Processed {photo}")