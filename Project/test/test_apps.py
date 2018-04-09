
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
        df = apps.get_data_frame('*', 'ZipToCityState')
        self.assertEqual(0, len(df.index))
        apps.cursor.close()

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
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
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
        self.assertEqual('2018-04-11', row['start_date'])
        self.assertEqual('2018-04-18', row['end_date'])
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
        # Create Non-Presidential reservation with check-in time, but no
        # check-out time
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-04-19',
             'end_date': '2018-04-26', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1,
             'check_in_time': '2018-04-11 12:12:12'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(2, row['number_of_guests'])
        self.assertEqual('2018-04-11', row['start_date'])
        self.assertEqual('2018-04-18', row['end_date'])
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(100, row['room_number'])
        self.assertEqual(1, row['customer_id'])
        self.assertEqual('2018-04-11 12:12:12', row['check_in_time'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Create Non-Presidential reservation with check-in and check-out time.
        # Should not free any staff. But add new transaction 'Room Charge'
        df = apps.add_reservation(
            {'number_of_guests': 2, 'start_date': '2018-05-01',
             'end_date': '2018-05-05', 'hotel_id': 9,
             'room_number': 100, 'customer_id': 1,
             'check_in_time': '2018-05-01 12:12:12',
             'check_out_time': '2018-05-05 09:09:09'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual('2018-05-05 09:09:09', row['check_out_time'])
        self.assertEqual(9, row['Transaction_id'])
        self.assertEqual('500.00', row['Transaction_amount'])
        self.assertEqual('5-night(s) Room Reservation Charge',
                         row['Transaction_type'])
        self.assertEqual('2018-05-05 09:09:09', row['Transaction_date'])
        self.assertNotIn('Staff_id', row)
        self.assertNotIn('Staff_assigned_hotel_id', row)
        self.assertNotIn('Staff_assigned_room', row)
        self.assertNotIn('Serves_staff_id', row)
        self.assertNotIn('Serves_reservation_id', row)
        # Create Presidential reservation w/out check-in and check-out time
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-01',
             'end_date': '2018-04-07', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(5, row['number_of_guests'])
        self.assertEqual('2018-04-01', row['start_date'])
        self.assertEqual('2018-04-07', row['end_date'])
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
        # Create Presidential reservation with check-in, but not check-out time.
        # Must assign Room Service and Catering Staff.
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-08',
             'end_date': '2018-04-12', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2,
             'check_in_time': '2018-04-08 15:15:15'})
        self.assertEqual(2, len(df.index))
        row1 = df.ix[0]
        row2 = df.ix[1]
        self.assertEqual(5, row1['number_of_guests'])
        self.assertEqual('2018-04-08', row1['start_date'])
        self.assertEqual('2018-04-12', row1['end_date'])
        self.assertEqual(9, row1['hotel_id'])
        self.assertEqual(500, row1['room_number'])
        self.assertEqual(2, row1['customer_id'])
        self.assertEqual('2018-04-08 15:15:15', row1['check_in_time'])
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
        self.assertNotIn('Transaction_id', row)
        self.assertNotIn('Transaction_amount', row)
        self.assertNotIn('Transaction_type', row)
        self.assertNotIn('Transaction_date', row)
        # Create Presidential reservation with check-in and check-out time.
        # No Staff must be freed. But must add new transaction 'Room Charge'.
        df = apps.add_reservation(
            {'number_of_guests': 5, 'start_date': '2018-04-15',
             'end_date': '2018-04-20', 'hotel_id': 9,
             'room_number': 500, 'customer_id': 2,
             'check_in_time': '2018-04-15 15:15:15',
             'check_out_time': '2018-04-20 04:04:04'})
        self.assertEqual(1, len(df.index))
        row = df.ix[0]
        self.assertEqual(5, row['number_of_guests'])
        self.assertEqual('2018-04-15', row['start_date'])
        self.assertEqual('2018-04-20', row['end_date'])
        self.assertEqual(9, row['hotel_id'])
        self.assertEqual(500, row['room_number'])
        self.assertEqual('2018-04-15 15:15:15', row['check_in_time'])
        self.assertEqual('2018-04-20 04:04:04', row['check_out_time'])
        self.assertEqual(10, row['Transaction_id'])
        self.assertEqual('50000.00', row['Transaction_amount'])
        self.assertEqual('5-night(s) Room Reservation Charge',
                         row['Transaction_type'])
        self.assertEqual('2018-04-20 04:04:04', row['Transaction_date'])
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
