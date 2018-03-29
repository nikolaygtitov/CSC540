
import unittest
import mysql.connector as mariadb
import pandas as pd

from Project.transaction import sql_transaction


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
