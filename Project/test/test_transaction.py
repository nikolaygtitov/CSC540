
import unittest
import mysql.connector as mariadb
import pandas as pd

from unittest_base import SQLUnitTestBase
from Project.transaction import sql_transaction


class TestTransaction(SQLUnitTestBase):

    @staticmethod
    def _connect_to_test_db():
        con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='nfschnoo', password='001027748', database='nfschnoo')
        return con

    def test_transaction_commit(self):
        cursor = self._con.cursor()
        with sql_transaction(self._con):
            cursor.execute("INSERT INTO ZipToCityState(zip, city, state) VALUES ('27965', 'Raleigh', 'NC')")
            df = pd.read_sql('SELECT * from ZipToCityState', con=self._con)
        self.assertEqual(1, len(df.index))
        self.assertEqual('27965', df['zip'].ix[0])
        self.assertEqual('Raleigh', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        cursor.close()

    def test_transaction_rollback(self):
        cursor = self._con.cursor()
        try:
            with sql_transaction(self._con):
                cursor.execute("INSERT INTO ZipToCityState(zip, city, state) VALUES ('27965', 'Raleigh', 'NC')")
                cursor.execute("INSERT INTO ZipToCityState(zip, city, state) VALUES ('27965', 'Raleigh', 'NC')")
                # Should not reach this point
                self.assertTrue(False)
        except Exception as e:
            # Verify rollback
            df = pd.read_sql('SELECT * from ZipToCityState', con=self._con)
            self.assertEqual(0, len(df.index))
        finally:
            cursor.close()


if __name__ == '__main__':
    unittest.main()