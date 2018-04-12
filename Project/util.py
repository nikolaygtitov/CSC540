"""
util.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the util.py file:

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

from contextlib import contextmanager


@contextmanager
def sql_transaction(con):
    try:
        yield
        con.commit()
    except Exception as e:
        con.rollback()
        raise e


@contextmanager
def print_error():
    try:
        yield
    except Exception as error:
        print '\n'
        print error
        print '\n'
