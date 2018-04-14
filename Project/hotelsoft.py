"""
hotelsoft.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540
This program implements the solution for the main Project assignment:

The design and development processes of Database Management System for WolfInns
are completed in the Project Report 1 and Project Report 2.

Description of the Project:
The Popular Hotel Chain database system is designed and built to manage and
maintain information of hotels, rooms, staff, and customers, including but not
limited to storing, updating, and deleting data. The database maintains a
variety of information records about hotels located in various cities around
the country, including staff, rooms, customers, and billing records.
For each customer stay it maintains service records, such as phone bills, dry
cleaning, gyms, room service, and special requests. It generates and maintains
billing accounts for each customer stay. It generates report occupancy by
hotel, room category, date range, and city.
The database system is developed for Wolf Inns and is used by hotels operators
and employees including management staff, front desk representatives, room
service, billing, and catering staff.
The Popular Hotel Chain database system resolves constraints on availability
and pricing of rooms, maintaining proper customer, billing, check-in, and
check-out information. Users of the database may perform different tasks
concurrently, each consisting of multiple sequential operations that have an
affect on the database.
There are four major tasks that are performed by corresponding users on the
database:
    1. Information Processing
    2. Maintaining Service Records
    3. Maintaining Billing Accounts
    4. Reports

Description of the Software:
This program allows retrieving, storing, manipulating and deleting any data
from the DBMS through various user-friendly applications instead of direct
interaction with MariaDB MySQL server via MySQL queries, such as SELECT,
INSERT, UPDATE, and DELETE.
The architecture of the software is designed as follows:
+---------------+     +---------------+    +-------------+     +------------+
|      UI       |     |    Client     |    |    APIs     |     |  DATABASE  |
|  hotelsoft.py | ->  | appsclient.py | -> |   apps.py   |  -> |   MariaDB  |
+---------------+     +---------------+    +-------------+     +------------+

The entire front-end interaction between a user and the program takes place via
UI, which is a menu driven system that enables interaction with the back-end
database.

The following is a sample of menu driven system of the implemented UI:

Here the output of UI

The program is written without any security constraints, such as user
permissions and others. All the data is fully retrievable from the MariaDB
MySQL regardless permissions.

Description of the hotelsoft.py file:
This is the main file that gets executed from the prompt by a user to initiate
the program. It connects to the NCSU MySQL MariaDB Server as specified in the
default MySQL settings/parameters in the code. In order to connect to different
database, please consider changing the following default database parameters
in the code:

db = maria_db.connect(host=DESIRED_HOST, user=USER_NAME,
                      password=PASSWORD, database=DATABASE)

This file contains the classes comprising the user interface for the WolfInn
Database Management System. The UI is a menu driven system that enables
interaction with the backend database.
The UI functions communicate with the Apps API through a Client class which
aggregates common functionality.

To execute the program run:
 > python hotesoft.py [-options]

   OPTIONS
   -c: run in check mode (USE SQL CHECK functionality)

@version: 1.0
@todo: Demo
@since: April 8, 2018
@status: Complete
@requires: Connection to MariaDB server at the NCSU. If default database
           parameters are changed, ignore both options below (unless DBMS used
           is at the NCSU MySQL Server).
           Option 1: Establish connection through NCSU VPN.
                     Installation of Cisco AnyConnect VPN Software is required.
                     Installation instructions of Cisco AnyConnect can be
                     found here:
https://oit.ncsu.edu/campus-it/campus-data-network/network-security/vpn/

           Option 2: Pull or copy source code to the NCSU remote machine and
                     run it there:
scp * unity_id@remote.eos.ncsu.edu:/afs/unity.ncsu.edu/users/u/unity_id/CSC540
@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu
@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott
"""

import sys
import os
from tabulate import tabulate
import mysql.connector as maria_db
from appsclient import *
from util import print_error
from demo_data import load_demo_data


################################################################################
# Menu Class                                                                   #
################################################################################
class Menu(object):
    """
    Template for menu objects which will comprise the menu system.
    Menu options are the sub-items for each parent menu that respond to
    selection. Menu options must be MenuOption objects.
    """

    def __init__(self, name, title, prompt='Select a menu option:'):
        """
        Instantiates a new menu
        Parameters:
            :param name: String identifier of menu for lookup
            :param title: Text to be printed at top of menu
            :param prompt: Text prompt for menu (override if necessary)
        Returns:
            :return: new Menu object
        """
        self.name = name
        self.title = title
        self.prompt = prompt
        self.options = []  # list of MenuOption objects

    def printm(self):
        """ Prints the menu to screen """
        print(self.title)
        print(self.prompt)
        for index, option in enumerate(self.options):
            print '  %s. %s' % (index + 1, option.title)

    def add(self, option):
        """
        Adds a new MenuOption object to Menu.options
        Parameters:
            :param option: MenuOption object to add
        """
        self.options.append(option)


# End of Menu class


################################################################################
# MenuOption Class                                                             #
################################################################################
class MenuOption(object):
    """
    Template for menu options (sub-items in a menu that respond to selection)
    """

    def __init__(self, title, handler):
        """
        Instantiate a new MenuOption
        Parameters:
            :param title: Text description to print to screen
            :param handler: Function to call when option is selected
        Returns:
            :return: new MenuOption object
        """
        self.title = title
        self.handler = handler


# End of MenuOption class

################################################################################
# MenuAction Class                                                             #
################################################################################
class MenuAction(object):
    """
    Template for menu actions (callable functions to be embedded in menu options
    """

    def __init__(self, name, title, api_info, handler):
        """
        Instantiate a new MenuAction
        Parameters:
            :param name: String identifier of menu for lookup
            :param title: Text description to print to screen
            :param api_info: Summary of fields required for API calls
            :param handler: Function to call when option is selected
        Returns:
            :return: new MenuAction object
        """
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
    """
    Main program - to be instantiated with custom options
    """

    def __init__(self, hotel_name, db, check=False):
        """
        Instantiate a new software instance
        Parameters:
            :param hotel_name: Text name of hotel to be printed to screen
            :param db: An initialized mysql.connector instance
            :param check: Boolean flag indicating whether to run SQL CHECKS
            menu_list: Empty list to house main menus
            action_list: Empty list to house available actions for menus
        Returns:
            :return: new HotelSoft object
        """
        self.client = AppsClient(db, check)
        self.hotel_name = hotel_name
        self.menu_list = []
        self.action_list = []
        self.db = db

    def add_menu(self, menu):
        """
        Adds a main menu node to the instance. Note: only use this for main
        menus.  Submenus should be added to their parents' options lists.
        Parameters:
            :param menu: Menu object to add
        """
        self.menu_list.append(menu)

    def get_menu(self, name):
        """
        Returns the menu with the given string identifier
        Parameters:
            :param name: string identifier for menu
        Returns:
            :return: Menu of interest
        """
        return next(x for x in self.menu_list if x.name == name)

    def add_menu_action(self, action):
        """
        Adds a new menu action to the instance
        Parameters:
            :param action: MenuAction object to add
        """
        self.action_list.append(action)

    def get_menu_action(self, name):
        """
        Returns the menu action with the given string identifier
        Parameters:
            :param name: string identifier for menu action
        Returns:
            :return: MenuAction of interest
        """
        return next(x for x in self.action_list if x.name == name)

    def show_title_screen(self):
        """ Displays splash screen at startup """
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

    def store_action(self, action, last_menu):
        """
        Stores an action and menu in a lambda function to be run later
        Parameters:
            :param action: Menu action of interest
            :param last_menu: Menu to revert to on fail or finish of action
        Returns:
            :return: Lambda function associated with action
        """
        return lambda: self.get_inputs(self.get_menu_action(action),
                                       self.get_menu(last_menu))

    def get_inputs(self, action, last_menu):
        """
        Displays prompts and captures inputs for all fields related to
        an action.
        Reverts to last_menu on fail or finish
        Parameters:
            :param action: Menu action of interest
            :param last_menu: Menu to revert to on fail or finish of action
        """
        with print_error():
            # Dictionaries for housing query arguments
            set_dict = {}
            where_dict = {}

            print(action.title)

            # Update and delete queries build a "where" dictionary
            if action.type == 'update' or action.type == 'delete':

                preview_table = self.client.select(None,
                                                   action.api_info.table_name)
                if isinstance(preview_table, pd.DataFrame):
                    print tabulate(
                        preview_table,
                        headers=preview_table.columns.values.tolist(),
                        tablefmt='psql')

                number_found = 0

                # Loop runs until user finds an item to update or delete
                while number_found == 0:
                    if action.type == 'update':
                        print('\nWhich item do you want to update?')
                        print('Enter one or more fields to identify it.')
                    if action.type == 'delete':
                        print('\nWhich item do you want to delete?')
                        print('Enter one or more fields to identify it.')
                    print('<<Press enter to ignore a parameter>>\n')

                    search_result = []

                    # Enter one or more parameters to find the entry
                    for index, arg in enumerate(
                            action.api_info.attr_names['where']):
                        example = '(%s)' % \
                                  action.api_info.examples['where'][index]
                        val = (arg in where_dict and '[%s]' % where_dict[arg]
                               or '')
                        item = raw_input(
                            ('%s %s %s' % (arg, example, val)).strip() + ': ').\
                            strip()
                        if item != '':
                            where_dict[arg] = item
                        # Try to find row - we may be able to end early
                        search_result = self.client.select(
                            where_dict, action.api_info.table_name)
                        number_found = len(search_result)
                        if number_found <= 1:
                            break
                    # See if that item can be found
                    # If not, re-prompt and try again
                    if number_found > 0:
                        print('\n')
                        print tabulate(
                            search_result,
                            headers=search_result.columns.values.tolist(),
                            tablefmt='psql')
                        if number_found > 1:
                            continue_filter = not raw_input(
                                'Multiple items found. Continue to filter? '
                                '(y/n): ').lower().startswith('n')
                            if continue_filter:
                                number_found = 0
                    else:
                        print('\nNo result found for %s' % where_dict)
                        print('Please try again')
                        where_dict = {}

                if number_found > 1:
                    print('WARNING: multiple items will be %sd' % action.type)

            # Insert and update queries build a "set" dictionary
            if action.type == 'insert' or action.type == 'update' or \
                    action.type == 'report':
                if action.type == 'insert' or action.type == 'report':
                    print('Enter the following fields:')
                elif action.type == 'update':
                    print('\nEnter the new values for the fields you ' +
                          'wish to update (set):')
                    print('(Press enter to ignore a parameter)')

                # Enter the normal parameters
                for index, arg in enumerate(action.api_info.attr_names['set']):
                    item = raw_input(
                        arg + '(%s): ' %
                        action.api_info.examples['set'][index]).strip()
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

            # Need this to execute actions with no arguments
            # i.e. no arguments to pass, nothing to print
            results = None
            if action.type == 'exec':
                action.handler()
            else:
                results = action.handler(param_dict, action.api_info)
            print '\nMenuAction Successful ' + u"\u2713"
            if isinstance(results, list):
                for result in results:
                    print tabulate(result,
                                   headers=result.columns.values.tolist(),
                                   tablefmt='psql')
            else:
                print tabulate(results,
                               headers=results.columns.values.tolist(),
                               tablefmt='psql')
            print('\n')

        # Run the next menu
        self.get_choice(last_menu)

    def store_menu(self, menu):
        """
        Stores a menu in a lambda function to be run later.

        Parameters:
            :param menu: Menu of interest

        Returns:
            :return: Lambda function associated with menu
        """
        return lambda: self.get_choice(self.get_menu(menu))

    @staticmethod
    def get_choice(menu):
        """
        Show the given Menu and get input
        Parameters:
            :param menu: Menu of interest
        """
        menu.printm()
        try:
            choice = int(raw_input('-> '))
            if choice < 1 or choice > len(menu.options):
                raise ValueError('Out of range')
        except ValueError:
            print('Invalid input')
            return HotelSoft.get_choice(menu)
        menu.options[choice - 1].handler()

    def start(self, menu):
        self.get_choice(self.get_menu(menu))

    @staticmethod
    def exit_program():
        """ Exits the program """
        print('Bye')
        sys.exit()


# end of HotelSoft class

################################################################################
# Initialize database
################################################################################
def get_db():
    """
    Helper function for initializing the mysql.connector database
    """
    try:
        db_choice = int(raw_input('\nEnter database settings manually (1) or ' +
                                  'use default (2): '))
        if db_choice < 1 or db_choice > 2:
            raise ValueError('Out of range')
    except ValueError:
        print('Invalid input')
        return get_db()
    if db_choice == 1:
        try:
            host = raw_input('Enter hostname/ip for database: ')
            user = raw_input('Enter username: ')
            password = raw_input('Enter password: ')
            database = raw_input('Enter database: ')
            db = maria_db.connect(host=host, user=user, password=password,
                                  database=database)
            return db
        except maria_db.Error:
            print ('Unable to establish database connection')
            return get_db()
    else:
        try:
            # ###############################################################
            # # Default database settings                                   #
            # db = maria_db.connect(host='classdb2.csc.ncsu.edu',           #
            #                       user='ngtitov',                         #
            #                       password='001029047',                   #
            #                       database='ngtitov')                     #
            # ###############################################################
            # db = maria_db.connect(host='classdb2.csc.ncsu.edu',
            #                       user='pdscott2',
            #                       password='2CGxZg27R3utum',
            #                       database='pdscott2')
            db = maria_db.connect(host='classdb2.csc.ncsu.edu',
                                  user='nfschnoo',
                                  password='001027748',
                                  database='nfschnoo')
            return db
        except maria_db.Error:
            print ('Unable to establish database connection')
            return get_db()


################################################################################
# Build the hotel software and run the program
################################################################################
def main():
    # Parse command line attr_names
    check = False
    if len(sys.argv) == 2 and sys.argv[1] == '-c':
        check = True

    # Init database
    db = get_db()

    # Init main software instance
    wolf_inn = HotelSoft('WOLF INN RALEIGH', db, check)

    # Add menu actions with handler functions to be called when they execute
    # MenuAction(table_name, type, title, table, handler):
    wolf_inn.add_menu_action(
        MenuAction('insert_hotel', 'ADD A NEW HOTEL', AppsParams.hotels,
                   wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_hotel', 'UPDATE A HOTEL', AppsParams.hotels,
                   wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_hotel', 'DELETE A HOTEL', AppsParams.hotels,
                   wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_room', 'ADD A NEW ROOM TO A HOTEL',
                   AppsParams.rooms, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_room', 'UPDATE A ROOM', AppsParams.rooms,
                   wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_room', 'DELETE A ROOM', AppsParams.rooms,
                   wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_staff', 'ADD A NEW STAFF MEMBER', AppsParams.staff,
                   wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_staff', 'UPDATE A STAFF MEMBER', AppsParams.staff,
                   wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_staff', 'DELETE A STAFF MEMBER', AppsParams.staff,
                   wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_customer', 'ADD A NEW CUSTOMER',
                   AppsParams.customers, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_customer', 'UPDATE A CUSTOMER',
                   AppsParams.customers, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_customer', 'DELETE A CUSTOMER',
                   AppsParams.customers, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_res', 'ADD A NEW RESERVATION',
                   AppsParams.reservations, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_res', 'UPDATE A RESERVATION',
                   AppsParams.reservations, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_res', 'DELETE A RESERVATION',
                   AppsParams.reservations, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('insert_charge', 'APPLY A TRANSACTION TO A RESERVATION',
                   AppsParams.transactions, wolf_inn.client.insert))
    wolf_inn.add_menu_action(
        MenuAction('update_charge', 'UPDATE A TRANSACTION',
                   AppsParams.transactions, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('delete_charge', 'DELETE A TRANSACTION',
                   AppsParams.transactions, wolf_inn.client.delete))
    wolf_inn.add_menu_action(
        MenuAction('update_check_in', 'CHECK IN A GUEST',
                   AppsParams.check_in, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('update_check_out', 'CHECK OUT A GUEST',
                   AppsParams.check_out, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('update_assign_staff', 'ASSIGN STAFF TO A ROOM',
                   AppsParams.staff, wolf_inn.client.update))
    wolf_inn.add_menu_action(
        MenuAction('report_gen_bill', 'GENERATE BILL',
                   AppsParams.gen_bill, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_hotel', 'OCCUPANCY BY HOTEL',
                   AppsParams.occ_hotel, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_room', 'OCCUPANCY BY ROOM TYPE',
                   AppsParams.occ_room, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_city', 'OCCUPANCY BY CITY',
                   AppsParams.occ_city, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_occ_date', 'OCCUPANCY BY DATE',
                   AppsParams.occ_date, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_list_staff', 'STAFF BY ROLE',
                   AppsParams.list_staff, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_customer_inter', 'CUSTOMER INTERACTIONS',
                   AppsParams.cust_inter, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_rev_hotel', 'REVENUE BY HOTEL',
                   AppsParams.rev_hotel, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_rev_all', 'REVENUE FOR ALL HOTELS',
                   AppsParams.rev_all, wolf_inn.client.get_report))
    wolf_inn.add_menu_action(
        MenuAction('report_room_avail', 'ROOM AVAILABILITY',
                   AppsParams.room_avail, wolf_inn.client.get_report_with_dict))
    wolf_inn.add_menu_action(
        MenuAction('exec_demo_load', 'LOAD DEMO DATA',
                   None, lambda: load_demo_data(db)))
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
        MenuOption('Information Processing', wolf_inn.store_menu('info')))
    wolf_inn.get_menu('main').add(
        MenuOption('Service Records', wolf_inn.store_menu('service')))
    wolf_inn.get_menu('main').add(
        MenuOption('Billing', wolf_inn.store_menu('billing')))
    wolf_inn.get_menu('main').add(
        MenuOption('Reports', wolf_inn.store_menu('reports')))
    wolf_inn.get_menu('main').add(
        MenuOption('Load Test Data',
                   wolf_inn.store_action('exec_demo_load', 'main')))
    wolf_inn.get_menu('main').add(MenuOption('Exit', wolf_inn.exit_program))

    # Add information management menu options
    wolf_inn.get_menu('info').add(
        MenuOption('Manage hotel information', wolf_inn.store_menu('hotels')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage room information', wolf_inn.store_menu('rooms')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage staff information', wolf_inn.store_menu('staff')))
    wolf_inn.get_menu('info').add(
        MenuOption('Manage customer information',
                   wolf_inn.store_menu('customer')))
    wolf_inn.get_menu('info').add(
        MenuOption('Check room availability',
                   wolf_inn.store_action('report_room_avail', 'info')))
    wolf_inn.get_menu('info').add(
        MenuOption('Reservations / Check-ins / Check-outs',
                   wolf_inn.store_menu('reservations')))
    wolf_inn.get_menu('info').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add hotel menu options
    wolf_inn.get_menu('hotels').add(
        MenuOption('Enter a new hotel',
                   wolf_inn.store_action('insert_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Update a hotel',
                   wolf_inn.store_action('update_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Delete a hotel',
                   wolf_inn.store_action('delete_hotel', 'hotels')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Return to previous menu', wolf_inn.store_menu('info')))
    wolf_inn.get_menu('hotels').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add room menu options
    wolf_inn.get_menu('rooms').add(
        MenuOption('Enter a new room', wolf_inn.store_action('insert_room',
                                                             'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Update a room', wolf_inn.store_action('update_room',
                                                          'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Delete a room', wolf_inn.store_action('delete_room',
                                                          'rooms')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Return to previous menu', wolf_inn.store_menu('info')))
    wolf_inn.get_menu('rooms').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add staff menu options
    wolf_inn.get_menu('staff').add(
        MenuOption('Enter a new staff member',
                   wolf_inn.store_action('insert_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Update a staff member',
                   wolf_inn.store_action('update_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Delete a staff member',
                   wolf_inn.store_action('delete_staff', 'staff')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Return to previous menu',
                   wolf_inn.store_menu('info')))
    wolf_inn.get_menu('staff').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add customer menu options
    wolf_inn.get_menu('customer').add(
        MenuOption('Enter a new customer',
                   wolf_inn.store_action('insert_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Update a customer',
                   wolf_inn.store_action('update_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Delete a customer',
                   wolf_inn.store_action('delete_customer', 'customer')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Return to previous menu', wolf_inn.store_menu('info')))
    wolf_inn.get_menu('customer').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add reservation menu options
    wolf_inn.get_menu('reservations').add(
        MenuOption('Make a reservation',
                   wolf_inn.store_action('insert_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Update a reservation',
                   wolf_inn.store_action('update_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Delete a reservation',
                   wolf_inn.store_action('delete_res', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Assign a room (check-in)',
                   wolf_inn.store_action('update_check_in', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Release a room (check-out)',
                   wolf_inn.store_action('update_check_out', 'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Assign staff to room',
                   wolf_inn.store_action('update_assign_staff',
                                         'reservations')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Return to previous menu', wolf_inn.store_menu('info')))
    wolf_inn.get_menu('reservations').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add service menu options
    wolf_inn.get_menu('service').add(
        MenuOption('Add a service charge',
                   wolf_inn.store_action('insert_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Update a service charge',
                   wolf_inn.store_action('update_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Delete a service charge',
                   wolf_inn.store_action('delete_charge', 'service')))
    wolf_inn.get_menu('service').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add billing menu options
    wolf_inn.get_menu('billing').add(
        MenuOption('Generate bill',
                   wolf_inn.store_action('report_gen_bill', 'billing')))
    wolf_inn.get_menu('billing').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Add reports menu options
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by hotel',
                   wolf_inn.store_action('report_occ_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by room type',
                   wolf_inn.store_action('report_occ_room', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by city',
                   wolf_inn.store_action('report_occ_city', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Occupancy by date range',
                   wolf_inn.store_action('report_occ_date', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List staff by role',
                   wolf_inn.store_action('report_list_staff', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('List customer interactions',
                   wolf_inn.store_action('report_customer_inter', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for a hotel',
                   wolf_inn.store_action('report_rev_hotel', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Revenue for all hotels',
                   wolf_inn.store_action('report_rev_all', 'reports')))
    wolf_inn.get_menu('reports').add(
        MenuOption('Back to main menu', wolf_inn.store_menu('main')))

    # Run the program
    wolf_inn.show_title_screen()
    wolf_inn.start('main')


if __name__ == "__main__":
    main()
