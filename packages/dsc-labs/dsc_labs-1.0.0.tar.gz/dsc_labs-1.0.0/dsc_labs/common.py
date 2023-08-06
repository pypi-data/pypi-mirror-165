import json
import yaml

from typing import Optional
from logging import INFO
from datetime import datetime
from dsc_labs.libs.config import DSCLabsAppConfig
from dsc_labs.libs.logger import DSCLabsLogger
from dsc_labs.libs.bugsnag import init_bugsnag


def get_common_config() -> dict:
    """
    Initialize common configurations.
    Return: A dict containing the whole common config data.
    """
    mlc = DSCLabsAppConfig("")
    common_config = mlc.get_config()

    return common_config


def datetime_to_utc(timestamp: datetime) -> str:
    return f'{timestamp.isoformat(timespec="milliseconds")}Z'


def current_utc_timestamp() -> str:
    """
    Return: The current UTC timestamp.
    """
    return datetime_to_utc(datetime.utcnow())


def int_to_utc(timestamp: int) -> str:
    return datetime_to_utc(datetime.fromtimestamp(timestamp/1e3))


def init_logger():
    """
    Initialize bugsnag and global logger object
    """
    mll = DSCLabsLogger()
    logger = mll.get_logger()
    logger.setLevel(INFO)
    return logger


def init_bugsnag_connector(config: dict, app_home: str) -> None:
    """
    Initialize Bugsnag API connector.
    """
    init_bugsnag(
        api_key=config.get('bugsnag', {}).get('api_key', ''),
        app_dir=app_home
    )


def read_json(file_path: str) -> Optional[dict]:
    """Read data from a local json file"""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception:
        return None


def read_yaml(file_path: str) -> Optional[dict]:
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file.read())
        except yaml.YAMLError:
            return None
