from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import status


class Utils:

    def __init__(self, request, template):
        self.request = request
        self.template = template

    def renderApi(self, context=None, using=None):
        content = loader.render_to_string(self.template, context, self.request, using=using)
        return HttpResponse(content, 'application/json', 200)

    def renderTemplate(self):
        return render(self.request, self.template)

