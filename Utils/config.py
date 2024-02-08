import toml


def get_config(table):
    with open("config.toml", "r") as file:
        config = toml.load(file)
    return config.get(table)


def set_config(key, value):
    with open("config.toml", "r") as file:
        config = toml.load(file)
    with open("config.toml", "w") as file:
        for table, data in config.items():
            if key in data.keys():
                config[table][key] = value
                break
        toml.dump(config, file)
