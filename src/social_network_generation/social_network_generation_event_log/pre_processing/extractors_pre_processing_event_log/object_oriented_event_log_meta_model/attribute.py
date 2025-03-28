"""
This file implements the class Attribute which gets as parameters a key and value
"""


# Attribute class depends on the existence of an event
class Attribute:
    def __init__(self, key: str, value) -> None:
        self.key = key
        self.value = value

    # Returns the key of the attribute: The identifier (column)
    def get_key(self) -> str:
        return self.key

    # Returns the value of the attribute: The value in row for column
    def get_value(self):
        return self.value


# Inherits Attribute -> Attributes which are always the same in the trace: case_id, ...
class CaseAttribute(Attribute):
    def __init__(self, key, value) -> None:
        super().__init__(key, value)


# Inherits Attribute -> Attributes which change for every event in trace: activity_check_one, time, resource
class EventAttribute(Attribute):
    def __init__(self, key, value) -> None:
        super().__init__(key, value)
