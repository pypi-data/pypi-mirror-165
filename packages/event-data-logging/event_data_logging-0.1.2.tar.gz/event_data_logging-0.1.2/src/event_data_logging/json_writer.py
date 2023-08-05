"""json_writer.py

contains classes: 
- JSONWriter: save dictionaries as entries in json
- TimestampModes: dataclass with option of SECONDS, NANOSECONDS
- StampedJSONWriter: save dictionaries as entries in json, but adds current timestamp
"""
import json
import time
import os
from typing import Dict
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from event_data_logging.file_handling import validate_filename


class JSONWriter:
    def __init__(self, goal_filename: Union[str, Path]) -> None:
        """jsonwriter

        Args:
            goal_filename (Union[str, Path]): Path that needs to be verified
                before it is used.
        """

        self.filename: Path = validate_filename(goal_filename)
        self.header_initialized: bool = False

    def save_event(self, save_data: Dict) -> None:
        """Saves a dict of event data along with the current timestamp.

        Args:
            data (dict): Dictionary of event data to save,
            eg {param_name : param_value} for a parameter change
        """

        data_string: str = json.dumps(save_data, ensure_ascii=False)

        if not self.header_initialized:
            with open(self.filename, "wb") as f:
                f.write("[\n".encode("utf8"))
                f.write(data_string.encode("utf8"))
                f.write("\n]".encode("utf8"))
                self.header_initialized = True

        else:
            with open(self.filename, "r+b") as f:
                f.seek(-1, os.SEEK_END)
                cur_char = f.read(1)
                # seek to before previous "\n]" end of file.
                while cur_char in [b"\n", b"]"]:
                    f.seek(-2, os.SEEK_CUR)
                    cur_char = f.read(1)
                # and delete remainder.
                f.truncate()
                # write new data.
                f.write(",\n".encode("utf8"))
                f.write(data_string.encode("utf8"))
                f.write("\n]".encode("utf8"))


@dataclass
class TimestampModes:
    """Selector that can be either 1 or 2"""

    SECONDS: int = 1
    NANOSECONDS: int = 2


class StampedJSONWriter(JSONWriter):
    def __init__(
        self, filename: Union[str, Path], timestamp_mode=TimestampModes.SECONDS
    ) -> None:
        """JSONWriter that adds timestamp entry to dictioanry

        Args:
            goal_filename (Union[str, Path]): Path that needs to be verified
                before it is used.
            timestamp_mode (int, optional): Set timestamp mode to SECONDS or
                NANOSECONDS. Defaults to TimestampModes.SECONDS.
        Raises:
            TypeError: TimestampMode is not of correct type, must be int
            Exception: value not in TimestampMode  options
        """
        if type(timestamp_mode) != int:
            raise TypeError("timestamp mode must be int")

        if timestamp_mode not in [1, 2]:
            raise Exception(f"Invalid timestamp integer")

        JSONWriter.__init__(self, filename)
        self._timestamp_mode: int = timestamp_mode

    @property
    def timestamp_mode(self) -> int:
        """Access the private _timestamp_mode variable

        Returns:
            int: integer from the TimestampMode dataclass
        """
        return self._timestamp_mode

    @timestamp_mode.setter
    def timestamp_mode(self, timestamp_mode: int) -> None:
        """Set the private _timestamp_mode, dictating the units of the timestamp.
            First verifies the input and raises exceptions if invalid.

        Args:
            timestamp_mode (int): selection from TimestampMode dataclass

        Raises:
            TypeError: TimestampMode is not of correct type, must be int
            Exception: value not in TimestampMode  options
        """

        if type(timestamp_mode) != int:
            raise TypeError("timestamp mode must be int")

        if timestamp_mode not in [1, 2]:
            raise Exception(f"Invalid timestamp integer")

        # if timestamp_mode == TimestampModes.SECOND:
        self._timestamp_mode = timestamp_mode

    def save_event(self, data: Dict) -> None:
        """add timestamp entry to dictionary, and write to json

        Args:
            data (Dict)
        """

        if self._timestamp_mode == TimestampModes.SECONDS:
            timestamp: Union[int, float] = time.time()
        else:  #  self._timestamp_mode == TimestampModes.NANOSECONDS:
            timestamp = time.time_ns()

        stamped_data: Dict = {"timestamp": timestamp, **data}

        super().save_event(stamped_data)
