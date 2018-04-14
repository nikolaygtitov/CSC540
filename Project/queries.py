"""
queries.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the queries.py file:
This file contains the statically defined complex queries.
These are the queries used by the project programs to generate reports,
generate the bill, and query room availability.

@version: 1.0
@todo: Demo
@since: March 24, 2018

@status: Complete
@requires: None
@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu
@authors: Nathan Schnoor
          Nikolay Titov
          Preston Scott
"""

# Query to report the occupancy grouped by hotel
# Parameters:
#     - query_date: The date for which to query the occupancy
#     - query_date: The date for which to query the occupancy
REPORT_OCCUPANCY_BY_HOTEL = """
SELECT name as 'Hotel Name', count(number_of_guests) AS 'Rooms Occupied', 
count(room_number) AS 'Total Rooms', 
(count(number_of_guests) / count(room_number) * 100) AS '% Occupancy' 
FROM (SELECT name, room_number, hotel_id, occupancy 
FROM Rooms JOIN Hotels ON Rooms.hotel_id = Hotels.id) AS HotelRooms 
NATURAL LEFT JOIN ((SELECT * from Reservations WHERE 
(DATEDIFF(start_date, %s) <= 0 AND DATEDIFF(end_date, %s) > 0)) AS CurrentRes)
GROUP BY hotel_id
""".strip()

# Query to report the occupancy grouped by room type
# Parameters:
#     - query_date: The date for which to query the occupancy
#     - query_date: The date for which to query the occupancy
REPORT_OCCUPANCY_BY_ROOM_TYPE = """
SELECT category as 'Room Type', 
 count(number_of_guests) AS 'Rooms Occupied', 
 count(room_number) AS 'Total Rooms', 
 (count(number_of_guests) / count(room_number) * 100) 
             AS '% Occupancy' 
FROM (SELECT name, room_number, hotel_id, occupancy, category 
FROM Rooms JOIN Hotels ON Rooms.hotel_id = Hotels.id) 
           AS HotelRooms NATURAL LEFT JOIN 
((SELECT * from Reservations 
  WHERE (DATEDIFF(start_date, %s) <= 0 AND 
         DATEDIFF(end_date, %s) > 0)) AS 
         CurrentRes)
GROUP BY category
"""

# Query to report the occupancy grouped by city
# Parameters:
#     - query_date: The date for which to query the occupancy
#     - query_date: The date for which to query the occupancy
REPORT_OCCUPANCY_BY_CITY = """
SELECT concat(city, ', ' ,state) as 'City, State', 
count(number_of_guests) AS 'Rooms Occupied', 
count(room_number) AS 'Total Rooms', 
(count(number_of_guests) / count(room_number) * 100) AS '% Occupancy' 
FROM ((SELECT name, room_number, hotel_id, occupancy, zip FROM Rooms JOIN 
Hotels ON Rooms.hotel_id = Hotels.id) AS HotelRooms) NATURAL JOIN 
ZipToCityState NATURAL LEFT JOIN ((SELECT * from Reservations WHERE 
(DATEDIFF(start_date, %s) <= 0 AND DATEDIFF(end_date, %s) > 0)) AS CurrentRes)
GROUP BY city, state
"""

# Query to report the occupancy grouped by city
# Parameters:
#     - query_end: The date for which to end the query
#     - query_start: The date for which to start the query
#     - query_end: The date for which to end the query
#     - query_start: The date for which to start the query
#     - query_end: The date for which to end the query
#     - query_start: The date for which to start the query
REPORT_OCCUPANCY_BY_DATE_RANGE = """
SELECT (SELECT SUM(GREATEST(0, DATEDIFF(LEAST(%s, end_date), 
GREATEST(%s, start_date)))) 
FROM Reservations) AS 'Actual Bookings', (SELECT COUNT(hotel_id) * 
DATEDIFF(%s, %s) FROM Rooms) AS 'Total Possible Bookings', 
((SELECT SUM(GREATEST(0, DATEDIFF(LEAST(%s, end_date), GREATEST(%s, start_date)))) 
FROM Reservations) / (SELECT COUNT(hotel_id) * DATEDIFF(%s, %s) FROM Rooms)) * 
100 AS '% Occupancy'
"""

# Query to report the staff grouped by role
# Parameters:
#     - hotel: The hotel ID for which to report staff
REPORT_STAFF_BY_ROLE = """
SELECT Staff.department as Department, Staff.title as Title, 
Staff.name as 'Staff Name', Staff.id as 'Staff ID'
FROM Staff
WHERE Staff.works_for_hotel_id = %s ORDER BY department, title;
"""

# Query to report the customer interactions for a given reservation
# Parameters:
#     -reservation_id: The reservation ID for which to report interactions
REPORT_CUSTOMER_INTERACTIONS = """
SELECT Staff.name as 'Staff Name', Serves.staff_id as 'Staff ID'
FROM Serves INNER JOIN Staff ON Serves.staff_id = Staff.id 
WHERE Serves.reservation_id = %s;
"""

# Query to report the revenue for a single hotel
# Parameters:
#     - start_date: The date for the start of the query
#     - end_date: The date for the end of the query
#     - hotel_id: The hotel ID for which to report revenue
REPORT_REVENUE_SINGLE_HOTEL = """
SELECT Hotels.name as 'Hotel Name', SUM(amount) as Revenue
FROM Transactions
JOIN Reservations ON Transactions.reservation_id = Reservations.id
JOIN Hotels ON Reservations.hotel_id = Hotels.id
WHERE date >= %s AND date <= %s AND hotel_id = %s;
"""

# Query to report the revenue for all hotels
# Parameters:
#     - start_date: The date for the start of the query
#     - end_Date: The date for the end of the query
REPORT_REVENUE_ALL_HOTELS = """
SELECT Hotels.name as 'Hotel Name', IFNULL(SUM(amount), 0) as Revenue
FROM Transactions
JOIN Reservations ON Transactions.reservation_id = Reservations.id RIGHT JOIN 
Hotels ON Hotels.id = Reservations.hotel_id
WHERE date >= %s AND date <= %s GROUP BY Hotels.id ORDER BY Hotels.name;
"""

# Desired column names for Room Availability query displayed in Pandas DataFrame
# Parameters: None
ROOM_AVAILABILITY_COLUMN_NAMES = """
id AS 'Hotel ID', name AS 'Hotel Name', street AS 'Street', city AS 'City', 
state AS 'State', Hotels.zip AS 'ZIP', phone_number AS 'Phone Number', 
room_number AS 'Room Number', category AS 'Category', occupancy AS 'Occupancy',
rate AS 'Rate per Night'
"""

# Table statement followed by FROM clause for Room Availability query
# Parameters: None
ROOM_AVAILABILITY_TABLE_STATEMENT = """
ZipToCityState JOIN Hotels ON ZipToCityState.zip = Hotels.zip JOIN Rooms ON 
Rooms.hotel_id = Hotels.id
"""

# Nested WHERE clause for Room Availability query used for Reservations table
# Parameters: None
ROOM_AVAILABILITY_NESTED_WHERE_CLAUSE = """
(Rooms.hotel_id, room_number) NOT IN (SELECT hotel_id, room_number FROM Reservations 
WHERE ((('{}' BETWEEN start_date AND end_date) OR ('{}' between start_date 
AND end_date) OR (start_date BETWEEN '{}' AND '{}') OR (end_date BETWEEN '{}' 
AND '{}'))
"""

# Query to generate a bill for total amount per specific reservation
# Parameters:
#     - reservation_id: Reservation ID for which total amount due is
#       calculated applying discount
GENERATE_BILL_TOTAL_AMOUNT_DUE = """
SELECT SUM(amount) AS 'Cost', discount_percentage * SUM(amount) AS 'Discount', 
SUM(amount) - (discount_percentage * SUM(amount)) AS 'Total Amount Due'
FROM Transactions, (SELECT IFNULL(is_hotel_card, 0) * 0.05 AS 
'discount_percentage' FROM Reservations JOIN Customers ON 
Reservations.customer_id = Customers.id WHERE Reservations.id = %s) as Discount
WHERE reservation_id = %s
"""

# Query to generate a bill for itemized charges per specific reservation
# Parameters:
#     - reservation_id: Reservation ID for which a list of itemized charges is
#       calculated (does not include discount)
GENERATE_BILL_ITEMIZED_CHARGES = """
SELECT id AS 'Transaction ID', amount AS 'Amount', type AS 'Description', 
date AS 'Date' 
FROM Transactions
WHERE reservation_id = %s
"""

# Query to find all the staff (staff_id) assigned to a particular reservation
# as dedicated staff
# Parameters:
#    - Reservations.id: Reservation ID of the room for which customer does a
#      check-out (to find all assigned staff members to free them)
QUERY_ASSIGNED_STAFF = """
SELECT Staff.id as staff_id
FROM Staff INNER JOIN Reservations
ON assigned_hotel_id = Reservations.hotel_id
AND assigned_room_number = Reservations.room_number
WHERE Reservations.id = %s
"""