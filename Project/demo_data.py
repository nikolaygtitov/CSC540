
def _drop_tables(db):
    cursor = db.cursor()
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
    db.commit()


def _create_tables(db):
    cursor = db.cursor()
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
    db.commit()


def load_demo_data(db):

    _drop_tables(db)
    _create_tables(db)

    cursor = db.cursor()
    print "Loading Demo Data"
    # ZipToCityState
    zip_data = [
        ['27', 'Raleigh', 'NC'],
        ['54', 'Rochester', 'NY'],
        ['28', 'Greensboro', 'NC'], # Zip: 27
        ['32', 'Raleigh', 'NC'],
        ['78', 'Rochester', 'NY'],
        ['14', 'Dallas', 'TX'],
    ]

    hotel_data = [
        [1, 'Hotel A', '21 ABC St', '27', '919'],
        [2, 'Hotel B', '25 XYZ St', '54', '718'],
        [3, 'Hotel C', '29 PQR St', '28', '984'], # Zip: 27
        [4, 'Hotel D', '28 GHW St', '32', '920'],
    ]

    room_data = [
        [1, 1, 'Economy', 1, 100],
        [1, 2, 'Deluxe', 2, 200],
        [2, 3, 'Economy', 1, 100],
        [3, 2, 'Executive', 3, 1000], # Available: no
        [4, 1, 'Presidential', 4, 5000],
        [1, 5, 'Deluxe', 2, 200],
    ]

    customer_data = [
        [1001, 'David', '1980-01-30', '123', 'david@gmail.com', '980 TRT St', '27', '593-9846', '1052', False],  # Zip: None
        [1002, 'Sarah', '1971-01-30', '456', 'sarah@gmail.com', '7720 MHT St', '28', '777-8352', '3020', True],  # Zip: None
        [1003, 'Joseph', '1987-01-30', '789', 'joseph@gmail.com', '231 DRY St', '78', '858-9430', '2497', False],
        [1004, 'Lucy', '1985-01-30', '213', 'lucy@gmail.com', '24 BST Dr', '14', '440-9328', None, None],  # Cash
    ]

    staff_data = [
        [100, 'Mary', '1978-04-01', 'Management', 'Manager', '654', '90 ABC St', '27', 1],  # Age: 40
        [101, 'John', '1973-02-14', 'Management', 'Manager', '564', '798 XYZ St', '54', 2],  # Age: 45
        [102, 'Carol', '1963-01-23', 'Management', 'Manager', '546', '351 MH St', '28', 3],  # Age: 55, Zip: 27
        [103, 'Emma', '1963-04-02', 'Management', 'Front Desk Staff', '546', '49 ABC St', '27', 1],  # Age: 55
        [104, 'Ava', '1963-02-03', 'Catering', 'Catering Staff', '777', '425 RG St', '27', 1],  # Age: 55
        [105, 'Peter', '1966-01-01', 'Management', 'Manager', '724', '475 RG St', '27', 4],
        [106, 'Olivia', '1990-09-13', 'Management', 'Front Desk Staff', '799', '325 PD St', '27', 4],  # Age: 27
    ]

    reservation_data = [
        [1, 1, '2017-05-10', '2017-05-13', '2017-05-10 15:17:00', '2017-05-13 10:22:00', 1, 1, 1001],
        [2, 2, '2017-05-10', '2017-05-13', '2017-05-10 16:11:00', '2017-05-13 09:27:00', 1, 2, 1002],
        [3, 1, '2016-05-10', '2016-05-14', '2016-05-10 15:45:00', '2016-05-14 11:10:00', 2, 3, 1003],
        [4, 2, '2018-05-10', '2018-05-12', '2018-05-10 14:30:00', '2018-05-12 10:00:00', 3, 2, 1004],
    ]

    transaction_data = [
        [16, 'Dry Ceaning', '2017-05-10', 1],
        [15, 'Gym', '2017-05-10', 1],
        [15, 'Gym', '2017-05-10', 2],
        [10, 'Room Service', '2016-05-10', 3],
        [5, 'Phone Bills', '2018-05-10', 4],
    ]

    for row in zip_data:
        cursor.execute('INSERT INTO ZipToCityState(zip, city, state)'
                       'VALUES(%s, %s, %s)', row)

    for row in hotel_data:
        cursor.execute('INSERT INTO Hotels(id, name, street, zip, phone_number)'
                       'VALUES(%s, %s, %s, %s, %s)', row)

    for row in room_data:
        cursor.execute("INSERT INTO "
                       "Rooms(hotel_id, room_number, category, occupancy, rate)"
                       "VALUES(%s, %s, %s, %s, %s)", row)

    for row in staff_data:
        cursor.execute("INSERT INTO "
                       "Staff(id, name, date_of_birth, department, "
                       "title, phone_number, street, zip, works_for_hotel_id)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       row)

    for row in customer_data:
        cursor.execute("INSERT INTO "
                       "Customers(id, name, date_of_birth, phone_number,"
                       "email, street, zip, ssn, "
                       "account_number, is_hotel_card)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       row)

    for row in reservation_data:
        cursor.execute("INSERT INTO "
                       "Reservations(id, number_of_guests, "
                       "start_date, end_date,"
                       "check_in_time, check_out_time, "
                       "hotel_id, room_number, customer_id)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

    for row in transaction_data:
        cursor.execute("INSERT INTO "
                       "Transactions(amount, type, date, reservation_id)"
                       "VALUES(%s, %s, %s, %s)", row)

    cursor.close()
    db.commit()


if __name__ == '__main__':
    import mysql.connector as mariadb
    con = mariadb.connect(host='classdb2.csc.ncsu.edu', user='nfschnoo',
                          password='001027748', database='nfschnoo')

    load_demo_data(con)
