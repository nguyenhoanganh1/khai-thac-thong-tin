from django.http import HttpResponse
from django.shortcuts import render


class Utils:

    @staticmethod
    def render_api_success(data):
        return HttpResponse(data, 'application/json', 200)
    @staticmethod
    def render_template(request, template):
        return render(request, template)

