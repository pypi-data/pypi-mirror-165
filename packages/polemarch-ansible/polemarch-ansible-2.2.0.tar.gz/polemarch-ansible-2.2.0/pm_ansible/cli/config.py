import os
import sys
import json
from collections import OrderedDict
from ansible.config.manager import (
    ConfigManager, Setting, find_ini_config_file, to_native
)


def get_settings():
    config_file = os.getenv('ANSIBLE_CONFIG', find_ini_config_file())
    if config_file:
        os.environ['ANSIBLE_CONFIG'] = to_native(config_file)
    config = ConfigManager()
    dict_settings = OrderedDict()
    defaults = config.get_configuration_definitions().copy()

    for setting in config.data.get_settings():
        if setting.name in defaults:
            defaults[setting.name] = setting

    for setting in sorted(defaults):
        if isinstance(defaults[setting], Setting):
            value = defaults[setting].value
        else:
            value = defaults[setting].get('default')  # nocv
        dict_settings[str(setting)] = value

    return dict_settings


def handler(*args, **kwargs):
    dict_settings = get_settings()
    json.dump(dict_settings, sys.stdout, indent=4)
