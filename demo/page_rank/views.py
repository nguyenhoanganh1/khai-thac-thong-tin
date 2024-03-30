from django.http import JsonResponse
from django.shortcuts import render, redirect

from .Algorithm.page_rank import pagerank, HubPageRank_Algorithm, extract_node_id
from .WebCrawlerBFS.crawler import fetch_by_bfs
from .forms import WebsiteForm
from configurations.orient_db_config import OrientDBConfig
from configurations.spark_config import SparkConfig
from utils.render_util import Utils


def crawl_data(request):
    fetch_by_bfs()
    return Utils.render_api_success('')


def build_web_graph(data):
    web_graph = {}
    for edge in data:
        out_node = extract_node_id(edge.get("out"))
        in_node = extract_node_id(edge.get("in"))

        if out_node in web_graph:
            web_graph[out_node].add(in_node)
        else:
            web_graph[out_node] = {in_node}

        if in_node not in web_graph:
            web_graph[in_node] = set()

    return web_graph


def manual(request):
    client = OrientDBConfig()
    query = f"SELECT FROM References limit 1000"
    result = client.make_query(query)
    converted_edges = []
    for edge_data in result:
        out_link = edge_data.oRecordData['out']
        in_link = edge_data.oRecordData['in']
        converted_edges.append({"out": out_link, "in": in_link})

    # print(f"converted_edges = {converted_edges}")

    graph = build_web_graph(converted_edges)

    hub_scores, authority_scores, pr_scores = HubPageRank_Algorithm(graph, converted_edges, max_iterations=40)

    print("\nHub Scores:", hub_scores)
    print("\nAuthority Scores:", authority_scores)
    print("\nPageRank Scores:", pr_scores)

    result = {
        "hub_scores": hub_scores,
        "authority_scores": authority_scores,
        "pr_scores": pr_scores
    }

    return JsonResponse(result)

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
