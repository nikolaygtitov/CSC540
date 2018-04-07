from apps import Apps
import pandas as pd
from util import sql_transaction


class ArgList(object):
    zip = ['zip', 'city', 'state']
    hotel = ['id', 'name', 'street', 'zip', 'phone_number']
    room = ['hotel_id', 'room_number', 'category', 'occupancy', 'rate']
    staff = ['id', 'name', 'title', 'date_of_birth', 'department',
               'phone_number', 'street', 'zip', 'works_for_hotel_id',
               'assigned_hotel_id', 'assigned_room_number']
    customer =  ['id', 'name', 'date_of_birth', 'phone_number', 'email',
               'street', 'zip', 'ssn', 'account_number', 'is_hotel_card']
    reservation = ['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id',
               'room_number', 'customer_id', 'check_in_time',
               'check_out_time']
    transaction = ['id', 'amount', 'type', 'date', 'reservation_id']


################################################################################
# Interface from UI to API
# - Edit this file to control interactions between UI and Apps
################################################################################
class APIHelper(object):
    def __init__(self, db, check=False):
        self.apps = Apps(db, check)
        self.db = db

    # Helper interfaces
    def call_select(self, where_dict, table_name ):
        #where_string = ' AND '.join([attr + '=%s' for attr in where_dict.iterkeys()])
        where_string = ' AND '.join([key + ('="%s"' % value) for key,value in where_dict.items()])
        return self.apps.get_data_frame('*', table_name, where_string)


    def zip_is_present(self, zip):
        result = self.apps.get_data_frame('*', 'ZipToCityState', ('zip=%s' % zip))
        if len(result) == 0:
            return False
        else:
            return True

    def call_add_hotel(self, param_dict):
        set_dict = param_dict['set']

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
                result = self.apps.add_zip(zip_dict)
                # TODO: Check if the following code is needed - I don't think so.
                #       This interferes with the transaction. Also check all other instances
                # if not isinstance(result, pd.DataFrame):
                #     return result

            # Insert the hotel
            hotel_dict = {k: set_dict[k] for k in ArgList.hotel if k in set_dict}
            return self.apps.add_hotel(hotel_dict)

    def call_update_hotel(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        with sql_transaction(self.db):
            # If a city and state is present, insert the new zip
            if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
                zip_dict = {k: set_dict[k] for k in ArgList.zip if k in set_dict}
                result = self.apps.add_zip(zip_dict)
                # if not isinstance(result, pd.DataFrame):
                #     return result

            # Update the hotel
            hotel_dict = {k: set_dict[k] for k in ArgList.hotel if k in set_dict}
            where_clause_dict = {k: where_dict[k] for k in ArgList.hotel if k in where_dict}
            return self.apps.update_hotel(hotel_dict, where_clause_dict)

    def call_delete_hotel(self, param_dict):
        where_dict = param_dict['where']
        with sql_transaction(self.db):
            return self.apps.delete_hotel(where_dict)

    def call_add_room(self, param_dict):
        set_dict = param_dict['set']

        # Insert the room
        room_dict = {k: set_dict[k] for k in ArgList.room if k in set_dict}
        return self.apps.add_room(room_dict)

    def call_update_room(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        # Update the room
        room_dict = {k: set_dict[k] for k in ArgList.room if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ArgList.room if k in where_dict}
        return self.apps.update_room(room_dict, where_clause_dict)

    def call_delete_room(self, param_dict):
        where_dict = param_dict['where']
        return self.apps.delete_room(where_dict)

    def call_add_staff(self, param_dict):
        set_dict = param_dict['set']

        # If a city and state is present, insert the new zip
        if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
            zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result

        # Insert the staff
        staff_dict = {k: set_dict[k] for k in ArgList.staff if k in set_dict}
        return self.apps.add_staff(staff_dict)

    def call_update_staff(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        # If a city and state is present, insert the new zip
        if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
            zip_dict = {k: set_dict[k] for k in ArgList.zip if k in set_dict}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result

        # Update the staff
        staff_dict = {k: set_dict[k] for k in ArgList.staff if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ArgList.staff if k in where_dict}
        return self.apps.update_staff(staff_dict, where_clause_dict)

    def call_delete_staff(self, param_dict):
        where_dict = param_dict['where']
        return self.apps.delete_staff(where_dict)

    def call_add_customer(self, param_dict):
        set_dict = param_dict['set']

        # If a city and state is present, insert the new zip
        if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
            zip_dict = {k: set_dict[k] for k in ('city', 'state', 'zip') if k in set_dict}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result

        # Insert the customer
        customer_dict = {k: set_dict[k] for k in ArgList.customer if k in set_dict}
        return self.apps.add_customer(customer_dict)

    def call_update_customer(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        # If a city and state is present, insert the new zip
        if 'zip' in set_dict and 'city' in set_dict and 'state' in set_dict:
            zip_dict = {k: set_dict[k] for k in ArgList.zip if k in set_dict}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result

        # Update the customer
        customer_dict = {k: set_dict[k] for k in ArgList.customer if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ArgList.customer if k in where_dict}
        return self.apps.update_customer(customer_dict, where_clause_dict)

    def call_delete_customer(self, param_dict):
        where_dict = param_dict['where']
        return self.apps.delete_customer(where_dict)

    def call_create_reservation(self, param_dict):
        set_dict = param_dict['set']

        # Insert the reservation
        reservation_dict = {k: set_dict[k] for k in ArgList.reservation if k in set_dict}
        return self.apps.add_reservation(reservation_dict)

    def call_update_reservation(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        # Update the reservation
        reservation_dict = {k: set_dict[k] for k in ArgList.reservation if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ArgList.reservation if k in where_dict}
        return self.apps.update_reservation(reservation_dict, where_clause_dict)

    def call_delete_reservation(self, param_dict):
        where_dict = param_dict['where']
        return self.apps.delete_reservation(where_dict)

    def call_check_in(self, param_dict):
        return 'Error - not yet implemented'

    def call_check_out(self, param_dict):
        return 'Error - not yet implemented'

    def call_assign_staff(self, param_dict):
        return 'Error - not yet implemented'

    def call_add_transaction(self, param_dict):
        set_dict = param_dict['set']

        # Insert the transaction
        transaction_dict = {k: set_dict[k] for k in ArgList.transaction if k in set_dict}
        return self.apps.add_transaction(transaction_dict)

    def call_update_transaction(self, param_dict):
        set_dict = param_dict['set']
        where_dict = param_dict['where']

        # Update the transaction
        transaction_dict = {k: set_dict[k] for k in ArgList.transaction if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ArgList.transaction if k in where_dict}
        return self.apps.update_transaction(transaction_dict, where_clause_dict)

    def call_delete_transaction(self, param_dict):
        where_dict = param_dict['where']
        return self.apps.delete_transaction(where_dict)

    def call_generate_bill(self, param_dict):
        return 'Error - not yet implemented'

    def call_occupancy_hotel(self, param_dict):
        query_dict = param_dict['set']

        return self.apps.report_occupancy_by_hotel(query_dict['query_date'])

    def call_occupancy_roomtype(self, param_dict):
        query_dict = param_dict['set']

        return self.apps.report_occupancy_by_room_type(query_dict['query_date'])

    def call_occupancy_city(self, param_dict):
        return 'Error - not yet implemented'

    def call_occupancy_date(self, param_dict):
        return 'Error - not yet implemented'

    def call_staff_report(self, param_dict):
        return 'Error - not yet implemented'

    def call_cust_inter(self, param_dict):
        return 'Error - not yet implemented'

    def call_revenue_hotel(self, param_dict):
        return 'Error - not yet implemented'

    def call_revenue_all(self, param_dict):
        return 'Error - not yet implemented'

    def call_cust_no_card(self, param_dict):
        return 'Error - not yet implemented'

    def call_pres_cust(self, param_dict):
        return 'Error - not yet implemented'

    def call_avail_hotel(self, param_dict):
        return 'Error - not yet implemented'

    def call_avail_roomtype(self, param_dict):
        return 'Error - not yet implemented'
