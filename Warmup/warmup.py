"""
warmup.py

CSC 540 (601) - Database Management concepts and Systems
Warm up Homework
This program implements the solution for the Warm up Homework.

It connects to MySQL MariaDB Server at NCSU, creates very basic table of CATs
along with their attributes, such as:
 - Name
 - Type
 - Age
 - Weight
 - Sex
Then it makes very basic query to retrieve each cat's name and weight.

Execute the program run:
 > python warmup.py

@version: 1.0
@todo: None
@since: January 18, 2018

@status: Complete, Trial
@requires: Connection to MariaDB server at the NCSU.
           Option 1: Establish connect through NCSU VPN.
           Installation of Cisco AnyConnect VPN Software is required.
           Installation instractions can be found here:
               https://oit.ncsu.edu/campus-it/campus-data-network/network
              -security/vpn/
           Option 2: Pull or copy source code to the NCSU remote machine and
           run it there:
               scp warmup.py unity_id@remote.eos.ncsu.edu:/afs/unity.ncsu.edu
               /users/u/unity_id

@contact: nfschnoo@ncsu.edu
          ngtitov@ncsu.edu
          pdscott2@ncsu.edu
          smdimig@ncsu.edu

@authors: Nathan Schnoor
          Nikolay G. Titov
          Preston Scott
          Stephen Dimig

"""

# Import required Python and MySQL libraries
import mysql.connector as mariadb
from tabulate import tabulate
# from pandas.io import sql
# import pymysql
import pandas as pd

# Initialization of constants
# Change all the constants accordingly USER, PASSWORD, DB
HOST = 'classdb2.csc.ncsu.edu'
USER = 'unity_id'
PASSWORD = 'student_id'
DB = 'db'

# Actual program starts here
# Establish a DB connection
mariadb_connection = mariadb.connect(host=HOST, user=USER, password=PASSWORD,
                                     database=DB)
cursor = mariadb_connection.cursor()

# Create table CATs along with their attributes
try:
    cursor.execute("CREATE TABLE CATS (CNAME VARCHAR(20), TYPE VARCHAR(30), "
                   "AGE INTEGER, WEIGHT FLOAT, SEX CHAR(1))")
    cursor.execute("INSERT INTO CATS VALUES ('Oscar', 'Egyptian Mau', 3, "
                   "23.4, 'F')")
    cursor.execute("INSERT INTO CATS VALUES ('Max', 'Turkish Van Cats', 2, "
                   "21.8, 'M')")
    cursor.execute("INSERT INTO CATS VALUES ('Tiger', 'Russian Blue', 1, "
                   "13.3, 'M')")
    cursor.execute("INSERT INTO CATS VALUES ('Sam', 'Persian Cats', 5, 24.3, "
                   "'M')")
    cursor.execute("INSERT INTO CATS VALUES ('Simba', 'Americal Bobtail', 3, "
                   "19.8, 'F')")
    cursor.execute("INSERT INTO CATS VALUES ('Lucy', 'Turkish Angora Cats', "
                   "2, 22.4, 'F')")
    mariadb_connection.commit()

except mariadb.Error as error:
    print 'Error: {}'.format(error)

# Query for the name and weight of each cat in MariaDB
query = "SELECT CNAME, WEIGHT FROM CATS"
df = pd.read_sql(query, con=mariadb_connection)

# Print result of the query
print tabulate(df, headers=df.columns.values.tolist(), tablefmt='psql')

# Close DB connection
mariadb_connection.close()
