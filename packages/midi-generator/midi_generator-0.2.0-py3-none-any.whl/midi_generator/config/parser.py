from io import TextIOWrapper
from .config import Configuration
import configparser
import logging

def parse_config_for_generate(config_file: TextIOWrapper) -> Configuration:
    config = configparser.ConfigParser()
    config.read_file(config_file)

    try: 
        return Configuration(
            bars=config['generate']['bars'],
            density=config['generate']['density'],
            rate=config['generate']['rate'],
            syncopation=config['generate']['syncopation'],
            scale=config['generate']['scale'],
            is_polyphonic=config['generate']['is_polyphonic']
        )
    except KeyError as e:
        logging.error('Error: {}'.format(e))
        exit(1)

def parse_genetic_config():
    pass