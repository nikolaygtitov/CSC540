"""
apps.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the apps.py file:
This file provides all required APIs for full interaction between front-end and
back-end programs. The APIs are constructed with the wrappers around MySQL
queries allowing the front-end (UI) to call appropriate functions performing
MySQL interactions. MySQL interactions include retrieving, storing, updating,
and deleting data from/into database. All query wrappers are enclosed within
a single class Apps.
To make a call to any of the APIs, the Apps class must be instantiated.
It has several private functions that serve as internal helper functions and
not intended to be referenced by either front-end of back-end.
All APIs are self-explanatory and do exactly what they are designed to do.
Some APIs perform several operations/tasks on the database. For example,
check-out API does the following operations:
1) Updates Reservations table with 'check_out_time' value
2) Frees all the assigned Staff to that reservation by updating Staff table
with NULL values for 'assigned_hotel_id' and 'assigned_room_number' attributes
of all Staff that are serving this reservation
3) Generates and inserts new transaction into Transactions table by
calculating the difference between 'start_date' and 'end_date',
and multiplying by the 'rate' of the room.

Following is the list APIs that may perform more than one operation at a time:
add_staff() - also performs assign_staff_to_room API if corresponding
attributes specified
update_staff() - also performs assign_staff_to_room API if corresponding
attributes specified
add_reservation() - also performs check-in/check-out APIs and may call
update_staff() API if corresponding attributes specified
update_reservation() - also performs check-in/check-out APIs and may call
update_staff() API if corresponding attributes specified

All APIs return Pandas DataFrame to the front-end layer.

@version: 1.0
@todo: Demo
@since: March 24, 2018

@status: Complete
@requires: Apps class to be instantiated
@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu

@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott
"""

# Import required Python and MySQL libraries
import mysql.connector as maria_db
import pandas as pd
from datetime import datetime
from queries import *


# This is the Apps class that contains all program applications (APIs)
class Apps(object):
    """
    Supports all defined program applications (APIs) in the Project Report 1
    and interacts with MariaDB MySQL server at NCSU (classdb2.csc.ncsu.edu)
    to store, update, and delete data.
    Creates and returns a Applications object with the given MariaDB connection
    and MariaDB CHECK constraint whether enabled or disabled.

    It inherits Python default object class if any of the object features need
    to be utilized.

    There are 2 (two) options to instantiate this class, depending on the
    CHECK constraints that are ignored by all MySQL engines, including the
    current MariaDB version used in the class. To enable CHECK constraints at
    the program application level, create an instance of this class as follows:

    object = Apps(maria_db_connection, check=True)

    To disable CHECK constraints at the program application level, ignore the
    check parameter:

    object = Apps(maria_db_connection)
    """
    def __init__(self, maria_db_connection, check=False):
        """
        Constructor method for the Apps class

        When an object of the class is constructed, this method is called to
        instantiate the object with given parameters.

        Parameters:
            :param maria_db_connection: MariaDB connection that created in the
            caller application based on the host, user, password, and database
            arguments. For this project host=classdb2.csc.ncsu.edu
            :param check: MySQL CHECK constraint boolean. Since CHECK
            constraint is ignored by all MySQL engines, all the check
            constraints must be performed at the application level.

        Returns:
            :return:

        TODO:
        """
        self.maria_db_connection = maria_db_connection
        self.cursor = maria_db_connection.cursor()
        self.check = check

    def get_data_frame(self, attributes, table_name, where_clause_dict=None):
        """
        Generates Pandas DataFrame with desired tuple(s)/row(s) in a table.

        For a given table name and WHERE clause, it does the following:
        1) Generates SELECT query for desired attributes specified by the
        argument
        2) Uses the SELECT query to create a Pandas DataFrame
        3) Returns Pandas DataFrame to the caller function

        Parameters:
            :param attributes: Comma-separated list of attributes desired to be
            shown in the resulting data frame or table (e.g. '*').
            :param table_name: Name of the table on which SELECT query is
            performed for generating Pandas DataFrame
            :param where_clause_dict: Dictionary of attributes and values used
            for generating WHERE clause. If all tuples/rows in a table are
            desired to be selected at once, this argument must be None.

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            desired tuple(s)/row(s)

        TODO:
        """
        # Build select query
        select_query = 'SELECT {} FROM {}'.format(attributes, table_name)
        # Add where clause
        where_values = []
        if where_clause_dict:
            select_query += ' WHERE {}'.format(
                ' AND '.join([key + '=%s' for key in where_clause_dict.keys()]))
            where_values = where_clause_dict.values()
        # Execute select query
        data_frame = pd.read_sql(select_query, params=where_values,
                                 con=self.maria_db_connection)
        return data_frame

    def _execute_simple_select_query(self, attributes, table_name,
                                     where_clause_dict=None):
        """
        Generates and executes SELECT query in python format with basic WHERE
        clause having only AND key words.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced only by
        internal caller functions.
        For a given attributes, table name, over which SELECT query is
        executed, and dictionary of attributes and values for corresponding
        WHERE clause, specified in the arguments respectively, it does the
        following:
        1) Generates WHERE clause with AND key words ONLY
        2) Generates an SELECT query statement that includes simple WHERE clause
        3) Executes this generated simple SELECT query
        The query is generated within the Python standards to prevent MySQL
        injection.

        Parameters:
            :param attributes: String of attributes separated by a comma for
            which SELECT query is executed
            :param table_name: Name of the table for which SELECT query is
            executed
            :param where_clause_dict: Dictionary of attributes and values used
            for generating WHERE clause. If all tuples/rows in a table are
            desired to be selected at once, this argument can be left out.

        Returns:
            :return:

        TODO:
        """
        # Generate select query statement and execute it
        if where_clause_dict:
            # Generate WHERE clause format only with AND key words
            where_attr_format = ' AND '.join([attr + '=%s' for attr in
                                              where_clause_dict.iterkeys()])
            select_query = "SELECT {} FROM {} WHERE {}".format(
                attributes, table_name, where_attr_format)
            self.cursor.execute(select_query, where_clause_dict.values())
        else:
            select_query = "SELECT {} FROM {}".format(attributes, table_name)
            self.cursor.execute(select_query)

    def _execute_select_query(self, attributes, table_name, where_clause=None,
                              where_values_list=None):
        """
        Generates and executes SELECT query in python format with complicated
        WHERE clause.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced only by
        internal caller functions.
        For a given attributes, table name, WHERE clause format, and list of
        values used for WHERE clause, over which SELECT query is executed, it
        does the following:
        1) Generates an SELECT query statement that includes complicated WHERE
        clause having different key words and even statements
        2) Executes this generated SELECT query
        The query is generated within the Python standards to prevent MySQL
        injection.

        Parameters:
            :param attributes: String of attributes separated by a comma for
            which SELECT query is executed
            :param table_name: Name of the table for which SELECT query is
            executed
            :param where_clause: String with complex WHERE clause format
            :param where_values_list: List of values used for WHERE clause
            included into SELECT query

        Returns:
            :return:

        TODO:
        """
        # Generate select query statement and execute it
        if where_clause is not None and where_values_list is not None:
            select_query = "SELECT {} FROM {} WHERE {}".format(
                attributes, table_name, where_clause)
            # Execute select query with complicated WHERE clause
            self.cursor.execute(select_query, where_values_list)
        else:
            select_query = "SELECT {} FROM {}".format(attributes, table_name)
            # Execute select query with complicated WHERE clause
            self.cursor.execute(select_query)

    def _execute_insert_query(self, dictionary, table_name):
        """
        Generates and executes INSERT query in python format.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced only by
        internal caller functions.
        For a given dictionary of attributes and values to be stored in a
        particular table, specified as an dictionary argument, it does the
        following:
        1) Generates an INSERT query statement
        2) Executes this generated INSERT query
        The query is generated within the Python standards to prevent MySQL
        injection.

        Parameters:
            :param dictionary: Dictionary of attributes and values to be stored
            in a table
            :param table_name: Name of the table for which INSERT query is
            executed

        Returns:
            :return:

        TODO:
        """
        # Generate insert query statement
        insert_query = "INSERT INTO {} ({}) VALUES ({})".format(
            table_name, ', '.join(dictionary.keys()), ', '.join(
                ['%s' for _ in dictionary.iterkeys()]))
        # Execute insert query
        self.cursor.execute(insert_query, dictionary.values())

    def _execute_update_query(self, select_attributes, table_name, dictionary,
                              where_clause_dict):
        """
        Generates and executes UPDATE query in python format.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced only by
        internal caller functions.
        For a given dictionary of attributes and values to be updated in a
        particular table, specified as an dictionary argument and table_name
        respectively, it does the following:
        1) Generates an UPDATE query statement
        2) Executes this generated UPDATE query
        3) Generates an WHERE clause for the SELECT query
        4) Calls a helper function get_data_frame() to retrieve updated tuple(s)
        The query is generated within the Python standards to prevent MySQL
        injection.

        Parameters:
            :param select_attributes: String for the SELECT query (follows by
            SELECT clause). Since this function returns Pandas DataFrame of
            desired tuple(s), it is required to specify these tuple(s).
            :param dictionary: Dictionary of attributes and values to be
            updated in a table
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause. It could be one or more attributes with
            corresponding values.
            :param table_name: Name of the table for which UPDATE query is
            executed

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a
            tuple(s) with successfully updated data in MySQL

        TODO:
        """
        # Get all attributes for SET clause
        set_attr_format = ', '.join([attr + '=%s' for attr in
                                     dictionary.iterkeys()])
        set_attr_args = dictionary.values()
        # Get all attributes for WHERE clause
        where_attr_format = ' AND '.join([attr + '=%s' for attr in
                                          where_clause_dict.iterkeys()])
        where_attr_args = where_clause_dict.values()
        # Construct update query statement
        update_query = "UPDATE {} SET {}".format(
            table_name, set_attr_format)
        if where_attr_args:
            update_query += ' WHERE {}'.format(where_attr_format)
        # Execute update query
        self.cursor.execute(update_query, set_attr_args + where_attr_args)

        # Generate WHERE clause for SELECT query
        select_where_clause_dict = {
            key: key in dictionary and dictionary[key] or old_where_value
            for key, old_where_value in where_clause_dict.iteritems()
        }

        # Query for this updated tuple and return it as Pandas DataFrame
        data_frame = self.get_data_frame(select_attributes, table_name,
                                         select_where_clause_dict)
        return data_frame

    def _execute_delete_query(self, table_name, dictionary):
        """
        Generates and executes DELETE query in python format.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced only by
        internal caller functions.
        For a given dictionary of attributes and values, specified as an
        dictionary argument, that must identify a tuple(s) in a particular
        table, it does the following:
        1) Generates an DELETE query statement
        2) Executes this generated DELETE query
        3) Generates an WHERE clause for the SELECT query
        4) Calls a helper function get_data_frame() to retrieve updated tuple(s)
        The query is generated within the Python standards to prevent MySQL
        injection.

        Parameters:
            :param table_name: Name of the table for which DELETE query is
            executed
            :param dictionary: Dictionary of attributes and values that
            identifies a tuple(s) in a table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(). The DataFrame must not
            contain any tuple(s), since the tuple(s) containing attribute
            values specified in the dictionary argument are deleted from a
            table.

        TODO:
        """
        where_attr_delete_format = ' AND '.join([attr + '=%s' for attr in
                                                dictionary.iterkeys()])

        # Generate delete query statement
        delete_query = "DELETE FROM {} WHERE {}".format(
            table_name, where_attr_delete_format)
        # Execute delete query
        self.cursor.execute(delete_query, dictionary.values())
        # Query this deleted tuple and return it as empty Pandas DataFrame
        data_frame = self.get_data_frame('*', table_name, dictionary)
        return data_frame

    def _check_out(self, reservation_id, check_out_time):
        """
        Performs the check-out logic operations on Staff and Transaction tables.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. It is referenced by two
        internal caller functions:
        i) add_reservation() - Within new reservation a check-out time
        follows immediately after check-in. It is very unlikely,
        but possible. This reservation must not have dedicated staff assigned.
        ii) update_reservation() - Customer checks-out.
        For a given reservation ID and check-out time, it does the following:
        1) Frees all dedicated staff that is assigned to the reservation by
        calling helper function update_staff()
        2) Inserts new transaction of type 'x-night(s) Reservation Room Charge'
        into the Transactions table by calling helper function add_transaction()

        Parameters:
            :param reservation_id: Reservation ID for reservation identified in
            the caller functions add_reservation() or update_reservation() by
            where_clause_dict attribute values
            :param check_out_time: Check-out time of the reservation. It must
            follow the DATETIME format YYYY-MM-DD HH:MM:SS. Used for
            transaction date.

        Returns:
            :return: Concatenated Pandas DataFrame(s) (two-dimensional
            size-mutable, heterogeneous tabular data structure with labeled
            axes) retrieved from internal helper functions:
                - update_staff() - which contains a tuple(s) with successfully
                updated data in Staff table (frees staff)
                - add_transaction() - which contains a tuple with successfully
                inserted data the Transaction tables (room charge)

        TODO: Testing
        """
        # Determine all staff assigned to this reservation
        self.cursor.execute(QUERY_ASSIGNED_STAFF, [reservation_id])
        staff_tuples = self.cursor.fetchall()
        staff_df_result = None
        transaction_df = None
        if staff_tuples is not None:
            for staff_id in staff_tuples:
                # Free all assigned staff by setting assigned hotel and
                # assigned room to NULL
                staff_df = self.update_staff(
                    {'assigned_hotel_id': None, 'assigned_room_number': None},
                    {'id': staff_id[0]})
                staff_df_result = staff_df.append(staff_df_result,
                                                  ignore_index=True)
            if staff_df_result is not None:
                staff_df_result = staff_df_result.rename(
                    index=str,
                    columns={'id': 'Staff_id',
                             'assigned_hotel_id': 'Staff_assigned_hotel_id',
                             'assigned_room_number': 'Staff_assigned_room'})
        # Add Room Charge transaction into Transactions table
        # Determine amount needs to be charged for the reservation
        self._execute_simple_select_query(
            'rate * DATEDIFF(end_date, start_date)',
            'Rooms NATURAL JOIN Reservations',
            {'id': reservation_id})
        amount = self.cursor.fetchall()
        # Determine number of nights customer reserved
        self._execute_simple_select_query('DATEDIFF(end_date, start_date)',
                                          'Reservations',
                                          {'id': reservation_id})
        number_nights = self.cursor.fetchall()
        if amount is not None and number_nights is not None:
            transaction_df = self.add_transaction(
                {'amount': amount[0][0],
                 'type': '{}-night(s) Room Reservation Charge'.format(
                     number_nights[0][0]),
                 'date': check_out_time,
                 'reservation_id': reservation_id})
            transaction_df = transaction_df.rename(
                index=str,
                columns={'id': 'Transaction_id',
                         'amount': 'Transaction_amount',
                         'type': 'Transaction_type',
                         'date': 'Transaction_date',
                         'reservation_id': 'Transaction_reserve_id'})
        # Returns
        result_df = pd.concat((transaction_df, staff_df_result), axis=1)
        return result_df

    def _assign_staff_to_room(self, hotel_id, room_number, staff_id=None,
                              reservation_id=None):
        """
        Assigns staff member to a room by adding it into Serves table.

        This is private function of the class and not intended to be referenced
        by either front-end or back-end layers. Request to assign staff to a
        room may come from four different internal caller functions:
        i) add_staff() - Staff is immediately assigned to a room once is added
        ii) update_staff() - Staff is assigned to a room as an update
        iii) add_reservation() - Customer checks-in immediately when
        reservation is created and this reservation is for Presidential Suite
        iv) update_reservation() - Customer checks-in and this reservation is
        for Presidential Suite

        If request comes from Staff functions, for a given hotel ID, room
        number, and staff ID, it does the following:
        1) Determines reservation ID
        2) Verifies that there is only one reservation for a given hotel ID and
        room number
        3) Inserts staff ID and reservation ID into Serves table by calling
        helper function add_serves() with appropriate dictionary of attributes
        and values
        If request comes from Reservation functions, for a given hotel ID, room
        number, and reservation ID, it does the following:
        1) Determines staff ID of one available Catering staff
        2) Determines staff ID of one available Room Service staff
        2) Inserts both staff IDs and reservation ID into Serves table by
        calling helper function add_serves() with appropriate dictionary of
        attributes and values
        If neither staff ID nor reservation ID cannot be found, nothing gets
        inserted into Serves table, but transaction must still succeed, unless
        there are some cursor errors.

        Parameters:
            :param hotel_id: ID of a hotel is needed for identifying unique
            reservation ID or determining whether room category in this hotel
            is Presidential Suite
            :param room_number: Room number is needed for identifying unique
            reservation ID or determining whether room category is Presidential
            Suite
            :param staff_id: ID of the staff member that gets assigned to a
            room. If request comes from Reservation functions, it is set to
            None.
            :param reservation_id: Reservation ID is needed to determine
            whether this reservation for Presidential Suite. If request comes
            from Staff functions, it is set to None.

        Returns:
            :return: Single Pandas DataFrame(s) (two-dimensional
            size-mutable, heterogeneous tabular data structure with labeled
            axes) retrieved from internal helper functions:
                - add_serves() - which contains a tuple with successfully
                inserted data in the Serves table (add staff to serves)
                - update_staff() - which contains a tuple with successfully
                updated data the Staff table (assign staff to a room)

        TODO: Testing
        """
        if staff_id is not None and reservation_id is None:
            # Staff is assigned from add_staff() or update_staff() functions
            # Determine Reservation ID
            where_clause = "hotel_id=%s AND room_number=%s AND " \
                           "check_in_time IS NOT NULL AND " \
                           "TRIM(check_in_time)<>'' AND " \
                           "(check_out_time IS NULL OR TRIM(check_out_time)='')"
            self._execute_select_query('id', 'Reservations', where_clause,
                                       [hotel_id, room_number])
            reservation_tuples = self.cursor.fetchall()
            assert len(reservation_tuples) == 1, \
                'Cannot assign staff to a room \'{}\' in hotel \'{}\' for ' \
                'which customer either did not check-in or already ' \
                'checked-out.\n'.format(room_number, hotel_id) \
                if len(reservation_tuples) == 0 else \
                'Found multiple active reservations for room \'{}\' in hotel ' \
                '\'{}\' with a checked-in customer. Cannot assign staff to ' \
                'multiple room simultaneously.\n'
            serves_df = self.add_serves(
                {'staff_id': staff_id,
                 'reservation_id': reservation_tuples[0][0]})
            serves_df = serves_df.rename(
                index=str, columns={'staff_id': 'Serves_staff_id',
                                    'reservation_id': 'Serves_reservation_id'})
            return serves_df
        if reservation_id is not None and staff_id is None:
            # Staff is assigned from add_reservation() or
            # update_reservation() functions
            # Check whether Reservation is Presidential Suite
            self._execute_simple_select_query('category', 'Rooms',
                                              {'hotel_id': hotel_id,
                                               'room_number': room_number})
            room_tuple = self.cursor.fetchall()
            if room_tuple is not None:
                room_category = room_tuple[0][0].split()
                if 'presidential' in (category.lower() for category in
                                      room_category):
                    # This is Presidential Suite
                    # Verify that this reservation is still active
                    self._execute_simple_select_query(
                        'check_out_time', 'Reservations',
                        {'id': reservation_id})
                    reservation_tuple = self.cursor.fetchall()
                    if reservation_tuple is None or \
                            not reservation_tuple[0][0] or \
                            reservation_tuple[0][0] == 'NULL':
                        # It needs to assign one available Catering staff
                        # and one Room Service as dedicated staff.
                        # Determine their Staff ID
                        where_clause = "works_for_hotel_id=%s AND " \
                                       "title LIKE '%{}%'  AND " \
                                       "(assigned_hotel_id IS NULL OR " \
                                       "assigned_hotel_id='') AND " \
                                       "(assigned_room_number IS NULL OR " \
                                       "assigned_room_number='')"
                        self._execute_select_query(
                            'id', 'Staff',
                            where_clause=where_clause.format('Catering'),
                            where_values_list=[hotel_id])
                        staff_tuples = self.cursor.fetchall()
                        catering_staff_df = None
                        room_service_staff_df = None
                        if staff_tuples is not None and staff_tuples[0][0]:
                            catering_staff_df = self.update_staff(
                                {'assigned_hotel_id': hotel_id,
                                 'assigned_room_number': room_number},
                                {'id': staff_tuples[0][0]},
                                reservation_id=reservation_id)
                        self._execute_select_query(
                            'id', 'Staff',
                            where_clause=where_clause.format('Room Service'),
                            where_values_list=[hotel_id])
                        staff_tuples = self.cursor.fetchall()
                        if staff_tuples and staff_tuples[0][0]:
                            room_service_staff_df = self.update_staff(
                                {'assigned_hotel_id': hotel_id,
                                 'assigned_room_number': room_number},
                                {'id': staff_tuples[0][0]},
                                reservation_id=reservation_id)
                        # Returns
                        if catering_staff_df is not None:
                            return catering_staff_df.append(
                                room_service_staff_df, ignore_index=True)
                        elif room_service_staff_df is not None:
                            return room_service_staff_df.append(
                                catering_staff_df, ignore_index=True)
        return None

    # Implementation of the program applications for the ZipToCityState table
    def add_zip(self, zip_dict):
        """
        Adds new tuple of ZIP code into ZipToCityState table.

        The ZipToCityState table must exist. It adds new ZIP code with
        corresponding city and state into ZipToCityState table by calling
        private helper function _execute_insert_query() that generates INSERT
        query statement and executes it. Once data is successfully stored in
        the table, it queries this tuple by calling helper function
        get_data_frame(), which returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param zip_dict: Dictionary of zip, state, and city attributes and
            values to be stored in ZipToCityState table. The content of the
            dictionary depends on the attributes and values received from UI
            and must include the following:
                - zip: ZIP code
                - city: City that corresponds to the ZIP code
                - state: State that corresponds to the ZIP code

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a
            tuple with successfully stored data in the ZipToCityState table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert zip_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'zip' in zip_dict and len(zip_dict['zip']) >= 5, \
                    'Exception: ZIP code must be specified and must be at ' \
                    'least 5 digits.\n'
                assert 'city' in zip_dict and zip_dict['city'], \
                    'Exception: City must be specified and must be non-empty.\n'
                assert 'state' in zip_dict and len(zip_dict['state']) == 2, \
                    'Exception: State must be specified and must be exactly ' \
                    'two characters.\n'
            # Execute insert query
            self._execute_insert_query(zip_dict, 'ZipToCityState')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame('*', 'ZipToCityState',
                                             {'zip': zip_dict['zip']})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_zip(self, zip_dict, where_clause_dict):
        """
        Updates a tuple in the ZipToCityState table.

        The ZipToCityState table must exist. It updates the ZipToCityState
        table with attributes and values specified in the zip_dict argument.
        The information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param zip_dict: Dictionary of attributes and values to be updated
            in the ZipToCityState table. The content of the dictionary depends
            on the attributes and values received from UI or other caller
            functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the ZipToCityState table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert zip_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in zip_dict.items():
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                '*', 'ZipToCityState', zip_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def delete_zip(self, zip_dict):
        """
        Deletes a tuple(s) from ZipToCityState table.

        The ZipToCityState table must exist. It deletes a tuple(s) from the
        ZipToCityState table identified by attributes and values in the
        zip_dict argument. The information gets deleted from the table by
        calling private helper function _execute_delete_query() that generates
        DELETE query statement and executes it. Once data is successfully
        deleted from the table, the helper function also tries to query this
        tuple and must return it as an empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the ZipToCityState table are
        identified.

        Parameters:
            :param zip_dict: Dictionary of attributes and values that identify
            a tuple(s) in the ZipToCityState table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert zip_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('ZipToCityState', zip_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Hotels table
    def add_hotel(self, hotel_dict):
        """
        Adds new tuple of hotel into Hotels table.

        The Hotels table must exist. It adds new hotel information into Hotels
        table with all corresponding information specified in the dictionary of
        attributes and values. The information gets added into the table by
        calling private helper function _execute_insert_query() that generates
        INSERT query statement and executes it. Once data is successfully
        stored in the table, it queries this tuple by calling helper function
        get_data_frame(), which returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param hotel_dict: Dictionary of hotel attributes and values to be
            stored in the Hotels table. The content of the dictionary depends
            on the attributes and values received from UI and may include the
            following:
                - id: ID of the hotel. It must be unique across the system.
                Since it is auto incremented by MySQL, it is not required.
                - name: Name of the hotel
                - street: Street address of the hotel
                - zip: ZIP code of the hotel
                - phone_number: Phone number of the hotel

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple
            with successfully stored data in the Hotels table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert hotel_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'name' in hotel_dict and hotel_dict['name'], \
                    'Exception: Name of the hotel must be specified and must ' \
                    'be non-empty.\n'
                assert 'street' in hotel_dict and hotel_dict['street'], \
                    'Exception: Street address of the hotel must be ' \
                    'specified and must be non-empty.\n'
                assert 'phone_number' in hotel_dict and \
                       hotel_dict['phone_number'], \
                    'Exception: Phone number of the hotel must be specified ' \
                    'and must be non-empty.\n'
            # Execute insert query
            self._execute_insert_query(hotel_dict, 'Hotels')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame(
                '*', 'Hotels', {'id': self.cursor.lastrowid})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_hotel(self, hotel_dict, where_clause_dict):
        """
        Updates a tuple in the Hotels table.

        The Hotels table must exist. It updates the Hotels table with
        attributes and values specified in the hotel_dict argument. The
        information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame. 
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param hotel_dict: Dictionary of attributes and values to be
            updated in the Hotels table. The content of the dictionary depends
            on the attributes and values received from UI or other caller
            functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the Hotels table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert hotel_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in hotel_dict.items():
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join([attr for attr in hotel_dict.iterkeys()])
            if 'id' not in hotel_dict.iterkeys():
                select_attr = 'id, ' + select_attr
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Hotels', hotel_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def delete_hotel(self, hotel_dict):
        """
        Deletes a tuple(s) from Hotels table.

        The Hotels table must exist. It deletes a tuple(s) from the Hotels
        table identified by attributes and values in the hotel_dict argument.
        The information gets deleted from the table by calling private helper
        function _execute_delete_query() that generates DELETE query statement
        and executes it. Once data is successfully deleted from the table, the
        helper function also tries to query this tuple and must return it as an
        empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Hotels table are identified.

        Parameters:
            :param hotel_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Hotels table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert hotel_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Hotels', hotel_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Rooms table
    def add_room(self, room_dict):
        """
        Adds new tuple of room into Rooms table.

        The Rooms table must exist. It adds new room information into Rooms
        table with all corresponding information specified in the dictionary of
        attributes and values. The information gets added into the table by
        calling private helper function _execute_insert_query() that generates
        INSERT query statement and executes it. Once data is successfully
        stored in the table, it queries this tuple by calling helper function
        get_data_frame(), which returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param room_dict: Dictionary of room attributes and values to be
            stored in the Rooms table. The content of the dictionary depends on
            the attributes and values received from UI and must include the
            following:
                - hotel_id: ID of the hotel where room is added
                - room_number: Room number
                - category: Category of the room (economy, deluxe, etc.)
                - occupancy: Maximum occupancy of the room. Must not exceed 9
                (nine) guests
                - rate: Rate per one night in US dollars of the room

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple
            with successfully stored data in the Rooms table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert room_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'room_number' in room_dict, \
                    'Exception: Room number must be specified and must be ' \
                    'positive integer.\n'
                assert 'category' in room_dict and room_dict['category'], \
                    'Exception: Category type of the room must be specified ' \
                    'and must be non-empty.\n'
                assert 'occupancy' in room_dict and \
                       0 < room_dict['occupancy'] < 10, \
                    'Exception: Maximum occupancy of the room must be ' \
                    'between 1 and 9 inclusive.\n'
            # Execute insert query
            self._execute_insert_query(room_dict, 'Rooms')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame(
                '*', 'Rooms', {'hotel_id': room_dict['hotel_id'],
                               'room_number': room_dict['room_number']})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_room(self, room_dict, where_clause_dict):
        """
        Updates a tuple in the Rooms table.

        The Rooms table must exist. It updates the Rooms table with attributes
        and values specified in the room_dict argument. The information gets
        updated in the table by calling private helper function
        _execute_update_query() that generates UPDATE query statement and
        executes it. Once data is successfully updated in the table, the helper
        function also queries this tuple and returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param room_dict: Dictionary of attributes and values to be updated
            in the Rooms table. The content of the dictionary depends on the
            attributes and values received from UI or other caller functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the Rooms table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert room_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in room_dict.items():
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join([attr for attr in room_dict.iterkeys()])
            if 'hotel_id' not in room_dict.iterkeys() or \
                    'room_number' not in room_dict.iterkeys():
                if 'room_number' not in room_dict.iterkeys():
                    select_attr = 'room_number, ' + select_attr
                if 'hotel_id' not in room_dict.iterkeys():
                    select_attr = 'hotel_id, ' + select_attr
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Rooms', room_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            return error
        except maria_db.Error as error:
            raise error

    def delete_room(self, room_dict):
        """
        Deletes a tuple(s) from Rooms table.

        The Rooms table must exist. It deletes a tuple(s) from the Rooms table
        identified by attributes and values in the room_dict argument. The
        information gets deleted from the table by calling private helper
        function _execute_delete_query() that generates DELETE query statement
        and executes it. Once data is successfully deleted from the table, the
        helper function also tries to query this tuple and must return it as an
        empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Rooms table are identified.

        Parameters:
            :param room_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Rooms table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert room_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Rooms', room_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Staff table
    def add_staff(self, staff_dict):
        """
        Adds new tuple of staff member into Staff table.

        The Staff table must exist. It adds new staff member information into
        Staff table with all corresponding information specified in the
        dictionary of attributes and values. The information gets added into
        the table by calling private helper function _execute_insert_query()
        that generates INSERT query statement and executes it. Once data is
        successfully stored in the table, it queries this tuple by calling
        helper function get_data_frame(), which returns it as Pandas DataFrame.
        If staff member immediately gets assigned to a room, it calls helper
        function assign_staff_to_room(), which determines reservation ID, and
        inserts a tuple into Serves table with appropriate staff ID and
        reservation ID.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param staff_dict: Dictionary of staff member attributes and values
            to be stored in the Staff table. The content of the dictionary
            depends on the attributes and values received from UI and may
            include the following:
                - id: Staff ID. It must be unique across the system. Since it
                is auto incremented by MySQL, it is not required.
                - name: Full name (first, middle, last names) of the staff
                member (e.g. George W. Bush)
                - title: Title of the staff member (e.g. Manager, Front Desk
                Representative, Room Service Staff, etc.)
                - date_of_birth: Date of birth of the staff member. It must
                follow the Date format YYYY-MM-DD
                - department: Department under which staff member works
                - phone_number: Contact phone number of the staff member
                - street: Street (home) address of staff member
                - zip: ZIP code of the home address of the staff member
                - works_for_hotel_id: ID of the hotel that staff member works
                for. Each staff member works for exactly one hotel.
                - assigned_hotel_id: Hotel ID to which the staff member
                currently is assigned to as dedicated staff. Each staff member
                can be assigned to at most one room in one particular hotel.
                - assigned_room_number: Room number to which the staff member
                currently is assigned to as dedicated staff. Each staff member
                can be assigned to at most one room in one particular hotel.

        Returns:
            :return: Concatenated Pandas DataFrame (two-dimensional
            size-mutable,heterogeneous tabular data structure with labeled
            axes) retrieved from the internal helper functions:
                - _assign_staff_to_room() - which contains a tuple(s) with
                successfully stored data in the Serves table (if staff gets
                assigned to a room)
                - get_data_frame() - which contains a tuple with successfully
                stored data in the Staff table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO: Testing
        """
        try:
            if self.check:
                # Perform validation
                assert staff_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'name' in staff_dict and staff_dict['name'], \
                    'Exception: Name of the staff member must be specified ' \
                    'and must be non-empty.\n'
                assert 'title' in staff_dict and staff_dict['title'], \
                    'Exception: Title of the staff member must be specified ' \
                    'and must be non-empty.\n'
                assert 'date_of_birth' in staff_dict and \
                       len(staff_dict['date_of_birth']) == 10, \
                    'Exception: Date of birth must follow the DATE format: ' \
                    'YYYY-MM-DD.\n'
                assert 'department' in staff_dict and \
                       staff_dict['department'], \
                    'Exception: Department under which staff member works ' \
                    'must be specified and must be non-empty.\n'
                assert 'phone_number' in staff_dict and \
                       staff_dict['phone_number'], \
                    'Contact phone number of the staff member must be ' \
                    'specified and must be non-empty.\n'
                assert 'street' in staff_dict and staff_dict['street'], \
                    'Street address of the staff member must be specified ' \
                    'and must be and must be non-empty.\n'
                if 'assigned_hotel_id' not in staff_dict:
                    assert 'assigned_room_number' not in staff_dict, \
                        'Exception: Hotel ID for a given room number that ' \
                        'staff member is assigned to as dedicated staff must ' \
                        'be specified.\n'
                else:
                    assert 'assigned_room_number' in staff_dict, \
                        'Exception: Room number for a given hotel ID that ' \
                        'staff member is assigned to as dedicated staff must ' \
                        'be specified.\n'
            # Execute insert query
            self._execute_insert_query(staff_dict, 'Staff')
            staff_id = self.cursor.lastrowid
            # Query for inserted Staff tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame('*', 'Staff', {'id': staff_id})
            # If staff gets assigned to a room, add it into Serves table
            if 'assigned_hotel_id' in staff_dict and \
                    'assigned_room_number' in staff_dict and \
                    staff_dict['assigned_hotel_id'] is not None and \
                    staff_dict['assigned_room_number'] is not None:
                # Assign staff to a room
                staff_df = self._assign_staff_to_room(
                    staff_dict['assigned_hotel_id'],
                    staff_dict['assigned_room_number'],
                    staff_id=staff_id, reservation_id=None)
                data_frame = pd.concat((data_frame, staff_df), axis=1)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_staff(self, staff_dict, where_clause_dict, reservation_id=None):
        """
        Updates a tuple in the Staff table.

        The Staff table must exist. It updates the Staff table with attributes
        and values specified in the room_dict argument. The information gets
        updated in the table by calling private helper function
        _execute_update_query() that generates UPDATE query statement and
        executes it. Once data is successfully updated in the table, the helper
        function also queries this tuple and returns it as Pandas DataFrame.
        If staff member gets assigned to a room through this update by the
        front-end layer (UI layer), it does not specify reservation_id argument.
        Therefore, it calls private helper function _assign_staff_to_room(),
        which determines reservation ID based on hotel_id, room_number,
        check-in and check-out times, which inserts a tuple into Serves table
        with appropriate staff ID and reservation ID.
        If staff member gets assigned by internal private caller functions
        _assign_staff_to_room(), reservation ID must be specified.
        Therefore, this function calls helper function add_serves(), which
        inserts a tuple into Serves table with appropriate staff ID and
        reservation ID. The sequence of calls with specified arguments for this
        situation must be as following:
        -> add_reservation OR update_reservation() ->
        -> _assign_staff_to_room(reservation_id) ->
        -> update_staff(staff_id, reservation_id) ->
        -> add_serves(staff_id, reservation_id)
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param staff_dict: Dictionary of attributes and values to be
            updated in the Staff table. The content of the dictionary depends
            on the attributes and values received from UI or other caller
            functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.
            :param reservation_id: ID of reservation associated with hotel ID
            and room number to which staff gets assigned. It is only specified
            when caller is internal private helper function
            _assign_staff_to_room(). It is None, if the call is made by the
            front-end layer.

        Returns:
            :return: Concatenated Pandas DataFrame (two-dimensional
            size-mutable,heterogeneous tabular data structure with labeled
            axes) retrieved from the internal helper functions:
                - add_serves() - which contains a tuple(s) with successfully
                stored data in the Serves table (if staff gets assigned to a
                room)
                - _execute_update_query() - which contains a tuple with
                successfully updated data in the Staff table (staff gets
                assigned to a room from UI layer)
                - _assign_staff_to_room() - which contains a tuple with
                successfully stored data in the Staff table (staff gets
                assigned to a room from reservation)

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO: Testing
        """
        try:
            if self.check:
                # Perform validation
                assert staff_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in staff_dict.items():
                    if attribute != 'assigned_hotel_id' and \
                            attribute != 'assigned_room_number':
                        assert value, \
                            'Exception: Attribute \'{}\' must be specified ' \
                            'to be updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join([attr for attr in staff_dict.iterkeys()])
            if not select_attr.startswith('id'):
                select_attr = 'id, ' + select_attr
            if 'id' not in staff_dict and 'id' in where_clause_dict and \
                    where_clause_dict['id']:
                staff_tuples = [where_clause_dict['id']]
            else:
                self._execute_simple_select_query('id', 'Staff',
                                                  where_clause_dict)
                staff_tuples = [x[0] for x in self.cursor.fetchall()]
            # If staff gets assigned to a room, add it into Serves table
            if staff_tuples and staff_tuples is not None and \
                    'assigned_hotel_id' in staff_dict and \
                    'assigned_room_number' in staff_dict and \
                    staff_dict['assigned_hotel_id'] is not None and \
                    staff_dict['assigned_room_number'] is not None:
                if reservation_id is not None:
                    # This gets called by update_reservation() ->
                    # -> assigned_staff_to_room()
                    serves_df_result = None
                    for staff in staff_tuples:
                        serves_df = self.add_serves(
                            {'staff_id': staff,
                             'reservation_id': reservation_id})
                        serves_df_result = serves_df.append(serves_df_result,
                                                            ignore_index=True)
                    if serves_df_result is not None:
                        serves_df_result = serves_df_result.rename(
                            index=str,
                            columns={'staff_id': 'Serves_staff_id',
                                     'reservation_id': 'Serves_reservation_id'})
                    select_attr = 'id, name, title, assigned_hotel_id, ' \
                                  'assigned_room_number'
                    # Execute update query
                    staff_df = self._execute_update_query(
                        select_attr, 'Staff', staff_dict, where_clause_dict)
                    staff_df = staff_df.rename(
                        index=str, columns={'id': 'Staff_id',
                                            'name': 'Staff_name',
                                            'title': 'Staff_title',
                                            'assigned_hotel_id':
                                                'Staff_assigned_hotel',
                                            'assigned_room_number':
                                                'Staff_assigned_room'})
                    data_frame = pd.concat((staff_df, serves_df_result), axis=1)
                    return data_frame
                else:
                    # This gets called by UI Layer
                    staff_df_result = None
                    for staff in staff_tuples:
                        staff_df = self._assign_staff_to_room(
                            staff_dict['assigned_hotel_id'],
                            staff_dict['assigned_room_number'],
                            staff_id=staff, reservation_id=reservation_id)
                        staff_df_result = staff_df.append(staff_df_result,
                                                          ignore_index=True)
                    # Execute update query
                    data_frame = self._execute_update_query(
                        select_attr, 'Staff', staff_dict, where_clause_dict)
                    data_frame = pd.concat((data_frame, staff_df_result),
                                           axis=1)
                    return data_frame
            # Execute update query - Staff is not assigned to room
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Staff', staff_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            return error
        except maria_db.Error as error:
            raise error

    def delete_staff(self, staff_dict):
        """
        Deletes a tuple(s) from Staff table.

        The Staff table must exist. It deletes a tuple(s) from the Staff table
        identified by attributes and values in the room_dict argument. The
        information gets deleted from the table by calling private helper
        function _execute_delete_query() that generates DELETE query statement
        and executes it. Once data is successfully deleted from the table, the
        helper function also tries to query this tuple and must return it as an
        empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Staff table are identified.

        Parameters:
            :param staff_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Staff table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert staff_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Staff', staff_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Customers table
    def add_customer(self, customer_dict):
        """
        Adds new tuple of customer into Customers table.

        The Customers table must exist. It adds new customer information into
        Customers table with all corresponding information specified in the
        dictionary of attributes and values. The information gets added into
        the table by calling private helper function _execute_insert_query()
        that generates INSERT query statement and executes it. Once data is
        successfully stored in the table, it queries this tuple by calling
        helper function get_data_frame(), which returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param customer_dict: Dictionary of customer attributes and values
            to be stored in the Customers table. The content of the dictionary
            depends on the attributes and values received from UI and may
            include the following:
                - id: Customer ID. It must be unique across the system. Since
                it is auto incremented by MySQL, it is not required.
                - name: Full name (first, middle, last names) of the customer
                (e.g. George W. Bush)
                - date_of_birth: Date of birth of the customer. It must follow
                the Date format YYYY-MM-DD
                - phone_number: Contact phone number of the customer
                - email: Contact email address of the customer
                - street: Street (home) address of the customer
                - zip: ZIP code of the home address of the customer
                - ssn: Social security number of the customer. Customers are
                responsible for the payment and always pay for themselves. It
                must follow the NNN-NN-NNNN format.
                - account_number: Account number of the customer that is
                charged for any services provided by hotel. Each customer has
                at most one payment method (account number).
                - is_hotel_card: Indicator whether the card (account number) is
                hotels credit card. Customer gets a 5% discount with hotels
                credit card.

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple
            with successfully stored data in the Customers table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert customer_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'name' in customer_dict and customer_dict['name'], \
                    'Exception: Name of the customer must be specified and ' \
                    'must be non-empty.\n'
                assert 'date_of_birth' in customer_dict and \
                       len(customer_dict['date_of_birth']) == 10, \
                    'Exception: Date of birth must be specified and must ' \
                    'follow the DATE format: YYYY-MM-DD.\n'
                assert 'phone_number' in customer_dict and \
                       customer_dict['phone_number'], \
                    'Exception: Contact phone number of the customer must be ' \
                    'specified and must be non-empty.\n'
                assert 'email' in customer_dict and customer_dict['email'], \
                    'Exception: Contact email address the customer must be ' \
                    'specified and must be non-empty.\n'
                assert 'street' in customer_dict and customer_dict['street'], \
                    'Exception: Street address of the customer must be ' \
                    'specified and must be and must be non-empty.\n'
                assert 'ssn' in customer_dict and \
                       len(customer_dict['ssn']) == 11, \
                    'Exception: Social Security Number must be specified and ' \
                    'must follow the NNN-NN-NNNN format.\n'
            # Execute insert query
            self._execute_insert_query(customer_dict, 'Customers')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame(
                '*', 'Customers', {'id': self.cursor.lastrowid})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_customer(self, customer_dict, where_clause_dict):
        """
        Updates a tuple in the Customers table.

        The Customers table must exist. It updates the Customers table with
        attributes and values specified in the customer_dict argument. The
        information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param customer_dict: Dictionary of attributes and values to be
            updated in the Customers table. The content of the dictionary
            depends on the attributes and values received from UI or other
            caller functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the Customers table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert customer_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in customer_dict.items():
                    if attribute != 'account_number' or \
                            attribute != 'is_hotel_card':
                        assert value, \
                            'Exception: Attribute \'{}\' must be specified ' \
                            'to be updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join([attr for attr in customer_dict.iterkeys()])
            if 'id' not in customer_dict:
                select_attr = 'id, ' + select_attr
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Customers', customer_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            return error
        except maria_db.Error as error:
            raise error

    def delete_customer(self, customer_dict):
        """
        Deletes a tuple(s) from Customers table.

        The Customers table must exist. It deletes a tuple(s) from the
        Customers table identified by attributes and values in the room_dict
        argument. The information gets deleted from the table by calling
        private helper function _execute_delete_query() that generates DELETE
        query statement and executes it. Once data is successfully deleted from
        the table, the helper function also tries to query this tuple and must
        return it as an empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Customers table are identified.

        Parameters:
            :param customer_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Customers table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert customer_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Customers', customer_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Reservations table
    def add_reservation(self, reservation_dict):
        """
        Adds new tuple of reservation into Reservations table.

        The Reservations table must exist. It adds newly created reservation
        information into Reservations table with all corresponding information
        specified in the dictionary of attributes and values. The information
        gets added into the table by calling private helper function
        _execute_insert_query() that generates INSERT query statement and
        executes it. Once data is successfully stored in the table, it queries
        this tuple by calling helper function get_data_frame(), which returns
        it as Pandas DataFrame.
        If Customer checks-in immediately after this reservation is created, it
        calls helper function assign_staff_to_room(), which determines whether
        this reservation is associate with Presidential Suite and if it is, it
        inserts a tuple into Serves table with appropriate staff ID and
        reservation ID.
        If Customer as well immediately checks-out as he/she checks-in (very
        unlikely but possible) after this reservation is created, it calls
        private helper function _check_out(), which frees all dedicated staff
        that is assigned to this reservation (since this is new reservation, it
        must not have any staff assigned to it) and inserts new transaction of
        type 'x-night(s) Reservation Room Charge' into the Transactions table.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param reservation_dict: Dictionary of reservation attributes and
            values to be stored in the Reservations table. The content of the
            dictionary depends on the attributes and values received from UI
            and may include the following:
                - id: Reservation ID. It must be unique across the system.
                Since it is auto incremented by MySQL, it is not required.
                - number_of_guests: Number of guests for this reservation. This
                number must not exceed the maximum room occupancy (nine) of any
                hotel.
                - start_date: Start date of the reservation. It must follow the
                Date format YYYY-MM-DD.
                - end_date: End date of the reservation. It must follow the
                Date format YYYY-MM-DD.
                - hotel_id: ID of the Hotel where reservation is made
                - room_number: Room number for this reservation
                - customer_id: Customer ID who made this reservation
                - check_in_time: Check-in time of the reservation. It must
                follow the DATETIME format YYYY-MM-DD HH:MM:SS.
                - check_out_time: Check-out time of the reservation. It must
                follow the DATETIME format YYYY-MM-DD HH:MM:SS.

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple 
            with successfully stored data in the Reservations table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO: 1) Not sure if still need this: Need to determine the Staff ID
        who adds this reservation and ID of this newly created reservation.
        This function always needs to call add_serves(staff_id, reservation_id)
        to add staff-reservation interaction.
        Testing
        """
        try:
            if self.check:
                # Perform validation
                assert reservation_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'number_of_guests' in reservation_dict and \
                       0 < reservation_dict['number_of_guests'] < 10, \
                    'Exception: Number of guests must be specified and must ' \
                    'be between 1 and 9 inclusive.\n'
                assert 'start_date' in reservation_dict and \
                       len(reservation_dict['start_date']) == 10, \
                    'Exception: Start date of the reservation must be ' \
                    'specified and must follow the DATE format: YYYY-MM-DD.\n'
                assert 'end_date' in reservation_dict and \
                       len(reservation_dict['end_date']) == 10, \
                    'Exception: End date of the reservation must be ' \
                    'specified and must follow the DATE format: YYYY-MM-DD.\n'
                start_date = datetime.strptime(reservation_dict['start_date'],
                                               '%Y-%m-%d')
                end_date = datetime.strptime(reservation_dict['end_date'],
                                             '%Y-%m-%d')
                assert start_date <= end_date, \
                    'Exception: Start date must be prior the end date.\n'
                if 'check_in_time' in reservation_dict:
                    assert len(reservation_dict['check_in_time']) == 19, \
                        'Exception: Check-in time of the reservation must be ' \
                        'specified and must follow the DATETIME format: ' \
                        'YYYY-MM-DD HH:MM:SS.\n'
                if 'check_out_time' in reservation_dict:
                    assert len(reservation_dict['check_out_time']) == 19, \
                        'Exception: Check-out time of the reservation must ' \
                        'be specified and must follow the DATETIME format: ' \
                        'YYYY-MM-DD HH:MM:SS.\n'
                    assert len(reservation_dict['check_in_time']) == 19, \
                        'Exception: Check-in time of the reservation must be ' \
                        'specified and must follow the DATETIME format: ' \
                        'YYYY-MM-DD HH:MM:SS.\n'
            # Execute insert query
            self._execute_insert_query(reservation_dict, 'Reservations')
            reservation_id = self.cursor.lastrowid
            # Query for inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame('*', 'Reservations',
                                             {'id': reservation_id})
            # If check-in, do all check-in logic: i) Check whether this
            # reservation is Presidential suite ii) Assign one Catering Staff
            # and one Room Service Staff to this reservation
            if 'check_in_time' in reservation_dict and \
                    reservation_dict['check_in_time'] and \
                    'check_out_time' not in reservation_dict:
                staff_df = self._assign_staff_to_room(
                    reservation_dict['hotel_id'],
                    reservation_dict['room_number'],
                    staff_id=None,
                    reservation_id=reservation_id)
                data_frame = pd.concat((data_frame, staff_df), axis=1)
                return data_frame
            # If check-out, do all check-out logic: i) Free dedicated staff
            # (should not be any dedicated staff since this is new reservation)
            # ii) Add new Room Charge transaction into Transactions table
            if 'check_out_time' in reservation_dict and \
                    reservation_dict['check_out_time']:
                staff_transact_df = self._check_out(
                    reservation_id, reservation_dict['check_out_time'])
                data_frame = pd.concat((data_frame, staff_transact_df), axis=1)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_reservation(self, reservation_dict, where_clause_dict):
        """
        Updates a tuple in the Reservations table.

        The Reservations table must exist. It updates the Customers table with
        attributes and values specified in the reservation_dict argument. The
        information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame.
        If update registers check-in time (but check-out times is still not
        registered), for all appropriate reservations identified by
        where_clause_dict attribute values it calls helper function
        assign_staff_to_room(), which determines whether this reservation is
        associate with Presidential Suite and if it is, it inserts a tuple into
        Serves table with appropriate staff ID and reservation ID.
        If this update registers check-out time, for all appropriate
        reservations identified by where_clause_dict attribute values, it calls
        private helper function _check_out(), which frees all dedicated staff
        that is assigned to a reservation and inserts new transaction of type
        'x-night(s) Reservation Room Charge' into the Transactions table.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param reservation_dict: Dictionary of attributes and values to be
            updated in the Reservations table. The content of the dictionary
            depends on the attributes and values received from UI or other
            caller functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Concatenated Pandas DataFrame (two-dimensional
            size-mutable, heterogeneous tabular data structure with labeled
            axes) retrieved from the internal helper functions:
                - _execute_update_query() - which contains a tuple(s) with
                successfully updated data in the Reservations table
                - ()_check_out() - which contains a concatenated tuple(s) of
                Staff data (frees staff) and new transaction (at the check-out
                inserts new transaction for room charge), retrieved from
                internal helper functions update_staff() and add_transaction()
                - () - which contains a tuple with successfully
                stored data in the Staff table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO: Testing
        """
        try:
            if self.check:
                # Perform validation
                assert reservation_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in reservation_dict.items():
                    if attribute != 'check_in_time' or \
                            attribute != 'check_out_time':
                        assert value, \
                            'Exception: Attribute \'{}\' must be specified ' \
                            'to be updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join(
                [attr for attr in reservation_dict.iterkeys()])
            if 'id' not in reservation_dict and 'id' in where_clause_dict:
                select_attr = 'id, ' + select_attr
            # Determine all Reservation tuples
            self._execute_simple_select_query(
                'id, check_in_time, check_out_time, hotel_id, room_number',
                'Reservations', where_clause_dict)
            reservation_tuples = self.cursor.fetchall()
            # If check-in, do all check-in logic: i) Ensure that check-out
            # has never been done previously, ii) check whether reservation is
            # associated with Presidential suite, and iii) assign one Catering
            # Staff and one Room Service Staff
            if 'check_in_time' in reservation_dict and \
                    reservation_dict['check_in_time'] and \
                    'check_out_time' not in reservation_dict and \
                    reservation_tuples is not None:
                staff_df_result = None
                for reservation in reservation_tuples:
                    # Check if neither check-in or check-out has never been
                    # done previously
                    if not reservation[1] or reservation[1] == 'NULL' and \
                            not reservation[2] or reservation[2] == 'NULL':
                        staff_df = self._assign_staff_to_room(
                            reservation[3], reservation[4], staff_id=None,
                            reservation_id=reservation[0])
                        if staff_df is not None:
                            staff_df_result = staff_df.append(staff_df_result,
                                                              ignore_index=True)
                # Execute update query
                data_frame = self._execute_update_query(
                    select_attr, 'Reservations', reservation_dict,
                    where_clause_dict)
                data_frame = pd.concat((data_frame, staff_df_result), axis=1)
                return data_frame
            # If check-out, do all check-out logic: i) Free dedicated staff,
            # ii) Add new Room Charge transaction into Transactions table
            if 'check_out_time' in reservation_dict and \
                    reservation_dict['check_out_time'] and \
                    reservation_tuples is not None:
                df_result = None
                for reservation in reservation_tuples:
                    # Check if check-out has never been done previously
                    if not reservation[2] or reservation[2] == 'NULL':
                        staff_transact_df = self._check_out(
                            reservation[0], reservation_dict['check_out_time'])
                        df_result = staff_transact_df.append(df_result,
                                                             ignore_index=True)
                # Execute update query
                data_frame = self._execute_update_query(
                    select_attr, 'Reservations', reservation_dict,
                    where_clause_dict)
                data_frame = pd.concat((data_frame, df_result), axis=1)
                return data_frame
            # Execute update query - It is not check-in or check-out
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Reservations', reservation_dict,
                where_clause_dict)
            return data_frame
        except AssertionError, error:
            return error
        except maria_db.Error as error:
            raise error

    def delete_reservation(self, reservation_dict):
        """
        Deletes a tuple(s) from Reservations table.

        The Reservations table must exist. It deletes a tuple(s) from the
        Reservations table identified by attributes and values in the room_dict
        argument. The information gets deleted from the table by calling
        private helper function _execute_delete_query() that generates DELETE
        query statement and executes it. Once data is successfully deleted from
        the table, the helper function also tries to query this tuple and must
        return it as an empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Reservations table are
        identified.

        Parameters:
            :param reservation_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Reservations table

        Returns:
            :return:  Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert reservation_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Reservations', reservation_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Reservations table
    def add_transaction(self, transaction_dict):
        """
        Adds new tuple of transaction into Transactions table.

        The Transactions table must exist. It adds newly created transaction
        information within one reservation into Transactions table with all
        corresponding information specified in the dictionary of attributes and
        values. The information gets added into the table by calling private
        helper function _execute_insert_query() that generates INSERT
        query statement and executes it. Once data is successfully stored in
        the table, it queries this tuple by calling helper function
        get_data_frame(), which returns it as Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be added obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param transaction_dict: Dictionary of transaction attributes and
            values to be stored in MySQL. The content of the dictionary depends
            on the attributes and values received from UI and may include the
            following:
                - id: Transaction ID. It must be unique across the system.
                Since it is auto incremented by MySQL, it is not required.
                - amount: Amount the transaction charged for specific services
                member (e.g. George W. Bush)
                - type: Description of type of the transaction. Describing the
                services that are used in some details.
                - date: Date of the transaction. It must follow the DATETIME
                format YYYY-MM-DD HH:MM:SS.
                - reservation_id: Reservation ID that this transaction does
                belongs to. Each transaction is associated with exactly one
                reservation.

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple
            with successfully stored data in the Transactions table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert transaction_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
                assert 'amount' in transaction_dict, \
                    'Exception: Amount of the transaction must be specified ' \
                    'in US dollars.\n'
                assert 'type' in transaction_dict and \
                       transaction_dict['type'], \
                    'Exception: Description of type of the transaction must ' \
                    'be specified and must be non-empty.\n'
                assert 'date' in transaction_dict and \
                       pd.to_datetime(transaction_dict['date'],
                                      errors='coerce') != pd.NaT, \
                    'Exception: Date of the transaction must follow the DATE ' \
                    'format: YYYY-MM-DD.\n'
            # Execute insert query
            self._execute_insert_query(transaction_dict, 'Transactions')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame(
                '*', 'Transactions', {'id': self.cursor.lastrowid})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_transaction(self, transaction_dict, where_clause_dict):
        """
        Updates a tuple in the Transactions table.

        The Transactions table must exist. It updates the Transactions table
        with attributes and values specified in the transaction_dict argument.
        The information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param transaction_dict: Dictionary of attributes and values to be
            updated in the Transactions table. The content of the dictionary
            depends on the attributes and values received from UI or other
            caller functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the Transactions table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert transaction_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
                for attribute, value in transaction_dict.items():
                    assert value, \
                        'Exception: Attribute \'{}\' must be specified to be ' \
                        'updated.\n'.format(attribute)
            # Select only columns that are modified and query for them
            select_attr = ', '.join(
                [attr for attr in transaction_dict.iterkeys()])
            if 'id' not in transaction_dict:
                select_attr = 'id, ' + select_attr
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                select_attr, 'Transactions', transaction_dict,
                where_clause_dict)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def delete_transaction(self, transaction_dict):
        """
        Deletes a tuple(s) from Transactions table.

        The Transactions table must exist. It deletes a tuple(s) from the
        Transactions table identified by attributes and values in the room_dict
        argument. The information gets deleted from the table by calling
        private helper function _execute_delete_query() that generates DELETE
        query statement and executes it. Once data is successfully deleted from
        the table, the helper function also tries to query this tuple and must
        return it as an empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Transactions table are
        identified.

        Parameters:
            :param transaction_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Transactions table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert transaction_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Transactions', transaction_dict)
        except maria_db.Error as error:
            raise error

    # Implementation of the program applications for the Serves table
    def add_serves(self, serves_dict):
        """
        Adds new tuple of staff serves reservation into Serves table.

        The Serves table must exist. It adds new tuple of the staff-reservation
        interaction (mapping) into Serves table. The new tuple is added by
        calling private helper function _execute_insert_query() that generates
        INSERT query statement and executes it, only when any staff member
        serves a reservation. Once data is successfully stored in the table,
        it queries this tuple by calling helper function get_data_frame(),
        which returns it as Pandas DataFrame.
        Staff member considered to be serving reservations if he/she is
        assigned to a room (reservation) as dedicated staff, creates
        reservation for a customer, prepares and delivers a meal, does dry
        cleaning for customer, does room service, does special requests, and
        etc.

        Parameters:
            :param serves_dict: Dictionary of the staff-reservation serves
            attributes and values to be stored in MySQL. The content of the
            dictionary depends on the attributes and values received from
            whether caller functions or UI and must include the following:
                - staff_id: Staff ID that serves reservation
                - reservation_id: Reservation ID that is served by the staff
                member

        Returns:
            :return: Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) retrieved
            from the helper function get_data_frame(), which contains a tuple
            with successfully stored data in the Serves table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert serves_dict, \
                    'Exception: Cannot add tuple into the table. Required ' \
                    'attributes are not specified.\n'
            # Execute insert query
            self._execute_insert_query(serves_dict, 'Serves')
            # Query for this inserted tuple and return it as Pandas DataFrame
            data_frame = self.get_data_frame(
                '*', 'Serves', {
                    'staff_id': serves_dict['staff_id'],
                    'reservation_id': serves_dict['reservation_id']})
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def update_serves(self, serves_dict, where_clause_dict):
        """
        Updates a tuple in the Serves table.

        The Serves table must exist. It updates the Serves table with
        attributes and values specified in the serves_dict argument. The
        information gets updated in the table by calling private helper
        function _execute_update_query() that generates UPDATE query statement
        and executes it. Once data is successfully updated in the table, the
        helper function also queries this tuple and returns it as Pandas
        DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that data to be updated obeys MySQL constraints that are ignored by
        current MySQL MariaDB version.

        Parameters:
            :param serves_dict: Dictionary of attributes and values to be
            updated in the Serves table. The content of the dictionary
            depends on the attributes and values received from UI or other
            caller functions.
            :param where_clause_dict: Dictionary of attributes and values used
            for WHERE clause in the UPDATE query. It may contain one or more
            attributes and corresponding values.

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of successfully updated data in the Serves table

        Exceptions:
            :raise: Assertion Error or MySQL Connector Error exceptions

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert serves_dict, \
                    'Exception: Cannot update tuple(s) in the table. ' \
                    'Attributes to be updated are not specified.\n'
                assert where_clause_dict, \
                    'Exception: Cannot update tuple(s) in the table. Tuple(s) \
                    to be updated cannot be identified. Identification ' \
                    'attributes are not specified.\n'
            # Execute update query
            # Also queries for updated tuple and returns it as Pandas DataFrame
            data_frame = self._execute_update_query(
                '*', 'Rooms', serves_dict, where_clause_dict)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def delete_serves(self, serves_dict):
        """
        Deletes a tuple(s) from Serves table.

        The Serves table must exist. It deletes a tuple(s) from theServes table
        identified by attributes and values in the room_dict argument. The
        information gets deleted from the table by calling private helper
        function _execute_delete_query() that generates DELETE query statement
        and executes it. Once data is successfully deleted from the table, the
        helper function also tries to query this tuple and must return it as an
        empty Pandas DataFrame.
        If check boolean parameter is enabled, it performs assertions ensuring
        that a tuple(s) to be deleted from the Serves table are identified.

        Parameters:
            :param serves_dict: Dictionary of attributes and values that
            identify a tuple(s) in the Serves table

        Returns:
            :return: Empty Pandas DataFrame (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes)

        Exceptions:
            :raise: MySQL Connector Error exception

        TODO:
        """
        try:
            if self.check:
                # Perform validation
                assert serves_dict, \
                    'Exception: Cannot identify tuple(s) to be deleted from ' \
                    'the table.\n'
            return self._execute_delete_query('Serves', serves_dict)
        except maria_db.Error as error:
            raise error

    def room_availability(self, dictionary):
        """
        Checks room(s) availability based on the given criteria (filters).

        For a given set of attributes and values specified in the argument
        dictionary, which are used as filters and must include mandatory items
        for start and end dates, this function does the following:
        1) Generates a string of attributes names displayed in Pandas DataFrame
        2) Generates a table statement followed by FROM in a query
        3) Generates nested WHERE clause which is used in Reservations table to
        query for specific dates
        4) Generate complete where clause with attributes and values specified
        in the dictionary argument
        5) Gets Pandas DataFrame for available room(s) by calling internal
        helper function get_data_frame() with arguments generated in this
        function

        Parameters:
            :param dictionary: Dictionary of attributes and values used as
            filtering options to identify available rooms. The content of the
            dictionary depends on the attributes and values received from UI
            and may include the following:
                - start_date: Start date
                - end_date: End date
                - hotel_id: ID of the specific Hotel. Room(s) availability are
                checked only within a particular hotel identified by this ID
                - name: Name of a hotel. Room(s) availability are checked only
                within a hotel(s) identified by this name
                - street: Desired street as additional filter for a hotel/room
                - city: Desired city as additional filter for a hotel/room
                - state: Desired state as additional filter for a hotel/room
                - zip: Desired ZIP code as additional filter for a hotel/room
                - category: Desired category of a room as additional filter
                (e.g. Economy, Deluxe, and etc.)
                - occupancy: Desired occupancy of a room as additional filter
                - rate: Desired rate as additional filter for a hotel/room

        Returns:
            :return: Pandas DataFrame(s) (two-dimensional size-mutable,
            heterogeneous tabular data structure with labeled axes) containing
            a tuple(s) of all available room based on the given criteria. This
            Pandas DataFrame contains the following columns:
                - Hotel ID | Hotel Name | Street | City | State | ZIP | Phone |
                  Room Number | Category | Occupancy | Rate
        """
        try:
            if self.check:
                # Perform validation
                assert len(dictionary) > 1, \
                    'Exception: Both Start and End Dates must be specified ' \
                    'to check availability of a Room(s).\n'
                assert 'start_date' in dictionary and \
                       dictionary['start_date'], \
                    'Exception: Invalid Start Date. Please specify valid ' \
                    'start date.\n'
                assert 'end_date' in dictionary and dictionary['end_date'] \
                       and len(dictionary['end_date']) == 10, \
                    'Exception: Invalid End Date. Please specify valid end ' \
                    'date.\n'
            # Start and end dates needed only for nested WHERE clause
            start_date = dictionary['start_date']
            end_date = dictionary['end_date']
            del dictionary['start_date']
            del dictionary['end_date']
            # Generate the entire SELECT query
            nested_where_clause = ROOM_AVAILABILITY_NESTED_WHERE_CLAUSE.format(
                start_date, end_date, start_date, end_date, start_date,
                end_date)
            # Generate final WHERE clause
            if 'hotel_id' in dictionary:
                nested_where_clause = nested_where_clause + \
                               ' AND hotel_id = {} ))'.format(
                                   dictionary['hotel_id'])
            else:
                nested_where_clause = nested_where_clause + '))'
            where_clause = ' AND '.join(
                [attr + '=%s' for attr in dictionary.iterkeys()]) + ' AND ' \
                if dictionary else ''
            where_clause = where_clause + nested_where_clause
            where_clause = where_clause % tuple(dictionary.values())

            # Build select query
            select_query = 'SELECT {} FROM {} WHERE {}'.format(
                ROOM_AVAILABILITY_COLUMN_NAMES,
                ROOM_AVAILABILITY_TABLE_STATEMENT,
                where_clause
            )

            # SELECT statement is ready. Get Pandas DataFrame and return it.
            # Execute select query
            data_frame = pd.read_sql(select_query,
                                     con=self.maria_db_connection)
            return data_frame
        except AssertionError, error:
            raise error
        except maria_db.Error as error:
            raise error

    def generate_bill(self, reservation_id):
        """
        Generates a bill of total amount due and itemized charges per specific
        reservation.

        For a given reservation ID, specified as an argument, this function
        does the following:
        1) Constructs total amount due Pandas DataFrame with three columns:
        | Cost | Discount | Total Amount Due
        2) Constructs a list of itemized charges as Pandas DataFrame with four
        columns: | Transaction ID | Amount | Description | Date
        3) Concatenates two Pandas DataFrames and returns it to the caller
        function

        Parameters:
            :param reservation_id: Reservation ID for which total amount due is
            calculated applying discount and a list of itemized charges is
            calculated (does not include discount). The same ID is used for
            two different queries.

        Returns:
            :return: Concatenated Pandas DataFrames (two-dimensional
            size-mutable, heterogeneous tabular data structure with labeled
            axes) retrieved from pandas.read_sql() function for two queries:
                - GENERATE_BILL_TOTAL_AMOUNT_DUE: generates a bill for total
                amount
                - GENERATE_BILL_ITEMIZED_CHARGES: generates a bill for itemized
                charges
        """
        if self.check:
            # Perform validation
            assert reservation_id is not None, \
                'Exception: Invalid Reservation ID. Please specify valid ' \
                'Reservation ID.\n'
        # Construct total amount due Pandas DataFrame
        total_due_df = pd.read_sql(GENERATE_BILL_TOTAL_AMOUNT_DUE,
                                   con=self.maria_db_connection,
                                   params=reservation_id * 2)
        # Construct list of itemized charges as Pandas DataFrame
        itemized_df = pd.read_sql(GENERATE_BILL_ITEMIZED_CHARGES,
                                  con=self.maria_db_connection,
                                  params=reservation_id)
        # Return two concatenated Pandas DataFrames
        return [itemized_df, total_due_df]
        # return pd.concat((total_due_df, itemized_df), axis=1)

    # Reports apps implemented below.
    def report_occupancy_by_hotel(self, query_date):
        """
        Generates a report of occupancy for all hotels on the query date,
        showing the number of rooms occupied and the percentage occupancy.

        Parameters:
            :param query_date: The date for which the occupancy will be reported

        Returns:
            :return: Pandas dataframe containing a row for each hotel, with the
            columns:
              Hotel Name: The name of hotel with the following occupancy
                          statistics
              Rooms Occupied: The total number of rooms occupied on the query
                              date for the given hotel.
              Total Rooms: The total number of rooms in the hotel.
              % Occupancy: The percent occupancy of the hotel, calculated by
                           the rooms occupied divided by the total rooms.
        """

        df = pd.read_sql(REPORT_OCCUPANCY_BY_HOTEL,
                         con=self.maria_db_connection,
                         params=[query_date] * 2)
        return df

    def report_occupancy_by_room_type(self, query_date):
        """
        Generates a report of occupancy across all hotels, grouped by room type.

        Parameters:
            :param query_date: The date for which the occupancy will be reported

        Returns:
            :return: Pandas dataframe containing a row for each room type,
            with the columns:
              Room Type: The room type with the following occupancy stats.
              Rooms Occupied: The number of rooms (of the row's room type)
                              occupied on the query date.
              Total Rooms: The total number of rooms of the row's type.
              % Occupancy: The percent occupancy for the room type.
        """

        df = pd.read_sql(REPORT_OCCUPANCY_BY_ROOM_TYPE,
                         con=self.maria_db_connection,
                         params=[query_date] * 2)
        return df

    def report_occupancy_by_city(self, query_date):
        """
        Generates a report of occupancy from all hotels, grouped by city.

        Parameters:
            :param query_date: The date for which the occupancy will be reported

        Returns:
            :return: Pandas dataframe containing a row for each city,
            with the columns:
              City, State: The city and state with the following occupancy stats
              Rooms Occupied: The number of rooms (of the row's room type)
                              occupied on the query date.
              Total Rooms: The total number of rooms of the row's type.
              % Occupancy: The percent occupancy for the room type.
        """

        df = pd.read_sql(REPORT_OCCUPANCY_BY_CITY,
                         con=self.maria_db_connection,
                         params=[query_date] * 2)
        return df

    def report_occupancy_by_date_range(self, query_start, query_end):
        """
        Generates a report of the occupancy over a date range

        Parameters:
            :param query_start: The date for which to start the report
            :param query_end: The date for which to end the report

        Returns:
            :return: Pandas dataframe containing a single row with the columns:
              Actual Bookings: The number of bookings made during the query
                               date range, where bookings is calculated by the
                               by the sum of reserved rooms for each night.
              Total Possible Bookings: The total number of bookings possible,
                                       based on the number of rooms and the
                                       length of the query date range.
              % Occupancy: The percentage of actual bookings divided by total
                           possible bookings.
        """

        df = pd.read_sql(REPORT_OCCUPANCY_BY_DATE_RANGE,
                         con=self.maria_db_connection,
                         params=[query_end,
                                 query_start] * 4)
        return df

    def report_staff_by_role(self, hotel_id):
        """
        Report all the staff in a given hotel
        sorted by their role (department and title)

        Parameters:
            :param hotel_id: The hotel id for which to report staff.

        Returns:
            :return: Pandas dataframe containing a list of staff that work
            for the given hotel, with the columns:
              Department
              Title
              Staff Name
              Staff ID
        """

        df = pd.read_sql(REPORT_STAFF_BY_ROLE,
                         con=self.maria_db_connection,
                         params=[hotel_id])
        return df

    def report_customer_interactions(self, reservation_id):
        """
        Generates a report of all customer interactions for a given reservation

        Parameters:
            :param reservation_id: The reservation for which to report
            customer interactions.

        Returns:
            :return: Pandas dataframe containing a list of all staff that
            served a given reservation, with the columns:
              Staff Name
              Staff ID
        """

        df = pd.read_sql(REPORT_CUSTOMER_INTERACTIONS,
                         con=self.maria_db_connection,
                         params=[reservation_id])
        return df

    def report_revenue_single_hotel(self, start_date, end_date, hotel_id):
        """
        Generate a report of the revenue for a given hotel.

        Parameters:
            :param start_date: The revenue report query start date.
            :param end_date: The revenue report query end date.
            :param hotel_id: The hotel id for which to report revenue.

        Returns:
            :return: Pandas dataframe containing the revenue for the given hotel
            over the queried date range, with the columns:
              Hotel Name
              Revenue
        """

        df = pd.read_sql(REPORT_REVENUE_SINGLE_HOTEL,
                         con=self.maria_db_connection,
                         params=[start_date, end_date, hotel_id])
        return df

    def report_revenue_all_hotels(self, start_date, end_date):
        """
        Generate a report of the revenue for all hotels.

        Parameters:
            :param start_date: The revenue report query start date.
            :param end_date: The revenue report query end date.

        Returns:
            :return: Pandas dataframe containing the revenue for all hotels
            over the queried date range, with the columns:
              Hotel Name
              Revenue
        """

        df = pd.read_sql(REPORT_REVENUE_ALL_HOTELS,
                         con=self.maria_db_connection,
                         params=[start_date, end_date])
        return df
