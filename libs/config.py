import json

config_path = "config/config.json"
strings_path = "config/strings.json"
slash_path = "config/slash.json"

with open(config_path) as config_file, \
        open(strings_path) as strings_file, \
        open(slash_path) as slash_file:

    config_json = json.loads(config_file.read())
    strings_json = json.loads(strings_file.read())
    slash_json = json.loads(slash_file.read())


def get_config(key):
    return config_json[key]


def get_string(key):
    return strings_json[key]


def get_slash(key):
    return slash_json[key]
