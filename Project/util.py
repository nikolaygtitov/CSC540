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
