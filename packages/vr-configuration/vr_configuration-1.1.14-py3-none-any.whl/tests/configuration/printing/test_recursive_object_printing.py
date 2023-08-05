from vr_configuration.hello_world.config import Config
from vr_configuration.hello_world.config_with_punctuation import \
    ConfigPunctuation
from vr_configuration.printing.recursive_object_printing import \
    print_object_recursively


def test_print_object_recursively():
    print_object_recursively(obj=Config)


def test_print_object_recursively_with_enum():
    print_object_recursively(obj=ConfigPunctuation)
