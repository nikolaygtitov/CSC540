
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

    def test_get_data_frame_star_no_where(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.get_data_frame('*', 'Hotels')
        self.assertEqual(9, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Raleigh Hurricanes', row['name'])
        self.assertEqual('100 Glenwood Ave', row['street'])
        self.assertEqual('27965', row['zip'])
        self.assertEqual('919-965-6743', row['phone_number'])
        row = df.ix[7]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        self.assertEqual('9000 Lincoln Ave', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('213-628-8344', row['phone_number'])
        apps.cursor.close()

    def test_get_data_frame_star_where_name(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.get_data_frame('*', 'Hotels',
                                 "name='Wolf Inn Los Angeles Sharks'")
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        self.assertEqual('9000 Lincoln Ave', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('213-628-8344', row['phone_number'])
        apps.cursor.close()

    def test_get_data_frame_multiple_fields(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.get_data_frame('name, zip', 'Hotels',
                                 "phone_number='213-628-8344'")
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        self.assertEqual('90050', row['zip'])
        apps.cursor.close()

    def test_get_data_frame_single_field(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.get_data_frame('name', 'Hotels',
                                 "phone_number='213-628-8344'")
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        apps.cursor.close()

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
        df = apps.get_data_frame('*', 'ZipToCityState')
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_add_hotel_no_id(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_hotel({
            'name': 'Test Hotel',
            'street': '123 Test St',
            'zip': '90050',
            'phone_number': '919-123-4567'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Test Hotel', row['name'])
        self.assertEqual('123 Test St', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('919-123-4567', row['phone_number'])
        apps.cursor.close()

    def test_add_hotel_id(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_hotel({
            'id': 100,
            'name': 'Test Hotel',
            'street': '123 Test St',
            'zip': '90050',
            'phone_number': '919-123-4567'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(100, row['id'])
        self.assertEqual('Test Hotel', row['name'])
        self.assertEqual('123 Test St', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('919-123-4567', row['phone_number'])
        # Add hotel with lower id - not the highest
        df = apps.add_hotel({
            'id': 99,
            'name': 'Test Hotel 2',
            'street': '456 Test St',
            'zip': '90050',
            'phone_number': '919-345-6789'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(99, row['id'])
        self.assertEqual('Test Hotel 2', row['name'])
        self.assertEqual('456 Test St', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('919-345-6789', row['phone_number'])
        apps.cursor.close()

    def test_add_hotel_fail_id_exists(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        apps.add_hotel({
            'id': 100,
            'name': 'Test Hotel',
            'street': '123 Test St',
            'zip': '90050',
            'phone_number': '919-123-4567'
        })
        try:
            apps.add_hotel({
                'id': 100,
                'name': 'Test Hotel 2',
                'street': '456 Test St',
                'zip': '90050',
                'phone_number': '919-234-5678'
            })
            self.assertTrue(False)
        except mariadb.Error:
            pass
        apps.cursor.close()

    def test_update_hotel_name_where_name(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'name': 'Test Hotel'
        }, {
            'name': 'Wolf Inn Raleigh Wolfpack'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Test Hotel', row['name'])
        apps.cursor.close()

    def test_update_hotel_id_where_id(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'id': 10
        }, {
            'id': 2
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        apps.cursor.close()

    def test_update_hotel_multiple_fields_where_id(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'id': 10,
            'name': 'Test Hotel',
            'street': '123 Test Dr',
            'zip': '90050',
            'phone_number': '919-987-6543'
        }, {
            'id': 2
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual('Test Hotel', row['name'])
        self.assertEqual('123 Test Dr', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('919-987-6543', row['phone_number'])
        apps.cursor.close()

    def test_update_hotel_name_where_multiple(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'name': 'Test Hotel'
        }, {
            'name': 'Wolf Inn Raleigh Wolfpack',
            'street': '875 Penny Rd',
            'zip': '27606',
            'phone_number': '919-546-7439'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Test Hotel', row['name'])
        apps.cursor.close()

    def test_update_hotel_id_where_multiple(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'id': 10
        }, {
            'name': 'Wolf Inn Raleigh Wolfpack',
            'street': '875 Penny Rd',
            'zip': '27606',
            'phone_number': '919-546-7439'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        apps.cursor.close()

    def test_update_hotel_multiple_fields_where_multiple(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({
            'id': 10,
            'name': 'Test Hotel',
            'street': '123 Test Dr',
            'zip': '90050',
            'phone_number': '919-987-6543'
        }, {
            'id': 2,
            'name': 'Wolf Inn Raleigh Wolfpack',
            'street': '875 Penny Rd',
            'zip': '27606',
            'phone_number': '919-546-7439'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual('Test Hotel', row['name'])
        self.assertEqual('123 Test Dr', row['street'])
        self.assertEqual('90050', row['zip'])
        self.assertEqual('919-987-6543', row['phone_number'])
        apps.cursor.close()

    def test_update_hotel_id_does_not_exist(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.update_hotel({'id': 10}, {'id': 100})
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_delete_hotel_id(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        apps.add_hotel({
            'id': 100,
            'name': 'Test Hotel',
            'street': '123 Test St',
            'zip': '90050',
            'phone_number': '919-123-4567'
        })
        df = apps.delete_hotel({'id': 100})
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_delete_hotel_id_does_not_exist(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.delete_hotel({'id': 100})
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_delete_hotel_name(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        apps.add_hotel({
            'id': 100,
            'name': 'Test Hotel',
            'street': '123 Test St',
            'zip': '90050',
            'phone_number': '919-123-4567'
        })
        df = apps.delete_hotel({'name': 'Test Hotel'})
        self.assertEqual(0, len(df.index))

    def test_add_staff(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        # Do not assign to room when created
        df = apps.add_staff(
            {'name': 'FirstTest LastTest', 'title': 'Room Service Staff',
             'date_of_birth': '1985-04-05', 'department': 'Service',
             'phone_number': '(919)-555-1111', 'street': 'TestStreet',
             'zip': '27606', 'works_for_hotel_id': 2})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('FirstTest LastTest', row['name'])
        self.assertEqual('Room Service Staff', row['title'])
        self.assertEqual('1985-04-05', row['date_of_birth'])
        self.assertEqual('Service', row['department'])
        self.assertEqual('(919)-555-1111', row['phone_number'])
        self.assertEqual('TestStreet', row['street'])
        self.assertEqual('27606', row['zip'])
        self.assertEqual(2, row['works_for_hotel_id'])
        # Assign staff to room when created
        df = apps.add_staff(
            {'name': 'FirstTestTwo LastTestTwo', 'title': 'Room Service Staff',
             'date_of_birth': '1989-03-10', 'department': 'Service',
             'phone_number': '(919)-666-2222', 'street': 'TestStreetTwo',
             'zip': '27606', 'works_for_hotel_id': 9,
             'assigned_hotel_id': 9, 'assigned_room_number': 100})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('FirstTestTwo LastTestTwo', row['name'])
        self.assertEqual('Room Service Staff', row['title'])
        self.assertEqual('1989-03-10', row['date_of_birth'])
        self.assertEqual('Service', row['department'])
        self.assertEqual('(919)-666-2222', row['phone_number'])
        self.assertEqual('TestStreetTwo', row['street'])
        self.assertEqual('27606', row['zip'])
        self.assertEqual(9, row['works_for_hotel_id'])
        self.assertEqual(9, row['assigned_hotel_id'])
        self.assertEqual(100, row['assigned_room_number'])
        self.assertEqual(11, row['Serves_staff_id'])
        self.assertEqual(9, row['Serves_reservation_id'])
        apps.cursor.close()

    def test_update_staff(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        # Assign to a room and also update some other 3 attributes
        # Search is done based on Name not ID, but should return ID as well
        df = apps.update_staff(
            {'date_of_birth': '1945-05-09',
             'phone_number': '(919)-222-0202',
             'street': 'Staff Updated St., Apt. A',
             'assigned_hotel_id': 9, 'assigned_room_number': 100},
            {'name': 'FirstStaff LastStaff'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(9, row['id'])
        self.assertEqual('1945-05-09', row['date_of_birth'])
        self.assertEqual('(919)-222-0202', row['phone_number'])
        self.assertEqual('Staff Updated St., Apt. A', row['street'])
        self.assertEqual(9, row['assigned_hotel_id'])
        self.assertEqual(100, row['assigned_room_number'])
        self.assertEqual(9, row['Serves_staff_id'])
        self.assertEqual(9, row['Serves_reservation_id'])
        apps.cursor.close()
        # Free staff from reservation based on ID
        df = apps.update_staff(
            {'assigned_hotel_id': None, 'assigned_room_number': None},
            {'id': 9})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(9, row['id'])
        self.assertEqual('NULL', row['assigned_hotel_id'])
        self.assertEqual('NULL', row['assigned_room_number'])
        apps.cursor.close()

    def test_delete_staff(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.delete_staff({'id': 9})
        self.assertEqual(0, len(df.index))
        df = apps.get_data_frame('*', 'Staff')
        self.assertEqual(8, len(df.index))
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
        self.assertEqual(25.0, df['Actual Bookings'].ix[0])
        self.assertEqual(8760, df['Total Possible Bookings'].ix[0])
        self.assertEqual(1.8721, df['% Occupancy'].ix[0])
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
