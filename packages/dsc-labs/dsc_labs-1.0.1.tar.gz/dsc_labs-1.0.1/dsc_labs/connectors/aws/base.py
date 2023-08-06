import boto3
from dsc_labs.libs.logger import DSCLabsLoggerMixin


class AWSConnector(DSCLabsLoggerMixin):
    def __init__(self, service: str, *argv, **kwargs) -> None:
        super().__init__()
        aws_access_key_id = kwargs.get('aws_access_key_id', None)
        aws_secret_access_key = kwargs.get('aws_secret_access_key', None)
        if (aws_access_key_id is None) or (aws_secret_access_key is None):
            self.client = boto3.client(service)
        else:
            self.client = boto3.client(service, *argv, **kwargs)
