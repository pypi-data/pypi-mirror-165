from configparser import ConfigParser, ExtendedInterpolation
import os


def load_ts_config():
    try:
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read("tailscale.ini")

        for each_section in config.sections():
            for each_key, each_val in config.items(each_section):
                os.environ[each_key] = each_val

    except Exception as e:
        raise e