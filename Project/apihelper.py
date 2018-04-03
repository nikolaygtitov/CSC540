from apps import Apps
import pandas as pd


################################################################################
# Interface from UI to API
# - Edit this file to control interactions between UI and Apps
################################################################################
class APIHelper(object):
    def __init__(self, db):
        self.apps = Apps(db)
        self.db = db

    # Helper interfaces
    def call_add_hotel(self, param_dict, prerequisite=None):
        param_dict = param_dict['modify']
        if prerequisite:
            zip_dict = {k: param_dict[k] for k in ('city', 'state', 'zip')}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result
        else:
            zip_string = 'zip="%s"' % param_dict['zip']
            zip_present = self.apps.get_data_frame('*', 'ZipToCityState', zip_string)
            if len(zip_present) == 0:
                return {'message': 'City and state required.'}

        hotel_dict = {k: param_dict[k] for k in ('name', 'street', 'zip', 'phone_number')}
        return self.apps.add_hotel(hotel_dict)

    def call_update_hotel(self, param_dict, prerequisite=None):
        modify_dict = param_dict['modify']
        where_dict = param_dict['where']
        set_dict = {k:v for (k,v) in modify_dict.items() if v != None}
        where_dict = {k: v for (k, v) in where_dict.items() if v != None}
        if prerequisite:
            zip_dict = {k: modify_dict[k] for k in ('city', 'state', 'zip')}
            result = self.apps.add_zip(zip_dict)
            if not isinstance(result, pd.DataFrame):
                return result
        elif 'zip' in set_dict:
            zip_string = 'zip="%s"' % modify_dict['zip']
            zip_present = self.apps.get_data_frame('*', 'ZipToCityState', zip_string)
            if len(zip_present) == 0:
                return {'message': 'City and state required to update zip.'}

        hotel_dict = {k: set_dict[k] for k in ('id', 'name', 'street', 'zip', 'phone_number') if k in set_dict}
        where_clause_dict = {k: where_dict[k] for k in ('id', 'name', 'street', 'zip', 'phone_number') if k in where_dict}
        return self.apps.update_hotel(hotel_dict, where_clause_dict)

    def call_delete_hotel(self, param_dict):
        where_dict = param_dict['modify']
        return self.apps.delete_hotel(where_dict)
    def call_add_room(self, param_dict):
        return 'Error - not yet implemented'

    def call_update_room(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_room(self, param_dict):
        return 'Error - not yet implemented'

    def call_add_staff(self, param_dict):
        return 'Error - not yet implemented'

    def call_update_staff(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_staff(self, param_dict):
        return 'Error - not yet implemented'

    def call_add_customer(self, param_dict):
        return 'Error - not yet implemented'

    def call_update_customer(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_customer(self, param_dict):
        return 'Error - not yet implemented'

    def call_create_reservation(self, param_dict):
        return 'Error - not yet implemented'

    def call_update_reservation(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_reservation(self, param_dict):
        return 'Error - not yet implemented'

    def call_check_in(self, param_dict):
        return 'Error - not yet implemented'

    def call_check_out(self, param_dict):
        return 'Error - not yet implemented'

    def call_assign_staff(self, param_dict):
        return 'Error - not yet implemented'

    def call_add_transaction(self, param_dict):
        return 'Error - not yet implemented'

    def call_update_transaction(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_transaction(self, param_dict):
        return 'Error - not yet implemented'

    def call_generate_bill(self, param_dict):
        return 'Error - not yet implemented'

    def call_occupancy_hotel(self, param_dict):
        return 'Error - not yet implemented'

    def call_occupancy_roomtype(self, param_dict):
        return 'Error - not yet implemented'

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
