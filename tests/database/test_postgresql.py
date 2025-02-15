import logging
import unittest

import pkg_resources
from psycopg2 import OperationalError

from migrator.database.PostgreSQLDatabase import PostgreSQLDatabase
from migrator.server.PostgreSQLServer import PostgreSQLServer

logging.basicConfig(
    filename="TestDatabase_PostgreSQL.log",
    level=logging.INFO,
    format="|"
    "%(asctime)-18s|"
    "%(levelname)-4s|"
    "%(module)-18s|"
    "%(filename)-18s:%(lineno)-4s|"
    "%(funcName)-18s|"
    "%(message)-32s|",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class PostgreSQLDatabaseTestCase(unittest.TestCase):
    """
    Test class for PostgreSQL database class.
    """

    def __build_server(self):
        """
        Build PostgreSQL server object to run unit tests against.

        Args:
            None

        Returns:
            server:     PostgreSQLServer object
                        PostgreSQLServer object representing a running
                        PostgreSQL server
        """
        server = None

        try:
            # create server object
            server = PostgreSQLServer(
                host="localhost", port="5432", dbname="testserver2"
            )

        except OperationalError:
            logging.warning("Verify MySQL server is running.")

        finally:
            return server

    def __get_result(self, path):
        """
        Run the test query contained in the given test file.

        Args:
            path:       string
                        filename containing SQL test query

        Returns:
            result:     string
                        First record returned by query
        """
        # build server
        server = self.__build_server()
        if server is None:
            self.skipTest("Verify PostgreSQL server is running")

        # load SQL query
        filepath = pkg_resources.resource_filename(__name__, path)
        f = open(filepath, "r")
        sql = f.read()
        f.close()

        # execute query
        cnxn = server.get_connection()
        cursor = cnxn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()[0]

        return result

    def test_database_type(self):
        """
        Test to ensure creating a PostgreSQL database object generates an object
        of the expected type.
        """
        # build server
        server = self.__build_server()
        if server is None:
            self.skipTest("Verify MySQL server is running")

        database = server.get_database()
        self.assertIsInstance(database, PostgreSQLDatabase)

    def test_migrations_run(self):
        """
        Test to ensure the _MigrationsRun table was created in the database.
        """
        # build SQL query and execute
        path = "postgresql/test_migrations_run.sql"
        result = self.__get_result(path)

        # run the test
        self.assertEqual(result, "_migrationsrun")

    def test_insert_migrations_run(self):
        """
        Test to ensure the _Insert_MigrationsRun procedure gets created in
        PostgreSQL databases during server/database connection.
        """
        # build SQL query and execute
        path = "postgresql/test_insert_migrations_run.sql"
        result = self.__get_result(path)

        # run the test
        self.assertEqual(result, "_insert_migrationsrun")

    def test_check_migration(self):
        """
        Test to ensure _Check_Migration function gets created in PostgreSQL
        databases during server/database connection.
        """
        # build SQL query and execute
        path = "postgresql/test_check_migration.sql"
        result = self.__get_result(path)

        # run the test
        self.assertEqual(result, "_check_migration")
