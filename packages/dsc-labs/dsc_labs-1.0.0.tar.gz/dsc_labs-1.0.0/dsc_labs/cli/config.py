#!/usr/bin/env python3
import argparse


from pprint import pprint

from dsc_labs.libs.logger import DSCLabsLogger
from dsc_labs.utils.aws_config_manager import AWSConfigManager

li = DSCLabsLogger(default_handler=True)
logger = li.get_logger()


def run(service, op, opts):
    try:
        cm = AWSConfigManager(service, opts)
        if op == 'get':
            value = cm.get_param()
            pprint(value)
        else:
            resp = cm.put_param()
            pprint(resp)
    except Exception as ex:
        logger.error('Failed: operation="%s" service="%s" error="%s"',
                     op, service, ex)


def main():
    parser = argparse.ArgumentParser(description='DSC-Labs services config helper')
    parser.add_argument(
        '-d', '--deployment',
        default='dev',
        help='The deployment type dev/prod'
    )
    parser.add_argument(
        '-r', '--region',
        default='us-east-1',
        help='The AWS region to use'
    )
    parser.add_argument(
        '-s', '--service',
        required=True,
        help='The service name for the config'
    )
    parser.add_argument(
        '-o', '--operation',
        required=True,
        choices=['get', 'put'],
        help='The desired operation: one of [get, put]'
    )
    parser.add_argument(
        '-c', '--config',
        help='The config file path when operation is put'
    )
    args = parser.parse_args()
    opts = {
        'deployment': args.deployment,
        'region': args.region,
        'config': args.config
    }
    run(args.service, args.operation, opts)
