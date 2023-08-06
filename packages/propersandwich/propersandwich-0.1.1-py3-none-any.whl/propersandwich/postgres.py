"""
This module will help to perform CRUD operations with Postgres databases
"""

import psycopg2
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def connection(database):
    """
    Create a session with a given database and return a new connection object.


    :param str database: the name of the database that will be used as prefix to get its credentials

    :returns: connection object
    :rtype: connection

    """

    dbname = os.getenv(f'{database}_DBNAME')
    user = os.getenv(f'{database}_USER')
    password = os.getenv(f'{database}_PASSWORD')
    host = os.getenv(f'{database}_HOST')
    port = os.getenv(f'{database}_PORT')

    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)



def query(database, sql_query) -> list:
    """
    Run a query against a database then returns it's result as a list


    :param str database: the name of the database that will be used as prefix to get its credentials
    :param str sql_query: The sql query that will be executed

    :returns: a list of records
    :rtype: list

    """
    try:
        conn = connection(database)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        logging.error(f'Error while executing query on {database} database', error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info(f'The connection to {database} database is now closed')

    return data



