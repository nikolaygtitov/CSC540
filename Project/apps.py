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

# Implementation of the program applications for the ZipToCityState table


def add_zip(_zip_, city, state):
    """Adds new tuple into ZipToCityState table

    The ZipToCityState table must exist. It adds new zip address with
    corresponding city and state into table. If check boolean parameter is
    enabled, it performs assertions ensuring that data to be added obeys MySQL
    constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param _zip_: ZIP code
        :param city: City that corresponds to the ZIP code
        :param state: State that corresponds to the ZIP code

    Returns:
        :returns: None

    TODO: None
    """
    try:
        if check:
            assert len(_zip_) >= 5, 'Exception: ZIP must be 5 or more digits.\n'
            assert city, 'Exception: City must be specified and must be ' \
                         'non-empty.\n'
            assert len(state) == 2, 'Exception: State must be exactly two ' \
                                    'characters.\n'

        insert_stmt = ("INSERT INTO ZipToCityState (zip, city, state) "
                       "VALUES (%s, %s, %s)")
        cursor.execute(insert_stmt, (_zip_, city, state))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Hotels table


def add_hotel(name, street, _zip_, phone_number, _id_=None):
    """Adds new tuple into Hotels table

    The Hotels table must exist. It adds new hotel into Hotels table with all
    corresponding information specified by parameters. If check boolean
    parameter is enabled, it performs assertions ensuring that data to be
    added obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param name: Name of the hotel
        :param street: Street address of the hotel
        :param _zip_: ZIP code of the hotel
        :param phone_number: Phone number of the hotel
        :param _id_: ID of the hotel. It must be unique across the system.
        Since it is auto incremented by MySQL, it is not required.

    Returns:
        :returns: None

    TODO: None
    """
    try:
        if check:
            assert name, 'Exception: Name of the hotel must be specified and ' \
                         'must be non-empty.\n'
            assert street, 'Exception: Street address of the hotel must be ' \
                           'specified and must be non-empty.\n'
            assert phone_number, 'Exception: Phone number of the hotel must ' \
                                 'be specified and must be non-empty.\n'

        if _id_ is None:
            insert_stmt = ("INSERT INTO Hotels (name, street, zip, "
                           "phone_number) VALUES (%s, %s, %s, %s)")
            cursor.execute(insert_stmt, (name, street, _zip_, phone_number))
        else:
            insert_stmt = ("INSERT INTO Hotels (id, name, street, zip, "
                           "phone_number) VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(insert_stmt, (_id_, name, street, _zip_,
                                         phone_number))

    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Rooms table


def add_room(hotel_id, room_number, category, occupancy, rate):
    """Adds new tuple into Rooms table

    The Rooms table must exist. It adds new room into Rooms table with all
    corresponding information specified by parameters. If check boolean
    parameter is enabled, it performs assertions ensuring that data to be
    added obeys MySQL constraints that are ignored by current MySQL MariaDB
    version.

    Parameters:
        :param hotel_id: ID of the hotel where room is added
        :param room_number: Room number
        :param category: Category of the room (economy, deluxe, etc.)
        :param occupancy: Maximum occupancy of the room. Must not exceed 9 (
        nine) guests
        :param rate: Rate per one night in US dollars of the room

    Returns:
        :returns: None

    TODO: None
    """
    try:
        if check:
            assert category, 'Exception: Category type of the room must be ' \
                             'specified and must be non-empty.\n'
            assert 0 < occupancy < 10, \
                'Exception: Maximum occupancy of the room must be between 1 ' \
                'and 9 inclusive.\n'

        insert_stmt = ("INSERT INTO Rooms (hotel_id, room_number, category, "
                       "occupancy, rate) VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(insert_stmt, (hotel_id, room_number, category,
                                     occupancy, rate))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Staff table


def add_staff(name, title, date_of_birth, department, phone_number, street,
              _zip_, works_for_hotel_id, assigned_hotel_id=None,
              assigned_room_number=None, _id_=None):
    """Adds new tuple into Staff table

    The Staff table must exist. It adds new staff member into Staff table
    with all corresponding information specified by parameters. If check
    boolean parameter is enabled, it performs assertions ensuring that data
    to be added obeys MySQL constraints that are ignored by current MySQL
    MariaDB version.

    Parameters:
        :param name: Full name (first, middle, last names) of the staff
        member (e.g. George W. Bush)
        :param title: Title of the staff member (e.g. Manager, Front Desk
        Representative, Room Service Staff, etc.)
        :param date_of_birth: Date of birth of the staff member. It must
        follow the Date format YYYY-MM-DD
        :param department: Department under which staff member works
        :param phone_number: Contact phone number of the staff member
        :param street: Street (home) address of staff member
        :param _zip_: ZIP code of the home address of the staff member
        :param works_for_hotel_id: ID of the hotel that staff member works
        for. Each staff member works for exactly one hotel.
        :param assigned_hotel_id: Hotel ID to which the staff member currently
        is assigned to as dedicated staff. Each staff member can be assigned to
        at most one room in one particular hotel.
        :param assigned_room_number: Room number to which the staff member
        currently is assigned to as dedicated staff. Each staff member can be
        assigned to at most one room in one particular hotel.
        :param _id_: Staff ID. It must be unique across the system. Since it
        is auto incremented by MySQL, it is not required.

    Returns:
        :returns: None

    TODO: If staff member is assigned to a particular room and hotel, we need
    to determine Staff ID and Reservation ID to call add_serves(staff_id,
    reservation_id) to add the staff-reservation interaction into Serves table.
    """
    try:
        if check:
            assert name, 'Exception: Name of the staff member must be ' \
                         'specified and must be non-empty.\n'
            assert title, 'Exception: Title of the staff member must be ' \
                          'specified and must be non-empty.\n'
            assert len(date_of_birth) == 10, \
                'Exception: Date of birth must follow the DATE format: ' \
                'YYYY-MM-DD.\n'
            assert department, \
                'Exception: Department under which staff member works must ' \
                'be specified and must be non-empty.\n'
            assert phone_number, 'Contact phone number of the staff member ' \
                                 'must be specified and must be non-empty.\n'
            assert street, 'Street address of the staff member must be ' \
                           'specified and must be and must be non-empty.\n'
            if assigned_hotel_id is None:
                assert assigned_room_number is None, \
                    'Exception: Hotel ID for a given room number that staff ' \
                    'member is assigned to as dedicated staff must be ' \
                    'specified.\n'
            else:
                assert assigned_room_number is not None, \
                    'Exception: Room number for a given hotel ID that staff ' \
                    'member is assigned to as dedicated staff must be ' \
                    'specified.\n'

        if _id_ is None:
            if assigned_hotel_id is None and assigned_room_number is None:
                insert_stmt = ("INSERT INTO Staff (name, title, "
                               "date_of_birth, department, phone_number, "
                               "street, zip, works_for_hotel_id) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_stmt, (name, title, date_of_birth,
                                             department, phone_number,
                                             street, _zip_, works_for_hotel_id))
            else:
                insert_stmt = ("INSERT INTO Staff (name, title, "
                               "date_of_birth, department, phone_number, "
                               "street, zip, works_for_hotel_id, "
                               "assigned_hotel_id, assigned_room_number) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                               "%s)")
                cursor.execute(insert_stmt, (name, title, date_of_birth,
                                             department, phone_number,
                                             street, _zip_, works_for_hotel_id,
                                             assigned_hotel_id,
                                             assigned_room_number))
        else:
            if assigned_hotel_id is None and assigned_room_number is None:
                insert_stmt = ("INSERT INTO Staff (id, name, title, "
                               "date_of_birth, department, phone_number, "
                               "street, zip, works_for_hotel_id) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_stmt, (_id_, name, title, date_of_birth,
                                             department, phone_number, street,
                                             _zip_, works_for_hotel_id))
            else:
                insert_stmt = ("INSERT INTO Staff (id, name, title, "
                               "date_of_birth, department, phone_number, "
                               "street, zip, works_for_hotel_id, "
                               "assigned_hotel_id, assigned_room_number) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                               "%s, %s)")
                cursor.execute(insert_stmt, (_id_, name, title, date_of_birth,
                                             department, phone_number,
                                             street, _zip_, works_for_hotel_id,
                                             assigned_hotel_id,
                                             assigned_room_number))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Customers table


def add_customer(name, date_of_birth, phone_number, email, street, _zip_, ssn,
                 account_number=None, is_hotel_card=None, _id_=None):
    """Adds new tuple into Customers table

    The Customers table must exist. It adds new customer into Customers table
    with all corresponding information specified by parameters. If check
    boolean parameter is enabled, it performs assertions ensuring that data
    to be added obeys MySQL constraints that are ignored by current MySQL
    MariaDB version.

    Parameters:
        :param name: Full name (first, middle, last names) of the customer (
        e.g. George W. Bush)
        :param date_of_birth: Date of birth of the customer. It must follow
        the Date format YYYY-MM-DD
        :param phone_number: Contact phone number of the customer
        :param email: Contact email address of the customer
        :param street: Street (home) address of the customer
        :param _zip_: ZIP code of the home address of the customer
        :param ssn: Social security number of the customer. Customers are
        responsible for the payment and always pay for themselves. It must
        follow the NNN-NN-NNNN format.
        :param account_number: Account number of the customer that is charged
        for any services provided by hotel. Each customer has at most one
        payment method (account number).
        :param is_hotel_card: Indicator whether the card (account number) is
        hotels credit card. Customer gets a 5% discount with hotels credit card.
        :param _id_: Customer ID. It must be unique across the system. Since
        it is auto incremented by MySQL, it is not required.

    Returns:
        :returns: None

    TODO: None
    """
    try:
        if check:
            assert name, 'Exception: Name of the customer must be specified ' \
                         'and must be non-empty.\n'
            assert len(date_of_birth) == 10, \
                'Exception: Date of birth must follow the DATE format: ' \
                'YYYY-MM-DD.\n'
            assert phone_number, 'Contact phone number of the customer must ' \
                                 'be specified and must be non-empty.\n'
            assert email, 'Contact email address the customer must be ' \
                          'specified and must be non-empty.\n'
            assert street, 'Street address of the customer must be specified ' \
                           'and must be and must be non-empty.\n'
            assert len(ssn) == 11

        if _id_ is None:
            if account_number is None:
                insert_stmt = ("INSERT INTO Customers (name, date_of_birth, "
                               "phone_number, email, street, zip, ssn, "
                               "is_hotel_card) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)")
                cursor.execute(insert_stmt, (name, date_of_birth, phone_number,
                                             email, street, _zip_, ssn,
                                             is_hotel_card))
            else:
                insert_stmt = ("INSERT INTO Customers (name, date_of_birth, "
                               "phone_number, email, street, zip, ssn, "
                               "account_number, is_hotel_card) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_stmt, (name, date_of_birth,
                                             phone_number, email, street,
                                             _zip_, ssn, account_number,
                                             is_hotel_card))
        else:
            if account_number is None:
                insert_stmt = ("INSERT INTO Customers (id, name, "
                               "date_of_birth, phone_number, email, street, "
                               "zip, ssn, is_hotel_card) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)")
                cursor.execute(insert_stmt, (_id_, name, date_of_birth,
                                             phone_number, email, street,
                                             _zip_, ssn, is_hotel_card))
            else:
                insert_stmt = ("INSERT INTO Customers (id, name, "
                               "date_of_birth, phone_number, email, street, "
                               "zip, ssn, account_number, is_hotel_card) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, "
                               "%s)")
                cursor.execute(insert_stmt, (_id_, name, date_of_birth,
                                             phone_number, email, street,
                                             _zip_, ssn, account_number,
                                             is_hotel_card))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Reservations table


def add_reservation(number_of_guests, start_date, end_date, hotel_id,
                    room_number, customer_id, check_in_time=None,
                    check_out_time=None, _id_=None):
    """Adds new tuple into Reservations table

    The Reservations table must exist. It adds newly created reservation into
    Reservations table with all corresponding information specified by
    parameters. If check boolean parameter is enabled, it performs assertions
    ensuring that data to be added obeys MySQL constraints that are ignored
    by current MySQL MariaDB version.

    Parameters:
        :param number_of_guests: Number of guests for this reservation. This
        number must not exceed the maximum room occupancy (nine) of any hotel.
        :param start_date: Start date of the reservation. It must follow the
        Date format YYYY-MM-DD.
        :param end_date: End date of the reservation. It must follow the Date
        format YYYY-MM-DD.
        :param hotel_id: ID of the Hotel where reservation is made
        :param room_number: Room number for this reservation
        :param customer_id: Customer ID who made this reservation
        :param check_in_time: Check-in time of the reservation. It must
        follow the DATETIME format YYYY-MM-DD HH:MM:SS.
        :param check_out_time: Check-out time of the reservation. It must
        follow the DATETIME format YYYY-MM-DD HH:MM:SS.
        :param _id_: Reservation ID. It must be unique across the system.
        Since it is auto incremented by MySQL, it is not required.

    Returns:
        :returns: None

    TODO: Need to determine the Staff ID who adds this reservation and ID of
    this newly created reservation. This function always needs to call
    add_serves(staff_id, reservation_id) to add staff-reservation interaction.
    May be need to call add_transaction() function to add this transaction
    for this reservation.
    """
    try:
        if check:
            assert 0 < number_of_guests < 10, \
                'Exception: Number of guests must be between 1 and 9 ' \
                'inclusive.\n'
            assert len(start_date) == 10, \
                'Exception: Start date of the reservation must follow the ' \
                'DATE format: YYYY-MM-DD.\n'
            assert len(end_date) == 10, \
                'Exception: End date of the reservation must follow the DATE ' \
                'format: YYYY-MM-DD.\n'
            if check_in_time is not None:
                assert len(check_in_time) == 19, \
                    'Exception: Check-in time of the reservation must follow ' \
                    'the DATETIME format: YYYY-MM-DD HH:MM:SS.\n'
            if check_out_time is not None:
                assert len(check_out_time) == 19, \
                    'Exception: Check-out time of the reservation must ' \
                    'follow the DATETIME format: YYYY-MM-DD HH:MM:SS.\n'
                assert len(check_in_time) == 19, \
                    'Exception: Check-in time of the reservation must follow ' \
                    'the DATETIME format: YYYY-MM-DD HH:MM:SS and check-out ' \
                    'time must not be specified before check-in time.\n'

        if _id_ is None:
            if check_in_time is None:
                insert_stmt = ("INSERT INTO Reservations (number_of_guests, "
                               "start_date, end_date, hotel_id, room_number, "
                               "customer_id) "
                               "VALUES (%s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_stmt, (number_of_guests, start_date,
                                             end_date, hotel_id, room_number,
                                             customer_id))
            else:
                if check_out_time is None:
                    insert_stmt = ("INSERT INTO Reservations ("
                                   "number_of_guests, start_date, end_date, "
                                   "check_in_time, hotel_id, room_number, "
                                   "customer_id) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                    cursor.execute(insert_stmt, (number_of_guests,
                                                 start_date, end_date,
                                                 check_in_time, hotel_id,
                                                 room_number, customer_id))
                else:
                    insert_stmt = ("INSERT INTO Reservations ("
                                   "number_of_guests, start_date, end_date, "
                                   "check_in_time, check_out_time, hotel_id, "
                                   "room_number, customer_id) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                    cursor.execute(insert_stmt, (number_of_guests,
                                                 start_date, end_date,
                                                 check_in_time,
                                                 check_out_time, hotel_id,
                                                 room_number, customer_id))
        else:
            if check_in_time is None:
                insert_stmt = ("INSERT INTO Reservations (id, "
                               "number_of_guests, start_date, end_date, "
                               "hotel_id, room_number, customer_id) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(insert_stmt, (_id_, number_of_guests,
                                             start_date, end_date, hotel_id,
                                             room_number, customer_id))
            else:
                if check_out_time is None:
                    insert_stmt = ("INSERT INTO Reservations (id, "
                                   "number_of_guests, start_date, end_date, "
                                   "check_in_time, hotel_id, room_number, "
                                   "customer_id) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                    cursor.execute(insert_stmt, (_id_, number_of_guests,
                                                 start_date, end_date,
                                                 check_in_time, hotel_id,
                                                 room_number, customer_id))
                else:
                    insert_stmt = ("INSERT INTO Reservations (id, "
                                   "number_of_guests, start_date, end_date, "
                                   "check_in_time, check_out_time, hotel_id, "
                                   "room_number, customer_id) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "
                                   "%s)")
                    cursor.execute(insert_stmt, (_id_, number_of_guests,
                                                 start_date, end_date,
                                                 check_in_time,
                                                 check_out_time, hotel_id,
                                                 room_number, customer_id))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Reservations table


def add_transaction(amount, _type_, date, reservation_id, _id_=None):
    """Adds new tuple into Transactions table

    The Transactions table must exist. It adds newly created transaction
    within one reservation into Transactions table with all corresponding
    information specified by parameters. If check boolean parameter is
    enabled, it performs assertions ensuring that data to be added obeys MySQL
    constraints that are ignored by current MySQL MariaDB version.

    Parameters:
        :param amount: Amount the transaction charged for specific services
        member (e.g. George W. Bush)
        :param _type_: Description of type of the transaction. Describing the
        services that are used in some details.
        :param date: Date of the transaction. It must follow the DATETIME
        format YYYY-MM-DD HH:MM:SS.
        :param reservation_id: Reservation ID that this transaction belongs
        to. Each transaction is associated with exactly one reservation.
        :param _id_: Transaction ID. It must be unique across the system.
        Since it is auto incremented by MySQL, it is not required.

    Returns:
        :returns: None

    TODO: None
    """
    try:
        if check:
            assert _type_, \
                'Exception: Description of type of the transaction must be ' \
                'specified and must be non-empty.\n'
            assert len(date) == 10, 'Exception: Date of the transaction must ' \
                                    'follow the DATE format: YYYY-MM-DD.\n'

        if _id_ is None:
            insert_stmt = ("INSERT INTO Transactions (amount, type, date, "
                           "reservation_id) VALUES (%s, %s, %s, %s)")
            cursor.execute(insert_stmt, (amount, _type_, date, reservation_id))
        else:
            insert_stmt = ("INSERT INTO Transactions (id, amount, type, date, "
                           "reservation_id) VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(insert_stmt, (_id_, amount, _type_, date,
                                         reservation_id))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)
    except AssertionError, e:
        print e
        return


# Implementation of the program applications for the Serves table


def add_serves(staff_id, reservation_id):
    """Adds new tuple into Serves table

    The Serves table must exist. It adds new tuple of the staff-reservation
    interaction (mapping) into Serves table. The new tuple is added only when
    any staff member serves a reservation. Staff member considered to be
    serving reservations if he/she is assigned to a room (reservation) as
    dedicated staff, creates reservation for a customer, prepares and
    delivers a meal, does dry cleaning for customer, does room service, does
    special requests, and etc.

    Parameters:
        :param staff_id: Staff ID that serves reservation
        :param reservation_id: Reservation ID that is served by the staff member

    Returns:
        :returns: None

    TODO: None
    """
    try:
        insert_stmt = ("INSERT INTO Serves (staff_id, reservation_id) "
                       "VALUES (%s, %s)")
        cursor.execute(insert_stmt, (staff_id, reservation_id))
    except mariadb.Error as error:
        print 'Error: {}'.format(error)


# Close DB connection
mariadb_connection.close()
