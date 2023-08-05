import filecmp
from event_data_logging import CSVWriter, StampedCSVWriter, TimestampModes
import pytest
import csv


def test_CSVWriter():
    """Write a file, test if it matches the test_data, and then remove file"""

    filename = "data/csv_data.csv"
    header = ["timestamp", "x", "y", "z"]
    csv_writer = CSVWriter(filename, header=header)

    for i in range(3):

        line = [1661110000123456789 + int(1e9) * i, 10 * i + 1, 10 * i + 2, 10 * i + 3]
        csv_writer.save_line(line)

    try:
        assert filecmp.cmp("data/csv_data.csv", "test_data/goal_csv_data.csv")
    finally:
        csv_writer.filename.unlink()


def test_StampedCSVWriter():
    """Write to a file, and verify that it contains timestamp."""
    filename = "data/csv_data.csv"
    xyz_header = ["x", "y", "z"]
    data_lines = []
    csv_writer = StampedCSVWriter(filename, header=xyz_header)
    try:
        for i in range(3):
            line = [
                str(10 * i + 1),
                str(10 * i + 2),
                str(10 * i + 3),
            ]
            csv_writer.save_line(line)
            data_lines.append(line)

        with open("test_data/goal_csv_data.csv") as csvfile:
            csv_data = csv.reader(csvfile)

            header = next(csv_data)
            assert header[0] == "timestamp"
            assert header[1:] == xyz_header
            for line, goal_line in zip(csv_data, data_lines):
                assert line[1:] == goal_line

        with pytest.raises(Exception) as e_info:
            csv_writer = StampedCSVWriter(
                filename, header=xyz_header, timestamp_mode=1.4
            )
        assert str(e_info.value) == "timestamp mode must be int"

        with pytest.raises(Exception) as e_info:
            csv_writer = StampedCSVWriter(filename, header=xyz_header, timestamp_mode=4)
        assert str(e_info.value) == "timestamp_mode value not in TimestampModes options"

    finally:
        csv_writer.filename.unlink()


def test_StampedCSVWriter_setters():
    """See if timestamp modes can be set correctly, and that errors are raised if not"""
    filename = "data/csv_data.csv"
    header = ["x", "y", "z"]
    csv_writer = StampedCSVWriter(filename, header=header)
    try:
        for i in range(3):
            line = [10 * i + 1, 10 * i + 2, 10 * i + 3]
            csv_writer.save_line(line)

        # should work the setter
        csv_writer.timestamp_mode = TimestampModes.SECONDS
        csv_writer.timestamp_mode = TimestampModes.NANOSECONDS

        # savewith different stamps
        for i in range(3):
            line = [10 * i + 1, 10 * i + 2, 10 * i + 3]
            csv_writer.save_line(line)

        # use get getter
        timestamp_mode = csv_writer.timestamp_mode

        with pytest.raises(Exception) as e_info:
            csv_writer.timestamp_mode = 1.1
        assert str(e_info.value) == "timestamp mode must be int"

        with pytest.raises(Exception) as e_info:
            csv_writer.timestamp_mode = 3
        assert str(e_info.value) == "timestamp_mode value not in TimestampModes options"
    finally:
        csv_writer.filename.unlink()
