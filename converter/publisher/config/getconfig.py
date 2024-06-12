import yaml

def getConfig(overrides=None):
    with open("./converter/publisher/config/config.yaml", "r") as yamlFileConfig:
        config = yaml.safe_load(yamlFileConfig)
    if overrides:
        config.update(overrides)
    return config
