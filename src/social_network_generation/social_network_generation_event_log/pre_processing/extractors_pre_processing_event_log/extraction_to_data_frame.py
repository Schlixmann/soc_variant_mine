"""
- This file provides a function (get_data_frame), which requires a path to a csv file as parameter
and returns a dataframe in right format for further process log analysis
"""

import pandas as pd
import pm4py as pm

# Based on the Path and the most important Log Attributes, create a Pandas DataFrame
def get_data_frame(path: str, case_id_name: str, activity_key_name: str, timestamp_key_name: str, sep: str):
    # First import the csv file and convert the csv file to an Event Log
    df = pd.read_csv(filepath_or_buffer=path, sep=sep)
    
    # Drop rows with missing case ID, activity label, or timestamp
    df.dropna(subset=[case_id_name, activity_key_name, timestamp_key_name], inplace=True)
    
    # Use pm4py's format_dataframe function
    df = pm.format_dataframe(df=df,
                             case_id=case_id_name,
                             activity_key=activity_key_name,
                             timestamp_key=timestamp_key_name)
    
    # Explicitly drop the old case_id column using .loc to avoid SettingWithCopyWarning
    df = df.drop(columns=[case_id_name])
    
    return df

