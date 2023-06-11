import yaml

default_settings = {"camera": 0, "hands": 1}

try:
    with open("settings.yaml", "r") as f:
        settings = {**default_settings, **yaml.safe_load(f)}
except yaml.YAMLError as exc:
    settings = default_settings

print(settings)