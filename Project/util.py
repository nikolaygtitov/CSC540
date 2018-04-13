"""
util.py

CSC 540 (601) - Database Management Concepts and Systems
Project for CSC 540

Description of the Project and Software read in the main program: hotelsoft.py

Description of the util.py file:
This file provides a library of functions used throughout this project.
One of these functions provides a simple way to wrap code in a sql transaction, that
will automatically commit or rollback on an error.
Another function provides a mechanism to print any exception caught.

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
    """
    Implements SQL commit/rollback transaction.
    Any code that executes successfully will commit.
    If an exception is caught, the transaction will rollback,
    then re-raise the exception.

    Example:
    with sql_transaction(db):
        <sql_operation_1>
        <sql_operation_2>
    :param con: The database connection
    :return: None
    """
    try:
        yield
        con.commit()
    except Exception as e:
        con.rollback()
        raise e


@contextmanager
def print_error():
    """
    Prints any exception caught in the wrapped code.
    :return: None
    """
    try:
        yield
    except Exception as error:
        print '\n'
        print error
        print '\n'
