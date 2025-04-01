import enum
from display.display_manager import DisplayManager
from utils.logging_setup import setup_logger

logger = setup_logger(__name__)

class SupportedWrappers(enum.Enum):
    epd7in3e = "epd7in3e"
    

def get_display_manager(wrapper: str) -> DisplayManager:
    logger.info(f"Initializing display manager for {wrapper}")
    if wrapper == SupportedWrappers.epd7in3e.name:
        from display.wrappers.epd7in3e_wrapper import EPD7IN3E_MANAGER
        return EPD7IN3E_MANAGER()
    else:
        logger.critical(f"Unsupported wrapper: {wrapper}")
        raise ValueError(f"Unsupported wrapper: {wrapper}")