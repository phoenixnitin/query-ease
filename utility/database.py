import psycopg2
import sqlparse

from logger import Logger


class Database:
    __host = None
    __port = None
    __database = None
    __username = None
    __password = None
    __connection = None
    __logger = Logger.get_logger()


    @classmethod
    def reset(cls, host, port, database, username, password):
        """
        Method to reset database connection
        """
        cls.__logger.info('resetting database details...')
        if cls.__connection is not None:
            cls.__close_existing_connection()
        cls.__host = host
        cls.__port = port
        cls.__database = database
        cls.__username = username
        cls.__password = password
        cls.__logger.info(f'database is ready to connect to {database} database of {host} host at port: {port}')
        cls.__connection = None

    @classmethod
    def get_connection(cls):
        """
        Method to access connection object
        """
        if cls.__connection is None:
            cls.__create_postgres_connection()
        return cls.__connection

    @classmethod
    def validate_query(cls, query):
        """
        Method to validate query
        """
        status = False
        query_type = cls.__get_query_type(query)
        cls.__logger.info(f'validating query...')
        if query_type == 'SELECT':
            if cls.__check_query_syntax_against_database(query):
                status = True
            else:
                cls.__logger.info(f'query syntax is incorrect')
        else:
            cls.__logger.info(f'query is not select query. given query type: {query_type}')
        return status

    @classmethod
    def execute_query(cls, query, commit=False):
        """
        Method to execute query
        """
        status, result = False, list()
        query_type = cls.__get_query_type(query)
        connection = cls.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            if commit:
                connection.commit()
            if query_type == 'SELECT':
                result = cursor.fetchall()
            status = True
        except Exception as exception:
            cls.__logger.exception(exception)
        finally:
            cursor.close()
            return status, result

    @classmethod
    def __check_query_syntax_against_database(cls, query):
        """
        Method to check query syntax against database using EXPLAIN
        """
        explain_query = f'EXPLAIN {query}'
        status, _ = cls.execute_query(explain_query)
        return status

    @classmethod
    def __get_query_type(cls, query):
        """
        Method to identify the type of the sql query
        """
        command_type = None
        try:
            cls.__logger.info('identifying query type...')
            parsed_query = sqlparse.parse(query)
            statement = parsed_query[0]
            command_type = statement.get_type()
            cls.__logger.info(f'identified as {command_type} query')
        except Exception as exception:
            cls.__logger.exception(exception)
        return command_type

    @classmethod
    def __create_postgres_connection(cls):
        """
        Method to create postgres connection
        """
        try:
            connection_info = cls.__create_connection_info()
            cls.__logger.info('connecting to database...')
            cls.__connection = psycopg2.connect(connection_info)
            cls.__logger.info('connected')
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __create_connection_info(cls):
        """
        Method to create postgres connection string
        """
        cls.__logger.info('creating postgres connection string...')
        connection_info = f'postgresql://{cls.__username}:{cls.__password}@{cls.__host}:{cls.__port}/{cls.__database}'
        cls.__logger.info('created')
        return connection_info

    @classmethod
    def __close_existing_connection(cls):
        """
        Method to close database connection
        """
        try:
            cls.__logger.info('closing database connection...')
            cls.__connection.close()
            cls.__logger.info('closed')
        except Exception as exception:
            cls.__logger.exception(exception)
