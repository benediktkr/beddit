import tomllib


def read_config(path="beddit.toml"):
    with open(path, 'r') as f:
        return tomllib.load(f)
