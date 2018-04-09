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
        {'where':['zip', 'city', 'state'],'set':['zip', 'city', 'state']},
        {'where':['24354', 'Marion', 'VA'], 'set':['24354', 'Marion', 'VA']})
    hotels = CrudAttributes(
        'Hotels',
        {'where':['id', 'name', 'street', 'zip', 'phone_number'],'set':['id', 'name', 'street', 'zip', 'phone_number']},
        {'where':['1', 'Wolf Inn Raleigh', '100 Main Street', '24354', '919-555-1212'],
        'set':['1', 'Wolf Inn Raleigh', '100 Main Street', '24354', '919-555-1212']},
        ['city', 'state'])
    rooms = CrudAttributes(
        'Rooms',
        {'where':['hotel_id', 'room_number', 'category', 'occupancy', 'rate'],'set':['hotel_id', 'room_number', 'category', 'occupancy', 'rate']},
        {'where':['1', '100', 'Economy', '2', '85.00'],'set':['1', '100', 'Economy', '2', '85.00']})
    staff = CrudAttributes(
        'Staff',
        {'where':['id', 'name', 'title', 'date_of_birth', 'department', 'phone_number', 'street', 'zip',
        'works_for_hotel_id', 'assigned_hotel_id', 'assigned_room_number'],
        'set':['id', 'name', 'title', 'date_of_birth', 'department', 'phone_number', 'street', 'zip',
        'works_for_hotel_id', 'assigned_hotel_id', 'assigned_room_number']},
        {'where':['1', 'John Doe', 'Manager', '1992-04-04', 'Maintenance', '919-555-1212', '100 Main Street', '25354',
        '1','1','100'],
        'set':['1', 'John Doe', 'Manager', '1992-04-04', 'Maintenance', '919-555-1212', '100 Main Street', '25354',
        '1','1','100']},
        ['city', 'state'])
    customers = CrudAttributes(
        'Customers',
        {'where':['id', 'name', 'date_of_birth', 'phone_number', 'email', 'street', 'zip', 'ssn', 'account_number',
        'is_hotel_card'],
        'set':['id', 'name', 'date_of_birth', 'phone_number', 'email', 'street', 'zip', 'ssn', 'account_number',
        'is_hotel_card']},
        {'where':['1', 'John Doe', '1992-04-04', '919-555-1212', 'john@email.com', '100 Main Street', '24354',
         '111-22-3333', '7145243', '0'],
         'set':['1', 'John Doe', '1992-04-04', '919-555-1212', 'john@email.com', '100 Main Street', '24354',
         '111-22-3333', '7145243', '0']},
        ['city', 'state'])
    reservations = CrudAttributes(
        'Reservations',
        {'where':['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 'customer_id',
        'check_in_time', 'check_out_time'],
        'set':['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 'customer_id',
        'check_in_time', 'check_out_time']},
        {'where':['1', '2', '2018-5-1', '2018-5-5', '1', '100', '1', '2018-5-1 2:00:00', '2018-5-5 10:00:00'],
        'set':['1', '2', '2018-5-1', '2018-5-5', '1', '100', '1', '2018-5-1 2:00:00', '2018-5-5 10:00:00']})
    check_in = CrudAttributes(
        'Reservations',
        {'where':['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 'customer_id',
        'check_in_time', 'check_out_time'],
        'set':['id', 'check_in_time']},
        {'where':['1', '2', '2018-5-1', '2018-5-5', '1', '100', '1', '2018-5-1 2:00:00', '2018-5-5 10:00:00'],
        'set':['reservation id', 'YYYY-MM-DD HH:MM:SS']})
    check_out = CrudAttributes(
        'Reservations',
        {'where':['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 'customer_id',
        'check_in_time', 'check_out_time'],
        'set':['id', 'check_out_time']},
        {'where':['1', '2', '2018-5-1', '2018-5-5', '1', '100', '1', '2018-5-1 2:00:00', '2018-5-5 10:00:00'],
        'set':['reservation id', 'YYYY-MM-DD HH:MM:SS']})
    transactions = CrudAttributes(
        'Transactions',
        {'where':['id', 'amount', 'type', 'date', 'reservation_id'],
        'set':['id', 'amount', 'type', 'date', 'reservation_id']},
        {'where':['1', '25.00', 'Room service', '2018-5-3', '1'],
        'set':['1', '25.00', 'Room service', '2018-5-3', '1']})
    serves = CrudAttributes(
        'Serves',
        ['staff_id', 'reservation_id'],
        ['1', '1'])
    gen_bill = ReportAttributes('Generate_bill', {'set':['reservation_id']}, {'set':['1']})
    occ_hotel = ReportAttributes('Occupancy_hotel', {'set':['query_date']}, {'set':['2018-4-4']})
    occ_room = ReportAttributes('Occupancy_room', {'set':['query_date']}, {'set':['2018-4-4']})
    occ_city = ReportAttributes('Occupancy_city', {'set':['query_date']}, {'set':['2018-4-4']})
    occ_date = ReportAttributes('Occupancy_date', {'set':['start_date', 'end_date']}, {'set':['2018-4-4', '2018-4-8']})
    list_staff = ReportAttributes('List_staff', {'set':['hotel_id']}, {'set':['1']})
    cust_inter = ReportAttributes('Customer_inter', {'set':['reservation_id']}, {'set':['1']})
    rev_hotel = ReportAttributes('Revenue_hotel',
                                 {'set':['start_date', 'end_date', 'hotel_id']},
                                 {'set':['2018-4-4', '2018-4-8', '1']})
    rev_all = ReportAttributes('Revenue_all',
                                 {'set':['start_date', 'end_date']},
                                 {'set':['2018-4-4', '2018-4-8']})
    cust_no_card = ReportAttributes('Customer_nocard',
                                 {'set':['start_date', 'end_date']},
                                 {'where':['2018-4-4', '2018-4-8']})
    room_avail = ReportAttributes('Room_avail',
                                 {'set':['start_date', 'end_date', 'hotel_id', 'name', 'zip']},
                                 {'set':['2018-4-4', '2018-4-8', '1', 'Wolf Inn Raleigh', '24354']})

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
        zip_result = None

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
                zip_result = self.apps.add_zip(zip_dict)
                if not isinstance(zip_result, pd.DataFrame):
                    return zip_result

            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names['set'] if k in set_dict}

            # select the correct API and submit
            result = {
                'Hotels': lambda x: self.apps.add_hotel(x),
                'Rooms': lambda x: self.apps.add_room(x),
                'Staff': lambda x: self.apps.add_staff(x),
                'Customers': lambda x: self.apps.add_customer(x),
                'Reservations': lambda x: self.apps.add_reservation(x),
                'Transactions': lambda x: self.apps.add_transaction(x)
            }[api_info.table_name](item_dict)

            if zip_result is not None:
                result = result.merge(zip_result, left_on='zip', right_on='zip', how='outer')
            return result

    def update(self, param_dict, api_info):
        set_dict = param_dict['set']
        where_dict = param_dict['where']
        zip_result = None

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
                zip_result = self.apps.add_zip(zip_dict)
                if not isinstance(zip_result, pd.DataFrame):
                    return zip_result

            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names['set'] if k in set_dict}
            where_clause_dict = {k: where_dict[k] for k in api_info.attr_names['set'] if k in where_dict}

            # select the correct API and submit
            result = {
                'Hotels': lambda x,y: self.apps.update_hotel(x,y),
                'Rooms': lambda x,y: self.apps.update_room(x,y),
                'Staff': lambda x,y: self.apps.update_staff(x,y),
                'Customers': lambda x,y: self.apps.update_customer(x,y),
                'Reservations': lambda x,y: self.apps.update_reservation(x,y),
                'Transactions': lambda x,y: self.apps.update_transaction(x,y)
            }[api_info.table_name](item_dict, where_clause_dict)

            if zip_result is not None:
                result = result.merge(zip_result, left_on='zip', right_on='zip', how='outer')
            return result

    def delete(self, param_dict, api_info):
        where_dict = param_dict['where']
        print where_dict
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
        arg_list = [set_dict[key] for key in api_info.attr_names['set']]

        with sql_transaction(self.db):
            result = {
                'Generate_bill' : lambda x: self.apps.generate_bill(x[0]),
                'Occupancy_hotel': lambda x: self.apps.report_occupancy_by_hotel(x[0]),
                'Occupancy_room': lambda x: self.apps.report_occupancy_by_room_type(x[0]),
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
        with sql_transaction(self.db):
            result = {
                'Room_avail': lambda x: self.apps.room_availability(x)
            }[api_info.report_name](set_dict)

            return result