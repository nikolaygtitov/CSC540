
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

    def test_delete_zip(self):
        apps = Apps(self._con, True)
        df = apps.add_zip({'zip': '27511', 'city': 'Cary', 'state': 'NC'})
        self.assertEqual(1, len(df.index))
        df = apps.delete_zip({'zip': '27511'})
        self.assertEqual(0, len(df.index))
        df = apps._execute_select_query('*', 'ZipToCityState')
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_report_occupancy_by_hotel(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_hotel('2017-01-16')
        self.assertEqual(8, len(df.index))
        self.assertEqual('Wolf Inn Miami Panthers', df['Hotel Name'].ix[5])
        self.assertEqual(1, df['Rooms Occupied'].ix[5])
        self.assertEqual(1, df['Total Rooms'].ix[5])
        self.assertEqual(100.0, df['% Occupancy'].ix[5])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_room_type(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_room_type('2017-01-16')
        self.assertEqual(4, len(df.index))
        self.assertEqual('Executive Suite', df['Room Type'].ix[2])
        self.assertEqual(1, df['Rooms Occupied'].ix[2])
        self.assertEqual(2, df['Total Rooms'].ix[2])
        self.assertEqual(50.0, df['% Occupancy'].ix[2])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_city(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_city('2017-01-16')
        self.assertEqual(6, len(df.index))
        self.assertEqual('Miami, FL', df['City, State'].ix[2])
        self.assertEqual(1, df['Rooms Occupied'].ix[2])
        self.assertEqual(1, df['Total Rooms'].ix[2])
        self.assertEqual(100.0, df['% Occupancy'].ix[2])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_date_range(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_date_range('2015-01-01', '2017-12-31')
        print df
        self.assertEqual(1, len(df.index))
        self.assertEqual(1, df['Actual Bookings'].ix[0])
        self.assertEqual(1, df['Total Possible Bookings'].ix[0])
        self.assertEqual(1, df['% Occupancy'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_staff_by_role(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_staff_by_role(2)
        self.assertEqual(2, len(df.index))
        self.assertEqual('Management Department', df['Department'].ix[0])
        self.assertEqual('Manager', df['Title'].ix[0])
        self.assertEqual('Joe S. Rogan', df['Staff Name'].ix[0])
        self.assertEqual(1, df['Staff ID'].ix[0])
        self.assertEqual('Room Service Department', df['Department'].ix[1])
        self.assertEqual('Room Service Staff', df['Title'].ix[1])
        self.assertEqual('Rory McDonald', df['Staff Name'].ix[1])
        self.assertEqual(8, df['Staff ID'].ix[1])
        self._con.commit()
        apps.cursor.close()

    def test_report_customer_interactions(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_customer_interactions(8)
        self.assertEqual(2, len(df.index))
        self.assertEqual('Conor McGregor', df['Staff Name'].ix[0])
        self.assertEqual(2, df['Staff ID'].ix[0])
        self.assertEqual('Luke Rockhold', df['Staff Name'].ix[1])
        self.assertEqual(3, df['Staff ID'].ix[1])
        self._con.commit()
        apps.cursor.close()

    def test_report_revenue_single_hotel(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_revenue_single_hotel('2015-01-01', '2017-12-31', 1)
        self.assertEqual(1, len(df.index))
        self.assertEqual('Wolf Inn Raleigh Hurricanes', df['Hotel Name'].ix[0])
        self.assertEqual(591.79, df['Revenue'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_revenue_all_hotels(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_revenue_all_hotels('2015-01-01', '2017-12-31')
        self.assertEqual(3, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Miami Panthers', row['Hotel Name'])
        self.assertEqual(12.00, row['Revenue'])
        row = df.ix[1]
        self.assertEqual('Wolf Inn Philadelphia Flyers', row['Hotel Name'])
        self.assertEqual(30.00, row['Revenue'])
        row = df.ix[2]
        self.assertEqual('Wolf Inn Raleigh Hurricanes', row['Hotel Name'])
        self.assertEqual(591.79, row['Revenue'])
        self._con.commit()
        apps.cursor.close()


if __name__ == '__main__':
    unittest.main()