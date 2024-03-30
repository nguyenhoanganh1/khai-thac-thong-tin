from collections import deque

def pagerank(graph, max_iterations=100, d=0.85, tolarance=1.0e-8):
    nodes = set(graph.keys())
    num_nodes = len(nodes)

    # Initialize PageRank scores
    pagerank_scores = {node: 1.0 / num_nodes for node in nodes}

    for iter in range(max_iterations):
        new_pagerank_scores = {}
        for node in nodes:
            new_pagerank_score = (1 - d) / num_nodes

            # Check incoming links
            for incoming_node, links in graph.items():
                if node in links:
                    num_outgoing_links = len(links)
                    new_pagerank_score += d * pagerank_scores[incoming_node] / num_outgoing_links

            new_pagerank_scores[node] = new_pagerank_score

        # Check for convergence
        delta = sum(abs(new_pagerank_scores[node] - pagerank_scores[node]) for node in nodes)
        print(f' - Số lần lặp [{iter}], delta = [{delta:6f}]')

        if delta < tolarance:
            print(f'Mô hình đạt ngưỡng bão hòa tại vòng lặp thứ: [{iter}]')
            break

        pagerank_scores = new_pagerank_scores

    print('Hoàn tất !\n')
    return pagerank_scores


def extract_node_id(link):
    # Extract node identifier from OrientDB record link
    return str(link.get_hash() if link else None)

def fetch_in_neighbors(data, x):
    in_neighbors = []
    for edge in data:
        if extract_node_id(edge.get("in")) == x:
            out_node = extract_node_id(edge.get("out"))
            if out_node is not None:
                in_neighbors.append(out_node)
    return in_neighbors


def HubPageRank_Algorithm(web_graph, data, max_iterations, d=0.85, beta=0.15, gamma=0.1, tolerance=1.0e-8):
    print('Bắt đầu tính toán trọng số Hub-PageRank của các website/webpage trong [web_graph]')

    # Initialize dictionaries to store scores
    hub_scores = dict.fromkeys(web_graph, 1.0)
    authority_scores = dict.fromkeys(web_graph, 1.0)
    pr_scores = dict.fromkeys(web_graph, 1.0)

    # Cấu trúc dictionary chứa rank-source cho mỗi nút - được xác định: beta / tổng số lượng các nút
    E_x = dict.fromkeys(web_graph, beta / len(web_graph))

    # Lặp quá trình tính toán h(x), a(x) và c(x) với số lần lặp [max_iterations]
    for iteration in range(max_iterations):
        last_hub_scores = hub_scores.copy()
        last_authority_scores = authority_scores.copy()
        last_pr_scores = pr_scores.copy()

        hub_scores = dict.fromkeys(last_hub_scores.keys(), 0)
        authority_scores = dict.fromkeys(last_authority_scores.keys(), 0)
        pr_scores = dict.fromkeys(last_pr_scores.keys(), 0)

        for node in hub_scores.keys():
            in_neighbors = fetch_in_neighbors(data, node)
            print(f"in_neighbors = {in_neighbors}")
            if len(in_neighbors) > 0:
                sum_hub_in_neighbors = sum(last_authority_scores[in_neighbor] for in_neighbor in in_neighbors)
                hub_scores[node] = d * sum_hub_in_neighbors

            out_neighbors = web_graph.get(node, set())
            if len(out_neighbors) > 0:
                sum_authority_out_neighbors = sum(last_hub_scores[out_neighbor] for out_neighbor in out_neighbors)
                authority_scores[node] = (1 - d) * sum_authority_out_neighbors + E_x[node]

            pr_scores[node] = (1 - gamma) * hub_scores[node] + gamma * authority_scores[node]

        # Bình thường hóa
        hub_norm_factor = 1.0 / max(hub_scores.values())
        authority_norm_factor = 1.0 / max(authority_scores.values())
        pr_norm_factor = 1.0 / max(pr_scores.values())

        for node in hub_scores:
            hub_scores[node] *= hub_norm_factor
            authority_scores[node] *= authority_norm_factor
            pr_scores[node] *= pr_norm_factor

        # Kiểm tra điều kiện dừng
        delta = max(
            max(abs(hub_scores[node] - last_hub_scores[node]) for node in hub_scores),
            max(abs(authority_scores[node] - last_authority_scores[node]) for node in authority_scores),
            max(abs(pr_scores[node] - last_pr_scores[node]) for node in pr_scores)
        )

        print(f' - Số lần lặp [{iteration}], delta = [{delta:6f}]')
        if delta < tolerance:
            print(f'Mô hình đạt ngưỡng bão hòa tại vòng lặp thứ: [{iteration}]')
            break

    print('Hoàn tất !\n')
    return hub_scores, authority_scores, pr_scores