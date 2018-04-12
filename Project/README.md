# CSC 540 (601) - Database Management Concepts and Systems

# Course Project

## Wolf Inn: Popular Hotel Chain Database System
The design and development processes of Database Management System for WolfInns
are completed in the Project Report 1 and Project Report 2.
### Description of the Project:
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
### Description of the Software:
This program allows retrieving, storing, manipulating and deleting any data
from the DBMS through various user-friendly applications instead of direct
interaction with MariaDB MySQL server via MySQL queries, such as SELECT,
INSERT, UPDATE, and DELETE.
The architecture of the software is designed as follows:
```
+---------------+     +---------------+    +-------------+     +------------+
|      UI       |     |    Client     |    |    APIs     |     |  DATABASE  |
|  hotelsoft.py | ->  | appsclient.py | -> |   apps.py   |  -> |   MariaDB  |
+---------------+     +---------------+    +-------------+     +------------+
```
The entire front-end interaction between a user and the program takes place via
UI, which is a menu driven system that enables interaction with the back-end
database.

The following is a sample of menu driven system of the implemented UI:
```
Here the output of UI
```

All of the following queries are performed in the back-end on the default MySQL
MariaDB NCSU Server at [classdb2.csc.ncsu.edu](https://courses.ncsu.edu/csc540/lec/001/wrap/FAQ_general.html):
* __*SELECT*__
* __*INSERT*__
* __*UPDATE*__
* __*DELETE*__

### File Contents and Descriptions:
The following is the list of existing files required by the program and their
content.
#### *hotelsoft.py*
This is the main file that gets executed from the prompt by a user to initiate
the program. It connects to the NCSU MySQL MariaDB Server as specified in the
default MySQL settings/parameters in the code. 

In order to connect to different
database, please consider changing the following default database parameters
in the code:
```
db = maria_db.connect(host=DESIRED_HOST, user=USER_NAME,
                      password=PASSWORD, database=DATABASE)
```
This file contains the classes comprising the user interface for the WolfInn
Database Management System. The UI is a menu driven system that enables
interaction with the backend database. The UI functions communicate with the
Apps API through a Client class which aggregates common functionality.
#### *apps.py*
This file provides all required APIs for full interaction between front-end and
back-end programs. The APIs are constructed with the wrappers around MySQL
queries allowing the front-end (UI) to call appropriate functions performing
MySQL interactions. MySQL interactions include retrieving, storing, updating,
and deleting data from/into database. All query wrappers are enclosed within
a single class Apps.


To make a call to any of the APIs, the Apps class must be instantiated.
It has several private functions that serve as internal helper functions and
not intended to be referenced by either front-end of back-end.


All APIs are self-explanatory and do exactly what they are designed to do.
Some APIs perform several operations/tasks on the database. For example,
check-out API does the following operations:
  1. Updates *Reservations* table with *'check_out_time'* value
  2. Frees all the assigned Staff to that reservation by updating *Staff* table
with *NULL* values for *'assigned_hotel_id'* and *'assigned_room_number'*
attributes of all Staff that are serving this reservation
  3. Generates and inserts new transaction into *Transactions* table by
calculating the difference between the *'start_date'* and *'end_date'* values,
and multiplying it by the room's *'rate'*.


Following is the list APIs that may perform more than one operation at a time:
* *add_staff()* - also performs *assign_staff_to_room()* API if corresponding
attributes specified
* *update_staff()* - also performs *assign_staff_to_room()* API if
corresponding attributes specified
* *add_reservation()* - also performs *check-in()/check-out()* APIs and may
call *update_staff()* API if corresponding attributes specified
* *update_reservation()* - also performs *check-in()/check-out()* APIs and may
call *update_staff()* API if corresponding attributes specified
#### *apihelper.py*
Describe it here... Copy from comments
#### *appsclient.py*
Describe it here... Copy from comments
#### *demo_data.py*
Describe it here... Copy from comments
#### *queries.py*
Describe it here... Copy from comments
#### *util.py*
Describe it here... Copy from comments

### Database Management System
Currently the program initiates connection with the default MySQL MariaDB
Server at the NCSU. In order to successfully establish connection with the NCSU
MySQL Server, which behind firewall and drops all external connection attempts,
use one of the two following options. Note: If default database parameters are
changed, ignore both options below (unless DBMS used is at the NCSU MySQL
Server).
* Option 1: Establish connection through NCSU VPN. Installation of Cisco
AnyConnect VPN Software is required. Installation instructions of Cisco
AnyConnect can be found [here](https://oit.ncsu.edu/campus-it/campus-data-network/network-security/vpn/)

* Option 2: Pull or copy source code to the NCSU remote machine and run the
program there:
```
scp * unity_id@remote.eos.ncsu.edu:/afs/unity.ncsu.edu/users/u/unity_id/CSC540
```
*Note:* Some of the required libraries, tools and other packages (e.g. pandas,
mysql.connector, tabulate, and etc.) may be missing at the NCSU servers.
Administrator's permissions are required to install any missing environment
libraries or tools.

### Intended Users:
The program is written without any security constraints, such as user
permissions and others. All the data is fully retrievable from the MariaDB
MySQL regardless permissions.

## Run the Software:
To start the program that connects to a default DBMS (MariaDB MySQL Server at
the NCSU) run the following command:
```
 > python hotesoft.py [-options]

   OPTIONS
   -c: run in check mode (Enable MySQL CHECK constraints in the program)
```
Note that default DBMS (MariaDB MySQL Server at the NCSU) version ignores all
the `CHECK` and `NOT NULL` constraints for insert and update operations.
To enable assertions within the program itself, ensuring that data to be
inserted or updated obeys MySQL constraints, run the program with `-c` option:
```
 > python hotesoft.py -c
```

## Configurations and Specifications:
The following describes environment configurations and software specifications. 
### Language:
Python
### Prerequisites:
*	Python version >= 2.7
* OS: any Linux distribution (Ubuntu, RedHat, etc) that has Python version >=
2.7
*	DBMS version: Ver 15.1 Distrib 5.5.57-MariaDB, for Linux (x86_64) using
readline 5.1
* DBMS must contain all necessary/required tables for proper and correct
software behavior
  * To create required tables in the DBMS, run the following:
* Tables may contain some data or be empty
### Constraints and Assumptions:
The following is list of reasonable assumptions our team had to make due to the
absence of real customer and lack of all/additional requirements and
specifications.

*Note*: Some of the constraints can be ignored if program executes without
check option `-c`.
* Hotels
  * Each hotel is uniquely identified by its ID.
  * Each hotel has at most one manager at a time.
  * Each hotel has a unique address information: *{street, city, state, zip}*
  attribute values are unique per hotel. Since zip code functionally determines
  *city* and *state* *[zip -> city, state]* (see below in section Other),
  *{street, zip}* attribute values are unique per hotel.
  * Maximum occupancy of any room at any hotel must not exceed *9 (nine)*
  guests.
  * The number of room(s) does not change once the Hotel is in use.
* Staff
  * Each member of hotel Staff is uniquely identified by his or her ID.
  * Each member of the Staff has at most one phone number.
  * Each member of the Staff works for exactly one hotel at a time.
  * Dedicated staff can be assigned to any Rooms other than presidential suites
  (e.g., per customer’s request).
  * Any member of the Staff can be assigned to any given room.
  * Billing staff work from the corporate office and do not serve customers.
  * Teaching staff, students, and developers (Team 2) may play the role of the
  Owners/Operators.
* Customers
  * Each customer is uniquely identified by his or her customer ID.
  * Each customer has at most one phone number and at most one email address.
  * SSN of each customer is unique.
  * Each SSN has following format *'NNN-NN-NNNN'*, where *N* is a digit in
  range of *0-9*.
  * Customers are responsible for the payment and always pay for themselves.
  * Each customer has at most one payment method.
  * Each non-null account number is unique across all customers.
  * Customers pay their entire bill at time of check-out.
* Reservations
  * Each reservation ID is unique across all hotels.
  * Only a single room can be reserved by each reservation.
  * Number of guests cannot exceed room maximum occupancy; otherwise, multiple
  distinct reservations must be made to intake all of guests.
* Transactions
  * Each transaction ID is unique across the system.
* Other
  * Room rate is measured per day.
  * All addresses are composed of *4* components: *street, city, state,* and
  *zip*
  * A zip code uniquely identifies both a city and state (e.g. *zip* code
  functionally determines *city* and *state [zip -> city, state]*)
  * The functional dependencies relating *zip, city,* and *state* (see above)
  hold across all entities (that contain those attributes). For example, given
  the functional dependency *zip -> {city, state}*, if one relation contains
  the tuple *{27695, Raleigh, NC}* every other relation (containing *zip,
  city,* and *state*) must have the same values *{Raleigh, NC}* for the tuple
  with zip *27695*.
  * Any state stored in DBMS has two-letter value (e.g. *NC* for North
  Carolina, *DC* for Washington DC)

## Contributing
Please contact the authors for any contributions.
## Authors
* **Nathan Schnoor** (nfschnoo@ncsu.edu)
* **Nikolay G. Titov** (ngtitov@ncsu.edu)
* **Preston Scott** (pdscott2@ncsu.edu)
