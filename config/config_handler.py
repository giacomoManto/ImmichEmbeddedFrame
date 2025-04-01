from utils.logging_setup import setup_logger
import os
import yaml

logger = setup_logger(__name__)

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
    for key in required_keys:
        if key not in config:
            logger.critical(f"Missing required configuration key: {key}")
            raise KeyError(f"Missing required configuration key: {key}")
    for key in optional_keys:   
        if key not in config:
            logger.warning(f"Optional configuration key missing: {key}")
            config[key] = None

    return config
