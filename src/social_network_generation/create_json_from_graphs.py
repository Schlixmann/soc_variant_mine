"""
This file creates a json document for the graph structure implemented and
can be used for graph objects created base on a text or event log.
"""

import json

def save_graphs_to_json_event_log(graphs: list, file_name: str, output_path):
    data = {}

    for i, graph in enumerate(graphs, start=1):
        graph_name = f"graph_{i:02d}"
        nodes = [{"resource": node} for node in graph['graph'][0]]
        edges = [{"resource_performer": edge[0], "resource_consumer": edge[1], "activity": edge[2]} for edge in graph['graph'][1]]

        graph_data = {'case_ids': graph['case_ids'], "nodes": nodes, "edges": edges}
        
        data[graph_name] = graph_data

    # JSON converter:
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    with open((output_path + file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    return json_output
