""""""
import os
import re
import sqlite3

def connect(path):
    """"""
    return sqlite3.connect(path)

def list_backups(directory):
    """"""
    r = re.compile(r"TrackAndGraphBackup-\d{8}-\d{6}.db")
    return [fname for fname in os.listdir(directory) if r.match(fname)]

def get_latest_backup(directory):
    """"""
    return sorted(list_backups(directory))[-1]

def connect_latest(directory):
    """"""
    filename = get_latest_backup(directory)
    path = os.path.join(directory, filename)
    return connect(path)
