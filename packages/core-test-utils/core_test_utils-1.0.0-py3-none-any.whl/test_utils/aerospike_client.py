__author__ = 'sarvesh.singh'

import aerospike
from test_utils.logger import Logger


class Aerospike:
    """
    Aerospike Connector for Devx
    """

    def __init__(self, host):
        """
        Connect to database and provide it's marker
        :param host:
        """
        self.logger = Logger(name='AEROSPIKE').get_logger
        self.logger.debug('Connecting to cassandra !!')
        self._host = host
        self._connection = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        self.logger.debug(
            f'Making Connection to DB with {self._host}'
        )
        write_policies = {'total_timeout': 2000, 'max_retries': 0}
        read_policies = {'total_timeout': 1500, 'max_retries': 1}
        policies = {'write': write_policies, 'read': read_policies}
        config = dict()
        config['hosts'] = [self._host]
        config['policies'] = policies
        self._connection = aerospike.client(config).connect()

    def shutdown(self):
        """
        Function to shut down db
        :return:
        """
        self.logger.debug(
            f'Shutting down DB with {self._host}'
        )
        self._connection.close()

    def show_namespaces(self):
        """
        Function to show namespaces
        :return:
        """
        self.logger.debug(
            f'Showing namespaces {self._host}'
        )
        return self._connection.info('namespaces')

    def put_data(self, keys=None, data=None):
        """
        Put data
        :return:
        """
        # Write a record
        self._connection.put(keys, data)

    def read_data(self, keys=None):
        """
        Read data
        :return:
        """
        # Read a record
        (keys, meta, record) = self._connection.get(keys)
        return record
