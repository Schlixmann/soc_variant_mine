"""
- This file imports the structure based on the XES Process Log UML Meta-Model
XES UML Meta Model: Event Log <>- (contains) - Traces <>- (contains) <>- Events <>- (contains) - Attributes
"""
# Required Imports:
import pandas as pd

from .object_oriented_event_log_meta_model.event_log import EventLog
from .object_oriented_event_log_meta_model.trace import Trace
from .object_oriented_event_log_meta_model.event import Event
from .object_oriented_event_log_meta_model.attribute import Attribute

def convert_df_to_event_log(df: pd.DataFrame):
    # Get unique case IDs
    cases = pd.unique(df['case:concept:name'])
    traces = []

    # Group the dataframe by case_id to avoid repeated filtering
    grouped_df = df.groupby('case:concept:name')

    for case in cases:
        # Get the events of the current case as a DataFrame
        case_df = grouped_df.get_group(case)
        
        # Get all event attribute keys (excluding unnecessary ones)
        attrib_keys = [col for col in case_df.columns if col not in ['case:concept:name', '@@index']]
        
        # Convert each event (row) in the case to Event objects
        events_of_trace = [
            Event([Attribute(attrib_key, event_value) for attrib_key, event_value in zip(attrib_keys, row)])
            for row in case_df[attrib_keys].values
        ]
        
        # Store the Trace of the Event Log
        trace = Trace(case, events_of_trace)
        traces.append(trace)

    # Return the Event Log
    return EventLog(traces)
