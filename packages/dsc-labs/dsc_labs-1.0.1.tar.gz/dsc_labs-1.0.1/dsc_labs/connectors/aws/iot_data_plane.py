from typing import Optional, Tuple
from dsc_labs.connectors.aws.base import AWSConnector


class IoTDataPlaneConnector(AWSConnector):
    def __init__(self,
                 aws_access_key_id: str = None,
                 aws_secret_access_key: str = None,
                 region_name: str = None) -> None:
        super().__init__('iot-data',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=region_name)

    def publish(self,
                topic: str,
                payload: bytes,
                qos: int = 1,
                retain: bool = False) -> Tuple[bool, str]:
        """
        Publishes an MQTT message
        :param topic: The name of the MQTT topic
        :param payload: The message body. MQTT accepts text, binary, and empty (null) message payloads
        :param qos: The Quality of Service (QoS) level
        :param retain: A Boolean value that determines whether to set the RETAIN flag when the message is published
        """
        try:
            self.client.publish(topic=topic, qos=qos, retain=retain, payload=payload)
            self.log.info('event=publish-mqtt-message-success topic={}'.format(topic))
            return True, ''
        except BaseException as e:
            error_msg = str(e)
            self.log.error('event=publish-mqtt-message-failure topic={} message="{}"'.format(topic, error_msg))
        return False, error_msg

    def get_retained_message(self, topic: str) -> Tuple[Optional[dict], str]:
        """
        Gets the details of a single retained message for the specified topic
        :param topic: The topic name of the retained message to retrieve
        :return: MQTT message
        """
        try:
            response = self.client.get_retained_message(
                topic=topic
            )
            self.log.info('event=get-retained-message-success topic={}'.format(topic))
            return response, ''
        except BaseException as e:
            error_msg = str(e)
            self.log.error('event=get-retained-message-failure topic={} message="{}"'.format(topic, error_msg))
        return None, error_msg
