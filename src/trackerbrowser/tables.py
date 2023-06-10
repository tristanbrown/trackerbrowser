"""Get the different relevant tables from Track & Graph"""

import pandas as pd
from .connection import connect

class DB():
    """"""
    def __init__(self, db_path):
        self.db_path = db_path

    def read_sql(self, query):
        """"""
        with connect(self.db_path) as conn:
            result = pd.read_sql_query(query, conn)
        return result

    @property
    def tables(self):
        """"""
        query = """SELECT name FROM sqlite_schema
            WHERE type='table' ORDER BY name;"""
        return self.read_sql(query)

    @property
    def groups(self):
        """"""
        query = """SELECT * FROM groups_table"""
        return self.read_sql(query)

    @property
    def trackers(self):
        """"""
        query = """SELECT * FROM features_table"""
        return self.read_sql(query)

    @property
    def datapoints(self):
        """"""
        query = """SELECT * FROM data_points_table"""
        return self.read_sql(query)
