import yaml


def get_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


config = get_config()
