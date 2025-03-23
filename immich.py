import requests
import logging
import json


class Immich:
    """
    This class contains methods for interacting with the Immich E-Ink Frame API.
    """
    
    def __init__(self, x_api_key: str, url: str, backup_url: str = None):
        """Initializes the Immich class with the API key and URL.

        Arguments:
            x_api_key -- api key for the Immich API
            url -- url to the Immich API
            backup_url -- backup url to the Immich API (for exmaple if you are out of network using vpn)
        """
        self.x_api_key = x_api_key
        self.url = url + "/api"
        self.backup_url = backup_url + "/api" if backup_url else None
        self.headers = {
            'Accept': 'application/json',
            'x-api-key': self.x_api_key
        }
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('frame.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info("Immich API initialized.")
        
    def makeRequest(self, method: str, endpoint: str, data: dict = None):
        """Makes a request to the Immich API. Handles error checking.

        Arguments:
            method -- Request method (GET, POST, PUT, DELETE...)
            endpoint -- api endpoint

        Keyword Arguments:
            data -- data included with request (default: {None})
        """
        try:
            response = requests.request(method, self.url + endpoint, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            if not self.backup_url:
                self.logger.error("Main URL connection error. Check network connection.")
                return None
            self.logger.error("Main URL connection error. Trying backup URL.")
            try:
                response = requests.request(method, self.backup_url + endpoint, headers=self.headers, data=data)
            except requests.exceptions.ConnectionError:
                self.logger.error("Backup URL connection error. Check network connection.")
                return None
            
        if response.status_code == 200:
            self.logger.info("Request successful.")
            return response.json()
        elif response.status_code == 401:
            self.logger.error("Status code 401. Unauthorized. Check your API key.")
        self.logger.error("Request failed. {}: {}".format(response.status_code, response.text))
        return None
    
    def downloadAsset(self, asset_id: str):
        acceptDefault = self.headers["Accept"]
        try:
            self.headers["Accept"] = "application/octet-stream"
            response = requests.request("GET", self.url + "/assets/{}/original".format(asset_id), headers=self.headers)
        except requests.exceptions.ConnectionError:
            self.headers["Accept"] = acceptDefault
            if not self.backup_url:
                self.logger.error("Main URL connection error. Check network connection.")
                return None
            try:
                self.headers["Accept"] = "application/octet-stream"
                response = requests.request("GET", self.backup_url + "/assets/{}/original".format(asset_id), headers=self.headers)
            except requests.exceptions.ConnectionError:
                self.headers["Accept"] = acceptDefault
                self.logger.error("Backup URL connection error. Check network connection.")
                return None
            
        self.headers["Accept"] = acceptDefault
        
        if response.status_code == 200:
            self.logger.info("Asset {} downloaded succesfully.".format(asset_id))
            return response.content
        elif response.status_code == 401:
            self.logger.error("Status code 401. Unauthorized. Check your API key.")
        self.logger.error("Request failed. {}: {}".format(response.status_code, response.text))
        return None
        
        
    def getAllAlbums(self):
        """Retrieves all albums from the Immich API.
        
        Returns:
            List of albums
        """
        albums = self.makeRequest("GET", "/albums")
        return albums
    
    def getAlbumInfo(self, album_id: str):
        """Retrieves a specific album from the Immich API.
        
        Arguments:
            album_id -- id of the album to retrieve from the API
        """
        return self.makeRequest("GET", "/albums/{}".format(album_id))
    
    def getAlbumInfoByName(self, album_name: str):
        """Retrieves a specific album from the Immich API by name.
        
        Arguments:
            album_name -- name of the album to retrieve from the API
        """
        albums = self.getAllAlbums()
        
        if albums is None:
            return None
        
        for album in albums:
            if album["albumName"] == album_name:
                return self.getAlbumInfo(album["id"])
        return None
    
    def getAssetInfo(self, asset_id: str):
        """Retrieves a specific asset from the Immich API.
        
        Arguments:
            asset_id -- id of the asset to retrieve from the API
        """
        return self.makeRequest("GET", "/assets/{}".format(asset_id))
