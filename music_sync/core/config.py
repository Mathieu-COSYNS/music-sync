import logging
import os

import xdg.BaseDirectory
import yaml


def _get_config_path(*resource, config_file="config.yaml", writable=False):
    """
    - If writable is false return the path of the first readable config file following
    xdg specs.\n
    - If writable is true return the path of the first readable and writable config file
    following xdg specs.\n
    - If no matching files are found return the path were the config file should be
    created.
    """
    for config_dir in xdg.BaseDirectory.load_config_paths(*resource):
        config_file_path = os.path.join(config_dir, config_file)
        if (
            os.path.isfile(config_file_path)
            and os.access(config_file_path, os.R_OK)
            and (not writable or os.access(config_file_path, os.W_OK))
        ):
            return config_file_path

    resource = os.path.join(*resource)
    assert not resource.startswith("/")
    return os.path.join(xdg.BaseDirectory.xdg_config_home, resource, config_file)


def get_config_path(resource="music_sync", **kwargs):
    return _get_config_path(resource, **kwargs)


def read_config(*resource, config_file="config.yaml"):
    config_file_path = _get_config_path(*resource, config_file=config_file)

    with open(config_file_path) as stream:
        config = yaml.safe_load(stream)
        logging.getLogger(__name__).debug(f"Read config in {config_file_path}")
        return config


def write_config(*resource, config_file="config.yaml", config=None):
    config_dir = xdg.BaseDirectory.save_config_path(*resource)
    with open(os.path.join(config_dir, config_file), "w") as file:
        yaml.dump(config, file, sort_keys=False)


def _get_config(*resource, config_file="config.yaml", default=None):
    try:
        return read_config(*resource, config_file=config_file)
    except FileNotFoundError:
        pass
    except Exception as err:
        logging.getLogger(__name__).error(err)
        return None

    try:
        write_config(*resource, config_file=config_file, config=default)
        return default
    except Exception as err:
        logging.getLogger(__name__).error(err)

    return None


def get_config(resource="music_sync", **kwargs):
    return _get_config(resource, **kwargs)
