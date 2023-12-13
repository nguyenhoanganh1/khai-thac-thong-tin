from django.shortcuts import render, redirect

from .forms import WebsiteForm
from configurations.orient_db_config import OrientDBConfig
from configurations.spark_config import SparkConfig
from utils.render_util import Utils


def manual(request):
    client = OrientDBConfig()
    spark = SparkConfig()
    result = spark.load_class_data("users")
    print(result)
    return Utils.render_api_success()


def lib(request):
    spark = SparkConfig()
    data = spark.load_class_data("users")
    print(data)
    return render(request, 'page_rank/lib.html')

def website_list(request):
    client = OrientDBConfig()
    websites = client.get_orient_client().query('select from Website')
    return render(request, 'page_rank/website_list.html', {'websites': websites})


def create_website(request):
    client = OrientDBConfig()
    class_name = 'Website'
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            node_data = {'name': name, 'url': url}
            result = client.create_node(class_name, [node_data])
            print(result)
            return redirect('website_list')
    else:
        form = WebsiteForm()

    return render(request, 'page_rank/create_website.html', {'form': form})
