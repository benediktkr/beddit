import tomli


def read_config(path="beddit.toml"):
    with open(path, 'r') as f:
        return tomli.loads(f.read())
