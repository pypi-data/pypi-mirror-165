import json
import yaml

from typing import Optional
from logging import INFO
from datetime import datetime, timedelta

from dsc_labs.libs.config import DSCLabsAppConfig
from dsc_labs.libs.logger import DSCLabsLogger
from dsc_labs.libs.bugsnag import init_bugsnag


def get_common_config(service_name: str = "") -> dict:
    """
    Initialize common configurations.
    :return: A dict containing the whole common config data.
    """
    mlc = DSCLabsAppConfig(service_name)
    common_config = mlc.get_config()

    return common_config


def datetime_to_utc(timestamp: datetime) -> str:
    """
    Convert timestamp (datetime object) to UTC time
    :param timestamp: datetime
    :return: UTC time as string with iso format
    """
    return f'{timestamp.isoformat(timespec="milliseconds")}Z'


def current_utc_timestamp() -> str:
    """
    Get current UTC timestamp
    :return: The current UTC timestamp.
    """
    return datetime_to_utc(datetime.utcnow())


def current_utc_timestamp_filename(datetime_format: str = '%Y-%m-%d_%H%M%S%f',
                                   delta_time: int = 0) -> str:
    """
    Get current utc timestamp (millisecond) as filename
    :param datetime_format: datetime format, should use dash and underscore instead of whitespace and colon
    :param delta_time: Delta time with each timezone. Ex: VN - timezone=7 (UTC+7)
    :return: Timestamp with filename format
    """
    now = datetime.utcnow() + timedelta(hours=delta_time)
    return now.strftime(datetime_format)


def int_to_utc(timestamp: int) -> str:
    """
    Convert timestamp (int) to UTC timestamp
    :param timestamp: Timestamp as int
    :return: The current UTC timestamp as string
    """
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
    """
    Read data from a local json file
    :param file_path: Path to json file
    :return: Dictionary if success, otherwise return None
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception:
        return None


def read_yaml(file_path: str) -> Optional[dict]:
    """
    Read data from a local yaml file
    :param file_path: Path to yaml file
    :return: Dictionary if success, otherwise return None
    """
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file.read())
        except yaml.YAMLError:
            return None
