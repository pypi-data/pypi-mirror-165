__author__ = 'sarvesh.singh'

import redis
from test_utils.logger import Logger


class Redis:
    """
    Redis Connector
    """

    def __init__(self, host, port):
        """
        Connect to redis and provide it's marker
        :param host:
        :param port:
        """
        self.logger = Logger(name='REDIS').get_logger
        self.logger.debug('Connecting to redis !!')
        self._host = host
        self._port = port

        # variables
        self._connection = None
        self._connect_to_redis()

    def _connect_to_redis(self):
        """
        Function to connect to redis
        :return:
        """
        self.logger.debug(
            f'Making Connection to Redis with {self._host} {self._port}'
        )
        self._connection = redis.Redis(host=self._host, port=self._port)

    def insert_key(self, key, value):
        """
        Insert key
        :param key:
        :param value:
        :return:
        """
        self.logger.debug(f'Setting key: {key} with value {value}')
        self._connection.set(key, value)

    def get_key(self, key):
        """
        Get key
        :param key:
        :return:
        """
        self.logger.debug(f'Getting key value: {key}')
        return self._connection.get(key).decode('utf-8')
