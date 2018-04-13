
import unittest
import mysql.connector as mariadb

from unittest_base import SQLUnitTestBase
from Project.apps import Apps
from Project.demo_data import load_demo_data

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
                                 {'name':'Wolf Inn Los Angeles Sharks'})
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
                                 {'phone_number':'213-628-8344'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        self.assertEqual('90050', row['zip'])
        apps.cursor.close()

    def test_get_data_frame_single_field(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.get_data_frame('name', 'Hotels',
                                 {'phone_number':'213-628-8344'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        apps.cursor.close()

    def test_execute_update_query_update_in_where_clause(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps._execute_update_query(
            'name, phone_number', 'Hotels',
            {'phone_number': '213-123-4567'},
            {'phone_number': '213-628-8344'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Wolf Inn Los Angeles Sharks', row['name'])
        self.assertEqual('213-123-4567', row['phone_number'])
        apps.cursor.close()

    def test_execute_update_query_update_not_in_where_clause(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps._execute_update_query(
            '*', 'Hotels',
            {'name': 'Test Hotel'},
            {'phone_number': '213-628-8344'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Test Hotel', row['name'])
        self.assertEqual('213-628-8344', row['phone_number'])
        apps.cursor.close()

    def test_execute_update_query_update_multiple(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps._execute_update_query(
            '*', 'Hotels',
            {'name': 'Same Name Hotel'},
            {'zip': '27606'})
        self.assertEqual(2, len(df.index))
        row = df.ix[0]
        self.assertEqual('Same Name Hotel', row['name'])
        self.assertEqual('919-546-7439', row['phone_number'])
        row = df.ix[1]
        self.assertEqual('Same Name Hotel', row['name'])
        self.assertEqual('(919)-555-5555', row['phone_number'])
        apps.cursor.close()

    def test_execute_update_query_update_empty_where(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps._execute_update_query(
            'amount', 'Transactions',
            {'amount': 1},
            {})
        self.assertEqual(8, len(df.index))
        self.assertListEqual([1] * 8, list(df['amount']))
        apps.cursor.close()

    def test_execute_select_query(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        apps._execute_select_query('*', 'Hotels', 'zip=%s', ['27606'])
        results = apps.cursor.fetchall()
        print results
        self.assertEqual(2, len(results))
        row = results[0]
        self.assertEqual('Wolf Inn Raleigh Wolfpack', row[1])
        row = results[1]
        self.assertEqual('Nikolay Test Inn', row[1])
        apps.cursor.close()

    def test_execute_select_query_no_where(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        apps._execute_select_query('*', 'Hotels')
        results = apps.cursor.fetchall()
        print results
        self.assertEqual(9, len(results))
        row = results[0]
        self.assertEqual('Wolf Inn Raleigh Hurricanes', row[1])
        row = results[1]
        self.assertEqual('Wolf Inn Raleigh Wolfpack', row[1])
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
        self.assertEqual('1985-04-05', str(row['date_of_birth']))
        self.assertEqual('Service', row['department'])
        self.assertEqual('(919)-555-1111', row['phone_number'])
        self.assertEqual('TestStreet', row['street'])
        self.assertEqual('27606', row['zip'])
        self.assertEqual(2, row['works_for_hotel_id'])
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Assign staff to room when created
        df = apps.add_staff(
            {'id': 100,
             'name': 'FirstTestTwo LastTestTwo', 'title': 'Room Service Staff',
             'date_of_birth': '1989-03-10', 'department': 'Service',
             'phone_number': '(919)-666-2222', 'street': 'TestStreetTwo',
             'zip': '27606', 'works_for_hotel_id': 9,
             'assigned_hotel_id': 9, 'assigned_room_number': 100})
        self.assertEqual(2, len(df.index))
        row = df.ix[0]
        self.assertEqual('FirstTestTwo LastTestTwo', row['name'])
        self.assertEqual('Room Service Staff', row['title'])
        self.assertEqual('1989-03-10', str(row['date_of_birth']))
        self.assertEqual('Service', row['department'])
        self.assertEqual('(919)-666-2222', row['phone_number'])
        self.assertEqual('TestStreetTwo', row['street'])
        self.assertEqual('27606', row['zip'])
        self.assertEqual(9, row['works_for_hotel_id'])
        self.assertEqual(9, row['assigned_hotel_id'])
        self.assertEqual(100, row['assigned_room_number'])
        row = df.ix[1]
        self.assertEqual(100, row['Serves_staff_id'])
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
            {'name': 'Service Dude'})
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
        self.assertEqual(9, len(df.index))
        apps.cursor.close()

    def test_add_reservation(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        # Create Non-Presidential reservation w/out check-in and check-out time
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-04-11',
             'end_date': '2018-04-18', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2, row['number_of_guests'])
        self.assertEqual('2018-04-11', str(row['start_date']))
        self.assertEqual('2018-04-18', str(row['end_date']))
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(100, row['room_number'])
        self.assertEqual(1, row['customer_id'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        apps.cursor.close()

    def test_add_reservation_check_in_time_non_presidential(self):
        # Create Non-Presidential reservation with check-in time, but no
        # check-out time
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-04-19',
             'end_date': '2018-04-26', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1,
             'check_in_time': '2018-04-11 12:12:12'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2, row['number_of_guests'])
        self.assertEqual('2018-04-19', str(row['start_date']))
        self.assertEqual('2018-04-26', str(row['end_date']))
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(100, row['room_number'])
        self.assertEqual(1, row['customer_id'])
        self.assertEqual('2018-04-11 12:12:12', str(row['check_in_time']))
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        apps.cursor.close()

    def test_add_reservation_check_in_check_out(self):
        # Create Non-Presidential reservation with check-in and check-out time.
        # Should not free any staff. But add new transaction 'Room Charge'
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-05-01',
             'end_date': '2018-05-05', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1,
             'check_in_time': '2018-05-01 12:12:12',
             'check_out_time': '2018-05-05 09:09:09'})
        self.assertEqual(2, len(df.index))
        row = df.ix[0]
        self.assertEqual('2018-05-05 09:09:09', str(row['check_out_time']))
        row = df.ix[1]
        self.assertEqual(9, row['Transaction_id'])
        self.assertEqual(400.0, row['Transaction_amount'])
        self.assertEqual('4-night(s) Room Reservation Charge',
                         row['Transaction_type'])
        self.assertEqual('2018-05-05', str(row['Transaction_date'].date()))
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        apps.cursor.close()

    def test_add_reservation_presidential(self):
        # Create Presidential reservation w/out check-in and check-out time
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-01',
             'end_date': '2018-04-07', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(5, row['number_of_guests'])
        self.assertEqual('2018-04-01', str(row['start_date']))
        self.assertEqual('2018-04-07', str(row['end_date']))
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(500, row['room_number'])
        self.assertEqual(2, row['customer_id'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        apps.cursor.close()

    def test_add_reservation_presidential_check_in(self):
        # Create Presidential reservation with check-in, but not check-out time.
        # Must assign Room Service and Catering Staff.
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-08',
             'end_date': '2018-04-12', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2,
             'check_in_time': '2018-04-08 15:15:15'})
        print df
        self.assertEqual(2, len(df.index))
        row1 = df.ix[0]
        row2 = df.ix[1]
        self.assertEqual(5, row1['number_of_guests'])
        self.assertEqual('2018-04-08', str(row1['start_date']))
        self.assertEqual('2018-04-12', str(row1['end_date']))
        self.assertEqual(9, row1['hotel_id'])
        self.assertEqual(500, row1['room_number'])
        self.assertEqual(2, row1['customer_id'])
        self.assertEqual('2018-04-08 15:15:15', str(row1['check_in_time']))
        self.assertEqual(10, row1['Staff_id'])
        self.assertEqual(9, row1['Staff_assigned_hotel_id'])
        self.assertEqual(500, row1['Staff_assigned_room'])
        self.assertEqual(10, row1['Serves_staff_id'])
        self.assertEqual(14, row1['Serves_reservation_id'])
        self.assertEqual(9, row2['Staff_id'])
        self.assertEqual(9, row2['Staff_assigned_hotel_id'])
        self.assertEqual(500, row2['Staff_assigned_room'])
        self.assertEqual(9, row2['Serves_staff_id'])
        self.assertEqual(14, row2['Serves_reservation_id'])
        self.assertNotIn('Transaction_id', row2)
        self.assertNotIn('Transaction_amount', row2)
        self.assertNotIn('Transaction_type', row2)
        self.assertNotIn('Transaction_date', row2)
        apps.cursor.close()

    def test_add_reservation_presidential_check_in_check_out(self):
        # Create Presidential reservation with check-in and check-out time.
        # No Staff must be freed. But must add new transaction 'Room Charge'.
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-15',
             'end_date': '2018-04-20', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2,
             'check_in_time': '2018-04-15 15:15:15',
             'check_out_time': '2018-04-20 04:04:04'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(5, row['number_of_guests'])
        self.assertEqual('2018-04-15', str(row['start_date']))
        self.assertEqual('2018-04-20', str(row['end_date']))
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(500, row['room_number'])
        self.assertEqual('2018-04-15 15:15:15', str(row['check_in_time']))
        self.assertEqual('2018-04-20 04:04:04', str(row['check_out_time']))
        self.assertEqual(10, row['Transaction_id'])
        self.assertEqual('50000.00', row['Transaction_amount'])
        self.assertEqual('5-night(s) Room Reservation Charge',
                         row['Transaction_type'])
        self.assertEqual('2018-04-20 04:04:04', str(row['Transaction_date']))
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        apps.cursor.close()

    def test_update_reservation(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        # Update Non-Presidential with check-in time and 2 more attributes.
        # No Staff must be assigned
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-04-11',
             'end_date': '2018-04-18', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual('2018-04-11', row['start_date'])
        self.assertEqual('2018-04-17', row['end_date'])
        df = apps.update_reservation(
            {'number_of_guests': 1, 'start_date': '2018-04-15',
             'end_date': '2018-04-17', 'check_in_time': '2018-04-15 15:15:15'},
            {'id': 10})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual(1, row['number_of_guests'])
        self.assertEqual('2018-04-15', row['start_date'])
        self.assertEqual('2018-04-17', row['end_date'])
        self.assertEqual('2018-04-15 15:15:15', row['check_in_time'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Update Non-Presidential with check-out time.
        # No Staff must be freed. But must add new transaction 'Room Charge'.
        df = apps.update_reservation(
            {'check_out_time': '2018-04-17 05:05:05'},
            {'id': 10})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual('2018-04-17 05:05:05', row['check_out_time'])
        self.assertEqual(10, row['Transaction_id'])
        self.assertEqual('200.00', row['Transaction_amount'])
        self.assertEqual('2-night(s) Room Reservation Charge',
                         row['Transaction_type'])
        self.assertEqual('2018-04-17 05:05:05', row['Transaction_date'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Update Non-Presidential with Presidential reservation setting
        # check-in and check-out times to NULL.
        df = apps.update_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-20',
             'end_date': '2018-04-23', 'room_number': 500, 'customer_id': 2,
                'check_in_time': None, 'check_out_time': None},
            {'id': 10})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(10, row['id'])
        self.assertEqual(5, row['number_of_guests'])
        self.assertEqual('2018-04-20', row['start_date'])
        self.assertEqual('2018-04-23', row['end_date'])
        self.assertEqual(500, row['room_number'])
        self.assertEqual(2, row['customer_id'])
        self.assertEqual('NULL', row['check_in_time'])
        self.assertEqual('NULL', row['check_out_time'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Update Presidential reservation with check-in time. Must assign 1
        # Catering Staff and 1 Service Room Staff to this reservation.
        df = apps.update_reservation(
            {'check_in_time': '2018-04-20 20:20:20'},
            {'id': 10})
        self.assertEqual(2, len(df.index))
        row1 = df.ix[0]
        row2 = df.ix[1]
        self.assertEqual(10, row1['id'])
        self.assertEqual('2018-04-20 20:20:20', row1['check_in_time'])
        self.assertEqual(10, row1['Staff_id'])
        self.assertEqual(9, row1['Staff_assigned_hotel_id'])
        self.assertEqual(500, row1['Staff_assigned_room'])
        self.assertEqual(10, row1['Serves_staff_id'])
        self.assertEqual(10, row1['Serves_reservation_id'])
        self.assertEqual(9, row2['Staff_id'])
        self.assertEqual(9, row2['Staff_assigned_hotel_id'])
        self.assertEqual(500, row2['Staff_assigned_room'])
        self.assertEqual(9, row2['Serves_staff_id'])
        self.assertEqual(10, row2['Serves_reservation_id'])
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        # Update Presidential reservation with check-out time. Must free 1
        # Catering Staff and 1 Service Room Staff. Must add add new transaction
        # 'Room Charge'.
        df = apps.update_reservation(
            {'check_out_time': '2018-04-23 11:11:11'},
            {'id': 10})
        self.assertEqual(3, len(df.index))
        row1 = df.ix[0]
        row2 = df.ix[1]
        self.assertEqual(10, row1['id'])
        self.assertEqual('2018-04-23 11:11:11', row1['check_out_time'])
        self.assertEqual(10, row1['Staff_id'])
        self.assertEqual('NULL', row1['Staff_assigned_hotel_id'])
        self.assertEqual('NULL', row1['Staff_assigned_room'])
        self.assertEqual(9, row2['Staff_id'])
        self.assertEqual('NULL', row2['Staff_assigned_hotel_id'])
        self.assertEqual('NULL', row2['Staff_assigned_room'])
        self.assertEqual(11, row1['Transaction_id'])
        self.assertEqual('30000.00', row1['Transaction_amount'])
        self.assertEqual('3-night(s) Room Reservation Charge',
                         row1['Transaction_type'])
        self.assertEqual('2018-04-23 11:11:11', row1['Transaction_date'])
        apps.cursor.close()

    def test_delete_reservation(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.delete_reservation({'id': 9})
        self.assertEqual(0, len(df.index))
        df = apps.get_data_frame('*', 'Reservations')
        self.assertEqual(8, len(df.index))
        apps.cursor.close()

    def test_availability_conflict_inside(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-1-1',
            'end_date': '2018-1-1',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual('Hotel A', row['Hotel Name'])
        self.assertEqual('21 ABC St', row['Street'])
        self.assertEqual('Raleigh', row['City'])
        self.assertEqual('NC', row['State'])
        self.assertEqual(5, row['Room Number'])
        self.assertEqual('27', row['ZIP'])
        self.assertEqual('919', row['Phone Number'])
        self.assertEqual(5, row['Room Number'])
        self.assertEqual(2, row['Occupancy'])
        self.assertEqual(200.0, row['Rate per Night'])
        apps.cursor.close()

    def test_availability_conflict_inside_no_hotel_id(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-1-1',
            'end_date': '2018-1-1',
        })
        self.assertEqual(4, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        row = df.ix[1]
        self.assertEqual(2, row['Hotel ID'])
        self.assertEqual(3, row['Room Number'])
        row = df.ix[2]
        self.assertEqual(3, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        apps.cursor.close()
        row = df.ix[3]
        self.assertEqual(4, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()

    def test_availability_conflict_outside(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-11',
            'end_date': '2017-5-12',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])

    def test_availability_conflict_outside_no_hotel_id(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-11',
            'end_date': '2017-5-12',
        })
        self.assertEqual(4, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        row = df.ix[1]
        self.assertEqual(2, row['Hotel ID'])
        self.assertEqual(3, row['Room Number'])
        row = df.ix[2]
        self.assertEqual(3, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        apps.cursor.close()
        row = df.ix[3]
        self.assertEqual(4, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()

    def test_availability_conflict_left(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-9',
            'end_date': '2017-5-12',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])

    def test_availability_conflict_left_no_hotel_id(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-9',
            'end_date': '2017-5-12',
        })
        self.assertEqual(4, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        row = df.ix[1]
        self.assertEqual(2, row['Hotel ID'])
        self.assertEqual(3, row['Room Number'])
        row = df.ix[2]
        self.assertEqual(3, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        apps.cursor.close()
        row = df.ix[3]
        self.assertEqual(4, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()

    def test_availability_conflict_right(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-12',
            'end_date': '2017-5-15',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        apps.cursor.close()

    def test_availability_conflict_right_no_hotel_id(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-12',
            'end_date': '2017-5-15',
        })
        self.assertEqual(4, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        row = df.ix[1]
        self.assertEqual(2, row['Hotel ID'])
        self.assertEqual(3, row['Room Number'])
        row = df.ix[2]
        self.assertEqual(3, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        apps.cursor.close()
        row = df.ix[3]
        self.assertEqual(4, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()

    def test_availability_all_available(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2012-1-12',
            'end_date': '2012-1-15',
        })
        self.assertEqual(6, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()
        row = df.ix[1]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        row = df.ix[2]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        row = df.ix[3]
        self.assertEqual(2, row['Hotel ID'])
        self.assertEqual(3, row['Room Number'])
        row = df.ix[4]
        self.assertEqual(3, row['Hotel ID'])
        self.assertEqual(2, row['Room Number'])
        row = df.ix[5]
        self.assertEqual(4, row['Hotel ID'])
        self.assertEqual(1, row['Room Number'])
        apps.cursor.close()

    def test_availability_left_boundary(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-9',
            'end_date': '2017-5-10',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        apps.cursor.close()

    def test_availability_right_boundary(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.room_availability({
            'start_date': '2017-5-13',
            'end_date': '2017-5-15',
            'hotel_id': 1
        })
        self.assertEqual(1, len(df.index))
        print df
        row = df.ix[0]
        self.assertEqual(1, row['Hotel ID'])
        self.assertEqual(5, row['Room Number'])
        apps.cursor.close()

    def test_check_out(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        apps.cursor.execute('UPDATE Reservations SET '
                            'check_out_time=NULL '
                            'WHERE id=4')
        self._con.commit()
        apps._check_out(4, '2018-05-12 10:02:00')
        df = apps.get_data_frame('*', 'Transactions', {
            'date': '2018-05-12 10:02:00'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2000.0, row['amount'])
        self.assertEqual('2-night(s) Room Reservation Charge', row['type'])
        self.assertEqual(4, row['reservation_id'])
        apps.cursor.close()

    def test_check_out_have_check_out_time(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        apps._check_out(4, '2018-05-12 10:02:00')
        df = apps.get_data_frame('*', 'Transactions', {
            'date': '2018-05-12 10:02:00'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2000.0, row['amount'])
        self.assertEqual('2-night(s) Room Reservation Charge', row['type'])
        self.assertEqual(4, row['reservation_id'])
        apps.cursor.close()

    def test_check_out_twice(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        apps._check_out(4, '2018-05-12 10:01:00')
        apps._check_out(4, '2018-05-12 10:02:00')
        df = apps.get_data_frame('*', 'Transactions', {
            'date': '2018-05-12 10:01:00'
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2000.0, row['amount'])
        self.assertEqual('2-night(s) Room Reservation Charge', row['type'])
        self.assertEqual(4, row['reservation_id'])
        df = apps.get_data_frame('*', 'Transactions', {
            'date': '2018-05-12 10:00:00'
        })
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_check_out_free_staff(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        # Assign Staff
        apps.cursor.execute('UPDATE Staff SET '
                            'assigned_hotel_id=1, '
                            'assigned_room_number=1 '
                            'WHERE id=103')
        apps.cursor.execute('UPDATE Staff SET '
                            'assigned_hotel_id=1, '
                            'assigned_room_number=1 '
                            'WHERE id=104')
        self._con.commit()
        # Check out
        apps._check_out(1, '2017-05-13 10:22:01')
        df = apps.get_data_frame('*', 'Staff', {
            'assigned_hotel_id': 1,
            'assigned_room_number': 1
        })
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_add_room(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.add_room({
            'hotel_id': 2,
            'room_number': 4,
            'category': 'Deluxe',
            'occupancy': 3,
            'rate': 250
        })
        row = df.ix[0]
        self.assertEqual('Deluxe', row['category'])
        self.assertEqual(3, row['occupancy'])
        self.assertEqual(250, row['rate'])
        df = apps.get_data_frame('*', 'Rooms', {
            'hotel_id': 2,
            'room_number': 4
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Deluxe', row['category'])
        self.assertEqual(3, row['occupancy'])
        self.assertEqual(250, row['rate'])
        apps.cursor.close()

    def test_add_room_conflict(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        try:
            df = apps.add_room({
                'hotel_id': 1,
                'room_number': 1,
                'category': 'Deluxe',
                'occupancy': 3,
                'rate': 250
            })
            self.assertTrue(False)
        except mariadb.Error:
            pass
        apps.cursor.close()

    def test_update_room_id(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.update_room({
            'category': 'Deluxe',
            'occupancy': 3,
            'rate': 250
        }, {
            'hotel_id': 1,
            'room_number': 1
        })
        row = df.ix[0]
        self.assertEqual('Deluxe', row['category'])
        self.assertEqual(3, row['occupancy'])
        self.assertEqual(250, row['rate'])
        df = apps.get_data_frame('*', 'Rooms', {
            'hotel_id': 1,
            'room_number': 1
        })
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('Deluxe', row['category'])
        self.assertEqual(3, row['occupancy'])
        self.assertEqual(250, row['rate'])
        apps.cursor.close()

    def test_delete_room(self):
        apps = Apps(self._con, False)
        load_demo_data(self._con)
        df = apps.add_room({
            'hotel_id': 2,
            'room_number': 4,
            'category': 'Deluxe',
            'occupancy': 3,
            'rate': 250
        })
        df = apps.get_data_frame('*', 'Rooms', {
            'hotel_id': 2,
            'room_number': 4
        })
        self.assertEqual(1, len(df.index))
        df = apps.delete_room({
            'hotel_id': 2,
            'room_number': 4
        })
        self.assertEqual(0, len(df.index))
        df = apps.get_data_frame('*', 'Rooms', {
            'hotel_id': 2,
            'room_number': 4
        })
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

    def test_report_occupancy_by_hotel(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_hotel('2017-01-16')
        self.assertEqual(9, len(df.index))
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
        self.assertEqual(10950, df['Total Possible Bookings'].ix[0])
        self.assertEqual(0.2283, df['% Occupancy'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_date_range_left_overlap(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_date_range('2017-01-13', '2017-01-17')
        print df
        self.assertEqual(1, len(df.index))
        self.assertEqual(2.0, df['Actual Bookings'].ix[0])
        self.assertEqual(40, df['Total Possible Bookings'].ix[0])
        self.assertEqual(5.0, df['% Occupancy'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_date_range_right_overlap(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_date_range('2017-01-17', '2017-01-27')
        print df
        self.assertEqual(1, len(df.index))
        self.assertEqual(5.0, df['Actual Bookings'].ix[0])
        self.assertEqual(100, df['Total Possible Bookings'].ix[0])
        self.assertEqual(5.0, df['% Occupancy'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_date_range_left_boundary(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_date_range('2017-01-13', '2017-01-15')
        print df
        self.assertEqual(1, len(df.index))
        self.assertEqual(0, df['Actual Bookings'].ix[0])
        self.assertEqual(20, df['Total Possible Bookings'].ix[0])
        self.assertEqual(0, df['% Occupancy'].ix[0])
        self._con.commit()
        apps.cursor.close()

    def test_report_occupancy_by_date_range_right_boundary(self):
        apps = Apps(self._con, True)
        self._insert_test_data()
        df = apps.report_occupancy_by_date_range('2017-01-22', '2017-01-24')
        print df
        self.assertEqual(1, len(df.index))
        self.assertEqual(0, df['Actual Bookings'].ix[0])
        self.assertEqual(20, df['Total Possible Bookings'].ix[0])
        self.assertEqual(0, df['% Occupancy'].ix[0])
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
