__author__ = 'sarvesh.singh'

import psycopg2
from test_utils.logger import Logger


class Postgresql:
    """
    Postgresql Connector
    """

    def __init__(self, host, username, password, database=None):
        """
        Connect to database and provide it's marker
        :param host:
        :param username:
        :param password:
        :param database:
        """
        self.logger = Logger(name='POSTGRESQL').get_logger
        self.logger.debug('Connecting to postgresql !!')
        self._host = host
        self._username = username
        self._password = password
        self._database = database

        # variables
        self._connection = None
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Function to connect to db
        :return:
        """
        self.logger.debug(
            f'Making Connection to DB with {self._username} {self._password} {self._host} {self._database}'
        )
        self._connection = psycopg2.connect(
            host=self._host,
            user=self._username,
            password=self._password,
            database=self._database,
        )

    def run_query(self, query):
        """
        Run db Query Only
        :param query:
        :return:
        """
        self.logger.debug(f'Running SQL Query {query} but not fetching data ...')
        with self._connection.cursor() as cursor:
            cursor.execute(query)

    def run_and_fetch_data(self, query):
        """
        Run db Query and Fetch Data from Database
        :param query:
        :return:
        """
        self.logger.debug(f'Running SQL Query {query} and fetching data ...')
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def delete_data_query(self, query):
        """
        Function to run query to delete data from database
        :param query:
        :return:
        """
        self.logger.debug(f'Running Delete Query {query}')
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            self._connection.commit()

    def insert_columns(self, query):
        """
        Function to insert new columns in db
        :param query:
        :return:
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            self._connection.commit()
