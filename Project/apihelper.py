from apps import Apps
import pandas as pd


################################################################################
# Interface from UI to API
# - Edit this file to control interactions between UI and Apps
################################################################################
class APIHelper(object):
    def __init__(self, db):
        self.apps = Apps(db)

    # Helper interfaces
    def call_add_hotel(self, param_dict):
        zip_dict = {x: param_dict[x] for x in ('zip', 'city', 'state')}
        hotel_dict = {x: param_dict[x] for x in ('name', 'street', 'zip',
                                                 'phone_number')}
        result1 = self.apps.add_zip(zip_dict)
        if isinstance(result1, pd.DataFrame):
            return self.apps.add_hotel(hotel_dict)
        else:
            return result1

    def call_update_hotel(self, param_dict):
        return 'Error - not yet implemented'

    def call_delete_hotel(self, param_dict):
        return 'Error - not yet implemented'

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
