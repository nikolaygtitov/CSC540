# CSC 540 - Database Management concepts and Systems

# Course Project

## Wolf Inn: Popular Hotel Chain Database System
The design and development processes of Database Management System for WolfInns are completed in the Project Report 1 and Project Report 2.
### Description of the Project:
The Popular Hotel Chain database system is designed and built to manage and maintain information of hotels, rooms, staff, and customers, including but not limited to storing, updating, and deleting data. The database maintains a variety of information records about hotels located in various cities around the country, including staff, rooms, customers, and billing records. 

For each customer stay it maintains service records, such as phone bills, dry cleaning, gyms, room service, and special requests. It generates and maintains billing accounts for each customer stay. It generates report occupancy by hotel, room category, date range, and city. The database system is developed for Wolf Inns and is used by hotels operators and employees including management staff, front desk representatives, room service, billing, and catering staff.

The Popular Hotel Chain database system resolves constraints on availability and pricing of rooms, maintaining proper customer, billing, check-in, and check-out information. Users of the database may perform different tasks concurrently, each consisting of multiple sequential operations that have an affect on the database.

There are four major tasks that are performed by corresponding users on the database:
1. Information Processing
2. Maintaining Service Records
3. Maintaining Billing Accounts
4. Reports
### Description of the Software:
It provides a user with friendly User Interface (text-based menu system) to select tasks and operations user needs/wants to perform.

The following is a sample of the User Interface that a user sees as the program started:
```
Here the output of UI
```

All of the following operations are performed on MySQL MariaDB NCSU Server at [classdb2.csc.ncsu.edu](https://courses.ncsu.edu/csc540/lec/001/wrap/FAQ_general.html):
* __SELECT__
* __INSERT__
* __UPDATE__
* __DELETE__

## Run the Software:
To start the program that connects to DBMS (MySQL MariaDB Server at NCSU) run the following command:
```
python hotelsoft.py
```
Note that current DBMS (MySQL MariaDB Server at NCSU) version ignores all the `CHECK` and `NOT NULL` constraints for insert and update operations.

To enable assertions within the program itself ensuring that data to be inserted or updated obeys MySQL constraints currently ignored, run the following command:
```
python hotelsoft.py -c
```
## Configurations and Specifications:
The following describes environment configurations and software specifications. 
### Language:
Python
### Prerequisites:
*	Python version >= 2.7
* OS: any Linux distribution (Ubuntu, RedHat, etc) that has Python version >= 2.7
*	DBMS version: Ver 15.1 Distrib 5.5.57-MariaDB, for Linux (x86_64) using readline 5.1
* DBMS must contain all necessary/required tables for proper and correct software behavior
  * To create required tables in the DBMS, run the following:
* Tables may contain some data or be empty
### Constraints and Assumptions:
The following is list of reasonable assumptions our team had to make due to the absence of real customer and lack of all/additional requirements and specifications.

Note that some of the constraints can be ignored if program executes without check option `-c`.
* Hotels
  * Each hotel is uniquely identified by its ID.
  * Each hotel has at most one manager at a time.
  * Each hotel has a unique address information: {street, city, state, zip} attribute values are unique per hotel. Since zip code functionally determines city and state [zip -> city, state] (see below in section Other), {street, zip} attribute values are unique per hotel.
  * Maximum occupancy of any room at any hotel must not exceed 9 (nine) guests.
  * The number of rooms doesn't change once the Hotel is in use.
* Staff
  * Each member of hotel Staff is uniquely identified by his or her ID
  * Each member of the Staff has at most one phone number
  * Each member of the Staff works for exactly one hotel at a time
  * Dedicated staff can be assigned to any Rooms other than presidential suites (e.g., per customer’s request)
  * Any member of the Staff can be assigned to any given room
  * Billing staff work from the corporate office and do not serve customers
  * Teaching staff, students, and developers (Team 2) may play the role of the Owners/Operators
* Customers
  * Each customer is uniquely identified by his or her customer ID
  * Each customer has at most one phone number and at most one email address
  * SSN of each customer is unique
  * Each SSN has following format ‘NNN-NN-NNNN’, where N is a digit from 0-9.
  * Customers are responsible for the payment and always pay for themselves
  * Each customer has at most one payment method
  * Each non-null account number is unique across all customers
  * Customers pay their entire bill at time of check-out
* Reservations
  * Each reservation ID is unique across all hotels
  * Only a single room can be reserved by each reservation
  * Number of guests cannot exceed room maximum occupancy; otherwise, multiple distinct reservations must be made to intake all of guests
* Transactions
  * Each transaction ID is unique across the system
* Other
  * Room rate is measured per day
  * All addresses are composed of 4 components: street, city, state, and zip
  * A zip code uniquely identifies both a city and state (e.g. zip code functionally determines city and state [zip -> city, state])
  * The functional dependencies relating zip, city, and state (see above) hold across all entities (that contain those attributes). For example, given the functional dependency zip -> {city, state}, if one relation contains the tuple {27695, Raleigh, NC} every other relation (containing zip, city, and state) must have the same values {Raleigh, NC} for the tuple with zip 27695.
  * Any state stored in DBMS has two-letter value (e.g. NC for North Carolina, DC for Washington DC)

## Contributing
Please contact the authors for any contributions.
## Authors
* **Nathan Schnoor**
* **Nikolay G. Titov**
* **Preston Scott**
