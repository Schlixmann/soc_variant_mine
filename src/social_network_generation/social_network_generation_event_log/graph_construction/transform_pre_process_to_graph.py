"""
This file provides methods that transforms the json document to a graph data structure.
"""

import json

def create_graph(pre_processed_el_json_path: str):
    # Output List:
    trace_network_results = []

    # list of network structure for each trace:
    structure_list = __get_list_from_json(json_file_path=pre_processed_el_json_path)

    # Go through every trace and create a network for every trace:
    for structure in structure_list:
        structure_network = structure['network_trace']

        node_list = __create_nodes(structure_network=structure_network)
        edge_list = __create_edges(structure_network=structure_network)

        # List of graphs for each trace as tuple:
        # Additionally return id and corresponding case ids for each trace
        trace_network_results.append({'id': structure['id'], 'case_ids': structure['case_ids'], 'graph': (node_list, edge_list)})

    return trace_network_results

# Creates nodes from the json pre-process document
# @private
def __create_nodes(structure_network: list[dict]):
    # Using a set for faster membership checking and insertion
    node_set = set()

    for network_value in structure_network:
        performer = network_value.get("Resource Performer", "")
        consumer = network_value.get("Resource Consumer", "")

        # If resource == consumer, only add the consumer if it is not empty
        if performer == consumer and consumer:
            node_set.add(consumer)
        else:
            # Add performer if it's not empty
            if performer:
                node_set.add(performer)
            # Add consumer if it's not empty
            if consumer:
                node_set.add(consumer)

    # Convert the set back to a list before returning (if list is needed)
    return list(node_set)

def __create_edges(structure_network: list[dict]):
    # Output List
    edge_set = set()

    # Go through values in the network
    for network_value in structure_network:
        if network_value["Resource Performer"] != "" and network_value["Resource Consumer"] != "":
            edge_set.add((network_value["Resource Performer"], network_value["Resource Consumer"], network_value["Activity"]))

    return list(edge_set)

def __get_list_from_json(json_file_path: str):
    # Get Json
    with open(json_file_path) as json_file:
        pre_processed_event_log = json.load(json_file)
    # Get pre-processed Event log data
    structure_list = pre_processed_event_log["pairs"]
    
    return structure_list