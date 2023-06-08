"""Get the different relevant tables from Track & Graph"""

import pandas as pd
from .connection import connect

def read_sql(path, query):
    """"""
    with connect(path) as conn:
        result = pd.read_sql_query(query, conn)
    return result

def list_tables(path):
    """"""
    query = """SELECT name FROM sqlite_schema
        WHERE type='table' ORDER BY name;"""
    return read_sql(path, query)

def get_groups(path):
    """"""
    query = """SELECT * FROM groups_table"""
    return read_sql(path, query)

def get_trackers(path):
    """"""
    query = """SELECT * FROM features_table"""
    return read_sql(path, query)

def get_datapoints(path):
    """"""
    query = """SELECT * FROM data_points_table"""
    return read_sql(path, query)
