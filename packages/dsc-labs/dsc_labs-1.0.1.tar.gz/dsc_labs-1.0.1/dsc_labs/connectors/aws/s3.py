import json

from typing import Union, Optional, Tuple
from botocore.exceptions import ClientError
from dsc_labs.connectors.aws.base import AWSConnector


class S3Connector(AWSConnector):
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None) -> None:
        super().__init__('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

    def download_object(self, bucket: str, key: str, local_path: str = '') -> Tuple[bool, str]:
        """
        Downloading a file from s3 to file_path
        :param bucket: S3 bucket name
        :param key: S3 object key
        :param local_path: path to save file
        :return: True if it is successful, False if it encountered error
        """

        try:
            self.client.download_file(Bucket=bucket, Key=key, Filename=local_path)
            self.log.info('event=download-s3-object-success bucket={} key={}'.format(bucket, key))
            return True, ''
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                error_msg = 'The object key does not exist.'
            elif e.response['Error']['Code'] == '403':
                error_msg = 'An error occurred (403) when calling the HeadObject operation: Forbidden.'
            else:
                error_msg = str(e)
            self.log.error('event=download-s3-object-failure bucket={} key={} message="{}"'
                           .format(bucket, key, error_msg))
        except BaseException as e:
            error_msg = str(e)
            self.log.error('event=download-s3-object-failure bucket={} key={}'.format(bucket, key))
        return False, error_msg

    def get_object(self, bucket: str, key: str) -> Tuple[Optional[dict], str]:
        """
        Get S3 object
        :param bucket: S3 bucket name
        :param key: S3 object key
        :return: Object if success, otherwise return None
        """
        try:
            s3_object = self.client.get_object(Bucket=bucket, Key=key)
            self.log.info('event=get-s3-object-success bucket={} key={}'.format(bucket, key))
            return s3_object, ''
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                error_msg = 'The object key does not exist.'
            elif e.response['Error']['Code'] == '403':
                error_msg = 'An error occurred (403) when calling the HeadObject operation: Forbidden.'
            else:
                error_msg = str(e)
            self.log.error('event=get-s3-object-failure bucket={} key={} message="{}"'
                           .format(bucket, key, error_msg))
            return None, error_msg

    def put_object(self,
                   bucket: str,
                   key: str,
                   data: Union[bytes, dict, str],
                   metadata=None) -> Tuple[bool, str]:
        """
        Put object into S3 bucket
        :param bucket: S3 bucket name
        :param key: S3 Object key
        :param data: Object data
        :param metadata: Object metadata
        :return: True if it is successful, False if it encountered error
        """

        if metadata is None:
            metadata = {}

        # convert dict to json string
        if isinstance(data, dict):
            data = json.dumps(data)

        try:
            self.client.put_object(Body=data, Bucket=bucket, Key=key, Metadata=metadata)
            self.log.info('event=put-s3-object-success bucket={} key={}'.format(bucket, key))
            return True, ''
        except ClientError as e:
            error_msg = str(e)
            self.log.error('event=put-s3-object-failure bucket="{}" key="{}" message="{}"'
                           .format(bucket, key, error_msg))
        except BaseException as e:
            error_msg = str(e)
            self.log.error('event=put-s3-object-failure bucket="{}" key="{}" message="{}"'
                           .format(bucket, key, error_msg))
        return False, error_msg

    def get_metadata_from_object(self, bucket: str, key: str) -> Tuple[dict, str]:
        """
        Get metadata from S3 object
        :param bucket: S3 bucket name
        :param key: S3 Object key
        :return: Metadata of S3 object
        """
        try:
            response = self.client.head_object(Bucket=bucket, Key=key)
            self.log.info('event=get-s3-metadata-success bucket={} key={}'.format(bucket, key))
            return response.get('Metadata'), ''
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                error_msg = 'The object key does not exist.'
            else:
                error_msg = str(e)
            self.log.error('event=get-s3-metadata-failure bucket="{}" key="{}" message="{}"'
                           .format(bucket, key, error_msg))
        except BaseException as e:
            error_msg = str(e)
            self.log.error('event=get-s3-metadata-failure bucket="{}" key="{}" message="{}"'
                           .format(bucket, key, error_msg))
        return {}, error_msg
