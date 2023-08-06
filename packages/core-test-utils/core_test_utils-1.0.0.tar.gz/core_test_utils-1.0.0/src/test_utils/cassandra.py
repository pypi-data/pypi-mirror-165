__author__ = 'sarvesh.singh'

from cassandra.cluster import Cluster
from test_utils.logger import Logger


class Cassandra:
    """
    Cassandra Connector for Devx
    """

    def __init__(self, host, database=None):
        """
        Connect to database and provide it's marker
        :param host:
        :param database:
        """
        self.logger = Logger(name='CASSANDRA').get_logger
        self.logger.debug('Connecting to cassandra !!')
        self._host = host
        self._database = database

        # variables
        self._cluster = None
        self._connection = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        self.logger.debug(
            f'Making Connection to DB with {self._host} {self._database}'
        )
        self._cluster = Cluster([self._host])
        self._connection = self._cluster.connect(self._database, wait_for_all_pools=True)

    def shutdown(self):
        """
        Function to shut down db
        :return:
        """
        self.logger.debug(
            f'Shutting down DB with {self._host} {self._database}'
        )
        self._cluster.shutdown()

    def run_query(self, query):
        """
        Run db Query Only
        :param query:
        :return:
        """
        self.logger.debug(f'Running SQL Query {query} but not fetching data ...')
        self._connection.execute(query)

    def run_and_fetch_data(self, query):
        """
        Run db Query and Fetch Data from Database
        :param query:
        :return:
        """
        _data = list()
        self.logger.debug(f'Running SQL Query {query} and fetching data ...')
        rows = self._connection.execute(query)
        for row in rows:
            _data.append(row)
        return _data
