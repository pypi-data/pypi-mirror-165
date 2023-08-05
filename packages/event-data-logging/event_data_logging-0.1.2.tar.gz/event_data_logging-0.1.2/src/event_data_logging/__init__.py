"""
The imports make it possible to import:
  from event_data_logging import JSONWriter
instead of:
  from event_data_logging.json_writer import JSONWriter
"""

__version__ = "0.1.2"


from event_data_logging.json_writer import JSONWriter, StampedJSONWriter, TimestampModes
from event_data_logging.csv_writer import CSVWriter, StampedCSVWriter
