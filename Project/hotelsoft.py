import sys
import os
import pandas as pd
from tabulate import tabulate
import mysql.connector as maria_db
from apihelper import APIHelper
from apihelper import ArgList
from util import print_error


################################################################################
# Template for Menus
# - Menus contain a name for reference, title/prompt for UI, and a list of 
# options to choose from.
# - Options are formed from MenuOptions objects
################################################################################
class Menu(object):
    def __init__(self, name, title, prompt='Select a menu option:'):
        self.name = name
        self.title = title
        self.prompt = prompt
        self.options = []  # list of MenuOption objects

    def printm(self):
        print(self.title)
        print(self.prompt)
        for index, option in enumerate(self.options):
            print '  %s. %s' % (index + 1, option.title)

    def add(self, option):
        self.options.append(option)


# End of Menu class


################################################################################
# Template for MenuOptions
# - MenuOptions include a title for the UI and a handler function that
# tells what to do when the option is selected (either show another menu
# or run a query)
# 
################################################################################
class MenuOption(object):
    def __init__(self, title, handler):
        self.title = title
        self.handler = handler


# End of MenuOption class





################################################################################
# Template for Queries
# - Queries have a name for reference, a title for the UI, an arglist for 
# accepting input from the user, and an handler function that tells what to 
# do when the item is selected.
# 
################################################################################
class Query(object):
    def __init__(self, name, type, table, title, arg_list, handler, optional_args=None):
        self.name = name
        self.type = type
        self.table = table
        self.title = title
        self.arg_list = arg_list
        self.handler = handler
        self.optional_args = optional_args
# End of Query class


################################################################################
# Hotel class which composes all other objects
# - Contains lists of menus, queries and their associated actions
# - Menus continue to loop until exit is selected
################################################################################
class HotelSoft(object):
    def __init__(self, hotel_name, db, check=False):
        self.helper = APIHelper(db, check)
        self.hotel_name = hotel_name
        self.menu_list = []
        self.query_list = []
        self.db = db

    def add_menu(self, menu):
        self.menu_list.append(menu)

    def get_menu(self, name):
        return next(x for x in self.menu_list if x.name == name)

    def add_query(self, query):
        self.query_list.append(query)

    def get_query(self, name):
        return next(x for x in self.query_list if x.name == name)

    def show_title_screen(self):
        title_length = len(self.hotel_name)
        pad = (40 - title_length) / 2
        title_string = '|' + (' ' * pad) + self.hotel_name + (' ' * pad) + '|'
        os.system('clear')
        print('+----------------------------------------+')
        print('|                               __       |')
        print('|                             .d$$b      |')
        print('|                          .` TO$:\      |')
        print('|                         /  : TP._;     |')
        print('|                        / _.;  :Tb|     |')
        print('|                       /   /   ;j$j     |')
        print('|                   _.-"       d$$$$     |')
        print('|                 .` ..       d$$$$; .   |')
        print('|                /  /P`      d$$$$ . |\  |')
        print('|               /   "      .d$$$P  |\^`l |')
        print('|             ``           `T$P`"""""  : |')
        print('|         ._.`      _.`                ; |')
        print('|      `-.-".-`-` ._.       _.-"    .-"  |')
        print('|    `.-" _____  ._              .-      |')
        print('|   -(.g$$$$$$$b.              .`        |')
        print('|     ""^^T$$$P^)            .(:         |')
        print('|       _/  -"  /.`         /:/;         |')
        print('|    ._.`-``-`  ")/         /;/;         |')
        print('| `-.-"..--""   " /         /  ;         |')
        print('|.-" ..--""        -`          :         |')
        print('|..--""--.-"         (\      .-(\        |')
        print('+----------------------------------------|')
        print(title_string)
        print('|        HOTEL MANAGEMENT SYSTEM         |')
        print('|              version 1.0               |')
        print('+----------------------------------------+')
        print('|         --- Nathan Schnoor ---         |')
        print('|         --- Nikolay Titov  ---         |')
        print('|         --- Preston Scott  ---         |')
        print('+----------------------------------------+')

    def run_query(self, query, last_menu):
        return lambda: self.get_inputs(self.get_query(query), self.get_menu(
            last_menu))

    def get_inputs(self, query, last_menu):
        with print_error():
            # Dictionaries for housing query arguments
            set_dict = {}
            where_dict = {}

            print(query.title)

            # Update and delete queries build a "where" dictionary
            if query.type == 'update' or query.type == 'delete':
                found = False

                # Loop runs until user finds an item to update or delete
                while found == False:
                    if query.type == 'update':
                        print('\nWhich item do you want to update?')
                        print('Enter one or more fields to identify it.')
                    if query.type == 'delete':
                        print('\nWhich item do you want to delete?')
                        print('Enter one or more fields to identify it.')
                    print('<<Press enter to ignore a parameter>>\n')

                    # Enter one or more parameters to find the entry
                    for arg in query.arg_list:
                        item = raw_input(arg + ': ').strip()
                        if item != '':
                            where_dict[arg] = item

                    # See if that item can be found
                    # If not, reprompt and try again
                    search_result = self.helper.call_select(where_dict, query.table)
                    if len(search_result) == 1:
                        found = True
                        print('\n')
                        print tabulate(search_result,
                                       headers=search_result.columns.values.tolist(),
                                       tablefmt='psql')
                    elif len(search_result > 1):
                        found = True
                        print('\n')
                        print tabulate(search_result,
                                       headers=search_result.columns.values.tolist(),
                                       tablefmt='psql')
                        print('WARNING: multiple items will be updated')
                    else:
                        print('\nNo result found for %s' % where_dict)
                        print('Please try again')

            # Insert and update queries build a "set" dictionary
            if query.type == 'insert' or query.type == 'update':
                if query.type == 'insert':
                    print('Enter the following fields:')
                elif query.type == 'update':
                    print('\nEnter the new values for the fields you wish to update (set):')
                    print('(Press enter to ignore a parameter)')

                #Enter the normal parameters
                for arg in query.arg_list:
                    item = raw_input(arg + ': ').strip()
                    if item != '':
                        set_dict[arg] = item

                # If a zip is entered, see if it is already present
                # If not, prompt for a city and state
                if 'zip' in set_dict:
                    zip_present = self.helper.zip_is_present(set_dict['zip'])
                    if not zip_present:
                        print('City and state required')
                        for arg in query.optional_args:
                            item = raw_input(arg + ': ').strip()
                            if item != '':
                                set_dict[arg] = item

            # Package up the set and where dictionaries and call handler
            param_dict = {'set': set_dict, 'where': where_dict}
            result = query.handler(param_dict)

            print '\nQuery Successful ' + u"\u2713"
            self.db.commit()
            print tabulate(result, headers=result.columns.values.tolist(),
                           tablefmt='psql')
            print('\n')

        # Run the next menu
        self.get_choice(last_menu)

    def show_menu(self, menu):
        return lambda: self.get_choice(self.get_menu(menu))

    @staticmethod
    def get_choice(menu):
        menu.printm()
        choice = input('-> ')
        menu.options[choice - 1].handler()

    def start(self, menu):
        self.get_choice(self.get_menu(menu))

    @staticmethod
    def exit_program():
        print('Bye')
        sys.exit()


# end of HotelSoft class


################################################################################
# Build the hotel software and runs the program
################################################################################
def main():
    # Parse command line args
    check = False
    if len(sys.argv) == 2 and sys.argv[1] == '-c':
        check = True

    ###############################################################
    # Update database details with correct settings               #
    db = maria_db.connect(host='127.0.0.1',  #
                          user='pscott',  #
                          password='FK8bb"IAlgnYGT8;G!/gy|SQ~',  #
                          database='wolfinn')  #
    ###############################################################


    wolf_inn = HotelSoft('WOLF INN RALEIGH', db, check)

    # Add queries with lambda functions to be called when they are selected
    wolf_inn.add_query(
        Query('add_hotel',
              'insert',
              'Hotels',
              'ADD A NEW HOTEL',
              ArgList.hotel,
              lambda *args: wolf_inn.helper.call_add_hotel(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('update_hotel',
              'update',
              'Hotels',
              'UPDATE A HOTEL',
              ArgList.hotel,
              lambda *args: wolf_inn.helper.call_update_hotel(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('delete_hotel',
              'delete',
              'Hotels',
              'DELETE A HOTEL',
              ArgList.hotel,
              lambda *args: wolf_inn.helper.call_delete_hotel(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('add_room',
              'insert',
              'Rooms',
              'ADD A NEW ROOM TO A HOTEL',
              ArgList.room,
              lambda *args: wolf_inn.helper.call_add_room(*args)))
    wolf_inn.add_query(
        Query('update_room',
              'update',
              'Rooms',
              'UPDATE A ROOM',
              ArgList.room,
              lambda *args: wolf_inn.helper.call_update_room(*args)))
    wolf_inn.add_query(
        Query('delete_room',
              'delete',
              'Rooms',
              'DELETE A ROOM',
              ArgList.room,
              lambda *args: wolf_inn.helper.call_delete_room(*args)))
    wolf_inn.add_query(
        Query('add_staff',
              'insert',
              'Staff',
              'ADD A NEW STAFF MEMBER',
              ArgList.staff,
              lambda *args: wolf_inn.helper.call_add_staff(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('update_staff',
              'update',
              'Staff',
              'UPDATE A STAFF MEMBER',
              ArgList.staff,
              lambda *args: wolf_inn.helper.call_update_staff(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('delete_staff',
              'delete',
              'Staff',
              'DELETE A STAFF MEMBER',
              ArgList.staff,
              lambda *args: wolf_inn.helper.call_delete_staff(*args),
              ['city', 'state']))
    wolf_inn.add_query(
        Query('add_customer',
              'insert',
              'Customers',
              'ADD A NEW CUSTOMER',
              ArgList.customer,
              lambda *args: wolf_inn.helper.call_add_customer(*args)
              ['city', 'state']))
    wolf_inn.add_query(
        Query('update_customer',
              'update',
              'Customers',
              'UPDATE A CUSTOMER',
              ArgList.customer,
              lambda *args: wolf_inn.helper.call_update_customer(*args)
              ['city', 'state']))
    wolf_inn.add_query(
        Query('delete_customer',
              'delete',
              'Customers',
              'DELETE A CUSTOMER',
              ArgList.customer,
              lambda *args: wolf_inn.helper.call_delete_customer(*args)
              ['city', 'state']))
    wolf_inn.add_query(
        Query('add_res',
              'insert',
              'Reservations',
              'ADD A NEW RESERVATION',
              ArgList.reservation,
              lambda *args: wolf_inn.helper.call_create_reservation(*args)))
    wolf_inn.add_query(
        Query('update_res',
              'update',
              'Reservations',
              'UPDATE A RESERVATION',
              ArgList.reservation,
              lambda *args: wolf_inn.helper.call_update_reservation(*args)))
    wolf_inn.add_query(
        Query('delete_res',
              'delete',
              'Reservations',
              'DELETE A RESERVATION',
              ArgList.reservation,
              lambda *args: wolf_inn.helper.call_delete_reservation(*args)))
    wolf_inn.add_query(
        Query('check_in',
              None,
              None,
              'CHECK IN A GUEST',
              ['id'],  # reservation id
              lambda *args: wolf_inn.helper.call_update_reservation(*args)))
    wolf_inn.add_query(
        Query('check_out',
              None,
              None,
              'CHECK OUT A GUEST',
              ['id'],  # reservation id
              lambda *args: wolf_inn.helper.call_check_out(*args)))
    wolf_inn.add_query(
        Query('assign_staff',
              None,
              None,
              'ASSIGN STAFF TO A ROOM',
              ['id'],  # staff id
              lambda *args: wolf_inn.helper.call_assign_staff(*args)))
    wolf_inn.add_query(
        Query('add_charge',
              'insert',
              'Transactions',
              'APPLY A TRANSACTION TO A RESERVATION',
              ArgList.transaction,
              lambda *args: wolf_inn.helper.call_add_transaction(*args)))
    wolf_inn.add_query(
        Query('update_charge',
              'update',
              'Transactions',
              'UPDATE A TRANSACTION',
              ArgList.transaction,
              lambda *args: wolf_inn.helper.call_update_transaction(*args)))
    wolf_inn.add_query(
        Query('delete_charge',
              'delete',
              'Transactions',
              'DELETE A TRANSACTION',
              ArgList.transaction,
              lambda *args: wolf_inn.helper.call_delete_transaction(*args)))
    wolf_inn.add_query(
        Query('gen_bill',
              'GENERATE BILL',
              None,
              None,
              ['id'],
              lambda *args: wolf_inn.helper.call_generate_bill(*args)))
    wolf_inn.add_query(
        Query('occ_hotel',
              None,
              None,
              'OCCUPANCY BY HOTEL',
              [],
              lambda *args: wolf_inn.helper.call_occupancy_hotel(*args)))
    wolf_inn.add_query(
        Query('occ_room',
              None,
              None,
              'OCCUPANCY BY ROOM TYPE',
              [],
              lambda *args: wolf_inn.helper.call_occupancy_roomtype(*args)))
    wolf_inn.add_query(
        Query('occ_city',
              None,
              None,
              'OCCUPANCY BY CITY',
              [],
              lambda *args: wolf_inn.helper.call_occupancy_city(*args)))
    wolf_inn.add_query(
        Query('occ_date',
              None,
              None,
              'OCCUPANCY BY DATE',
              ['start_date', 'end_date'],
              lambda *args: wolf_inn.helper.call_occupancy_date(*args)))
    wolf_inn.add_query(
        Query('list_staff',
              None,
              None,
              'STAFF BY ROLE',
              [],
              lambda *args: wolf_inn.helper.call_staff_report(*args)))
    wolf_inn.add_query(
        Query('customer_inter',
              None,
              None,
              'CUSTOMER INTERACTIONS',
              ['id'],
              lambda *args: wolf_inn.helper.call_cust_inter(*args)))
    wolf_inn.add_query(
        Query('rev_hotel',
              None,
              None,
              'REVENUE BY HOTEL',
              ['id'],  # hotel_id
              lambda *args: wolf_inn.helper.call_revenue_hotel(*args)))
    wolf_inn.add_query(
        Query('rev_all',
              None,
              None,
              'REVENUE FOR ALL HOTELS',
              [],
              lambda *args: wolf_inn.helper.call_revenue_all(*args)))
    wolf_inn.add_query(
        Query('customer_no_card',
              None,
              None,
              'CUSTOMERS WITH NO HOTEL CREDIT CARD',
              [],
              lambda *args: wolf_inn.helper.call_cust_no_card(*args)))
    wolf_inn.add_query(
        Query('pres_customer',
              None,
              None,
              'CURRENT PRESIDENTIAL CUSTOMERS',
              [],
              lambda *args: wolf_inn.helper.call_pres_cust(*args)))
    wolf_inn.add_query(
        Query('room_avail1',
              None,
              None,
              'ROOM AVAILABILITY BY HOTEL',
              ['id'],  # hotel id
              lambda *args: wolf_inn.helper.call_avail_hotel(*args)))
    wolf_inn.add_query(
        Query('room_avail2',
              None,
              None,
              'ROOM AVAILABILITY BY HOTEL AND ROOM TYPE',
              ['id'],
              lambda *args: wolf_inn.helper.call_avail_roomtype(*args)))

    # Add main menus
    wolf_inn.add_menu(Menu('main', 'MAIN MENU'))
    wolf_inn.add_menu(Menu('info', 'INFORMATION PROCESSING'))
    wolf_inn.add_menu(Menu('service', 'SERVICE RECORDS'))
    wolf_inn.add_menu(Menu('billing', 'BILLING'))
    wolf_inn.add_menu(Menu('reports', 'REPORTS'))
    wolf_inn.add_menu(Menu('hotels', 'MANAGE HOTEL INFORMATION'))
    wolf_inn.add_menu(Menu('rooms', 'MANAGE ROOM INFORMATION'))
    wolf_inn.add_menu(Menu('staff', 'MANAGE STAFF INFORMATION'))
    wolf_inn.add_menu(Menu('customer', 'MANAGE CUSTOMER INFORMATION'))
    wolf_inn.add_menu(Menu('reservations', 'RESERVATIONS'))

    # Add main menu options
    wolf_inn.get_menu('main').add(
        MenuOption('Information Processing', wolf_inn.show_menu('info')))
    wolf_inn.get_menu('main').add(
        MenuOption('Service Records', wolf_inn.show_menu('service')))
    wolf_inn.get_menu('main').add(
        MenuOption('Billing', wolf_inn.show_menu('billing')))
    wolf_inn.get_menu('main').add(
        MenuOption('Reports', wolf_inn.show_menu('reports')))
    wolf_inn.get_menu('main').add(MenuOption('Exit', wolf_inn.exit_program))

    # Add information management menu options
    wolf_inn.get_menu('info').add(
        MenuOption('Manage hotel information', wolf_inn.show_menu('hotels')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage room information', wolf_inn.show_menu('rooms')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage staff information', wolf_inn.show_menu('staff')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage customer information',
                   wolf_inn.show_menu('customer')))
    wolf_inn.get_menu('info').add(
        MenuOption('Check room availability by hotel',
                   wolf_inn.run_query('room_avail1', 'info')))
    wolf_inn.get_menu('info').add(
        MenuOption('Check room availability by room type',
                   wolf_inn.run_query('room_avail2', 'info')))
    wolf_inn.get_menu('info').add(
        MenuOption('Reservations / Check-ins / Check-outs',
                   wolf_inn.show_menu('reservations')))
    wolf_inn.get_menu('info').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add hotel menu options
    wolf_inn.get_menu('hotels').add(
        MenuOption('Enter a new hotel',
                   wolf_inn.run_query('add_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Update a hotel',
                   wolf_inn.run_query('update_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Delete a hotel',
                   wolf_inn.run_query('delete_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Return to previous menu', wolf_inn.show_menu('info')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add room menu options
    wolf_inn.get_menu('rooms').add(
        MenuOption('Enter a new room', wolf_inn.run_query('add_room', 'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Update a room', wolf_inn.run_query('update_room', 'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Delete a room', wolf_inn.run_query('delete_room', 'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Return to previous menu', wolf_inn.show_menu('info')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add staff menu options
    wolf_inn.get_menu('staff').add(
        MenuOption('Enter a new staff member',
                   wolf_inn.run_query('add_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Update a staff member',
                   wolf_inn.run_query('update_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Delete a staff member',
                   wolf_inn.run_query('delete_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Return to previous menu',
                   wolf_inn.show_menu('info')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add customer menu options
    wolf_inn.get_menu('customer').add(
        MenuOption('Enter a new customer',
                   wolf_inn.run_query('add_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Update a customer',
                   wolf_inn.run_query('update_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Delete a customer',
                   wolf_inn.run_query('delete_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Return to previous menu', wolf_inn.show_menu('info')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add reservation menu options
    wolf_inn.get_menu('reservations').add(
        MenuOption('Make a reservation',
                   wolf_inn.run_query('add_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Update a reservation',
                   wolf_inn.run_query('update_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Delete a reservation',
                   wolf_inn.run_query('delete_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Assign a room (check-in)',
                   wolf_inn.run_query('check_in', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Release a room (check-out)',
                   wolf_inn.run_query('check_out', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Assign staff to room',
                   wolf_inn.run_query('assign_staff', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Return to previous menu', wolf_inn.show_menu('info')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add service menu options
    wolf_inn.get_menu('service').add(
        MenuOption('Add a service charge',
                   wolf_inn.run_query('add_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Update a service charge',
                   wolf_inn.run_query('update_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Delete a service charge',
                   wolf_inn.run_query('delete_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add billing menu options
    wolf_inn.get_menu('billing').add(
        MenuOption('Generate bill', wolf_inn.run_query('gen_bill', 'billing')))
    wolf_inn.get_menu('billing').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add reports menu options
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by hotel',
                   wolf_inn.run_query('occ_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by room type',
                   wolf_inn.run_query('occ_room', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by city',
                   wolf_inn.run_query('occ_city', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by date range',
                   wolf_inn.run_query('occ_date', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List staff by role',
                   wolf_inn.run_query('list_staff', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List customer interactions',
                   wolf_inn.run_query('customer_inter', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for a hotel',
                   wolf_inn.run_query('rev_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for all hotels',
                   wolf_inn.run_query('rev_all', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Customers Without Credit Cards',
                   wolf_inn.run_query('customer_no_card', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List Presidential Customers',
                   wolf_inn.run_query('pres_customer', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))





    # Run the program
    wolf_inn.show_title_screen()
    wolf_inn.start('main')





if __name__ == "__main__":
    main()
