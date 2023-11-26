import pyorient


class OrientDbConfig:
    def getOrientClient(self):
        return pyorient.OrientDB("localhost", 2424)

    def getSession(self):
        client = self.getOrientClient()
        session_id = client.connect("root", "admin")
        return session_id

    def makeQuery(self, query):
        client = self.getOrientClient()
        return client.query(query)

    def makeQueryCallBack(self, query: str, callback):
        client = self.getOrientClient()
        return client.query_async(query, callback)

    def createTable(self, createTableQuery: str, insertTableQuery: str):
        client = self.getOrientClient()
        table = client.command(createTableQuery)
        if not insertTableQuery:
            client.command(insertTableQuery)
        return table

    def findOne(self, id):
        client = self.getOrientClient()
        return client.record_load(id)

    def create(self, table, request):
        # request = { '@my_class': { 'accommodation': 'house', 'work': 'office', 'holiday': 'sea' } }
        client = self.getOrientClient()
        return client.record_create(table, request)

    def update(self, id, version, request):
        # request = {'@my_class': {'accommodation': 'hotel', 'work': 'home', 'holiday': 'hills'}}
        client = self.getOrientClient()
        return client.record_update(id, id, request, version)
