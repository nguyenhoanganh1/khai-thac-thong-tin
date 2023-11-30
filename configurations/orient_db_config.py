import pyorient
from pyorient.utils import Singleton

from utils.query_util import QueryUtil


class OrientDbConfig:
    host = "localhost"
    port = 2424
    username = "root"
    password = "admin"

    __metaclass__ = Singleton

    def open_database(self, databaseName):
        client = self.get_orient_client(self)
        return client.db_open(databaseName, self.username, self.password)

    def get_orient_client(self):
        client = pyorient.OrientDB(self.host, self.port)
        client.set_session_token(True)
        return client

    def get_session(self):
        client = self.get_orient_client(self)
        session_id = client.connect(self.username, self.password)
        return session_id

    def make_query(self, query):
        client = self.get_orient_client(self)
        return client.query(query)

    def make_query_call_back(self, query: str, callback):
        client = self.get_orient_client(self)
        return client.query_async(query, callback)

    def check_database_exists(self, databaseName):
        client = self.get_orient_client(self)
        return client.db_exists(databaseName, pyorient.STORAGE_TYPE_MEMORY)

    def get_one(self, id):
        client = self.get_orient_client(self)
        return client.record_load(id)

    def create(self, table, request):
        # request = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' } }
        client = self.get_orient_client(self)
        return client.record_create(table, request)

    def create_cluster(self, clusterName):
        client = self.get_orient_client(self)
        return client.data_cluster_add(clusterName, pyorient.CLUSTER_TYPE_PHYSICAL)

    def create_database(self, databaseName):
        client = self.get_orient_client(self)
        return client.db_create(databaseName, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)

    def create_class(self, tableName: str, insertTableQuery: None):
        client = self.get_orient_client(self)
        create_class_query = client.command(QueryUtil.create_class(tableName))
        table = client.command(create_class_query)
        if not insertTableQuery:
            client.command(insertTableQuery)
        return table

    def record_create(self, cluster_id, rec):
        # rec = {'@my_class': {'accommodation': 'house', 'work': 'office', 'holiday': 'sea'}}
        client = self.get_orient_client(self)
        rec_position = client.record_create(cluster_id, rec)
        return rec_position

    def record_update(self, rec_position_rid, rec_position_version, request):
        # request = {'@my_class': {'accommodation': 'hotel', 'work': 'home', 'holiday': 'hills'}}
        client = self.get_orient_client(self)
        return client.record_update(rec_position_rid, rec_position_rid, request, rec_position_version)

    def record_delete(self, cluster_id, rec_position_rid):
        client = self.get_orient_client(self)
        return client.record_delete(cluster_id, rec_position_rid)
