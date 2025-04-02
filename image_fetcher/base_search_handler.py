from abc import ABC, abstractmethod
from image_fetcher.immich import Immich

class BaseSearchHandler(ABC):
    
    @abstractmethod
    def search(self, server: Immich) -> dict:
        pass
            
        
