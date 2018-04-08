import sys
import os
import pandas as pd
from tabulate import tabulate
import mysql.connector as maria_db
from appsclient import *
from util import print_error


################################################################################
# Template for Menus
# - Menus contain a table_name for reference, title/prompt for UI, and a list of
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
# - Queries have a table_name for reference, a title for the UI, an arglist for
# accepting input from the user, and an handler function that tells what to
# do when the item is selected.
# 
################################################################################
class MenuAction(object):
    def __init__(self, name, title, api_info, handler):
        self.name = name
        self.type = name.split('_')[0]
        self.title = title
        self.api_info = api_info
        self.handler = handler
# End of MenuAction class

################################################################################
# Hotel class which composes all other objects
# - Contains lists of menus, queries and their associated actions
# - Menus continue to loop until exit is selected
################################################################################
class HotelSoft(object):
    def __init__(self, hotel_name, db, check=False):
        self.client = AppsClient(db, check)
        self.hotel_name = hotel_name
        self.menu_list = []
        self.action_list = []
        self.db = db

    def add_menu(self, menu):
        self.menu_list.append(menu)

    def get_menu(self, name):
        return next(x for x in self.menu_list if x.name == name)

    def add_menu_action(self, query):
        self.action_list.append(query)

    def get_menu_action(self, name):
        return next(x for x in self.action_list if x.name == name)

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

    def run_query(self, action, last_menu):
        return lambda: self.get_inputs(self.get_menu_action(action), self.get_menu(
            last_menu))

    def get_inputs(self, action, last_menu):
        with print_error():
            # Dictionaries for housing query arguments
            set_dict = {}
            where_dict = {}

            print(action.title)

            # Update and delete queries build a "where" dictionary
            if action.type == 'update' or action.type == 'delete':
                found = False

                # Loop runs until user finds an item to update or delete
                while found == False:
                    if action.type == 'update':
                        print('\nWhich item do you want to update?')
                        print('Enter one or more fields to identify it.')
                    if action.type == 'delete':
                        print('\nWhich item do you want to delete?')
                        print('Enter one or more fields to identify it.')
                    print('<<Press enter to ignore a parameter>>\n')

                    # Enter one or more parameters to find the entry
                    for index, arg in enumerate(action.api_info.attr_names):
                        item = raw_input(arg + '(e.g. %s): ' % action.api_info.examples[index]).strip()
                        if item != '':
                            where_dict[arg] = item

                    # See if that item can be found
                    # If not, reprompt and try again
                    search_result = self.client.select(where_dict, action.api_info.table_name)
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
            if action.type == 'insert' or action.type == 'update' or action.type == 'report':
                if action.type == 'insert' or action.type == 'report':
                    print('Enter the following fields:')
                elif action.type == 'update':
                    print('\nEnter the new values for the fields you wish to update (set):')
                    print('(Press enter to ignore a parameter)')

                #Enter the normal parameters
                for index, arg in enumerate(action.api_info.attr_names):
                    item = raw_input(arg + '(e.g. %s): ' % action.api_info.examples[index]).strip()
                    if item != '':
                        set_dict[arg] = item

                # If a zip is entered, see if it is already present
                # If not, prompt for a city and state
                if 'zip' in set_dict:
                    zip_present = self.client.zip_is_present(set_dict['zip'])
                    if not zip_present:
                        print('City and state required')
                        for arg in action.api_info.secondary_args:
                            item = raw_input(arg + ': ').strip()
                            if item != '':
                                set_dict[arg] = item

            # Package up the set and where dictionaries and call api
            param_dict = {'set': set_dict, 'where': where_dict}
            result = action.handler(param_dict, action.api_info)

            print '\nMenuAction Successful ' + u"\u2713"
            self.db.commit()
            print tabulate(result, headers=result.columns.values.tolist(), tablefmt='psql')
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
    # Parse command line attr_names
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

    # Add menu actions with handler functions to be called when they execute
    # MenuAction(table_name, type, title, table, handler):
    wolf_inn.add_menu_action(
        MenuAction('insert_hotel', 'ADD A NEW HOTEL', AppsParams.hotels, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_hotel', 'UPDATE A HOTEL', AppsParams.hotels, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_hotel', 'DELETE A HOTEL', AppsParams.hotels, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_room', 'ADD A NEW ROOM TO A HOTEL', AppsParams.rooms, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_room', 'UPDATE A ROOM', AppsParams.rooms, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_room', 'DELETE A ROOM', AppsParams.rooms, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_staff', 'ADD A NEW STAFF MEMBER', AppsParams.staff, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_staff', 'UPDATE A STAFF MEMBER', AppsParams.staff, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_staff', 'DELETE A STAFF MEMBER', AppsParams.staff, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_customer', 'ADD A NEW CUSTOMER', AppsParams.customers, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_customer', 'UPDATE A CUSTOMER', AppsParams.customers, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_customer', 'DELETE A CUSTOMER', AppsParams.customers, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_res', 'ADD A NEW RESERVATION', AppsParams.reservations, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_res', 'UPDATE A RESERVATION', AppsParams.reservations, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_res', 'DELETE A RESERVATION', AppsParams.reservations, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_charge', 'APPLY A TRANSACTION TO A RESERVATION', AppsParams.transactions, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_charge', 'UPDATE A TRANSACTION', AppsParams.transactions, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_charge', 'DELETE A TRANSACTION', AppsParams.transactions, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('check_in', 'CHECK IN A GUEST', None, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('check_out', 'CHECK OUT A GUEST', None, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('assign_staff', 'ASSIGN STAFF TO A ROOM', None, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_gen_bill', 'GENERATE BILL', AppsParams.gen_bill, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_hotel', 'OCCUPANCY BY HOTEL', AppsParams.occ_hotel, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_room', 'OCCUPANCY BY ROOM TYPE', AppsParams.occ_room, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_city', 'OCCUPANCY BY CITY', AppsParams.occ_city, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_date', 'OCCUPANCY BY DATE', AppsParams.occ_date, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_list_staff', 'STAFF BY ROLE', AppsParams.list_staff, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_customer_inter', 'CUSTOMER INTERACTIONS', AppsParams.cust_inter, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_rev_hotel', 'REVENUE BY HOTEL', AppsParams.rev_hotel, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_rev_all', 'REVENUE FOR ALL HOTELS', AppsParams.rev_all, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_room_avail', 'ROOM AVAILABILITY', AppsParams.room_avail, wolf_inn.client.get_report_with_dict))

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
        MenuOption('Check room availability',
                   wolf_inn.run_query('report_room_avail', 'info')))
    wolf_inn.get_menu('info').add(
        MenuOption('Reservations / Check-ins / Check-outs',
                   wolf_inn.show_menu('reservations')))
    wolf_inn.get_menu('info').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add hotel menu options
    wolf_inn.get_menu('hotels').add(
        MenuOption('Enter a new hotel',
                   wolf_inn.run_query('insert_hotel', 'hotels')))
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
        MenuOption('Enter a new room', wolf_inn.run_query('insert_room', 'rooms')))
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
                   wolf_inn.run_query('insert_staff', 'staff')))
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
                   wolf_inn.run_query('insert_customer', 'customer')))
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
                   wolf_inn.run_query('insert_res', 'reservations')))
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
        MenuOption('Generate bill',
                   wolf_inn.run_query('report_gen_bill', 'billing')))
    wolf_inn.get_menu('billing').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Add reports menu options
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by hotel',
                   wolf_inn.run_query('report_occ_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by room type',
                   wolf_inn.run_query('report_occ_room', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by city',
                   wolf_inn.run_query('report_occ_city', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by date range',
                   wolf_inn.run_query('report_occ_date', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List staff by role',
                   wolf_inn.run_query('report_list_staff', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List customer interactions',
                   wolf_inn.run_query('report_customer_inter', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for a hotel',
                   wolf_inn.run_query('report_rev_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for all hotels',
                   wolf_inn.run_query('report_rev_all', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Back to main menu', wolf_inn.show_menu('main')))

    # Run the program
    wolf_inn.show_title_screen()
    wolf_inn.start('main')


if __name__ == "__main__":
    main()
