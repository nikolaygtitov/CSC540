
# Query to report the occupancy grouped by hotel
# Parameters:
#   query_date - The date for which to query the occupancy
#   query_date - The date for which to query the occupancy
REPORT_OCCUPANCY_BY_HOTEL = """
SELECT name as 'Hotel Name', 
 count(number_of_guests) AS 'Rooms Occupied', 
 count(room_number) AS 'Total Rooms', 
(count(number_of_guests) / count(room_number) * 100) 
             AS '% Occupancy' 
FROM (SELECT name, room_number, hotel_id, occupancy 
FROM Rooms JOIN Hotels ON Rooms.hotel_id = Hotels.id) 
AS HotelRooms NATURAL LEFT JOIN 
      ((SELECT * from Reservations 
        WHERE (datediff(start_date, %s) <= 0 AND 
         datediff(end_date, %s) > 0)) AS   
         CurrentRes)
GROUP BY hotel_id
""".strip()

# Query to report the occupancy grouped by room type
# Parameters:
#   query_date - The date for which to query the occupancy
#   query_date - The date for which to query the occupancy
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
  WHERE (datediff(start_date, %s) <= 0 AND 
         datediff(end_date, %s) > 0)) AS 
         CurrentRes)
GROUP BY category
"""

# Query to report the occupancy grouped by city
# Parameters:
#   query_date - The date for which to query the occupancy
#   query_date - The date for which to query the occupancy
REPORT_OCCUPANCY_BY_CITY = """
SELECT concat(city, ', ' ,state) as 'City, State', 
 count(number_of_guests) AS 'Rooms Occupied', 
 count(room_number) AS 'Total Rooms', 
(count(number_of_guests) / count(room_number) * 100) 
                  AS '% Occupancy' 
FROM ((SELECT name, room_number, hotel_id, occupancy, zip
 FROM Rooms JOIN Hotels ON Rooms.hotel_id = Hotels.id)                 
       AS HotelRooms) 
NATURAL JOIN ZipToCityState  
NATURAL LEFT JOIN 
((SELECT * from Reservations 
  WHERE (datediff(start_date, %s) <= 0 AND 
         datediff(end_date, %s) > 0)) AS 
         CurrentRes)
GROUP BY city, state
"""

# Query to report the occupancy grouped by city
# Parameters:
#   query_end   - The date for which to end the query
#   query_start - The date for which to start the query
#   query_end   - The date for which to end the query
#   query_start - The date for which to start the query
REPORT_OCCUPANCY_BY_DATE_RANGE = """
SELECT (SELECT SUM(GREATEST(0, DATEDIFF(LEAST(@query_end, 
                                              end_date), 
  GREATEST(@query_start, start_date)))) 
FROM Reservations) AS 'Actual Bookings', 
(SELECT COUNT(hotel_id) * DATEDIFF(@query_end, @query_start) 
 FROM Rooms) AS 'Total Possible Bookings', 
((SELECT SUM(GREATEST(0, LEAST(%s, end_date) - 
             GREATEST(%s, start_date))) 
 FROM Reservations) / 
(SELECT COUNT(hotel_id) * DATEDIFF(%s, %s) 
 FROM Rooms)) * 100 AS '% Occupancy'

"""

# Query to report the staff grouped by role
# Parameters:
#   hotel  - The hotel id for which to report staff
REPORT_STAFF_BY_ROLE = """
SELECT
  Staff.department as Department,
  Staff.title as Title,
  Staff.name as 'Staff Name',
  Staff.id as 'Staff ID'
FROM Staff
WHERE Staff.works_for_hotel_id = %s
ORDER BY department, title;
"""

# Query to report the customer interactions for a given reservation
# Parameters:
#   reservation_id  - The reservation id for which to report interactions
REPORT_CUSTOMER_INTERACTIONS = """
SELECT
Staff.name as 'Staff Name',
Serves.staff_id as 'Staff ID'
FROM Serves
INNER JOIN Staff ON Serves.staff_id = Staff.id
WHERE Serves.reservation_id = %s;
"""

# Query to report the revenue for a single hotel
# Parameters:
#   start_date  - The date for the start of the query
#   end_Date    - The date for the end of the query
#   hotel       - The hotel id for which to report revenue
REPORT_REVENUE_SINGLE_HOTEL = """
SELECT Hotels.name as 'Hotel Name',
 SUM(amount) as Revenue
FROM Transactions
JOIN Reservations ON Transactions.reservation_id = 
                     Reservations.id
JOIN Hotels ON Reservations.hotel_id = Hotels.id
WHERE date >= %s
AND date <= %s
AND hotel_id = %s;
"""

# Query to report the revenue for all hotels
# Parameters:
#   start_date  - The date for the start of the query
#   end_Date    - The date for the end of the query
REPORT_REVENUE_ALL_HOTELS = """
SELECT Hotels.name as 'Hotel Name',
       IFNULL(SUM(amount), 0) as Revenue
FROM Transactions
JOIN Reservations ON Transactions.reservation_id =                     
                      Reservations.id
RIGHT JOIN Hotels ON Hotels.id = Reservations.hotel_id
WHERE date >= %s AND date <= %s
GROUP BY Hotels.id
ORDER BY Hotels.name;
"""
