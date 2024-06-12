import yaml

def getConfig():
    with open("./converter/publisher/config/config.yaml", "r") as yamlFileConfig:
        return yaml.safe_load(yamlFileConfig)
    if overrides:
        config.update(overrides)
    return config
