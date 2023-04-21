"""Get the different relevant tables from Track & Graph"""

import pandas as pd

def list_tables(conn):
    """"""
    query = """SELECT name FROM sqlite_schema
        WHERE type='table' ORDER BY name;"""
    return pd.read_sql_query(query, conn)

def get_groups(conn):
    """"""
    query = """SELECT * FROM groups_table"""
    return pd.read_sql_query(query, conn)

def get_trackers(conn):
    """"""
    query = """SELECT * FROM features_table"""
    return pd.read_sql_query(query, conn)

def get_datapoints(conn):
    """"""
    query = """SELECT * FROM data_points_table"""
    return pd.read_sql_query(query, conn)
