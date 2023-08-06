from io import TextIOWrapper
from midi_generator.config import Configuration
import configparser
import logging

from .types import Scale, Mode, Key


def parse_config_for_generate(config_file: TextIOWrapper) -> Configuration:
    config = configparser.ConfigParser()
    config.read_file(config_file)

    try: 
        return Configuration(
            bars=int(config['generate']['bars']),
            density=float(config['generate']['density']),
            rate=list(config['generate']['rate']),
            syncopation=float(config['generate']['syncopation']),
            scale=Scale(Key(config['generate']['scale']), Mode(config['generate']['mode']))
        )
    except KeyError as e:
        logging.error('Error: {}'.format(e))
        exit(1)


def parse_genetic_config():
    pass
