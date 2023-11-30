from functools import wraps

from django.db.migrations import serializer
from django.http import JsonResponse
from rest_framework import status

from configurations.orient_db_config import OrientDbConfig
# from configurations.spark_config import SparkConfig
from utils.render_util import Utils


class PageRankView:

    def create_database(self):
        config = OrientDbConfig
        database = config.create_database(config, "user")
        response = {
            'id': 1,
            'name': database
        }
        return JsonResponse(response)

    def manual(self):
        template = 'page_rank/manual.html'
        session_id = OrientDbConfig.get_session
        utils = Utils(self, template)
        return utils.renderTemplate()
