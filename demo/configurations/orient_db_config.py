import pyorient
from utils.query_util import QueryUtil

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class OrientDBConfig:

    __metaclass__ = Singleton

    host = "localhost"
    port = 2424
    username = "root"
    password = "admin"
    database = "demo"

    """
    Connect
    """
    def get_orient_client(self):
        print("Connecting to the server...")
        client = pyorient.OrientDB(self.host, self.port)
        session_id = client.connect(self.username, self.password)
        print("OK - sessionID: ", session_id, "\n")

        if client.db_exists(self.database, pyorient.STORAGE_TYPE_PLOCAL):
            client.db_open(self.database, self.username, self.password)
            return client

        client.db_close()

    def close(self):
        client = self.get_orient_client()
        client.db_close()


    """
    Cluster
    """
    def create_cluster(self, cluster_name):
        client = self.get_orient_client()
        cluster =  client.data_cluster_add(cluster_name, pyorient.CLUSTER_TYPE_PHYSICAL)

        client.db_close()
        return cluster
    """
    Database
    """
    def create_database(self, db_name):
        client = self.get_orient_client()
        db = None
        if not client.db_exists(self.database, pyorient.STORAGE_TYPE_PLOCAL):
            db = client.db_create(db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)

        client.db_close()
        return db
    def check_database_exists(self, db_name):
        client = self.get_orient_client()
        return client.db_exists(db_name, pyorient.STORAGE_TYPE_MEMORY)

    def reload_db(self):
        client = self.get_orient_client()
        client.db_reload()

    def drop_database(self, db_name):
        client = self.get_orient_client()
        client.db_drop(db_name)

    """
    Table
    """
    def command(self, command):
        client = self.get_orient_client()
        client.command(command)

    def create_class(self, class_name, supper_table):
        client = self.get_orient_client()
        dbClasses = client.command("SELECT name FROM (SELECT expand(classes) FROM metadata:schema)")
        classFound = False
        for idx, val in enumerate(dbClasses):
            if (val.name == class_name):
                classFound = True
                break

        table = None

        if (classFound == False):
            table = client.command(QueryUtil.create_class(class_name, supper_table))
            print("Class " + class_name + " correctly created")
        else:
            print("Class " + class_name + " already exists into the DB")
        client.db_close()

        return table

    """
    Record
    """

    def make_query(self, query):
        client = self.get_orient_client()
        return client.query(query)
    def make_query_call_back(self, query: str, callback):
        client = self.get_orient_client()
        return client.query_async(query, callback)

    def get_one(self, id):
        client = self.get_orient_client()
        return client.record_load(id)

    def record_create_in_table(self, table, request):
        # request = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' } }
        print(table, request)
        client = self.get_orient_client()
        return client.record_create(table, request)

    def record_create_in_cluster(self, cluster_id, rec):
        # rec = {'@my_class': {'accommodation': 'house', 'work': 'office', 'holiday': 'sea'}}
        client = self.get_orient_client()
        rec_position = client.record_create(cluster_id, rec)
        return rec_position

    def record_update(self, rec_position_rid, rec_position_version, request):
        # request = {'@my_class': {'accommodation': 'hotel', 'work': 'home', 'holiday': 'hills'}}
        client = self.get_orient_client()
        return client.record_update(rec_position_rid, rec_position_rid, request, rec_position_version)

    def record_delete(self, cluster_id, rec_position_rid):
        client = self.get_orient_client()
        return client.record_delete(cluster_id, rec_position_rid)


    """
    Create Node
    """
    def create_node(self, node_type, properties):
        command = f"CREATE VERTEX {node_type} SET {properties}"
        self.client.command(command)

    def create_edge(self, edge_type, from_node, to_node):
        command = f"CREATE EDGE {edge_type} FROM {from_node} TO {to_node}"
        self.client.command(command)

    def create_node(self, class_name, node_data):
        client = self.get_orient_client()
        create_node_query = f"insert into {class_name} set {node_data}"
        client.command(create_node_query)


    def create_nodes(self, class_name, node_data_list):
        client = self.get_orient_client()
        try:
            for node_data in node_data_list:
                create_node_query = f"insert into {class_name} set name = '{node_data.get('name')}', url = '{node_data.get('url')}'"
                client.command(create_node_query)
        finally:
            client.db_close()

    def create_node_and_relations(self, node_data, in_neighbors_data, class_name='WebsiteRelation'):
        client = self.get_orient_client()

        try:
            create_node_query = f"CREATE VERTEX Website SET {node_data}"
            node_result = client.command(create_node_query)
            node_rid = node_result[0]._rid

            # Tạo các in-neighbors và thiết lập quan hệ
            for neighbor_data in in_neighbors_data:
                create_neighbor_query = f"CREATE EDGE {class_name} FROM {neighbor_data['in']} TO {node_rid} SET {neighbor_data}"
                client.command(create_neighbor_query)

        finally:
            # Đóng kết nối sau khi sử dụng
            client.db_close()

    def create_relationship(self, class_name, relationship_data_list):
        client = self.get_orient_client()
        try:
            for rel_data in relationship_data_list:
                create_rel_query = f"CREATE EDGE {class_name} FROM {rel_data['out']} TO {rel_data['in']} SET weight = :weight"
                params = {'weight': rel_data.get('weight', 1)}
                client.command(create_rel_query, params)
        finally:
            client.db_close()