#!/usr/bin/env python3

import os
import yaml
import boto3


from yaml.parser import ParserError

from dsc_labs.libs.logger import DSCLabsLogger


class AWSConfigManager:
    def __init__(self, service, opts):
        li = DSCLabsLogger(default_handler=True)
        self.log = li.get_logger()
        self.deployment = opts['deployment']
        self.service = service
        self.config = opts.get('config')
        self.client = boto3.client('ssm', region_name=opts['region'])
        self.parameter_path = 'config.dsc-labs.%s.%s-service' % (
            self.deployment, self.service
        )

    def get_param(self):
        parameter = self.client.get_parameter(
            Name=self.parameter_path,
            WithDecryption=True
        )
        value = parameter.get('Parameter', {}).get('Value', '')
        if not value:
            raise RuntimeError('Unable to get the specified parameter from AWS')
        return yaml.safe_load(value)

    def is_config_readable(self):
        return os.path.exists(self.config) and os.access(self.config, os.R_OK)

    @staticmethod
    def is_config_valid(config_val):
        try:
            yaml.safe_load(config_val)
            return True
        except ParserError:
            return False

    def put_param(self):
        if not self.config:
            raise RuntimeError('Need a config file for put operation')
        if not self.is_config_readable():
            raise IOError('Unable to read config from file: %s' % self.config)
        config_val = open(self.config).read()
        if not self.is_config_valid(config_val):
            raise RuntimeError('Invalid config file: %s' % self.config)
        resp = self.client.put_parameter(
            Name=self.parameter_path,
            Description='deployment=%s service_name=%s-service' % (
                self.deployment,
                self.service
            ),
            Value=config_val,
            Overwrite=True,
            Type='SecureString',
            Tier='Standard'
        )
        status = resp.get('ResponseMetadata', {}).get('HTTPStatusCode')
        if status != 200:
            raise RuntimeError('Failed to update config for %s' % self.service)
        return status
