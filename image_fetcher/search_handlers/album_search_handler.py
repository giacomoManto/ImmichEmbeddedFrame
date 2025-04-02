from image_fetcher.base_search_handler import BaseSearchHandler
import os

class AlbumSearchHandler(BaseSearchHandler):
    def __init__(self, album_name):
        self.album_name = album_name
    
    def search(self, server) -> dict:
        album = server.getAlbumInfoByName(self.album_name)
        id_extension = {}
        for photo in album['assets']:
            file_name, file_extension = os.path.splitext(photo["originalPath"])
            id_extension[photo["id"]] = file_extension
        
        return id_extension