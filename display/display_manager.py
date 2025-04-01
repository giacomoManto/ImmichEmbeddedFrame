from abc import ABC, abstractmethod

class DisplayManager(ABC):
    @abstractmethod
    def width(self):
        return

    @abstractmethod
    def height(self):
        return
    
    def aspect(self):
        return float(self.width()) / float(self.height())
    
    @abstractmethod
    def init(self):
        pass
    
    @abstractmethod
    def clear(self):
        pass
    
    @abstractmethod
    def display(self, image):
        pass
    
    @abstractmethod
    def sleep(self):
        pass
    
    @abstractmethod
    def get_act_path(self) -> str:
        return