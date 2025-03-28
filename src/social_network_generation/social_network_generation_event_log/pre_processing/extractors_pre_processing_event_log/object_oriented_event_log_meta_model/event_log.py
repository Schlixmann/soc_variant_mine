"""
This file consists of the class EventLog which requires as Parameter a List of Traces

The class implements several functions which provide insights of the current process log
and therefore for the real process executions
"""

# Required Imports:
from typing import List, Union, Any, Dict

# Imported class
from .trace import Trace


# Object-oriented structure of the XES Document UML Model for Event Logs
class EventLog:

    def __init__(self, traces: List[Trace]) -> None:
        self.traces = traces
        
    def get_network_output_of_distinct_traces_in_event_log(self, resource_structure_type: str) -> List[Dict[str, Union[int, Dict[Any, List[str]]]]]:
    
        # All Distinct Traces in the format: (list of case ids, Trace)
        distinct_trace_list = self.__get_distinct_traces(resource_structure_type=resource_structure_type)
        
        # Output list
        output_list = []
        
        # Iterate through distinct traces with an increasing ID
        for distinct_trace_id, (case_ids, trace) in enumerate(distinct_trace_list, start=1):
            event_list = trace.get_events_of_trace()
            
            # Create the network trace by iterating through events and next events using zip
            network_list = [
                {
                    "Resource Performer": event[resource_structure_type],
                    "Resource Consumer": next_event[resource_structure_type] if next_event else "",
                    "Activity": event["Activity"]
                }
                for event, next_event in zip(event_list, event_list[1:] + [None])]
            
            # Add to the output
            output_list.append({
                'id': distinct_trace_id,
                'case_ids': case_ids,
                'network_trace': network_list})
        
        return output_list
    
    # Helper method to get all distinct traces in the log
    # @private
    # A distinct trace in that case is defined as a unique list of resource activity pairs
    def __get_distinct_traces(self, resource_structure_type: str) -> list:
        distinct_traces = []
        trace_map = {}  # Dictionary to store distinct traces based on event ID set

        # Iterate through the traces of the event log
        for trace in self.traces:
            trace_structure_dict_list = trace.get_resource_activity_organisation_structure_pairs_of_trace().items()

            # Iterate through the case_id, events pair for each trace
            for case_id, events in trace_structure_dict_list:
                # Generate the event ID set for the current trace using tuples (resource, activity)
                event_id_set = frozenset((event.get(resource_structure_type, ""), event.get('Activity', "")) for event in events)

                # Check if this trace is already in the trace_map
                if event_id_set in trace_map:
                    # Add case_id to the existing distinct trace
                    trace_map[event_id_set][0].append(case_id)
                else:
                    # If it's a new distinct trace, add it to the trace_map and distinct_traces
                    trace_map[event_id_set] = ([case_id], Trace(case_id=case_id, events=events))
                    distinct_traces.append(trace_map[event_id_set])

        # Return the list of distinct traces
        return distinct_traces    
