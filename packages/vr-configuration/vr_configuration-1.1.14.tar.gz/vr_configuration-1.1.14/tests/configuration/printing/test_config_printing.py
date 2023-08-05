from vr_configuration.hello_world.config import Config
from vr_configuration.hello_world.config_with_punctuation import \
    ConfigPunctuation
from vr_configuration.printing.configuration_printing import print_config


def test_print_config():
    print_config(config=Config)


def test_print_config_with_enum():
    print_config(config=ConfigPunctuation)
