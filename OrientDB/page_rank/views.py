from django.shortcuts import render

from configurations.orient_db_config import OrientDBConfig
from utils.render_util import Utils


def manual(request):
    client = OrientDBConfig()
    tableName = "dogs"
    supperTable = "V"
    client.create_class(tableName, supperTable)
    record = client.get_orient_client().query('select from users')
    for k in record:
        print(k)
    return Utils.render_api_success(record)


def lib(request):
    return render(request, 'page_rank/lib.html')
