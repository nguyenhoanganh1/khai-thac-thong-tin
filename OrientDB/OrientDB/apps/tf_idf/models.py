from django.forms import models


class SearchRequest(models.Model):
    searching =  models.CharField()
