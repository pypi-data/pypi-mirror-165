from vr_configuration.hello_world.config_with_punctuation import \
    ConfigPunctuation
from vr_configuration.hello_world.punctuation_enum import PunctuationEnum


def main():
    # Use custom fields just like built-in fields
    if ConfigPunctuation.punctuation == PunctuationEnum.ExclamationMark:
        print(f'{ConfigPunctuation.greeting}, {ConfigPunctuation.greetee}!')


if __name__ == '__main__':
    main()
