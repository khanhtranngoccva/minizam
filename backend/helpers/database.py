import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect("host=localhost port=8888 dbname=minizam user=minizam password=minizam")


class AtomicConnection:
    def __init__(self):
        self.connection = get_connection()
        self.cursor: psycopg.Cursor = self.connection.cursor(row_factory=dict_row)

    def __enter__(self):
        self.cursor.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.__exit__(exc_type, exc_val, exc_tb)
        # Autocommit if no exception happens
        if exc_type is None and exc_val is None:
            self.connection.commit()


def setup_database():
    from helpers.analysis.sample import Sample
    from helpers.analysis.fingerprinting import Fingerprint

    Sample.setup_table()
    Fingerprint.setup_table()
