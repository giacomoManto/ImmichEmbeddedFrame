from utils.logging_setup import setup_logger
import os
import yaml
import enum

logger = setup_logger(__name__)

class ConfigKeys(enum.Enum):
    SERVER_ADDRESS = "server_address"
    X_API_KEY = "x_api_key"
    DISPLAY_MANAGER = "display_manager"
    ALBUM_NAME = "album_name"
    BACKUP_ADDRESS = "backup_address"
    ALBUM_FETCH_INTERVAL = "album_fetch_interval"
    CLEAR_INTERVAL = "clear_interval"
    PHOTO_INTERVAL = "photo_interval"
    PHOTO_STORAGE = "photo_storage"
    LOG_FILE = "log_file"

def get_config():    
    # Load and parse the config.yaml file
    config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")

    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Validate the configuration
    if not config:
        logger.critical("Configuration file is empty or invalid.")
        raise ValueError("Configuration file is empty or invalid.")
    
    # Check for required keys
    required_keys = ["server_address", "x_api_key", "display_manager", "album_name"]
    optional_keys = ["backup_address"]
    default_keys = {"album_fetch_interval": 60, "clear_interval": 3600, "photo_interval": 30, "photo_storage": "/var/cache/eink-daemon", "log_file": "/var/log/eink-daemon.log"}
    
    # Validate keys
    for key in required_keys:
        if key not in config:
            logger.critical(f"Missing required configuration key: {key}")
            raise KeyError(f"Missing required configuration key: {key}")
    for key in optional_keys:   
        if key not in config:
            logger.warning(f"Optional configuration key missing: {key}")
            config[key] = None
    for key in default_keys:
        if key not in config:
            logger.warning(f"Default configuration key missing: {key}")
            config[key] = default_keys[key]
    return config
