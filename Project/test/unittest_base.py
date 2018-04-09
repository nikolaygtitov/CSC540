
import unittest
import mysql.connector as mariadb
import pandas as pd

from Project.util import sql_transaction


class SQLUnitTestBase(unittest.TestCase):

    @staticmethod
    def _connect_to_test_db():
        con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='nfschnoo', password='001027748', database='nfschnoo')
        return con

    def setUp(self):
        self._con = self._connect_to_test_db()
        cursor = self._con.cursor()
        print 'Dropping tables'
        self._delete_tables(cursor)
        print 'Creating tables'
        self._create_tables(cursor)
        cursor.close()

    def tearDown(self):
        self._con.close()

    def _create_tables(self, cursor):
        cursor.execute("""
            CREATE TABLE ZipToCityState (
                zip VARCHAR(10) PRIMARY KEY,
                city VARCHAR(32) NOT NULL,
                state VARCHAR(2) NOT NULL,
                CHECK(LENGTH(zip)>=5 AND LENGTH(city)>0 AND LENGTH(state)=2)
            );""")
        cursor.execute("""
            CREATE TABLE Hotels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(128) NOT NULL,
                street VARCHAR(64) NOT NULL,
                zip VARCHAR(10) NOT NULL,
                phone_number VARCHAR(32) NOT NULL, 
                CONSTRAINT fk_hotels_ziptocitystate_zip FOREIGN KEY (zip) REFERENCES ZipToCityState(zip) 
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                CONSTRAINT uc_hotels UNIQUE (street, zip),
                CHECK(LENGTH(name)>0 AND LENGTH(street)>0 AND LENGTH(phone_number)>0)	
            );""")
        cursor.execute("""
            CREATE TABLE Rooms (
                hotel_id INT,
                room_number SMALLINT UNSIGNED,
                category VARCHAR(64) NOT NULL,
                occupancy TINYINT UNSIGNED NOT NULL,
                rate DECIMAL(8,2) UNSIGNED NOT NULL,
                PRIMARY KEY (hotel_id, room_number),
                CONSTRAINT fk_rooms_hotels_id FOREIGN KEY (hotel_id) REFERENCES Hotels(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE,
                CHECK(LENGTH(category)>0 AND (occupancy BETWEEN 1 AND 9))
            );""")

        cursor.execute("""
            CREATE TABLE Staff (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(64) NOT NULL,
                title VARCHAR(64) NOT NULL,
                date_of_birth DATE NOT NULL,
                department VARCHAR(64) NOT NULL,
                phone_number VARCHAR(32) NOT NULL,
                street VARCHAR(64) NOT NULL,
                zip VARCHAR(10) NOT NULL,
                works_for_hotel_id INT NOT NULL,
                assigned_hotel_id INT,
                assigned_room_number SMALLINT UNSIGNED,
                CONSTRAINT fk_staff_ziptocitystate_zip FOREIGN KEY (zip) REFERENCES ZipToCityState(zip) 
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                CONSTRAINT fk_staff_hotels_id FOREIGN KEY (works_for_hotel_id) REFERENCES Hotels(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE,
                CONSTRAINT fk_staff_rooms_hotel_id_room_number FOREIGN KEY (assigned_hotel_id, assigned_room_number) 
                    REFERENCES Rooms(hotel_id,room_number) ON UPDATE CASCADE ON DELETE SET NULL,
                CHECK(LENGTH(name)>0 AND LENGTH(title)>0 AND LENGTH(department)>0 AND LENGTH(phone_number)>0 
                    AND LENGTH(street)>0)
            );""")

        cursor.execute("""
            CREATE TABLE Customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(64) NOT NULL,
                date_of_birth DATE NOT NULL,
                phone_number VARCHAR(32) NOT NULL,
                email VARCHAR(64) NOT NULL,
                street VARCHAR(64) NOT NULL,
                zip VARCHAR(10) NOT NULL,
                ssn VARCHAR(11) UNIQUE NOT NULL,
                account_number VARCHAR(128) UNIQUE,
                is_hotel_card BOOLEAN,
                CONSTRAINT fk_customers_ziptocitystate_zip FOREIGN KEY (zip) REFERENCES ZipToCityState(zip) 
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                CHECK(LENGTH(name)>0 AND LENGTH(phone_number)>0 AND LENGTH(email)>0 AND LENGTH(street)>0 
                    AND LENGTH(ssn)=11 AND LENGTH(account_number)>0)
            );""")

        cursor.execute("""
            CREATE TABLE Reservations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                number_of_guests TINYINT UNSIGNED NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                check_in_time DATETIME,
                check_out_time DATETIME,
                hotel_id INT NOT NULL,
                room_number SMALLINT UNSIGNED NOT NULL,
                customer_id INT NOT NULL,
                CONSTRAINT fk_reservations_rooms_hotel_id_room_number FOREIGN KEY (hotel_id, room_number) 
                    REFERENCES Rooms(hotel_id, room_number) ON UPDATE CASCADE ON DELETE RESTRICT,
                CONSTRAINT fk_reservations_customers_id FOREIGN KEY (customer_id) REFERENCES Customers(id) 
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                CHECK((number_of_guests BETWEEN 1 AND 9) AND start_date > end_date AND check_in_time <= start_date 
                    AND check_out_time >= end_date)
            );""")

        cursor.execute("""
            CREATE TABLE Transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(8,2) UNSIGNED NOT NULL,
                type VARCHAR(128) NOT NULL,
                date DATETIME NOT NULL,
                reservation_id INT NOT NULL,
                CONSTRAINT fk_transactions_reservation_id FOREIGN KEY (reservation_id) REFERENCES Reservations(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE,
                CHECK(LENGTH(type)>0)
            );""")

        cursor.execute("""
            CREATE TABLE Serves (
                staff_id INT NOT NULL,
                reservation_id INT NOT NULL,
                CONSTRAINT fk_serves_staff_id FOREIGN KEY (staff_id) REFERENCES Staff(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE,
                CONSTRAINT fk_serves_reservation_id FOREIGN KEY (reservation_id) REFERENCES Reservations(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE
            );""")
        self._con.commit()

    def _delete_tables(self, cursor):
        try:
            cursor.execute('DROP TABLE Serves')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Transactions')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Reservations')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Customers')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Staff')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Rooms')
        except:
            pass
        try:
            cursor.execute('DROP TABLE Hotels')
        except:
            pass
        try:
            cursor.execute('DROP TABLE ZipToCityState')
        except:
            pass
        self._con.commit()

    def _insert_test_data(self):
        cursor = self._con.cursor()

        # ZipToCityState
        zip_data = [
            ['27965', 'Raleigh', 'NC'],
            ['27606', 'Raleigh', 'NC'],
            ['10001', 'New York', 'NY'],
            ['19141', 'Philadelphia', 'PA'],
            ['02130', 'Boston', 'MA'],
            ['33222', 'Miami', 'FL'],
            ['90010', 'Los Angeles', 'CA'],
            ['90050', 'Los Angeles', 'CA']
        ]
        for row in zip_data:
            cursor.execute('INSERT INTO ZipToCityState(zip, city, state)'
                           'VALUES(%s, %s, %s)', row)

        # Hotels
        hotel_data = [
            ['Wolf Inn Raleigh Hurricanes',
             '100 Glenwood Ave', '27965', '919-965-6743'],
            ['Wolf Inn Raleigh Wolfpack', '875 Penny Rd',
             '27606', '919-546-7439'],
            ['Wolf Inn New York Rangers', '6004 8th Ave',
             '10001', '929-877-0072'],
            ['Wolf Inn Philadelphia Flyers',
             '1234 N Broad St', '19141', '215-633-4374'],
            ['Wolf Inn Boston Bruins', '7865 Morton St',
             '02130', '617-683-1078'],
            ['Wolf Inn Miami Panthers', '890 Orange St',
             '33222', '305-627-291'],
            ['Wolf Inn Los Angeles Kings', '640 Irolo St',
             '90010', '323-920-3782'],
            ['Wolf Inn Los Angeles Sharks',
             '9000 Lincoln Ave', '90050', '213-628-8344'],
            ['Nikolay Test Inn',
             '1111 Who Knows Dr.', '27606', '(919)-555-5555']
        ]
        for row in hotel_data:
            cursor.execute('INSERT INTO Hotels(name, street, zip, phone_number)'
                           'VALUES(%s, %s, %s, %s)', row)

        # Rooms
        room_data = [
            [1, 100, 'Economy', 2, 85.50],
            [2, 200, 'Deluxe', 2, 160.00],
            [3, 300, 'Executive Suite', 1, 450.60],
            [4, 100, 'Economy', 2, 200.10],
            [5, 200, 'Deluxe', 2, 350.40],
            [6, 300, 'Executive Suite', 1, 600.00],
            [7, 400, 'Presidential Suite', 1, 1200.00],
            [8, 400, 'Presidential Suite', 1, 2000.00],
            [9, 100, 'Economy', 2, 100.00]
        ]
        for row in room_data:
            cursor.execute("INSERT INTO "
                           "Rooms(hotel_id, room_number, category, occupancy, rate)"
                           "VALUES(%s, %s, %s, %s, %s)", row)

        # Staff
        staff_data = [
            ['Joe S. Rogan', 'Manager', '1970-08-30', 'Management Department',
             '919-398-1209', '2505 Avent Ferry Rd, Apt. A', '27606', 2, None,
             None],
            ['Conor McGregor', 'Front Desk Representative', '1989-06-25',
             'Front End', '213-738-9201', '830 Sunshine St', '90050', 8, None,
             None],
            ['Luke Rockhold', 'Room Service Staff', '1984-09-05',
             'Room Service Department', '323-832-8912', '7626 Banana Lane',
             '90010', 7, 7, 400],
            ['John Jones', 'Catering Staff', '1982-10-06', 'Deli Department',
             '215-839-2508', '409 Stamp St, Apt. 213', '02130', 5, 5, 200],
            ['Tony Ferguson', 'Billing Staff', '1986-12-31',
             'Billing Department', '929-029-2789', '644 10th Ave, Apt. 12',
             '10001', 3, None, None],
            ['Brian Ortega', 'Repairman', '1970-08-30', 'Repairs Department',
             '215-348-7853', '6409 Walnut St, Apt. 409', '19141', 4, None,
             None],
            ['Robbie Lawler', 'Janitor', '1970-08-30', 'Cleaning Department',
             '305-638-9832', '6559 Oyster Lane', '33222', 6, None, None],
            ['Rory McDonald', 'Room Service Staff', '1980-02-15',
             'Room Service Department', '919-383-2991',
             '2300 Sugar Bush Rd, Apt. 52', '27965', 2, 2, 200],
            ['FirstStaff LastStaff', 'Catering Staff', '1956-05-09',
             'Cooking Hell Department', '(919)-111-0101',
             'Staff St., Apt. 59', '27606', 9, None, None]

        ]
        for row in staff_data:
            cursor.execute("INSERT INTO "
                           "Staff(name, title, date_of_birth, department, "
                           "phone_number, street, zip, works_for_hotel_id,"
                           "assigned_hotel_id, assigned_room_number)"
                           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           row)

        # Customers
        customer_data = [
            ['George W. Bush', '1956-04-01', '+1(305)782-8720',
             'georgewbush@gmail.com', '5463 Corn Ave, Apt.C', '33222',
             '000-00-0001', '4616-7828-8992-6717 CVS:123', False],
            ['Barack H. Obama', '1964-09-11', '+1(213)867-9302',
             'barackhobama@gmail.com', '1200 Beverly Hills', '90050',
             '000-00-0002', 'Routing:000237 Account:0209309030293', False],
            ['William G. Clinton', '1953-11-27', '+1(929)873-8921',
             'willianandmonica@gmail.com', '6050 12-th Ave', '10001',
             '000-00-0003', '0001-3234-4323-7483', True],
            ['Donald N. Trump', '1946-05-25', '+1(929)909-2893',
             'donaldtrump@gmail.com', '3209 6-th St. Apt 29', '10001',
             '000-00-0004', '0001-8392-3344-2384', True],
            ['Dana White', '1973-08-15', '215-893-9018', 'danawhite@ufc.com',
             '6723 Pecan St. Apt 65', '19141', '100-10-0001'],
            ['Anderson Silva', '1978-07-23', '617-893-8932',
             'anderson@yahoo.com', '78 Center Ave, Apt 80',
             '02130', '100-10-0002'],
            ['Stephen Thompson', '1987-23-09', '919-893-6622',
             'tstephen@nokia.com', '839 Garner St, Apt 20',
             '27965', '100-10-0003'],
            ['Study Goodwin', '1995-01-01', '919-782-8211',
             'spgoodwin@ncsu.edu', '63 Centennial Pkwy, Unit 54', '27606',
             '100-10-0004']
        ]
        for row in customer_data:
            if len(row) == 9:
                cursor.execute("INSERT INTO "
                               "Customers(name, date_of_birth, phone_number,"
                               "email, street, zip, ssn, "
                               "account_number, is_hotel_card)"
                               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               row)
            else:
                cursor.execute("INSERT INTO "
                               "Customers(name, date_of_birth, phone_number,"
                               "email, street, zip, ssn)"
                               "VALUES(%s, %s, %s, %s, %s, %s, %s)", row)

        # Reservations
        reservation_data = [
            [2, '2015-03-30', '2015-04-05',
             '2015-03-30 18:43:25', '2015-04-05 08:32:42', 1, 100, 2],
            [1, '2016-05-25', '2016-05-28',
             '2016-05-25 23:34:18', '2016-05-28 12:01:24', 3, 300, 1],
            [2, '2016-08-10', '2016-08-15',
             '2016-08-11 03:12:42', '2016-08-15 14:25:52', 2, 200, 6],
            [1, '2017-01-15', '2017-01-22',
             '2017-01-16 01:24:31', '2017-01-22 06:26:01', 6, 300, 7],
            [2, '2017-11-27', '2017-12-01',
             '2017-11-27 21:31:15', '2017-12-05 09:11:07', 4, 100, 5],
            [2, '2018-01-07', '2018-01-12',
             '2018-01-07 16:32:27', '2018-01-12 07:51:29', 5, 200, 8],
            [1, '2018-01-16', '2018-01-20',
             '2018-01-17 04:45:00', '2018-01-20 11:52:19', 7, 400, 3],
            [1, '2018-02-25', '2018-02-26',
             '2018-02-25 03:41:21', '2018-02-26 13:12:55', 8, 400, 4],
            [1, '2018-04-08', '2018-04-10',
             '2018-04-08 12:12:12', None, 9, 100, 1]
        ]

        for row in reservation_data:
            cursor.execute("INSERT INTO "
                           "Reservations(number_of_guests, "
                           "start_date, end_date,"
                           "check_in_time, check_out_time, "
                           "hotel_id, room_number, customer_id)"
                           "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", row)

        # Transactions
        transaction_data = [
            [8893.37, '4-nights room reservation', '2018-01-20 11:52:19', 8],
            [567.90, '6-nights room reservation', '2015-04-05 08:32:42', 1],
            [485.68, 'Special Dinner: Filet Mignon', '2018-01-18 19:32:23', 7],
            [23.89, 'International phone calls', '2015-04-03 21:46:12', 1],
            [210.20, 'Dry Cleaning', '2018-01-11 17:36:07', 6],
            [30.00, 'Utilization of gym special equipment',
             '2017-12-05 09:54:11', 5],
            [83.00,
             'Room Service: Extra towels, and other bathroom accessories',
             '2018-02-26 06:34:23', 8],
            [12.00, 'Special Request: Preferred room', '2017-01-16 01:24:31', 4]

        ]

        for row in transaction_data:
            cursor.execute("INSERT INTO "
                           "Transactions(amount, type, date, reservation_id)"
                           "VALUES(%s, %s, %s, %s)", row)

        # Serves
        serves_data = [
            [1, 3],
            [2, 8],
            [3, 8],
            [4, 4],
            [5, 1],
            [6, 5],
            [7, 7],
            [8, 6]
        ]

        for row in serves_data:
            cursor.execute("INSERT INTO "
                           "Serves(staff_id, reservation_id)"
                           "VALUES(%s, %s)", row)

        cursor.close()
        self._con.commit()
