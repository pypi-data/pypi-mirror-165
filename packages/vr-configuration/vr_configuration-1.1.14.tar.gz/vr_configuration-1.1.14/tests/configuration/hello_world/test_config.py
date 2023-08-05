from vr_configuration.hello_world.config import Config


def test_config_greeting():
    assert Config.greeting


def test_config_greetee():
    assert Config.greetee
