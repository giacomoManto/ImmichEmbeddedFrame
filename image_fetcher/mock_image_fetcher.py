from image_fetcher.image_fetcher import ImageFetcher
import os
from utils.logging_setup import setup_logger

class MockImageFetcher(ImageFetcher):
    def __init__(self, processor, data_path):
        self.logger = setup_logger(__name__)
        self.processor = processor
        self.originals_path = os.path.join(data_path, "original")
        self.processed_path = os.path.join(data_path, "processed")
        self.asset_ids_and_extensions = {}
        for photo in data_path:
            file_name, file_extension = os.path.splitext(photo)
            self.asset_ids_and_extensions[file_name] = file_extension
        
        os.makedirs(self.originals_path, exist_ok=True)
        os.makedirs(self.processed_path, exist_ok=True)
        self.load_local()
            
    def load_local(self):
        for photo in os.listdir(self.originals_path):
            file_name, file_extension = os.path.splitext(photo)
            self.asset_ids_and_extensions[file_name] = file_extension
            self.logger.info(f"Loaded {photo} from originals")
        
    def download_and_process(self) -> list[str]:
        self.load_local()
        self.process()
        
        img_paths = []
        for photo in os.listdir(self.processed_path):
            img_paths.append(os.path.join(self.processed_path, photo))
        return img_paths
            
    
    def purge_local(self):
        self.logger.debug("Mock purging local assets")
        pass
                    
    def download(self):
        self.logger.debug("Mock downloading assets from server")

    def process(self):
        self.logger.info("Processing images")
        processed_photos = os.listdir(self.processed_path)
        for photo in os.listdir(self.originals_path):
            file_name, file_extension = os.path.splitext(photo)
            if file_name + ".bmp" not in processed_photos:
                self.processor.apply_act_palette(os.path.join(self.originals_path, photo), os.path.join(self.processed_path, file_name + ".bmp"))
                self.logger.info(f"Processed {photo}")