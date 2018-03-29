
import unittest
import mysql.connector as mariadb

from unittest_base import SQLUnitTestBase
from Project.apps import Apps


class TestApps(SQLUnitTestBase):

    @staticmethod
    def _connect_to_test_db():
        con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='nfschnoo', password='001027748',
                              database='nfschnoo')
        return con

    def test_add_zip(self):
        apps = Apps(self._con, True)
        df = apps.add_zip({'zip': '27511', 'city': 'Cary', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Cary', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        apps.cursor.close()

    def test_update_zip(self):
        apps = Apps(self._con, True)
        # Add zip
        df = apps.add_zip({'zip': '27511', 'city': 'Raleigh', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Raleigh', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        # Update zip
        df = apps.update_zip({'city': 'Cary'}, {'zip': '27511'})
        self.assertEqual(1, len(df.index))
        self.assertEqual('27511', df['zip'].ix[0])
        self.assertEqual('Cary', df['city'].ix[0])
        self.assertEqual('NC', df['state'].ix[0])
        apps.cursor.close()


if __name__ == '__main__':
    unittest.main()