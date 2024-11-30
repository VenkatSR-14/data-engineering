import logging
import yaml
import os

CONFIG_PATH = "config/config.yaml"

def setup_logging(config_path = CONFIG_PATH):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    log_level = config['logging']['level']
    log_file = config['logging']['file']
    
    logging.basicConfig(
        level = getattr(logging, log_level),
        format =  "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)