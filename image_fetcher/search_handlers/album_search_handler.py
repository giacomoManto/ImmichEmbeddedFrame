from image_fetcher.base_search_handler import BaseSearchHandler
import os
from utils.logging_setup import setup_logger

class AlbumSearchHandler(BaseSearchHandler):
    def __init__(self, album_name):
        self.album_name = album_name
        self.logger = setup_logger(__name__)
    
    def search(self, server) -> dict:
        album = server.getAlbumInfoByName(self.album_name)
        if album is None:
            self.logger.error(f"Album '{self.album_name}' not found.")
            return {}
        id_extension = {}
        for photo in album['assets']:
            file_name, file_extension = os.path.splitext(photo["originalPath"])
            id_extension[photo["id"]] = file_extension
        
        return id_extension