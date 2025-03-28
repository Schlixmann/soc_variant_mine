"""
This file and the corresponding methods are responsible tp create the pre-processed event log which can be used for
resource-activity compliance verification.
"""
from pandas import DataFrame
import json
import os

from social_network_generation.social_network_generation_event_log.pre_processing.extractors_pre_processing_event_log.extraction_to_data_frame import \
    get_data_frame
from social_network_generation.social_network_generation_event_log.pre_processing.extractors_pre_processing_event_log.extraction_to_event_log import \
    convert_df_to_event_log


def create_network_distinct_traces_of_event_log_pre_process_json(dataframe_input_path: str,
                                                                 case_id_column_name: str,
                                                                 activity_column_name: str,
                                                                 timestamp_key_name: str,
                                                                 resource_key_name: str,
                                                                 used_separator: str,
                                                                 file_name: str,
                                                                 output_path: str):
    # Get pandas dataframe out of the file
    dataframe = __load_data_frame(dataframe_input_path,
                                  case_id_column_name,
                                  activity_column_name,
                                  timestamp_key_name,
                                  used_separator)
    print("Data Frame loaded!")
    
    # Get Event Log based on dataframe, according to XES Meta model
    event_log = convert_df_to_event_log(df=dataframe)
    print("Custom Event Log loaded!")

    # List of: Network of Resource Performer, Resource Consumer, and Activity:
    resulting_networks_of_distinct_traces = event_log.get_network_output_of_distinct_traces_in_event_log(resource_structure_type=resource_key_name)
    data = {"pairs": resulting_networks_of_distinct_traces}
    print("Graph structure loaded!")

    # Ensure the directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # JSON converter
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)

    # Write results in new .json file in the output folder
    with open(os.path.join(output_path, file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    return json_output

# Helper method to load the data frame which is based on the XES event log
# @private
def __load_data_frame(path: str, case_id_column_name: str, activity_column_name: str,
                      timestamp_key_name: str, used_separator: str) -> DataFrame:
    # Error checking
    possible_activity_id_column_names = ["", " "]
    if case_id_column_name in possible_activity_id_column_names and not activity_column_name == type(str):
        raise ValueError("Invalid activity_check_one name.")

    possible_case_id_column_names = ["", " "]
    if case_id_column_name in possible_case_id_column_names and not case_id_column_name == type(str):
        raise ValueError("Invalid case id/ trace id name.")

    possible_separators = [";", ",", ":", "-"]
    if used_separator not in possible_separators:
        raise ValueError("Invalid separator between column values. Expected one of: %s" % possible_separators)

    return get_data_frame(path, case_id_column_name, activity_column_name, timestamp_key_name, used_separator)
