import yaml


def load_config(config_file: str = "config.yaml"):
    """
    Load configuration from a file.

    This function opens and reads a YAML formatted configuration file and returns the content as a dictionary.
    If no file path is specified, it defaults to 'config.yaml'.

    Parameters:
    - config_file (str): The path to the configuration file. Defaults to "config.yaml".

    Returns:
    - dict: The configuration content loaded from the file.
    """
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config
