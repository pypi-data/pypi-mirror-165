#!/usr/bin/env python3

import os
import yaml
from typing import Any, Dict

from dsc_labs.utils.aws_config_manager import AWSConfigManager

DEPLOYMENT = os.environ.get('DEPLOYMENT') or 'dev'
LOCAL_CONFIG = os.environ.get('LOCAL_CONFIG')
REGION = os.environ.get('AWS_REGION') or 'us-east-1'


class DSCLabsAppConfig:
    """
    Load and return service configuration

    If ``LOCAL_CONFIG`` is set, use it to read config
    Else read config from AWS Config Manager
    """
    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    def get_config(self) -> Dict[str, Any]:
        if LOCAL_CONFIG and os.path.exists(LOCAL_CONFIG):
            return self.get_local_config()
        return self.get_aws_config()

    @staticmethod
    def get_local_config() -> Dict[str, Any]:
        with open(LOCAL_CONFIG) as lc:
            return yaml.safe_load(lc.read())

    def get_aws_config(self) -> Dict[str, Any]:
        opts = {
            'deployment': DEPLOYMENT,
            'region': REGION
        }
        cm = AWSConfigManager(self.service_name, opts)
        return cm.get_param()
