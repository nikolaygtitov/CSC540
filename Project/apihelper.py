from apps import Apps
import pandas as pd

class APIHelper(object):
    def __init__(self, db):
        self.apps = Apps(db)

    ### Helper interfaces
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
    def call_delete_hotel(param_dict):
        return 'Error - not yet implemented' 
    def call_add_room(param_dict):
        return 'Error - not yet implemented' 
    def call_update_room(param_dict):
        return 'Error - not yet implemented' 
    def call_delete_room(param_dict):
        return 'Error - not yet implemented'
    def call_add_staff(param_dict):
        return 'Error - not yet implemented'
    def call_update_staff(param_dict):
        return 'Error - not yet implemented'
    def call_delete_staff(param_dict):
        return 'Error - not yet implemented'
    def call_add_customer(param_dict):
        return 'Error - not yet implemented'
    def call_update_customer(param_dict):        
        return 'Error - not yet implemented'
    def call_delete_customer(param_dict):
        return 'Error - not yet implemented'
    def call_create_reservation(param_dict):
        return 'Error - not yet implemented'
    def call_update_reservation(param_dict):
        return 'Error - not yet implemented'
    def call_delete_reservation(param_dict):
        return 'Error - not yet implemented'
    def call_check_out(param_dict):
        return 'Error - not yet implemented'
    def call_check_out(param_dict):
        return 'Error - not yet implemented'
    def call_assign_staff(param_dict):
        return 'Error - not yet implemented'
    def call_add_transaction(param_dict):
        return 'Error - not yet implemented'
    def call_update_transaction(param_dict):
        return 'Error - not yet implemented'
    def call_delete_transaction(param_dict):
        return 'Error - not yet implemented'
    def call_generate_bill(param_dict):
        return 'Error - not yet implemented'
    def call_occupancy_hotel(param_dict):
        return 'Error - not yet implemented'
    def call_occupancy_roomtype(param_dict):
        return 'Error - not yet implemented'
    def call_occupancy_city(param_dict):
        return 'Error - not yet implemented'
    def call_occupancy_date(param_dict):
        return 'Error - not yet implemented'
    def call_staff_report(param_dict):
        return 'Error - not yet implemented'
    def call_cust_inter(param_dict):
        return 'Error - not yet implemented'
    def call_revenue_hotel(param_dict):
        return 'Error - not yet implemented'
    def call_revenue_all(param_dict):
        return 'Error - not yet implemented'
    def call_cust_no_card(param_dict):
        return 'Error - not yet implemented'
    def call_pres_cust(param_dict):
        return 'Error - not yet implemented'
    def call_avail_hotel(param_dict):
        return 'Error - not yet implemented'
    def call_avail_roomtype(param_dict):
        return 'Error - not yet implemented'