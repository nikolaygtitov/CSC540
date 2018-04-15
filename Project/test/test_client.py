import unittest
import mysql.connector as mariadb
import math

from unittest_base import SQLUnitTestBase
from Project.apps import Apps
from Project.appsclient import *
from Project.demo_data import load_demo_data

class TestApps(SQLUnitTestBase):

    @staticmethod
    def _connect_to_test_db():
        con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='pdscott2',
                              password='2CGxZg27R3utum',
                              database='pdscott2')
        return con

    def test_insert_hotel(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'name':'WolfInn Test', 'street':'104 Main', 'zip':'27965', 'phone_number':'919-555-1212'}}
        api_info = AppsParams.hotels
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual('WolfInn Test', row['name'])
        self.assertEqual('104 Main', row['street'])
        self.assertEqual('27965', row['zip'])
        self.assertEqual('919-555-1212', row['phone_number'])

    def test_insert_hotel_with_new_zip(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'name':'WolfInn Test', 'street':'104 Main', 'zip':'00000', 'city': 'Nowhere', 'state': 'PA','phone_number':'919-555-1212'}}
        api_info = AppsParams.hotels
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual('WolfInn Test', row['name'])
        self.assertEqual('104 Main', row['street'])
        self.assertEqual('00000', row['zip'])
        self.assertEqual('919-555-1212', row['phone_number'])
        self.assertEqual('Nowhere', row['city'])
        self.assertEqual('PA', row['state'])

    def test_update_hotel(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'name':'WolfInn Newtest'}, 'where':{'id':1}}
        api_info = AppsParams.hotels
        result = client.update(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['id'])
        self.assertEqual('WolfInn Newtest', row['name'])

    def test_update_hotel_zip(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'zip':'00000','city': 'Nowhere', 'state': 'PA'}, 'where':{'id':1}}
        api_info = AppsParams.hotels
        result = client.update(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['id'])
        self.assertEqual('00000', row['zip']) 
        self.assertEqual('Nowhere', row['city']) 
        self.assertEqual('PA', row['state']) 

    def test_delete_hotel(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'id':100, 'name':'WolfInn Test', 'street':'104 Main', 
            'zip':'00000', 'city': 'Nowhere', 'state': 'PA','phone_number':'919-555-1212'}}
        api_info = AppsParams.hotels
        client.insert(param_dict, api_info)
        param_dict = {'where':{'id':100}}
        result = client.delete(param_dict, api_info)
        self.assertEqual(0, len(result.index))

    def test_insert_room(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'hotel_id':1,'room_number':101, 'category':'Economy', 'occupancy':2, 'rate':85.00}}
        api_info = AppsParams.rooms
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['hotel_id'])
        self.assertEqual(101, row['room_number'])
        self.assertEqual('Economy', row['category'])
        self.assertEqual(2, row['occupancy'])
        self.assertEqual(85.0, row['rate'])

    def test_update_room(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'category':'Deluxe'}, 'where':{'hotel_id':1, 'room_number':100}}
        api_info = AppsParams.rooms
        result = client.update(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['hotel_id'])
        self.assertEqual(100, row['room_number'])
        self.assertEqual('Deluxe', row['category'])

    def test_delete_room(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'where':{'hotel_id':9, 'room_number':500}}
        api_info = AppsParams.rooms
        result = client.delete(param_dict, api_info)
        self.assertEqual(0, len(result.index))

    def test_insert_staff(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'name': 'Charlie', 'title': 'Manager', 'date_of_birth':'1980-4-4', 'department':'Sales',
                   'phone_number':'919-555-1212', 'street':'101 Main', 'zip':'27965', 'works_for_hotel_id':1}}
        api_info = AppsParams.staff
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual('Charlie', row['name'])
        self.assertEqual('Manager', row['title'])
        self.assertEqual('1980-04-04', str(row['date_of_birth']))
        self.assertEqual('Sales', row['department'])
        self.assertEqual('919-555-1212', row['phone_number'])
        self.assertEqual('101 Main', row['street'])
        self.assertEqual('27965', row['zip'])
        self.assertEqual(1, row['works_for_hotel_id'])

    def test_update_staff(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'assigned_hotel_id':9, 'assigned_room_number':100}, 'where':{'id':1}}
        api_info = AppsParams.staff
        result = client.update(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['id'])
        self.assertEqual(9, row['assigned_hotel_id'])
        self.assertEqual('100', str(row['assigned_room_number']))

    def test_delete_staff(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'where':{'id':1}}
        api_info = AppsParams.staff
        result = client.delete(param_dict, api_info)
        self.assertEqual(0, len(result.index))


    def test_insert_customer(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'name':'Charlie', 'date_of_birth':'1980-4-4', 'phone_number':'919-555-1212', 
            'email':'anon@anon.com', 'street':'100 Main', 'zip': '27965', 'ssn':'111-22-3333', 
            'account_number':'10000009', 'is_hotel_card':0}}
        api_info = AppsParams.customers
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual('Charlie', row['name'])
        self.assertEqual('1980-04-04', str(row['date_of_birth']))
        self.assertEqual('919-555-1212', row['phone_number'])
        self.assertEqual('anon@anon.com', row['email'])
        self.assertEqual('100 Main', row['street'])
        self.assertEqual('27965', row['zip'])
        self.assertEqual('111-22-3333', row['ssn'])
        self.assertEqual('10000009', row['account_number'])
        self.assertEqual(0, row['is_hotel_card'])

    def test_update_customer(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'ssn':'333-22-1111'}, 'where':{'id':1}}
        api_info = AppsParams.customers
        result = client.update(param_dict, api_info)
        print result
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['id'])
        self.assertEqual('333-22-1111', row['ssn'])

    def test_delete_customer(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'id':1000,'name':'Charlie', 'date_of_birth':'1980-4-4', 'phone_number':'919-555-1212', 
            'email':'anon@anon.com', 'street':'100 Main', 'zip': '27965', 'ssn':'111-22-3333', 
            'account_number':'10000009', 'is_hotel_card':0}}
        api_info = AppsParams.customers
        result = client.insert(param_dict, api_info)
        param_dict = {'where':{'id':1000}}
        result = client.delete(param_dict, api_info)
        self.assertEqual(0, len(result.index))


    def test_insert_reservation(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'number_of_guests':2, 'start_date':'2018-4-4', 'end_date':'2018-4-10',
                   'hotel_id':1, 'room_number':100, 'customer_id':1}}
        api_info = AppsParams.reservations
        result = client.insert(param_dict, api_info)
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(2, row['number_of_guests'])
        self.assertEqual('2018-04-04', str(row['start_date']))
        self.assertEqual('2018-04-10', str(row['end_date']))
        self.assertEqual(1, row['hotel_id'])
        self.assertEqual(100, row['room_number'])
        self.assertEqual(1, row['customer_id'])

    def test_update_reservation(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'set':{'check_in_time':'2018-4-4 2:00:00'}, 'where':{'id':1}}
        api_info = AppsParams.reservations
        result = client.update(param_dict, api_info)
        print result
        self.assertEqual(1, len(result.index))
        row = result.ix[0]
        self.assertEqual(1, row['id'])
        self.assertEqual('2018-04-04 02:00:00', str(row['check_in_time']))

    def test_delete_reservation(self):
        client = AppsClient(self._con, True)
        self._insert_test_data()
        param_dict = {'where':{'id':1}}
        api_info = AppsParams.reservations
        result = client.delete(param_dict, api_info)
        self.assertEqual(0, len(result.index))

if __name__ == '__main__':
    unittest.main()