"""
This file consists of the class Trace which gets as parameter a unique case id and a List of Events
The class Trace implements some functions which help to understand the respective process execution
"""

# Required Imports:
from typing import List

# Imported class
from .event import Event


# Trace class depends on the existence of an Event Log
class Trace:

    def __init__(self, case_id: str, events: List[Event]) -> None:
        self.case_id = case_id
        self.events = events

    def get_case_id(self) -> str:
        return self.case_id

    def get_events_of_trace(self) -> List[Event]:
        return self.events

    # Returns a dict object with case_id as key and all resource, activity_check_one pairs (:= event) as value
    def get_resource_activity_organisation_structure_pairs_of_trace(self) -> dict:
        return {self.case_id: [e.get_resource_activity_organisation_structure_pair() for e in self.events]}

    # Returns a dict object with case_id as key and all resource, activity pairs (:= event) as value
    def get_resource_activity_pairs_of_trace(self) -> dict:
        return {self.case_id: [e.get_resource_activity_pair() for e in self.events]}
