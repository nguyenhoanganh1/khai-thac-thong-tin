class QueryUtil:

    @staticmethod
    def create_class(tableName: str, supperTable):
        return "create class {} extends {}".format(tableName, supperTable)

    @staticmethod
    def create_database(databaseName: str):
        return "create database {}".format(databaseName)

    @staticmethod
    def insert_record_to_table(tableName, request: dict):
        query = "insert ỉnto table {}".format(tableName)
        if not request:
            query += " set "
            for k, v in request.items():
                query += " {} = '{}' ".format(k, v)
        return query