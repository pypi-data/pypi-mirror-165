"""csv_writer.py
Contains classes
- CSVWriter: save lists as lines in a csv
- StampedCSVWriter: inherits from CSVWriter, but prepends a timestamp to the list
"""

import csv
import time
from pathlib import Path
from typing import Union

from event_data_logging.file_handling import validate_filename
from event_data_logging.json_writer import TimestampModes


class CSVWriter:
    def __init__(
        self, goal_filename: Union[str, Path], header: Union[list, None] = None
    ):
        """csv writer constructor

        Args:
            goal_filename (Union[str, Path]): Path that needs to be verified
                before it is used.
            header (Union[list, None], optional): If header is known at
                construction, write it to the file. Defaults to None.
        """

        self.filename: Path = validate_filename(goal_filename)

        self.header_initialized: bool = False
        if header is not None:
            self.save_header(header)
            self.header_initialized = True

    def save_line(self, line_to_save: list) -> None:
        """saves list to line in csv

        Args:
            line_to_save (list)
        """
        with open(self.filename, "a+") as file:
            writer = csv.writer(file)
            writer.writerow(line_to_save)

    def save_header(self, header_line: list) -> None:
        """saves list of header items as line in csv

        Args:
            header_line (list): _description_
        """
        with open(self.filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(header_line)


class StampedCSVWriter(CSVWriter):
    def __init__(
        self,
        goal_filename: Union[str, Path],
        header: Union[list, None] = None,
        timestamp_mode: int = TimestampModes.SECONDS,
    ):
        """StampedCSVWriter constructor. Functions as CSVWriter, but prepends a timestamp

        Args:
            goal_filename (Union[str, Path]): Path that needs to be verified
                before it is used.
            header (Union[list, None], optional): if header is available, write
                it to file in constructor. Defaults to None.
            timestamp_mode (int, optional): Set timestamp mode to SECONDS or
                NANOSECONDS. Defaults to TimestampModes.SECONDS. This determines
                the units of the epoch timestamps in the csv file
        Raises:
            TypeError: TimestampMode is not of correct type, must be int
            Exception: value not in TimestampMode  options
        """

        if header is not None:
            header = ["timestamp", *header]

        # verify input
        if type(timestamp_mode) != int:
            raise TypeError("timestamp mode must be int")
        if timestamp_mode not in [1, 2]:
            raise Exception(f"timestamp_mode value not in TimestampModes options")

        CSVWriter.__init__(self, goal_filename, header)
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
            timestamp_mode (int): selection from TimestampMode dataclass.

        Raises:
            TypeError: TimestampMode is not of correct type, must be int
            Exception: value not in TimestampMode  options
        """

        if type(timestamp_mode) != int:
            raise TypeError("timestamp mode must be int")
        if timestamp_mode not in [1, 2]:
            raise Exception(f"timestamp_mode value not in TimestampModes options")

        self._timestamp_mode = timestamp_mode

    def save_line(self, data: list) -> None:
        """Prepend timestamp and write list as csv line

        Args:
            data (list): list of items to save
        """

        if self._timestamp_mode == TimestampModes.SECONDS:
            timestamp: Union[int, float] = time.time()
        else:
            # self._timestamp_mode == TimestampModes.NANOSECONDS:
            timestamp = time.time_ns()

        stamped_data: list = [timestamp, *data]

        super().save_line(stamped_data)
