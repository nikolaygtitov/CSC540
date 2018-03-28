import sys
import os
import pandas as pd
from pandas.io import sql
from tabulate import tabulate
import mysql.connector as maria_db
from apihelper import APIHelper

################################################################################
# Template for Menus
# - Menus contain a name for reference, title/prompt for UI, and a list of 
# options to choose from.
# - Options are formed from MenuOptions objects
################################################################################
class Menu(object):
    def __init__(self, name, title, prompt = 'Select a menu option:'):
        self.name = name
        self.title = title
        self.prompt = prompt
        self.options = []  # list of MenuOption objects

    def printm(self):
        print(self.title)
        print(self.prompt)
        for index, option in enumerate(self.options):
            print(('  %s. %s') % (index + 1, option.title)) 

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
    def __init__(self, name, title, arglist, handler):
        self.name = name
        self.title = title
        self.arglist = arglist
        self.handler = handler
# End of Query class

################################################################################
# Hotel class which composes all other objects
# - Contains lists of menus, queries and their associated actions
# - Menus continue to loop until exit is selected
################################################################################
class HotelSoft(object):
    def __init__(self, hotelname, db):
        self.helper = APIHelper(db)
        self.hotelname = hotelname
        self.menulist = []
        self.querylist = []

    def addmenu(self, menu):
        self.menulist.append(menu)

    def getmenu(self, name):
        return next(x for x in self.menulist if x.name == name)

    def addquery(self, query):
        self.querylist.append(query)

    def getquery(self, name):
        return next(x for x in self.querylist if x.name == name)

    def show_title_screen(self):
        titlelength = len(self.hotelname)
        pad = (40 - titlelength) / 2
        titlestring = '|' + (' ' * pad) + self.hotelname + (' ' * pad) + '|' 
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
        print(titlestring)
        print('|        HOTEL MANAGEMENT SYSTEM         |')
        print('|              version 1.0               |')
        print('+----------------------------------------+')
        print('|         --- Nathan Schnoor ---         |')
        print('|         --- Nikolay Titov  ---         |')
        print('|         --- Preston Scott  ---         |')
        print('+----------------------------------------+')

    def runquery(self, query, lastmenu):
        return lambda: self.getinputs(self.getquery(query), self.getmenu(lastmenu))

    def getinputs(self, query, lastmenu):
        print(query.title)
        if len(query.arglist) > 0:
            print('Enter the following fields:')
        param_dict = {}
        for arg in query.arglist:
            item = raw_input(arg + ': ').strip()
            if item != '':
                param_dict[arg] = item
            else:
                param_dict[arg] = None
        result = query.handler(param_dict)
        if isinstance(result, pd.DataFrame):
            print '\nQuery Successful ' + u"\u2713"
            print tabulate(result, headers=result.columns.values.tolist(), 
                tablefmt='psql')
            print '\n'
        else:
            print '\n' 
            print result 
            print '\n'
               
        self.getchoice(lastmenu)

    def showmenu(self, menu):
        return lambda: self.getchoice(self.getmenu(menu))

    def getchoice(self, menu):
        menu.printm()
        choice = input('-> ')
        menu.options[choice-1].handler()

    def start(self, menu):
        self.getchoice(self.getmenu(menu))

    def exit_program(self):
        print('Bye')
        sys.exit()

# end of HotelSoft class

################################################################################
# Build the hotel software and runs the program
################################################################################
def main():

    ###############################################################
    # Update database details with correct settings               # 
    db = maria_db.connect(host='127.0.0.1',                       #
                          user='pscott',                          #
                          password='FK8bb"IAlgnYGT8;G!/gy|SQ~',   #
                          database='wolfinn')                     #
    ###############################################################

    wolfinn = HotelSoft('WOLF INN RALEIGH', db)

    #Add queries with lambda functions to be called when they are selected 
    wolfinn.addquery(Query('addhotel',
        'ADD A NEW HOTEL',
        ['name', 'street', 'city', 'state', 'zip', 'phone_number'],
        lambda *args : wolfinn.helper.call_add_hotel(*args)))
    wolfinn.addquery(Query('updatehotel', 
        'UPDATE A HOTEL',
        ['id', 'name', 'street', 'city', 'state', 'zip', 'phone_number'],
        lambda *args : wolfinn.helper.call_update_hotel(*args)))
    wolfinn.addquery(Query('deletehotel',
        'DELETE A HOTEL',
        ['id'],
        lambda *args : wolfinn.helper.call_delete_hotel(*args)))    
    wolfinn.addquery(Query('addroom',
        'ADD A NEW ROOM TO A HOTEL',
        ['hotel_id', 'room_number', 'category', 'occupancy', 'rate'],
        lambda *args : wolfinn.helper.call_add_room(*args)))
    wolfinn.addquery(Query('updateroom',
        'UPDATE A ROOM',
        ['hotel_id', 'room_number', 'category', 'occupancy', 'rate'],
        lambda *args : wolfinn.helper.call_update_room(*args)))
    wolfinn.addquery(Query('deleteroom',
        'DELETE A ROOM',
        ['hotel_id', 'room_number'],
        lambda *args : wolfinn.helper.call_delete_room(*args)))
    wolfinn.addquery(Query('addstaff',
        'ADD A NEW STAFF MEMBER',
        ['name', 'title', 'date_of_birth', 'department', 'phone_number', 'street',
         'zip', 'works_for_hotel_id', 'assigned_hotel_id', 'assigned_room_number'],
        lambda *args : wolfinn.helper.call_add_staff(*args)))
    wolfinn.addquery(Query('updatestaff',
        'UPDATE A STAFF MEMBER',
        ['id', 'name', 'title', 'date_of_birth', 'department', 'phone_number', 'street',
         'zip', 'works_for_hotel_id', 'assigned_hotel_id', 'assigned_room_number'],
        lambda *args : wolfinn.helper.call_update_staff(*args)))
    wolfinn.addquery(Query('deletestaff',
        'DELETE A STAFF MEMBER',
        ['id'],
        lambda *args : wolfinn.helper.call_delete_staff(*args)))
    wolfinn.addquery(Query('addcust',
        'ADD A NEW CUSTOMER',
        ['name', 'date_of_birth', 'phone_number', 'email', 'street', 'zip', 'ssn',
            'account_number', 'is_hotel_card'],
        lambda *args : wolfinn.helper.call_add_customer(*args)))
    wolfinn.addquery(Query('updatecust',
        'UPDATE A CUSTOMER',
        ['id','name', 'date_of_birth', 'phone_number', 'email', 'street', 'zip', 
            'ssn', 'account_number', 'is_hotel_card'],
        lambda *args : wolfinn.helper.call_update_customer(*args)))
    wolfinn.addquery(Query('deletecust',
        'DELETE A CUSTOMER',
        ['id'],
        lambda *args : wolfinn.helper.call_delete_customer(*args)))
    wolfinn.addquery(Query('addres',
        'ADD A NEW RESERVATION',
        ['number_of_guests', 'start_date', 'end_date', 'hotel_id', 'room_number', 
            'customer_id', 'check_in_time', 'check_out_time'],
        lambda *args : wolfinn.helper.call_create_reservation(*args)))
    wolfinn.addquery(Query('updateres',
        'UPDATE A RESERVATION',
        ['id', 'number_of_guests', 'start_date', 'end_date', 'hotel_id', 
            'room_number', 'customer_id', 'check_in_time', 'check_out_time'],
        lambda *args : wolfinn.helper.call_update_reservation(*args)))
    wolfinn.addquery(Query('deleteres',
        'DELETE A RESERVATION',
        ['id'],
        lambda *args : wolfinn.helper.call_delete_reservation(*args)))
    wolfinn.addquery(Query('checkin', 
        'CHECK IN A GUEST',
        ['id'],        #reservation id
        lambda *args : wolfinn.helper.call_update_reservation(*args)))
    wolfinn.addquery(Query('checkout',
        'CHECK OUT A GUEST',
        ['id'],          #reservation id
        lambda *args : wolfinn.helper.call_check_out(*args)))
    wolfinn.addquery(Query('assignstaff',
        'ASSIGN STAFF TO A ROOM',
        ['id'],            # staff id
        lambda *args : wolfinn.helper.call_assign_staff(*args)))
    wolfinn.addquery(Query('addcharge',
        'APPLY A TRANSACTION TO A RESERVATION',
        ['amount', 'type', 'date, reservation_id'],
        lambda *args : wolfinn.helper.call_add_transaction(*args)))
    wolfinn.addquery(Query('updatecharge',
        'UPDATE A TRANSACTION',
        ['id','amount', 'type', 'date, reservation_id'],
        lambda *args : wolfinn.helper.call_update_transaction(*args)))
    wolfinn.addquery(Query('deletecharge',
        'DELETE A TRANSACTION',
        ['id'],
        lambda *args : wolfinn.helper.call_delete_transaction(*args)))
    wolfinn.addquery(Query('genbill',
        'GENERATE BILL',
        ['id'],
        lambda *args : wolfinn.helper.call_generate_bill(*args)))
    wolfinn.addquery(Query('occhotel',
        'OCCUPANCY BY HOTEL',
        [],
        lambda *args : wolfinn.helper.call_occupancy_hotel(*args)))
    wolfinn.addquery(Query('occroom',
        'OCCUPANCY BY ROOM TYPE',
        [],
        lambda *args : wolfinn.helper.call_occupancy_roomtype(*args)))
    wolfinn.addquery(Query('occcity',
        'OCCUPANCY BY CITY',
        [],
        lambda *args : wolfinn.helper.call_occupancy_city(*args)))
    wolfinn.addquery(Query('occdate',
        'OCCUPANCY BY DATE',
        ['start_date', 'end_date'],
        lambda *args : wolfinn.helper.call_occupancy_date(*args)))
    wolfinn.addquery(Query('liststaff',
        'STAFF BY ROLE',
        [],
        lambda *args : wolfinn.helper.call_staff_report(*args)))
    wolfinn.addquery(Query('custinter',
        'CUSTOMER INTERACTIONS',
        ['id'],
        lambda *args : wolfinn.helper.call_cust_inter(*args)))
    wolfinn.addquery(Query('revhotel',
        'REVENUE BY HOTEL',
        ['id'],   #hotel_id
        lambda *args : wolfinn.helper.call_revenue_hotel(*args)))
    wolfinn.addquery(Query('revall',
        'REVENUE FOR ALL HOTELS',
        [],
        lambda *args : wolfinn.helper.call_revenue_all(*args)))
    wolfinn.addquery(Query('custnocard', 
        'CUSTOMERS WITH NO HOTEL CREDIT CARD',
        [],
        lambda *args : wolfinn.helper.call_cust_no_card(*args)))
    wolfinn.addquery(Query('prescust',
        'CURRENT PRESIDENTIAL CUSTOMERS',
        [],
        lambda *args : wolfinn.helper.call_pres_cust(*args)))
    wolfinn.addquery(Query('roomavail1',
        'ROOM AVAILABILITY BY HOTEL',
        ['id'],          #hotel id
        lambda *args : wolfinn.helper.call_avail_hotel(*args)))
    wolfinn.addquery(Query('roomavail2',
        'ROOM AVAILABILITY BY HOTEL AND ROOM TYPE',
        ['id'],
        lambda *args : wolfinn.helper.call_avail_roomtype(*args)))

    #Add main menus 
    wolfinn.addmenu(Menu('main','MAIN MENU'))
    wolfinn.addmenu(Menu('info','INFORMATION PROCESSING'))
    wolfinn.addmenu(Menu('service','SERVICE RECORDS'))
    wolfinn.addmenu(Menu('billing','BILLING'))
    wolfinn.addmenu(Menu('reports','REPORTS'))
    wolfinn.addmenu(Menu('hotels','MANAGE HOTEL INFORMATION'))
    wolfinn.addmenu(Menu('rooms','MANAGE ROOM INFORMATION'))
    wolfinn.addmenu(Menu('staff','MANAGE STAFF INFORMATION'))
    wolfinn.addmenu(Menu('customer','MANAGE CUSTOMER INFORMATION'))
    wolfinn.addmenu(Menu('reservations','RESERVATIONS'))


    # Add main menu options
    wolfinn.getmenu('main').add(MenuOption('Information Processing', 
                            wolfinn.showmenu('info')))
    wolfinn.getmenu('main').add(MenuOption('Service Records', 
                            wolfinn.showmenu('service')))
    wolfinn.getmenu('main').add(MenuOption('Billing', 
                            wolfinn.showmenu('billing')))
    wolfinn.getmenu('main').add(MenuOption('Reports', 
                            wolfinn.showmenu('reports')))
    wolfinn.getmenu('main').add(MenuOption('Exit', wolfinn.exit_program))


    # Add information management menu options
    wolfinn.getmenu('info').add(MenuOption('Manage hotel information', 
                            wolfinn.showmenu('hotels')))
    wolfinn.getmenu('info').add(MenuOption('Manage room information', 
                            wolfinn.showmenu('rooms')))
    wolfinn.getmenu('info').add(MenuOption('Manage staff information', 
                            wolfinn.showmenu('staff')))
    wolfinn.getmenu('info').add(MenuOption('Manage customer information', 
                            wolfinn.showmenu('customer')))
    wolfinn.getmenu('info').add(MenuOption('Check room availability by hotel', 
                            wolfinn.runquery('roomavail1', 'info')))
    wolfinn.getmenu('info').add(MenuOption('Check room availability by room type', 
                            wolfinn.runquery('roomavail2', 'info')))
    wolfinn.getmenu('info').add(MenuOption('Reservations / Check-ins / Check-outs', 
                            wolfinn.showmenu('reservations')))
    wolfinn.getmenu('info').add(MenuOption('Back to main menu', 
                            wolfinn.showmenu('main')))

    # Add hotel menu options
    wolfinn.getmenu('hotels').add(MenuOption('Enter a new hotel', 
                              wolfinn.runquery('addhotel', 'hotels')))
    wolfinn.getmenu('hotels').add(MenuOption('Update a hotel', 
                              wolfinn.runquery('updatehotel', 'hotels')))
    wolfinn.getmenu('hotels').add(MenuOption('Delete a hotel', 
                              wolfinn.runquery('deletehotel', 'hotels')))
    wolfinn.getmenu('hotels').add(MenuOption('Return to previous menu', 
                              wolfinn.showmenu('info')))
    wolfinn.getmenu('hotels').add(MenuOption('Back to main menu', 
                              wolfinn.showmenu('main')))

    # Add room menu options
    wolfinn.getmenu('rooms').add(MenuOption('Enter a new room', 
                             wolfinn.runquery('addroom', 'rooms')))  
    wolfinn.getmenu('rooms').add(MenuOption('Update a room', 
                             wolfinn.runquery('updateroom', 'rooms'))) 
    wolfinn.getmenu('rooms').add(MenuOption('Delete a room', 
                             wolfinn.runquery('deleteroom', 'rooms')))
    wolfinn.getmenu('rooms').add(MenuOption('Return to previous menu', 
                             wolfinn.showmenu('info')))
    wolfinn.getmenu('rooms').add(MenuOption('Back to main menu', 
                             wolfinn.showmenu('main')))

    # Add staff menu options
    wolfinn.getmenu('staff').add(MenuOption('Enter a new staff member', 
                             wolfinn.runquery('addstaff', 'staff')))
    wolfinn.getmenu('staff').add(MenuOption('Update a staff member', 
                             wolfinn.runquery('updatestaff', 'staff')))
    wolfinn.getmenu('staff').add(MenuOption('Delete a staff member', 
                             wolfinn.runquery('deletestaff', 'staff')))
    wolfinn.getmenu('staff').add(MenuOption('Return to previous menu', 
                             wolfinn.showmenu('info')))
    wolfinn.getmenu('staff').add(MenuOption('Back to main menu', 
                             wolfinn.showmenu('main')))    

    # Add customer menu options
    wolfinn.getmenu('customer').add(MenuOption('Enter a new customer', 
                                wolfinn.runquery('addcust', 'customer'))) 
    wolfinn.getmenu('customer').add(MenuOption('Update a customer', 
                                wolfinn.runquery('updatecust', 'customer'))) 
    wolfinn.getmenu('customer').add(MenuOption('Delete a customer', 
                                wolfinn.runquery('deletecust', 'customer')))
    wolfinn.getmenu('customer').add(MenuOption('Return to previous menu', 
                                wolfinn.showmenu('info')))
    wolfinn.getmenu('customer').add(MenuOption('Back to main menu', 
                                wolfinn.showmenu('main'))) 

    # Add reservation menu options
    wolfinn.getmenu('reservations').add(MenuOption('Make a reservation', 
                                    wolfinn.runquery('addres', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Update a reservation', 
                                    wolfinn.runquery('updateres', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Delete a reservation', 
                                    wolfinn.runquery('deleteres', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Assign a room (check-in)', 
                                    wolfinn.runquery('checkin', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Release a room (check-out)', 
                                    wolfinn.runquery('checkout', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Assign staff to room', 
                                    wolfinn.runquery('assignstaff', 'reservations')))
    wolfinn.getmenu('reservations').add(MenuOption('Return to previous menu', 
                                    wolfinn.showmenu('info')))
    wolfinn.getmenu('reservations').add(MenuOption('Back to main menu', 
                                    wolfinn.showmenu('main '))) 

    # Add service menu options
    wolfinn.getmenu('service').add(MenuOption('Add a service charge', 
                               wolfinn.runquery('addcharge', 'service')))
    wolfinn.getmenu('service').add(MenuOption('Update a service charge', 
                               wolfinn.runquery('updatecharge', 'service')))
    wolfinn.getmenu('service').add(MenuOption('Delete a service charge', 
                               wolfinn.runquery('deletecharge', 'service')))
    wolfinn.getmenu('service').add(MenuOption('Back to main menu', 
                               wolfinn.showmenu('main')))

    # Add billing menu options
    wolfinn.getmenu('billing').add(MenuOption('Generate bill', 
                               wolfinn.runquery('genbill', 'billing')))
    wolfinn.getmenu('billing').add(MenuOption('Back to main menu', 
                               wolfinn.showmenu('main')))

    # Add reports menu options
    wolfinn.getmenu('reports').add(MenuOption('Occupancy by hotel', 
                               wolfinn.runquery('occhotel', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Occupancy by room type', 
                               wolfinn.runquery('occroom', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Occupancy by city', 
                               wolfinn.runquery('occcity', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Occupancy by date range', 
                               wolfinn.runquery('occdate', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('List staff by role', 
                               wolfinn.runquery('liststaff', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('List customer interactions', 
                               wolfinn.runquery('custinter', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Revenue for a hotel', 
                               wolfinn.runquery('revhotel', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Revenue for all hotels', 
                               wolfinn.runquery('revall', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Customers Without Credit Cards', 
                               wolfinn.runquery('custnocard', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('List Presidential Customers', 
                               wolfinn.runquery('prescust', 'reports')))
    wolfinn.getmenu('reports').add(MenuOption('Back to main menu', 
                                               wolfinn.showmenu('main')))



    # Run the program
    wolfinn.show_title_screen()
    wolfinn.start('main')

if __name__ == "__main__":
    main()