from apps import Apps
import pandas as pd
from util import sql_transaction

class Attributes(object):
    def __init__(self, attr_names, examples):
        self.attr_names = attr_names
        self.examples = examples

class CrudAttributes(Attributes):
    def __init__(self, table_name, attr_names, examples, secondary_args=None):
        super(CrudAttributes, self).__init__(attr_names, examples)
        self.table_name = table_name
        self.secondary_args = secondary_args

class ReportAttributes(Attributes):
    def __init__(self, report_name, attr_names, examples):
        super(ReportAttributes, self).__init__(attr_names, examples)
        self.report_name = report_name

class AppsParams(object):
    zip = CrudAttributes(
        'ZipToCityState',
        ['zip', 'city', 'state'],
        ['24354', 'Marion', 'VA'])
    hotels = CrudAttributes(
        'Hotels',
        ['id', 'name', 'street', 'zip', 'phone_number'],
        ['1', 'Wolf Inn Raleigh', '100 Main Street', '24354', '919-555-1212'],
        ['city', 'state'])
    rooms = CrudAttributes(
        'Rooms',
        ['hotel_id', 'room_number', 'category', 'occupancy', 'rate'],
        ['1', '100', 'Economy', '2', '85.00'])
    staff = CrudAttributes(
        'Staff',
        ['id', 'name', 'title', 'date_of_birth', 'department', 'phone_number', 'street', 'zip',
        'works_for_hotel_id', 'assigned_hotel_id', 'assigned_room_number'],
        ['1', 'John Doe', 'Manager', '1992-04-04', 'Maintenance', '919-555-1212', '100 Main Street', '25354',
        '1','1','100'],
        ['city', 'state'])
    customers = CrudAttributes(
        'Customers',
        ['id', 'name', 'date_of_birth', 'phone_number', 'email', 'street', 'zip', 'ssn', 'account_number',
        'is_hotel_card'],
        ['1', 'John Doe', '1992-04-04', '919-555-1212', 'john@email.com', '24354', '7145243' '0'],
        ['city', 'state'])
    reservations = CrudAttributes(
        'Reservations',
        ['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 'customer_id',
        'check_in_time', 'check_out_time'],
        ['1', '2', '2018-5-1', '2018-5-5', '1', '100', '1', '2018-5-1 2:00:00', '2018-5-5 10:00:00'])
    transactions = CrudAttributes(
        'Transactions',
        ['id', 'amount', 'type', 'date', 'reservation_id'],
        ['1', '25.00', 'Room service', '2018-5-3', '1'])
    serves = CrudAttributes(
        'Serves',
        ['staff_id', 'reservation_id'],
        ['1', '1'])
    gen_bill = ReportAttributes('Generate_bill', ['reservation_id'], ['1'])
    occ_hotel = ReportAttributes('Occupancy_hotel', ['query_date'], ['2018-4-4'])
    occ_room = ReportAttributes('Occupancy_room', ['query_date'], ['2018-4-4'])
    occ_city = ReportAttributes('Occupancy_city', ['query_date'], ['2018-4-4'])
    occ_date = ReportAttributes('Occupancy_date', ['start_date', 'end_date'], ['2018-4-4', '2018-4-8'])
    list_staff = ReportAttributes('List_staff', ['hotel_id'], ['1'])
    cust_inter = ReportAttributes('Customer_inter', ['reservation_id'], ['1'])
    rev_hotel = ReportAttributes('Revenue_hotel',
                                 ['start_date', 'end_date', 'hotel_id'],
                                 ['2018-4-4', '2018-4-8', '1'])
    rev_all = ReportAttributes('Revenue_all',
                                 ['start_date', 'end_date'],
                                 ['2018-4-4', '2018-4-8'])
    cust_no_card = ReportAttributes('Customer_nocard',
                                 ['start_date', 'end_date'],
                                 ['2018-4-4', '2018-4-8'])
    room_avail = ReportAttributes('Room_avail',
                                 ['start_date', 'end_date', 'hotel_id', 'name', 'zip'],
                                 ['2018-4-4', '2018-4-8', '1', 'Wolf Inn Raleigh', '24354'])





################################################################################
# Interface from UI to API
# - Edit this file to control interactions between UI and Apps
################################################################################
class AppsClient(object):
    def __init__(self, db, check=False):
        self.apps = Apps(db, check)
        self.db = db

    # Helper interfaces
    def select(self, where_dict, table_name):
        where_string = ' AND '.join([key + ('="%s"' % value) for key,value in where_dict.items()])
        return self.apps.get_data_frame('*', table_name, where_string)

    def zip_is_present(self, zip):
        result = self.apps.get_data_frame('*', 'ZipToCityState', ('zip=%s' % zip))
        if len(result) == 0:
            return False
        else:
            return True

    def insert(self, param_dict, api_info):
        set_dict = param_dict['set']

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
                result = self.apps.add_zip(zip_dict)
                if not isinstance(result, pd.DataFrame):
                    return result

            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names if k in set_dict}

            # select the correct API and submit
            result = {
                'Hotels': lambda x: self.apps.add_hotel(x),
                'Rooms': lambda x: self.apps.add_room(x),
                'Staff': lambda x: self.apps.add_staff(x),
                'Customers': lambda x: self.apps.add_customer(x),
                'Reservations': lambda x: self.apps.add_reservation(x),
                'Transactions': lambda x: self.apps.add_transaction(x)
            }[api_info.table_name](item_dict)

            return result

    def update(self, param_dict, api_info):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
                result = self.apps.add_zip(zip_dict)
                if not isinstance(result, pd.DataFrame):
                    return result

            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names if k in set_dict}
            where_clause_dict = {k: where_dict[k] for k in api_info.attr_names if k in where_dict}

            # select the correct API and submit
            result = {
                'Hotels': lambda x,y: self.apps.update_hotel(x,y),
                'Rooms': lambda x,y: self.apps.update_room(x,y),
                'Staff': lambda x,y: self.apps.update_staff(x,y),
                'Customers': lambda x,y: self.apps.update_customer(x,y),
                'Reservations': lambda x,y: self.apps.update_reservation(x,y),
                'Transactions': lambda x,y: self.apps.update_transaction(x,y)
            }[api_info.table_name](item_dict, where_clause_dict)

            return result

    def delete(self, param_dict, arg_list, api_info):
        where_dict = param_dict['where']

        with sql_transaction(self.db):
            # select the correct API and submit
            result = {
                'Hotels': lambda x: self.apps.delete_hotel(x),
                'Rooms': lambda x: self.apps.delete_room(x),
                'Staff': lambda x: self.apps.delete_staff(x),
                'Customers': lambda x: self.apps.delete_customer(x),
                'Reservations': lambda x: self.apps.delete_reservation(x),
                'Transactions': lambda x: self.apps.delete_transaction(x)
            }[api_info.table_name](where_dict)

            return result

    def get_report(self, param_dict, api_info):
        set_dict = param_dict['set']
        arg_list = [set_dict[key] for key in api_info.attr_names]

        result = {
            'Generate_bill' : lambda x: self.apps.generate_bill(x[0]),
            'Occupancy_hotel': lambda x: self.apps.report_occupancy_by_hotel(x[0]),
            'Occupancy_room': lambda x: self.apps.report_occupancy_by_room(x[0]),
            'Occupancy_city': lambda x: self.apps.report_occupancy_by_city(x[0]),
            'Occupancy_date': lambda x: self.apps.report_occupancy_by_date_range(x[0], x[1]),
            'List_staff': lambda x: self.apps.report_staff_by_role(x[0]),
            'Customer_inter': lambda x: self.apps.report_customer_interactions(x[0]),
            'Revenue_hotel': lambda x: self.apps.report_revenue_single_hotel(x[0], x[1], x[2]),
            'Revenue_all': lambda x: self.apps.report_revenue_all_hotels(x[0], x[1])
        }[api_info.report_name](arg_list)

        return result


    def get_report_with_dict(self, param_dict, api_info):
        set_dict = param_dict['set']
        print set_dict
        result = {
            'Room_avail': lambda x: self.apps.room_availability(x)
        }[api_info.report_name](set_dict)

        return result