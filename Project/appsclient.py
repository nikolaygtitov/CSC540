"""
appsclient.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the appsclient.py file:
This file contains the client classes for communicating directly with the
Apps.py API.  These classes are intended to be instantiated by HotelSoft.py.
See hotelsoft.py for execution instructions.

@version: 1.0
@todo: Demo
@since: April 8, 2018
@status: Complete
@requires: To be instantiated
@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu
@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott
"""

from apps import Apps
import pandas as pd
from util import sql_transaction


################################################################################
# Supporting classes                                                           #
################################################################################
class Attributes(object):
    """
    Base class for attributes objects.
    """
    def __init__(self, attr_names, examples):
        """
        Instantiates attributes base class
        Parameters:
            :param attr_names: a list of attribute name strings
            :param examples: a list of attribute example strings
        """
        self.attr_names = attr_names
        self.examples = examples


class CrudAttributes(Attributes):
    """
    Subclass of Attributes for CRUD related database interactions
    """
    def __init__(self, table_name, attr_names, examples, secondary_args=None):
        """
        Instantiates CRUD attributes subclass
        Parameters:
            :param table_name: the name of the database table to CRUD
            :param attr_names: a list of attribute name strings
            :param examples: a list of attribute example strings
            :param secondary_args: a list of follow-up attributes (zip handling)
        """
        super(CrudAttributes, self).__init__(attr_names, examples)
        self.table_name = table_name
        self.secondary_args = secondary_args


class ReportAttributes(Attributes):
    """
    Subclass of Attributes for Report related database interactions
    """
    def __init__(self, report_name, attr_names, examples):
        """
        Instantiates Reports attributes subclass
        Parameters:
            :param report_name: string identifier for the related report
            :param attr_names: a list of attribute name strings
            :param examples: a list of attribute example strings
        """
        super(ReportAttributes, self).__init__(attr_names, examples)
        self.report_name = report_name


class AppsParams(object):
    """
    Static class containing attribute lists for all CRUD and Report interactions
    """
    zip_code = CrudAttributes(
        'ZipToCityState',
        {'where': ['zip', 'city', 'state'],
         'set': ['zip', 'city', 'state']},
        {'where': ['e.g. 24354', 'e.g. Raleigh', 'e.g. NC'],
         'set': ['e.g. 24354', 'e.g. Raleigh', 'e.g. NC']})
    hotels = CrudAttributes(
        'Hotels',
        {'where': ['id', 'name', 'street', 'zip', 'phone_number'],
         'set': ['id', 'name', 'street', 'zip', 'phone_number']},
        {'where': ['Hotel ID', 'e.g. Wolf Inn Raleigh', 'e.g. 100 Main Street',
                   'e.g. 24354', 'e.g. 919-555-1212'],
         'set': ['Hotel ID', 'e.g. Wolf Inn Raleigh', 'e.g. 100 Main Street',
                 'e.g. 24354', 'e.g. 919-555-1212']},
        ['city', 'state'])
    rooms = CrudAttributes(
        'Rooms',
        {'where': ['hotel_id', 'room_number', 'category', 'occupancy', 'rate'],
         'set': ['hotel_id', 'room_number', 'category', 'occupancy', 'rate']},
        {'where': ['Hotel ID', 'e.g. 100', 'e.g. Economy', 'e.g. 2',
                   'e.g. 85.00'],
         'set': ['Hotel ID', 'e.g. 100', 'e.g. Economy', 'e.g. 2',
                 'e.g. 85.00']})
    staff = CrudAttributes(
        'Staff',
        {'where': ['id', 'name', 'title', 'date_of_birth', 'department',
                   'phone_number', 'street', 'zip', 'works_for_hotel_id',
                   'assigned_hotel_id', 'assigned_room_number'],
         'set': ['id', 'name', 'title', 'date_of_birth', 'department',
                 'phone_number', 'street', 'zip', 'works_for_hotel_id',
                 'assigned_hotel_id', 'assigned_room_number']},
        {'where': ['Staff ID', 'e.g. John Doe', 'e.g. Manager', 'YYYY-MM-DD',
                   'e.g. Maintenance', '919-555-1212', 'e.g. 100 Main Street',
                   'e.g. 25354', 'e.g. 1', 'e.g. 1', 'e.g. 100'],
         'set': ['Staff ID', 'e.g. John Doe', 'e.g. Manager', 'YYYY-MM-DD',
                 'e.g. Maintenance', '919-555-1212', 'e.g. 100 Main Street',
                 'e.g. 25354', 'e.g. 1', 'e.g. 1', 'e.g. 100']},
        ['city', 'state'])
    customers = CrudAttributes(
        'Customers',
        {'where': ['id', 'name', 'date_of_birth', 'phone_number', 'email',
                   'street', 'zip', 'ssn', 'account_number', 'is_hotel_card'],
         'set': ['id', 'name', 'date_of_birth', 'phone_number', 'email',
                 'street', 'zip', 'ssn', 'account_number', 'is_hotel_card']},
        {'where': ['Customer ID', 'e.g. John Doe', 'YYYY-MM-DD',
                   'e.g. 919-555-1212', 'e.g. john@email.com',
                   'e.g. 100 Main Street', 'e.g. 24354', 'e.g. 111-22-3333',
                   'e.g. 7145243', '0 or 1'],
         'set': ['Customer ID', 'e.g. John Doe', 'YYYY-MM-DD',
                 'e.g. 919-555-1212', 'e.g. john@email.com',
                 'e.g. 100 Main Street', 'e.g. 24354', 'e.g. 111-22-3333',
                 'e.g. 7145243', '0 or 1']},
        ['city', 'state'])
    reservations = CrudAttributes(
        'Reservations',
        {'where': ['id', 'number_of_guests', 'start_date', 'end_date',
                   'hotel_id', 'room_number', 'customer_id', 'check_in_time',
                   'check_out_time'],
         'set': ['id', 'number_of_guests', 'start_date', 'end_date',
                 'hotel_id', 'room_number', 'customer_id', 'check_in_time',
                 'check_out_time']},
        {'where': ['Reservation ID', 'e.g. 2', 'YYYY-MM-DD', 'YYYY-MM-DD',
                   'e.g. 1', 'e.g. 100', 'e.g. 1', 'YYYY-MM-DD HH:MM:SS',
                   'YYYY-MM-DD HH:MM:SS'],
         'set': ['Reservation ID', 'e.g. 2', 'YYYY-MM-DD', 'YYYY-MM-DD',
                 'e.g. 1', 'e.g. 100', 'e.g. 1', 'YYYY-MM-DD HH:MM:SS',
                 'YYYY-MM-DD HH:MM:SS']})
    check_in = CrudAttributes(
        'Reservations',
        {'where': ['id', 'number_of_guests', 'start_date', 'end_date',
                   'hotel_id', 'room_number', 'customer_id', 'check_in_time',
                   'check_out_time'],
         'set': ['check_in_time']},
        {'where': ['Reservation ID', 'e.g. 2', 'YYYY-MM-DD', 'YYYY-MM-DD',
                   'e.g. 1', 'e.g. 100', 'e.g. 1', 'YYYY-MM-DD HH:MM:SS',
                   'YYYY-MM-DD HH:MM:SS'],
         'set': ['YYYY-MM-DD HH:MM:SS']})
    check_out = CrudAttributes(
        'Reservations',
        {'where': ['id', 'number_of_guests', 'start_date', 'end_date',
                   'hotel_id', 'room_number', 'customer_id', 'check_in_time',
                   'check_out_time'],
         'set': ['id', 'check_out_time']},
        {'where': ['Reservation ID', 'e.g. 2', 'YYYY-MM-DD', 'YYYY-MM-DD',
                   'e.g. 1', 'e.g. 100', 'e.g. 1', 'YYYY-MM-DD HH:MM:SS',
                   'YYYY-MM-DD HH:MM:SS'],
         'set': ['YYYY-MM-DD HH:MM:SS']})
    transactions = CrudAttributes(
        'Transactions',
        {'where': ['id', 'amount', 'type', 'date', 'reservation_id'],
         'set': ['id', 'amount', 'type', 'date', 'reservation_id']},
        {'where': ['Transaction ID', 'e.g. 25.00', 'e.g. Room service',
                   'YYYY-MM-DD', 'e.g. 1'],
         'set': ['Transaction ID', 'e.g. 25.00', 'e.g. Room service',
                 'YYYY-MM-DD', 'e.g. 1']})
    serves = CrudAttributes(
        'Serves', ['staff_id', 'reservation_id'], ['e.g. 1', 'e.g. 1'])
    gen_bill = ReportAttributes(
        'Generate_bill', {'set': ['reservation_id']}, {'set': ['e.g. 1']})
    occ_hotel = ReportAttributes(
        'Occupancy_hotel', {'set': ['query_date']}, {'set': ['YYYY-MM-DD']})
    occ_room = ReportAttributes(
        'Occupancy_room', {'set': ['query_date']}, {'set': ['YYYY-MM-DD']})
    occ_city = ReportAttributes(
        'Occupancy_city', {'set': ['query_date']}, {'set': ['YYYY-MM-DD']})
    occ_date = ReportAttributes(
        'Occupancy_date', {'set': ['start_date', 'end_date']},
        {'set': ['YYYY-MM-DD', 'YYYY-MM-DD']})
    list_staff = ReportAttributes(
        'List_staff', {'set': ['hotel_id']}, {'set': ['e.g. 1']})
    cust_inter = ReportAttributes(
        'Customer_inter', {'set': ['reservation_id']}, {'set': ['e.g. 1']})
    rev_hotel = ReportAttributes(
        'Revenue_hotel', {'set': ['start_date', 'end_date', 'hotel_id']},
        {'set': ['YYYY-MM-DD', 'YYYY-MM-DD', 'e.g. 1']})
    rev_all = ReportAttributes(
        'Revenue_all', {'set': ['start_date', 'end_date']},
        {'set': ['YYYY-MM-DD', 'YYYY-MM-DD']})
    cust_no_card = ReportAttributes(
        'Customer_nocard', {'set': ['start_date', 'end_date']},
        {'where': ['YYYY-MM-DD', 'YYYY-MM-DD']})
    room_avail = ReportAttributes(
        'Room_avail', {'set': ['start_date', 'end_date', 'hotel_id', 'name',
                               'zip']},
        {'set': ['YYYY-MM-DD', 'YYYY-MM-DD', 'e.g. 1', 'e.g. Wolf Inn Raleigh',
                 'e.g. 24354']})


################################################################################
# Main Interface from UI to API                                                #
################################################################################
class AppsClient(object):
    """
    Client interface to Apps API
    """
    def __init__(self, db, check=False):
        """
        Instantiates client class.
        This class in turn instantiations the Apps API class and passes the db
        connection

        Parameters:
            :param db: a mysql.connector connection
            :param check: Boolean indicating whether SQL checks should be used
        """
        self.apps = Apps(db, check)
        self.db = db

    # Helper interfaces
    def select(self, where_dict, table_name):
        """
        Used to make basic SELECT queries to the database.  Interfaces with
        get_data_frame method in Apps.py
        Parameters:
            :param where_dict: dictionary of attributes for the select clause
            :param table_name: Name of SQL table to search
        Returns:
            :return: Pandas data frame or Error
        """
        if where_dict is not None:
            return self.apps.get_data_frame('*', table_name, where_dict)
        else:
            return self.apps.get_data_frame('*', table_name)

    def zip_is_present(self, zip_code):
        """
        Used to check existence of a zip code in the database.

        Parameters:
            :param zip_code: Zip code of interest

        Returns:
            :return: Pandas data frame or Error
        """
        result = self.apps.get_data_frame('*', 'ZipToCityState',
                                          {'zip': zip_code})
        if len(result) == 0:
            return False
        else:
            return True

    def insert(self, param_dict, api_info):
        """
        Used to make INSERT transactions on the database. Interfaces with the
        insert method of the appropriate entity in Apps.py. Since zip is a 
        foreign key constraint, any zip information is entered first.

        Parameters:
            :param param_dict: Attribute dictionary containing embedded 'set'
            and 'where' dictionaries for formulating SQL statement.  For
            inserts, only the 'set' dictionary need be used.
            :param api_info: The api information (attribute lists) for the
            relevant entity

        Returns:
            :return: Pandas data frame or Error
        """
        set_dict = param_dict['set']
        zip_result = None

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip')
                            if k in set_dict}
                zip_result = self.apps.add_zip(zip_dict)
                if not isinstance(zip_result, pd.DataFrame):
                    return zip_result
            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names['set']
                         if k in set_dict}
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
                result = result.merge(zip_result, left_on='zip',
                                      right_on='zip', how='outer')
            return result

    def update(self, param_dict, api_info):
        """
        Used to make UPDATE transactions on the database. Interfaces with the
        update method of the appropriate entity in Apps.py. Since zip is a 
        foreign key constraint, any zip information is entered first.

        Parameters:
            :param param_dict: Attribute dictionary containing embedded 'set'
            and 'where' dictionaries for formulating SQL statement.
            :param api_info: The api information (attribute lists) for the
            relevant entity

        Returns:
            :return: Pandas data frame or Error
        """
        set_dict = param_dict['set']
        where_dict = param_dict['where']
        zip_result = None
        print set_dict
        print where_dict
        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip')
                            if k in set_dict}
                zip_result = self.apps.add_zip(zip_dict)
                if not isinstance(zip_result, pd.DataFrame):
                    return zip_result
            # Remove extra arguments (city, state)
            item_dict = {k: set_dict[k] for k in api_info.attr_names['set']
                         if k in set_dict}
            where_clause_dict = {k: where_dict[k]
                                 for k in api_info.attr_names['set']
                                 if k in where_dict}
            # select the correct API and submit
            result = {
                'Hotels': lambda x, y: self.apps.update_hotel(x, y),
                'Rooms': lambda x, y: self.apps.update_room(x, y),
                'Staff': lambda x, y: self.apps.update_staff(x, y),
                'Customers': lambda x, y: self.apps.update_customer(x, y),
                'Reservations': lambda x, y: self.apps.update_reservation(x, y),
                'Transactions': lambda x, y: self.apps.update_transaction(x, y)
            }[api_info.table_name](item_dict, where_clause_dict)

            if zip_result is not None:
                result = result.merge(zip_result, left_on='zip',
                                      right_on='zip', how='outer')
            return result

    def delete(self, param_dict, api_info):
        """
        Used to make DELETE transactions on the database. Interfaces with the
        delete method of the appropriate entity in Apps.py. Since zip is a 
        foreign key constraint, any zip information is entered first.

        Parameters:
            :param param_dict: Attribute dictionary containing embedded 'set'
            and 'where'dictionaries for formulating SQL statement. For deletes,
            only the 'where' dictionary need be used.
            :param api_info: The api information (attribute lists) for the
            relevant entity

        Returns:
            :return: Pandas data frame or Error
        """
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
        """
        Used to call pre-formulated SQL queries for generating reports.

        Parameters:
            :param param_dict: Attribute dictionary containing embedded 'set'
            and 'where' dictionaries for formulating SQL statement. For reports
            only the 'set' dictionary need be used.
            :param api_info: The api information (attribute lists) for the
            relevant report

        Returns:
            :return: Pandas data frame or Error
        """
        set_dict = param_dict['set']
        arg_list = [set_dict[key] for key in api_info.attr_names['set']]

        with sql_transaction(self.db):
            result = {
                'Generate_bill': lambda x: self.apps.generate_bill(x[0]),
                'Occupancy_hotel': lambda x:
                self.apps.report_occupancy_by_hotel(x[0]),
                'Occupancy_room': lambda x:
                self.apps.report_occupancy_by_room_type(x[0]),
                'Occupancy_city': lambda x:
                self.apps.report_occupancy_by_city(x[0]),
                'Occupancy_date': lambda x:
                self.apps.report_occupancy_by_date_range(x[0], x[1]),
                'List_staff': lambda x:
                self.apps.report_staff_by_role(x[0]),
                'Customer_inter': lambda x:
                self.apps.report_customer_interactions(x[0]),
                'Revenue_hotel': lambda x:
                self.apps.report_revenue_single_hotel(x[0], x[1], x[2]),
                'Revenue_all': lambda x:
                self.apps.report_revenue_all_hotels(x[0], x[1])
            }[api_info.report_name](arg_list)

            return result

    def get_report_with_dict(self, param_dict, api_info):
        """
        Used to call pre-formulated SQL queries for generating reports. Similar
        to previous function except api call uses a dictionary instead of a
        list.

        Parameters:
            :param param_dict: Attribute dictionary containing embedded 'set'
            and 'where' dictionaries for formulating SQL statement. For reports
            only the 'set' dictionary need be used.
            :param api_info: The api information (attribute lists) for the
            relevant report

        Returns:
            :return: Pandas data frame or Error
        """
        set_dict = param_dict['set']
        print set_dict
        with sql_transaction(self.db):
            result = {
                'Room_avail': lambda x: self.apps.room_availability(x)
            }[api_info.report_name](set_dict)
            return result
