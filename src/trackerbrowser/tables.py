"""Get the different relevant tables from Track & Graph"""

import pandas as pd
from pathlib import Path
from .connection import connect
from trackerbrowser import util

class DB:
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

    def get_datapoints(self, ids=None):
        """"""
        query = """SELECT * FROM data_points_table
        """
        if ids is not None:
            query += f"""WHERE feature_id IN {util.list_for_query(ids)}
        """
        return self.read_sql(query)

class TrackerFileSystem:
    """"""

    def __init__(self, db_path):
        self.db = DB(db_path)
        self._entities = None

    @property
    def entities(self):
        groups = self.db.groups
        trackers = self.db.trackers
        if self._entities is None:
            self._entities = pd.concat([
                groups[['id', 'name', 'display_index', 'parent_group_id']],
                trackers[['id', 'name', 'display_index', 'group_id']].rename({'group_id': 'parent_group_id'}, axis=1),
            ],
            keys=['group', 'tracker'], names=['entity_type', None]
            ).reset_index().drop('level_1', axis=1).set_index('id')
        return self._entities

    @staticmethod
    def path_parts(path):
        if not path.startswith('/'):
            path = '/' + path
        parts = Path(path).parts
        return (part.replace('/', '') for part in parts)

    def ls(self, path=''):
        split_path = self.path_parts(path)
        result = self.entities
        for segment in split_path:
            parent_group_id = result.loc[result['name'] == segment].index.to_list()[0]
            result = self.entities.loc[
                self.entities['parent_group_id'] == parent_group_id, :].sort_values('display_index')
        return result

    def get_tree(self, root):
        trackers = []
        merged = self.ls(root).reset_index()
        while not merged.empty:
            merged = merged[['id', 'entity_type', 'name']]
            trackers.append(merged[merged['entity_type'] == 'tracker'].copy())
            parent_groups = merged[merged['entity_type'] == 'group'].copy()
            merged = pd.merge(
                how='left',
                left=parent_groups[['id', 'name']],
                right=self.entities.reset_index()[['parent_group_id', 'id', 'entity_type', 'name']],
                left_on='id',
                right_on='parent_group_id'
            )
            merged['name'] = merged['name_x'] + "/" + merged['name_y']
            merged = merged.rename({'id_y': 'id'}, axis=1)

        result = pd.concat(trackers).rename({'name': 'path'}, axis=1).drop('entity_type', axis=1)
        return result.sort_values('id').set_index('id')
