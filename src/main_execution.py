"""
This file is responsible for execution. Run this file to execute the whole social mining process from text, event logs
and a corresponding compliance check
"""

import os
import json

# Imports for event log pre-processing
from social_network_generation.social_network_generation_event_log.pre_processing.pre_process_event_log_generator import \
    create_network_distinct_traces_of_event_log_pre_process_json

# Create graph data structure from pre-processed event log
from social_network_generation.social_network_generation_event_log.graph_construction.transform_pre_process_to_graph import \
    create_graph as create_graph_from_event_log

# Create json from graph data:
from social_network_generation.create_json_from_graphs import \
    save_graphs_to_json_event_log

# visualize the graph structure
from visualization.visualization.visualizer import \
    visualize_directed_graph

# Pm4Py implementations
import pm4py
from social_network_generation.social_network_generation_event_log.pm4py_sna_statistics.pm4py_social_network_resource_analysis import \
    working_together, handover_of_work

# This main method executes the whole process in one run
def pre_process_event_log_for_snm():
    
    """
    # TEST Event Log:
    path_log_test = os.path.join(os.getcwd(), "data/test/test_event_log.csv")
    
    # Required data:
    log_file_path = path_log_test
    case_id_column_name = 'concept:instance'
    activity_column_name = 'concept:name'
    timestamp_key_name = 'time:timestamp'
    # Check the resource key name, sometimes it can be the case that role is used sometimes it can be the case that unit is used
    resource_key_name = 'org:unit'
    used_separator = ','
    # Pre-processing
    file_name_pre_process_event_log = 'test_snm'
    output_path_pre_process = os.path.join(os.getcwd(),'results/pre_processed_el/')
    """
    
    # Input Real-World Event Log:
    path_log_klinklogs_slim = os.path.join(os.getcwd(), "snm_HM/data/Playground/Klinkdaten_FULL_documentation_rid.csv")

    # Required data:
    log_file_path = path_log_klinklogs_slim
    case_id_column_name = 'rid'
    activity_column_name = 'concept:name'
    timestamp_key_name = 'time:timestamp'
    # Check the resource key name, sometimes it can be the case that role is used sometimes it can be the case that unit is used
    resource_key_name = 'org:resource'
    used_separator = ','
    # Pre-processing
    file_name_pre_process_event_log = 'kliniklogs_2022_converted_documentation_slim_snm_new'
    output_path_pre_process = os.path.join(os.getcwd(),'results/pre_processed_el/')
    
    # Create pre-processed output file for specified log: Bicycle:
    create_network_distinct_traces_of_event_log_pre_process_json(dataframe_input_path=log_file_path,
                                                                 case_id_column_name=case_id_column_name,
                                                                 activity_column_name=activity_column_name,
                                                                 timestamp_key_name=timestamp_key_name,
                                                                 resource_key_name=resource_key_name,
                                                                 used_separator=used_separator,
                                                                 file_name=file_name_pre_process_event_log,
                                                                 output_path=output_path_pre_process)

    output_path_pre_process = output_path_pre_process + file_name_pre_process_event_log + ".json"
    print(output_path_pre_process)

def create_graphs():
    
    """
    TEST Pre-Processed Event Log
    
    # Path to pre-processed event log
    path_pre_processed_event_log = os.path.join(os.getcwd(), "results/pre_processed_el/test_snm.json")
    graphs_event_log = create_graph_from_event_log(pre_processed_el_json_path=path_pre_processed_event_log)
    # Graphs constructed from the event log
    graphs_event_log_file_name = "test_graphs"
    output_path_graphs_event_log =  os.path.join(os.getcwd(), "results/snm_el/graphs/")
    """
    
    # Path to pre-processed event log
    path_pre_processed_event_log = os.path.join(os.getcwd(), "snm_HM/results/pre_processed_el/kliniklogs_2022_converted_documentation_slim_snm_new.json")
    graphs_event_log = create_graph_from_event_log(pre_processed_el_json_path=path_pre_processed_event_log)
    # Graphs constructed from the event log
    graphs_event_log_file_name = "klinik_example_graphs"
    output_path_graphs_event_log =  os.path.join(os.getcwd(), "snm_HM/results/snm_el/graphs/")
    

    # Change Parameters to create the graphs for each trace in log
    save_graphs_to_json_event_log(graphs=graphs_event_log,
                                  file_name=graphs_event_log_file_name,
                                  output_path=output_path_graphs_event_log)

    
def visualize_graphs():
    
    """
    TEST Event Log graph data
    
    graphs_event_log  = os.path.join(os.getcwd(), "results/snm_el/graphs/klinik_example_graphs.json")
    visualization_file_name = "test_graphs_visualisation"
    output_path_visualizations_standard_event_log = os.path.join(os.getcwd(), "results/snm_el/visualizations/test/")
    """
    
    graphs_event_log  = os.path.join(os.getcwd(), "snm_HM/results/snm_el/graphs/klinik_example_graphs.json")
    visualization_file_name = "klinik_example_graphs_visualisation"
    output_path_visualizations_standard_event_log = os.path.join(os.getcwd(), "snm_HM/results/snm_el/visualizations/klinik_example/")
    
    # Load JSON content from the file
    with open(graphs_event_log, 'r', encoding='utf-8') as json_file:
        graph_list = json.load(json_file)
        
    counter = 0

    # Iterate through the graph list
    for graph_key, graph_value in graph_list.items():
        print(f"Processing {graph_key}...")
        
        # Extract nodes and edges from the graph
        node_list = graph_value['nodes']
        edge_list = graph_value['edges']

        visualize_directed_graph(vertices=node_list,
                                 edges=edge_list,
                                 output_path=output_path_visualizations_standard_event_log,
                                 output_file_name=visualization_file_name + "_trace_" + str(counter+1))

        counter = counter + 1


"""
def pm4py_snm():
    # General Home, Absolute Path
    # home_path = setup_environment()

    # TODO: Event Log File Paths:
    # Input Synthetic Event Logs:

    # Bicycle Manufacturing:
    # path_log_bm = "/data/input/log/selected/BM_event_log.csv"
    # log_file_path_bm = home_path + path_log_bm

    # Schedule Meeting:
    # path_log_sm = "/data/input/log/selected/SM_event_log.csv"
    # log_file_path_sm = home_path + path_log_sm

    # Running Example:
    # path_log_re = "/data/input/log/selected/RE_event_log.csv"
    # log_file_path_re = home_path + path_log_re

    # Input Real-World Event Log:
    # BPIC:
    path_log_bpic = "/data/input/log/selected/BPIC_SNG_EL_Eval/PermitLog.csv"
    log_file_path_bpic = path_log_bpic

    path_log = log_file_path_bpic
    case_id_name_log = "concept:instance"
    activity_name_in_log = "concept:name"
    resource_key = "org:role"

    try:
        # The Working together metric calculates how many times two individuals work together for resolving a process instance.
        wt_values = working_together(path_log=path_log,
                                     case_id_name_in_log=case_id_name_log,
                                     activity_name_in_log=activity_name_in_log,
                                     resource_key=resource_key)

        # Visualize working together
        pm4py.view_sna(wt_values)

        # The Handover of Work metric measures how many times an individual is followed by another individual in the execution of a business process.
        hw_values = handover_of_work(path_log=path_log,
                                     case_id_name_in_log=case_id_name_log,
                                     activity_name_in_log=activity_name_in_log,
                                     resource_key=resource_key)

        # Visualize Handover of work
        pm4py.view_sna(hw_values)

    except ValueError:
        pass
"""

if __name__ == "__main__":
    # Pre-Process Event log for SNM:
    pre_process_event_log_for_snm()
    print("Event Log pre-processed!")
    
    # Create Graph data
    create_graphs()
    print("Graphs created!")
    
    # Visualize Graph data
    visualize_graphs()
    print("Graphs visulaized!")
    
