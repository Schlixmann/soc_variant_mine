import os
import json
from pathlib import Path

FILE_PATH = "snm_HM/results/pre_processed_el/kliniklogs_2022_converted_documentation_slim_snm_new.json"
OUT_PATH = "snm_HM/results/pre_processed_el/kliniklogs_2022_converted_documentation_slim_snm_out.json"

def aggregate_traces(file:Path, out:Path):
    with open(file, "r") as f:
        data = json.load(f)
    
    unique_traces = {}

    for item in data["pairs"]:
        trace = str([element["Activity"] for element in item["network_trace"]])
        if trace not in unique_traces.keys():
            pair = {
                "id" : len(unique_traces),
                "case_ids" : item["case_ids"],
                "network_trace" : []
            }
            
            for activity in item["network_trace"]:
                trace_dict = {
                    "Resource Performer" : [activity["Resource Performer"] for _ in item["case_ids"]],
                    "Resource Consumer" : [activity["Resource Consumer"] for _ in item["case_ids"]],
                    "Activity" : activity["Activity"]
                }
                pair["network_trace"].append(trace_dict)
            unique_traces[trace] = pair
        
        else:
            pair = unique_traces[trace]
            pair["case_ids"].extend(item["case_ids"])
            for i, activity in enumerate(pair["network_trace"]):
                activity["Resource Performer"].extend([item["network_trace"][i]["Resource Performer"] for _ in item["case_ids"]])
                activity["Resource Consumer"].extend(item["network_trace"][i]["Resource Consumer"] for _ in item["case_ids"])
    
    aggregated_traces = {"pairs" : list(unique_traces.values())}
    with open(out, "w") as f:
        json.dump(aggregated_traces, f, indent=2)
    

            


if __name__ == "__main__":

    aggregate_traces(file=FILE_PATH, out=OUT_PATH)