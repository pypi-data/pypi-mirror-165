__author__ = 'sarvesh.singh'

import time
from test_utils.logger import Logger
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.errors import TopicAlreadyExistsError
from kafka.admin import NewTopic


class KafkaClient:
    """
    KafkaClient
    """

    def __init__(self, bootstrap_servers):
        """
        Connect to Kafka and provide it's marker
        :param bootstrap_servers:
        """
        self.logger = Logger(name='KAFKA').get_logger
        self.logger.debug('Connecting to Kafka !!')
        self._bootstrap_servers = bootstrap_servers

        self._consumer = KafkaConsumer(bootstrap_servers=self._bootstrap_servers,
                                       auto_offset_reset='earliest',
                                       consumer_timeout_ms=1000)
        self._producer = KafkaProducer(bootstrap_servers=self._bootstrap_servers)
        self._admin = KafkaAdminClient(bootstrap_servers=self._bootstrap_servers)

    def create_topic(self, topic_name=None):
        """
        Func to create kafka topic
        :param topic_name:
        :return:
        """
        try:
            topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            self._admin.create_topics([topic])
            time.sleep(2)
            self.logger.info(f'Topics list: {self._consumer.topics}')
        except TopicAlreadyExistsError as err:
            print(f"Request for topic creation is failed as {topic_name} is already created due to {err}")
        except Exception as err:
            print(f"Request for topic creation is failing due to {err}")

    def delete_topic(self, topic_name=None):
        """
        Func to delete kafka topic
        :param topic_name:
        :return:
        """
        try:
            self._admin.delete_topics([topic_name])
            self.logger.info(f'Topic {topic_name} deleted !!')
            time.sleep(2)
        except BaseException as ex:
            if ex.message == 'UNKNOWN_TOPIC_OR_PARTITION':
                self.logger.info(f'Topic: {topic_name} does not exist !!')
                time.sleep(2)
            else:
                raise Exception(f'Topic: {topic_name} not deleted ERR: {ex}')

    def produce_event(self, topic_name=None, data=None):
        """
        Func to produce kafka event to a topic
        :param topic_name:
        :param data:
        :return:
        """
        self._producer.send(topic_name, data.encode('utf-8'))
        self._producer.close()

    def consume_event(self, topic_name=None):
        """
        Func to consume kafka event from a topic
        :param topic_name:
        :return:
        """
        while True:
            self._consumer.subscribe([topic_name])
            for message in self._consumer:
                if message is not None:
                    return message.value.decode('utf-8')
