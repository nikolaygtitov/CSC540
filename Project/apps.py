"""
apps.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540
This program implements the solution for the main Project assignment:

The design and development processes of Database Management System for
WolfInns are completed in the Project Report 1
and Project Report 2.

Description of the Project:
The Popular Hotel Chain database system is designed and built to manage and
maintain information of hotels, rooms, staff, and customers, including but
not limited to storing, updating, and deleting data. The database maintains
a variety of information records about hotels located in various cities
around the country, including staff, rooms, customers, and billing records.
For each customer stay it maintains service records, such as phone bills,
dry cleaning, gyms, room service, and special requests. It generates and
maintains billing accounts for each customer stay. It generates report
occupancy by hotel, room category, date range, and city.
The database system is developed for Wolf Inns and is used by hotels'
operators and employees including management staff, front desk
representatives, room service, billing, and catering staff. The Popular Hotel
Chain database system resolves constraints on availability and pricing of
rooms, maintaining proper customer, billing, check-in, and check-out
information. Users of the database may perform different tasks concurrently,
each consisting of multiple sequential operations that have an affect on the
database. There are four major tasks that are performed by corresponding
users on the database:
    1. Information Processing
    2. Maintaining Service Records
    3. Maintaining Billing Accounts
    4. Reports

Description of the program project.py:
It provides a user with friendly UI to select tasks and operations user
needs/wants to perform.
All of the following operations are performed on MySQL MariaDB Server at NCSU
(classdb2.csc.ncsu.edu):
    - INSERTs
    - SELECTs
    - DROP TABLEs

Description of the program apps.py:
It provides the wrappers around MySQL queries allowing the northbound (UI) to
call appropriate functions to perform MySQL interaction including storing,
retrieving and deleting data.

Execute the program run:
 > python project.py

@version: 1.0
@todo: Integrate UI with apps, Add Transactions, Add documentation, Demo
@since: March 24, 2018

@status: Incomplete
@requires: Connection to MariaDB server at the NCSU.
           Option 1: Establish connection through NCSU VPN.
                     Installation of Cisco AnyConnect VPN Software is required.
                     Installation instructions of Cisco AnyConnect can be
                     found here:
https://oit.ncsu.edu/campus-it/campus-data-network/network-security/vpn/

           Option 2: Pull or copy source code to the NCSU remote machine and
                     run it there:
scp project.py unity_id@remote.eos.ncsu.edu:/afs/unity.ncsu.edu/users/u/unity_id

@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu

@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott

"""

# Import required Python and MySQL libraries
import mysql.connector as mariadb
import pandas as pd
from datetime import datetime

# Initialization of constants
# Change all the constants accordingly USER, PASSWORD, DB
HOST = 'classdb2.csc.ncsu.edu'
USER = 'ngtitov'
PASSWORD = '001029047'
DB = 'ngtitov'
check = True

# Actual program starts here
# Establish a DB connection
mariadb_connection = mariadb.connect(host=HOST, user=USER, password=PASSWORD,
                                     database=DB)
cursor = mariadb_connection.cursor()


def execute_select_query(attributes, table_name, where_clause=None):
    """Generates and executes SELECT query in python format.

    For a given table name and WHERE clause, 1) Generates SELECT query for
    desired attributes specified by the argument; 2) Uses the SELECT query to
    create a Pandas DataFrame and return it to the caller function.

    Parameters:
        :param attributes: String of attributes desired to be shown in the
        resulting table/clause (e.g. *)
        :param table_name: Name of the table on which SELECT query needs to be
        executed
        :param where_clause: String specifying the WHERE clause for SELECT
        query. It can be None if all tuples (rows) in the table are desired to
        be shown in the resulting table.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing
        desired tuple(s)/row(s); On FAILURE - Error message
    """
    try:
        # Query for desired tuple(s) and return it as Pandas DataFrame
        if where_clause is None:
            select_query = "SELECT {} FROM {}".format(attributes, table_name)
        else:
            select_query = "SELECT {} FROM {} WHERE {}".format(
                attributes, table_name, where_clause)
        data_frame = pd.read_sql(select_query, con=mariadb_connection)
        return data_frame
    except mariadb.Error as error:
        return error


def execute_insert_query(dictionary, table_name):
    """Generates and executes INSERT query in python format.

    For a given dictionary of attributes and values to be stored in a
    particular table, specified as an dictionary argument, it 1) Generates an
    INSERT query statement, 2) Executes this generated INSERT query and 3)
    Commits or rollback depending if there were any errors. The query is
    generated within the Python standards to prevent MySQL injection.

    Parameters:
        :param dictionary: Dictionary of attributes and values to be stored in
        a table
        :param table_name: Name of the table for which INSERT query is executed

    Returns:
        :returns: On SUCCESS - None; On FAILURE - Error message

    TODO:
    """
    try:
        # Construct insert query statement
        attributes_tuple = ''
        values_tuple = ''
        data_values_list = []
        # Get all attributes and values from dictionary
        for attribute, value in dictionary.items():
            attributes_tuple += attribute + ', '
            values_tuple += '%s, '
            data_values_list.append(value)
        attributes_tuple = attributes_tuple.rstrip(', ')
        values_tuple = values_tuple.rstrip(', ')
        insert_query = "INSERT INTO {} ({}) VALUES ({})".format(
            table_name, attributes_tuple, values_tuple)
        # Execute insert query
        cursor.execute(insert_query, data_values_list)
        mariadb_connection.commit()
        return None
    except mariadb.Error as error:
        return error


def execute_update_query(table_name, dictionary, where_clause_dict):
    """Generates and executes UPDATE query in python format.

    For a given dictionary of attributes and values to be updated in a
    particular table, specified as an dictionary argument, it 1) Generates an
    UPDATE query statement, 2) Executes this generated UPDATE query and 3)
    Commits or rollback depending if there were any errors. The query is
    generated within the Python standards to prevent MySQL injection.

    Parameters:
        :param dictionary: Dictionary of attributes and values to be updated in
        a table
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause. It could be one or more attributes with corresponding
        values.
        :param table_name: Name of the table for which UPDATE query is executed

    Returns:
        :returns: On SUCCESS - None; On FAILURE - Error message

    TODO:
    """
    try:
        # Construct update query statement
        set_attr = ''
        data_values_list = []
        where_attr_update = ''
        where_attr_select = {}
        # Get all attributes and values from dictionary
        for set_attribute, set_value in dictionary.items():
            set_attr += set_attribute + '=%s, '
            data_values_list.append(set_value)
            where_attr_select[set_attribute] = set_value
        set_attr = set_attr.rstrip(', ')
        # Get all attributes for WHERE clause
        for where_attribute, where_value in where_clause_dict.items():
            where_attr_update += where_attribute + '=%s AND '
            data_values_list.append(where_value)
            where_attr_select[where_attribute] = where_value
            where_attr_update = where_attr_update.rstrip(' AND ')
        update_query = "UPDATE {} SET {} WHERE {}".format(
            table_name, set_attr, where_attr_update)
        # Execute update query
        cursor.execute(update_query, data_values_list)
        mariadb_connection.commit()
        # Generate WHERE clause for SELECT query
        where_clause = ''
        for attr, value in where_attr_select.items():
            where_clause += attr + '=' + value + ' AND '
        where_clause = where_clause.rstrip(' AND ')
        # Query for this updated tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', table_name, where_clause)
        return data_frame
    except mariadb.Error as error:
        return error


# Implementation of the program applications for the ZipToCityState table


def add_zip(zip_dict):
    """Adds new tuple of ZIP code into ZipToCityState table.

    The ZipToCityState table must exist. It adds new ZIP code with
    corresponding city and state into ZipToCityState table by calling helper
    function execute_insert_query() that generates INSERT query statement and
    executes it. Once data is successfully stored in the table, it quires this
    tuple by calling helper function execute_select_query(), which returns it
    as Pandas DataFrame. If check boolean parameter is enabled, it performs
    assertions ensuring that data to be added obeys MySQL constraints that are
    ignored by current MySQL MariaDB version.

    Parameters:
        :param zip_dict: Dictionary of zip, state, and city attributes and
        values to be stored in ZipToCityState table. The content of the
        dictionary depends on the attributes and values received from UI and
        must include the following:
            - zip: ZIP code
            - city: City that corresponds to the ZIP code
            - state: State that corresponds to the ZIP code

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO:
    """
    try:
        if check:
            # Perform validation
            assert 'zip' in zip_dict and len(zip_dict['zip']) >= 5, \
                'Exception: ZIP code must be specified and must be at least ' \
                '5 digits.\n'
            assert 'city' in zip_dict and zip_dict['city'], \
                'Exception: City must be specified and must be non-empty.\n'
            assert 'state' in zip_dict and len(zip_dict['state']) == 2, \
                'Exception: State must be specified and must be exactly two ' \
                'characters.\n'
        # Execute insert query
        result = execute_insert_query(zip_dict, 'ZipToCityState')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'ZipToCityState',
                                          'zip={}'.format(zip_dict['zip']))
        return data_frame
    except AssertionError, e:
        return e


def update_zip(zip_dict, where_clause_dict):
    """Updates a tuple in the ZipToCityState table.

    The ZipToCityState table must exist. It updates the ZipToCityState table
    with attributes and values specified in the zip_dict argument. The
    information gets updated in the table by calling helper function
    execute_update_query() that generates UPDATE query statement and
    executes it. Once data is successfully updated in the table, the helper
    function also quires this tuple and returns it as Pandas DataFrame. If
    check boolean parameter is enabled, it performs assertions ensuring that
    data to be updated obeys MySQL constraints that are ignored by current
    MySQL MariaDB version.

    Parameters:
        :param zip_dict: Dictionary of attributes and values to be updated in
        the ZipToCityState table. The content of the dictionary depends on the
        attributes and values received from UI or other caller functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the ZipToCityState table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in zip_dict.items():
                assert value, \
                    'Exception: Attribute \'{}\' must be specified to be ' \
                    'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('ZipToCityState', zip_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Hotels table


def add_hotel(hotel_dict):
    """Adds new tuple of hotel into Hotels table.

    The Hotels table must exist. It adds new hotel information into Hotels
    table with all corresponding information specified in the dictionary of
    attributes and values. The information gets added into the table by calling
    helper function execute_insert_query() that generates INSERT query statement
    and executes it. Once data is successfully stored in the table, it quires
    this tuple by calling helper function execute_select_query(), which returns
    it as Pandas DataFrame. If check boolean parameter is enabled, it performs
    assertions ensuring that data to be added obeys MySQL constraints that are
    ignored by current MySQL MariaDB version.

    Parameters:
        :param hotel_dict: Dictionary of hotel attributes and values to be
        stored in the Hotels table. The content of the dictionary depends on
        the attributes and values received from UI and may include the
        following:
            - id: ID of the hotel. It must be unique across the system. Since
            it is auto incremented by MySQL, it is not required.
            - name: Name of the hotel
            - street: Street address of the hotel
            - zip: ZIP code of the hotel
            - phone_number: Phone number of the hotel

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO:
    """
    try:
        if check:
            # Perform validation
            assert 'name' in hotel_dict and hotel_dict['name'], \
                'Exception: Name of the hotel must be specified and must be ' \
                'non-empty.\n'
            assert 'street' in hotel_dict and hotel_dict['street'], \
                'Exception: Street address of the hotel must be specified ' \
                'and must be non-empty.\n'
            assert 'phone_number' in hotel_dict and hotel_dict[
                'phone_number'], \
                'Exception: Phone number of the hotel must be specified and ' \
                'must be non-empty.\n'
        # Execute insert query
        result = execute_insert_query(hotel_dict, 'Hotels')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'Hotels', 'id=LAST_INSERT_ID()')
        return data_frame
    except AssertionError, e:
        return e


def update_hotel(hotel_dict, where_clause_dict):
    """Updates a tuple in the Hotels table.

    The Hotels table must exist. It updates the Hotels table with attributes
    and values specified in the hotel_dict argument. The information gets
    updated in the table by calling helper function execute_update_query()
    that generates UPDATE query statement and executes it. Once data is
    successfully updated in the table, the helper function also quires this
    tuple and returns it as Pandas DataFrame. If check boolean parameter is
    enabled, it performs assertions ensuring that data to be updated obeys
    MySQL constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param hotel_dict: Dictionary of attributes and values to be updated in
        the Hotels table. The content of the dictionary depends on the
        attributes and values received from UI or other caller functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Hotels table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in hotel_dict.items():
                assert value, \
                    'Exception: Attribute \'{}\' must be specified to be ' \
                    'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Hotels', hotel_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Rooms table


def add_room(room_dict):
    """Adds new tuple of room into Rooms table.

    The Rooms table must exist. It adds new room information into Rooms table
    with all corresponding information specified in the dictionary of
    attributes and values. The information gets added into the table by calling
    helper function execute_insert_query() that generates INSERT query
    statement and executes it. Once data is successfully stored in the table,
    it quires this tuple by calling helper function execute_select_query(),
    which returns it as Pandas DataFrame. If check boolean parameter is
    enabled, it performs assertions ensuring that data to be added obeys
    MySQL constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param room_dict: Dictionary of room attributes and values to be
        stored in the Rooms table. The content of the dictionary depends on the
        attributes and values received from UI and must include the following:
            - hotel_id: ID of the hotel where room is added
            - room_number: Room number
            - category: Category of the room (economy, deluxe, etc.)
            - occupancy: Maximum occupancy of the room. Must not exceed 9
            (nine) guests
            - rate: Rate per one night in US dollars of the room

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO:
    """
    try:
        if check:
            # Perform validation
            assert 'room_number' in room_dict, \
                'Exception: Room number must be specified and must be ' \
                'positive integer.\n'
            assert 'category' in room_dict and room_dict['category'], \
                'Exception: Category type of the room must be specified and ' \
                'must be non-empty.\n'
            assert 'occupancy' in room_dict and \
                   0 < room_dict['occupancy'] < 10, \
                'Exception: Maximum occupancy of the room must be between 1 ' \
                'and 9 inclusive.\n'
        # Execute insert query
        result = execute_insert_query(room_dict, 'Rooms')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query(
            '*', 'Rooms', 'hotel_id={} AND room_number = {}'.format(
                room_dict['hotel_id'], room_dict['room_number']))
        return data_frame
    except AssertionError, e:
        print e
        return


def update_room(room_dict, where_clause_dict):
    """Updates a tuple in the Rooms table.

    The Rooms table must exist. It updates the Rooms table with attributes and
    values specified in the room_dict argument. The information gets updated in
    the table by calling helper function execute_update_query() that generates
    UPDATE query statement and executes it. Once data is successfully updated
    in the table, the helper function also quires this tuple and returns it as
    Pandas DataFrame. If check boolean parameter is enabled, it performs
    assertions ensuring that data to be updated obeys MySQL constraints that
    are ignored by current MySQL MariaDB version.

    Parameters:
        :param room_dict: Dictionary of attributes and values to be updated in
        the Rooms table. The content of the dictionary depends on the
        attributes and values received from UI or other caller functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Rooms table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in room_dict.items():
                assert value, \
                    'Exception: Attribute \'{}\' must be specified to be ' \
                    'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Rooms', room_dict, where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Staff table


def add_staff(staff_dict):
    """Adds new tuple of staff member into Staff table.

    The Staff table must exist. It adds new staff member information into Staff
    table with all corresponding information specified in the dictionary of
    attributes and values. The information gets added into the table by calling
    helper function execute_insert_query() that generates INSERT query
    statement and executes it. Once data is successfully stored in the table,
    it quires this tuple by calling helper function execute_select_query(),
    which returns it as Pandas DataFrame. If check boolean parameter is
    enabled, it performs assertions ensuring that data to be added obeys MySQL
    constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param staff_dict: Dictionary of staff member attributes and values to
        be stored in the Staff table. The content of the dictionary depends on
        the attributes and values received from UI and may include the
        following:
            - id: Staff ID. It must be unique across the system. Since it is
            auto incremented by MySQL, it is not required.
            - name: Full name (first, middle, last names) of the staff member
            (e.g. George W. Bush)
            - title: Title of the staff member (e.g. Manager, Front Desk
            Representative, Room Service Staff, etc.)
            - date_of_birth: Date of birth of the staff member. It must follow
            the Date format YYYY-MM-DD
            - department: Department under which staff member works
            - phone_number: Contact phone number of the staff member
            - street: Street (home) address of staff member
            - zip: ZIP code of the home address of the staff member
            - works_for_hotel_id: ID of the hotel that staff member works for.
            Each staff member works for exactly one hotel.
            - assigned_hotel_id: Hotel ID to which the staff member currently
            is assigned to as dedicated staff. Each staff member can be
            assigned to at most one room in one particular hotel.
            - assigned_room_number: Room number to which the staff member
            currently is assigned to as dedicated staff. Each staff member can
            be assigned to at most one room in one particular hotel.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO: If staff member is assigned to a particular room and hotel, we need
    to determine Staff ID and Reservation ID to call add_serves(staff_id,
    reservation_id) to add the staff-reservation interaction into Serves table.
    """
    try:
        if check:
            assert 'name' in staff_dict and staff_dict['name'], \
                'Exception: Name of the staff member must be specified and ' \
                'must be non-empty.\n'
            assert 'title' in staff_dict and staff_dict['title'], \
                'Exception: Title of the staff member must be specified and ' \
                'must be non-empty.\n'
            assert 'date_of_birth' in staff_dict and \
                   len(staff_dict['date_of_birth']) == 10, \
                'Exception: Date of birth must follow the DATE format: ' \
                'YYYY-MM-DD.\n'
            assert 'department' in staff_dict and staff_dict['department'], \
                'Exception: Department under which staff member works must ' \
                'be specified and must be non-empty.\n'
            assert 'phone_number' in staff_dict and \
                   staff_dict['phone_number'], \
                'Contact phone number of the staff member must be specified ' \
                'and must be non-empty.\n'
            assert 'street' in staff_dict and staff_dict['street'], \
                'Street address of the staff member must be specified and ' \
                'must be and must be non-empty.\n'
            if 'assigned_hotel_id' not in staff_dict:
                assert 'assigned_room_number' not in staff_dict, \
                    'Exception: Hotel ID for a given room number that staff ' \
                    'member is assigned to as dedicated staff must be ' \
                    'specified.\n'
            else:
                assert 'assigned_room_number' in staff_dict, \
                    'Exception: Room number for a given hotel ID that staff ' \
                    'member is assigned to as dedicated staff must be ' \
                    'specified.\n'
        # Execute insert query
        result = execute_insert_query(staff_dict, 'Staff')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'Staff', 'id=LAST_INSERT_ID()')
        return data_frame
    except AssertionError, e:
        print e
        return


def update_staff(staff_dict, where_clause_dict):
    """Updates a tuple in the Staff table.

    The Staff table must exist. It updates the Staff table with attributes and
    values specified in the room_dict argument. The information gets updated in
    the table by calling helper function execute_update_query() that generates
    UPDATE query statement and executes it. Once data is successfully updated
    in the table, the helper function also quires this tuple and returns it as
    Pandas DataFrame. If check boolean parameter is enabled, it performs
    assertions ensuring that data to be updated obeys MySQL constraints that
    are ignored by current MySQL MariaDB version.

    Parameters:
        :param staff_dict: Dictionary of attributes and values to be updated in
        the Staff table. The content of the dictionary depends on the
        attributes and values received from UI or other caller functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Staff table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in staff_dict.items():
                if attribute != 'assigned_hotel_id' or \
                        attribute != 'assigned_room_number':
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Staff', staff_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Customers table


def add_customer(customer_dict):
    """Adds new tuple of customer into Customers table.

    The Customers table must exist. It adds new customer information into
    Customers table with all corresponding information specified in the
    dictionary of attributes and values. The information gets added into the
    table by calling helper function execute_insert_query() that generates
    INSERT query statement and executes it. Once data is successfully stored in
    the table, it quires this tuple by calling helper function
    execute_select_query(), which returns it as Pandas DataFrame. If check
    boolean parameter is enabled, it performs assertions ensuring that data to
    be added obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param customer_dict: Dictionary of customer attributes and values to
        be stored in the Customers table. The content of the dictionary depends
        on the attributes and values received from UI and may include the
        following:
            - id: Customer ID. It must be unique across the system. Since it is
            auto incremented by MySQL, it is not required.
            - name: Full name (first, middle, last names) of the customer
            (e.g. George W. Bush)
            - date_of_birth: Date of birth of the customer. It must follow the
            Date format YYYY-MM-DD
            - phone_number: Contact phone number of the customer
            - email: Contact email address of the customer
            - street: Street (home) address of the customer
            - zip: ZIP code of the home address of the customer
            - ssn: Social security number of the customer. Customers are
            responsible for the payment and always pay for themselves. It
            must follow the NNN-NN-NNNN format.
            - account_number: Account number of the customer that is charged
            for any services provided by hotel. Each customer has at most one
            payment method (account number).
            - is_hotel_card: Indicator whether the card (account number) is
            hotels credit card. Customer gets a 5% discount with hotels credit
            card.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO:
    """
    try:
        if check:
            assert 'name' in customer_dict and customer_dict['name'], \
                'Exception: Name of the customer must be specified and must ' \
                'be non-empty.\n'
            assert 'date_of_birth' in customer_dict and \
                   len(customer_dict['date_of_birth']) == 10, \
                'Exception: Date of birth must be specified and must follow ' \
                'the DATE format: YYYY-MM-DD.\n'
            assert 'phone_number' in customer_dict and \
                   customer_dict['phone_number'], \
                'Exception: Contact phone number of the customer must be ' \
                'specified and must be non-empty.\n'
            assert 'email' in customer_dict and customer_dict['email'], \
                'Exception: Contact email address the customer must be ' \
                'specified and must be non-empty.\n'
            assert 'street' in customer_dict and customer_dict['street'], \
                'Exception: Street address of the customer must be specified ' \
                'and must be and must be non-empty.\n'
            assert 'ssn' in customer_dict and \
                   len(customer_dict['ssn']) == 11, \
                'Exception: Social Security Number must be specified and ' \
                'must follow the NNN-NN-NNNN format.\n'
        # Execute insert query
        result = execute_insert_query(customer_dict, 'Customers')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'Customers',
                                          'id=LAST_INSERT_ID()')
        return data_frame
    except AssertionError, e:
        print e
        return


def update_customer(customer_dict, where_clause_dict):
    """Updates a tuple in the Customers table.

    The Customers table must exist. It updates the Customers table with
    attributes and values specified in the customer_dict argument. The
    information gets updated in the table by calling helper function
    execute_update_query() that generates UPDATE query statement and executes
    it. Once data is successfully updated in the table, the helper function
    also quires this tuple and returns it as Pandas DataFrame. If check boolean
    parameter is enabled, it performs assertions ensuring that data to be
    updated obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param customer_dict: Dictionary of attributes and values to be updated
        in the Customers table. The content of the dictionary depends on the
        attributes and values received from UI or other caller functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Customers table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in customer_dict.items():
                if attribute != 'account_number' or \
                        attribute != 'is_hotel_card':
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Customers', customer_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Reservations table


def add_reservation(reservation_dict):
    """Adds new tuple of reservation into Reservations table.

    The Reservations table must exist. It adds newly created reservation
    information into Reservations table with all corresponding information
    specified in the dictionary of attributes and values. The information gets
    added into the table by calling helper function execute_insert_query() that
    generates INSERT query statement and executes it. Once data is successfully
    stored in the table, it quires this tuple by calling helper function
    execute_select_query(), which returns it as Pandas DataFrame. If check
    boolean parameter is enabled, it performs assertions ensuring that data to
    be added obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param reservation_dict: Dictionary of reservation attributes and
        values to be stored in the Reservations table. The content of the
        dictionary depends on the attributes and values received from UI and
        may include the following:
            - id: Reservation ID. It must be unique across the system. Since it
            is auto incremented by MySQL, it is not required.
            - number_of_guests: Number of guests for this reservation. This
            number must not exceed the maximum room occupancy (nine) of any
            hotel.
            - start_date: Start date of the reservation. It must follow the
            Date format YYYY-MM-DD.
            - end_date: End date of the reservation. It must follow the Date
            format YYYY-MM-DD.
            - hotel_id: ID of the Hotel where reservation is made
            - room_number: Room number for this reservation
            - customer_id: Customer ID who made this reservation
            - check_in_time: Check-in time of the reservation. It must follow
            the DATETIME format YYYY-MM-DD HH:MM:SS.
            - check_out_time: Check-out time of the reservation. It must follow
            the DATETIME format YYYY-MM-DD HH:MM:SS.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL;
        On FAILURE - Error message

    TODO: Need to determine the Staff ID who adds this reservation and ID of
    this newly created reservation. This function always needs to call
    add_serves(staff_id, reservation_id) to add staff-reservation interaction.
    May be need to call add_transaction() function to add this transaction
    for this reservation.
    """
    try:
        if check:
            assert 'number_of_guests' in reservation_dict and \
                   0 < reservation_dict['number_of_guests'] < 10, \
                'Exception: Number of guests must be specified and must be ' \
                'between 1 and 9 inclusive.\n'
            assert 'start_date' in reservation_dict and \
                   len(reservation_dict['start_date']) == 10, \
                'Exception: Start date of the reservation must be specified ' \
                'and must follow the DATE format: YYYY-MM-DD.\n'
            assert 'end_date' in reservation_dict and \
                   len(reservation_dict['end_date']) == 10, \
                'Exception: End date of the reservation must be specified ' \
                'and must follow the DATE format: YYYY-MM-DD.\n'
            start_date = datetime.strptime(reservation_dict['start_date'],
                                           '%Y-%m-%d')
            end_date = datetime.strptime(reservation_dict['end_date'],
                                         '%Y-%m-%d')
            assert start_date <= end_date, \
                'Exception: Start date must be prior the end date'
            if 'check_in_time' in reservation_dict:
                assert len(reservation_dict['check_in_time']) == 19, \
                    'Exception: Check-in time of the reservation must be ' \
                    'specified and must follow the DATETIME format: ' \
                    'YYYY-MM-DD HH:MM:SS.\n'
            if 'check_out_time' in reservation_dict:
                assert len(reservation_dict['check_out_time']) == 19, \
                    'Exception: Check-out time of the reservation must be ' \
                    'specified and must follow the DATETIME format: ' \
                    'YYYY-MM-DD HH:MM:SS.\n'
                assert len(reservation_dict['check_in_time']) == 19, \
                    'Exception: Check-in time of the reservation must be ' \
                    'specified and must follow the DATETIME format: ' \
                    'YYYY-MM-DD HH:MM:SS.\n'
        # Execute insert query
        result = execute_insert_query(reservation_dict, 'Reservations')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'Reservations',
                                          'id=LAST_INSERT_ID()')
        return data_frame
    except AssertionError, e:
        print e
        return


def update_reservation(reservation_dict, where_clause_dict):
    """Updates a tuple in the Reservations table.

    The Reservations table must exist. It updates the Customers table with
    attributes and values specified in the reservation_dict argument. The
    information gets updated in the table by calling helper function
    execute_update_query() that generates UPDATE query statement and executes
    it. Once data is successfully updated in the table, the helper function
    also quires this tuple and returns it as Pandas DataFrame. If check boolean
    parameter is enabled, it performs assertions ensuring that data to be
    updated obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param reservation_dict: Dictionary of attributes and values to be
        updated in the Reservations table. The content of the dictionary
        depends on the attributes and values received from UI or other caller
        functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Reservations table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in reservation_dict.items():
                if attribute != 'check_in_time' or \
                        attribute != 'check_out_time':
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Reservations', reservation_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Reservations table


def add_transaction(transaction_dict):
    """Adds new tuple of transaction into Transactions table.

    The Transactions table must exist. It adds newly created transaction
    information within one reservation into Transactions table with all
    corresponding information specified in the dictionary of attributes and
    values. The information gets added into the table by calling helper
    function execute_insert_query() that generates INSERT query statement and
    executes it. Once data is successfully stored in the table, it quires this
    tuple by calling helper function execute_select_query(), which returns it
    as Pandas DataFrame. If check boolean parameter is enabled, it performs
    assertions ensuring that data to be added obeys MySQL constraints that
    are ignored by current MySQL MariaDB version.

    Parameters:
        :param transaction_dict: Dictionary of transaction attributes and
        values to be stored in MySQL. The content of the dictionary depends on
        the attributes and values received from UI and may include the
        following:
            - id: Transaction ID. It must be unique across the system. Since it
            is auto incremented by MySQL, it is not required.
            - amount: Amount the transaction charged for specific services
            member (e.g. George W. Bush)
            - type: Description of type of the transaction. Describing the
            services that are used in some details.
            - date: Date of the transaction. It must follow the DATETIME format
            YYYY-MM-DD HH:MM:SS.
            - reservation_id: Reservation ID that this transaction belongs to.
            Each transaction is associated with exactly one reservation.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL
        On FAILURE - Error message

    TODO:
    """
    try:
        if check:
            assert 'amount' in transaction_dict, \
                'Exception: Amount of the transaction must be specified in ' \
                'US dollars.\n'
            assert 'type' in transaction_dict and transaction_dict['type'], \
                'Exception: Description of type of the transaction must be ' \
                'specified and must be non-empty.\n'
            assert 'date' in transaction_dict and \
                   len(transaction_dict['date']) == 10, \
                'Exception: Date of the transaction must follow the DATE ' \
                'format: YYYY-MM-DD.\n'
        # Execute insert query
        result = execute_insert_query(transaction_dict, 'Transactions')
        if result is not None:
            return result
        # Query for this inserted tuple and return it as Pandas DataFrame
        data_frame = execute_select_query('*', 'Transactions',
                                          'id=LAST_INSERT_ID()')
        return data_frame
    except AssertionError, e:
        print e
        return


def update_transaction(transaction_dict, where_clause_dict):
    """Updates a tuple in the Transactions table.

    The Transactions table must exist. It updates the Transactions table with
    attributes and values specified in the transaction_dict argument. The
    information gets updated in the table by calling helper function
    execute_update_query() that generates UPDATE query statement and executes
    it. Once data is successfully updated in the table, the helper function
    also quires this tuple and returns it as Pandas DataFrame. If check boolean
    parameter is enabled, it performs assertions ensuring that data to be
    updated obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param transaction_dict: Dictionary of attributes and values to be
        updated in the Transactions table. The content of the dictionary
        depends on the attributes and values received from UI or other caller
        functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Transactions table;
        On FAILURE - Error message

    TODO:
    """
    try:
        # Perform validation on updating attributes
        if check:
            for attribute, value in transaction_dict.items():
                assert value, \
                    'Exception: Attribute \'{}\' must be specified to be ' \
                    'updated.\n'.format(attribute)
        # Execute update query
        # It also queries for updated tuple and returns it as Pandas DataFrame
        data_frame = execute_update_query('Rooms', transaction_dict,
                                          where_clause_dict)
        return data_frame
    except AssertionError, e:
        return e


# Implementation of the program applications for the Serves table


def add_serves(serves_dict):
    """Adds new tuple of staff serves reservation into Serves table.

    The Serves table must exist. It adds new tuple of the staff-reservation
    interaction (mapping) into Serves table. The new tuple is added by calling
    helper function execute_insert_query() that generates INSERT query
    statement and executes it, only when any staff member serves a reservation.
    Once data is successfully stored in the table, it quires this tuple by
    calling helper function execute_select_query(), which returns it as Pandas
    DataFrame.
    Staff member considered to be serving reservations if he/she is assigned to
    a room (reservation) as dedicated staff, creates reservation for a
    customer, prepares and delivers a meal, does dry cleaning for customer,
    does room service, does special requests, and etc.

    Parameters:
        :param serves_dict: Dictionary of the staff-reservation serves
        attributes and values to be stored in MySQL. The content of the
        dictionary depends on the attributes and values received from whether
        caller functions or UI and must include the following:
            - staff_id: Staff ID that serves reservation
            - reservation_id: Reservation ID that is served by the staff member

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully stored data in MySQL
        On FAILURE - Error message

    TODO:
    """
    # Execute insert query
    result = execute_insert_query(serves_dict, 'Serves')
    if result is not None:
        return result
    # Query for this inserted tuple and return it as Pandas DataFrame
    data_frame = execute_select_query(
        '*', 'Serves', 'staff_id={} AND reservation_id={}'.format(
            serves_dict['staff_id'], serves_dict['reservation_id']))
    return data_frame


def update_serves(serves_dict, where_clause_dict):
    """Updates a tuple in the Serves table.

    The Serves table must exist. It updates the Serves table with attributes
    and values specified in the serves_dict argument. The information gets
    updated in the table by calling helper function execute_update_query() that
    generates UPDATE query statement and executes it. Once data is successfully
    updated in the table, the helper function also quires this tuple and
    returns it as Pandas DataFrame. If check boolean parameter is enabled, it
    performs assertions ensuring that data to be updated obeys MySQL
    constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param serves_dict: Dictionary of attributes and values to be
        updated in the Serves table. The content of the dictionary
        depends on the attributes and values received from UI or other caller
        functions.
        :param where_clause_dict: Dictionary of attributes and values used for
        WHERE clause in the UPDATE query. It may contain one or more attributes
        and corresponding values.

    Returns:
        :returns: On SUCCESS - Pandas DataFrame (two-dimensional size-mutable,
        heterogeneous tabular data structure with labeled axes) containing a
        tuple of successfully update tuple in the Serves table;
        On FAILURE - Error message

    TODO:
    """
    # Execute update query
    # It also queries for updated tuple and returns it as Pandas DataFrame
    data_frame = execute_update_query('Rooms', serves_dict, where_clause_dict)
    return data_frame


# Close DB connection
mariadb_connection.close()
