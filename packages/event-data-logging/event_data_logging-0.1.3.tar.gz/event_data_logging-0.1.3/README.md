# event_data_logging

Save events to json or csv files. This package comes in 4 flavors:

- CSVWriter
- StampedCSVWriter
- JSONWriter
- StampedJSONWriter

All of these will check if the given filename already exists and add a numerical suffix if it does to give a unused new filename. Additionally, if a filename that includes directories is used, the directories will be created if they don't exist, if possible.

The StampedWriters will add a leading entry with the current [epoch timestamp](https://www.wikiwand.com/en/Epoch_time) to each event or line saved. The default format is in seconds with fraction of a second as decimal numbers. Alternatively you can save the timestamps as nanoseconds instead.

Readme content:

- [Install](#install)
- [Usage](#usage)
- [Developing](#developing)
- [ros2 message handling](#rosmessage)

<a name=install></a>

## Install

Install from PYPI

    pip install event_data_logging

Alternatively, install from github

    pip install git+https://git@github.com/maimonlab/event_data_logging.git

<a name=usage></a>

## Usage

### JSON example without timestamps

```python
from event_data_logging.json_writer import JSONWriter
test_events = [
    {"bar_color": [1, 2, 3]},
    {"bar_width_degrees": 10},
    {"example_float": 0.1},
]
filename = "data/json_data.json"
writer = JSONWriter(filename)
for event in test_events:
    writer.save_event(event)
```

This would create the file `data/json_data.json` with content:

```
[
{"bar_color": [1, 2, 3]},
{"bar_width_degrees": 10},
{"example_float": 0.1}
]
```

### JSON example with timestamp

```python
from event_data_logging.json_writer import StampedJSONWriter
test_events = [
    {"bar_color": [1, 2, 3]},
    {"bar_width_degrees": 10},
    {"example_float": 0.1},
]
filename = "data/stamped_json_data.json"
writer = StampedJSONWriter(filename)
for event in test_events:
    writer.save_event(event)
```

This would create the file `data/stamped_json_data.json` with content:

```
[
{"timestamp": 1661201947.0682852, "bar_color": [1, 2, 3]},
{"timestamp": 1661201947.0683577, "bar_width_degrees": 10},
{"timestamp": 1661201947.0684075, "example_float": 0.1}
]
```

### CSV example with nanosecond timestamp

```python
from event_data_logging.csv_writer import StampedCSVWriter, TimestampModes
filename = "data/csv_data.csv"
xyz_header = ["x", "y", "z"]
csv_writer = StampedCSVWriter(
    filename, header=xyz_header, timestamp_mode=TimestampModes.NANOSECONDS
)
for i in range(3):
    line = [
        str(10 * i + 1),
        str(10 * i + 2),
        str(10 * i + 3),
    ]
    csv_writer.save_line(line)
```

This will give the file `data/csv_data.csv` with the following content:

```
timestamp,x,y,z
1661110000123456789,1,2,3
1661110001123456789,11,12,13
1661110002123456789,21,22,23
```

## Developing

<a name=developing></a>

To install the testing dependencies, install with

    pip install -e .[test]

You can run the tests with pytest, and check the coverage. To do so, use the following commands:

    coverage run -m pytest

The coverage report prints to the terminal with:

    coverage report

This report shows how much of all the code is actually run during the test.

### Uploading to pypi

Build the distribution

    python3 -m build

Upload the distribution to pypi

    python3 -m twine upload --repository pypi dist/* --verbose

<a name=rosmessage></a>

### ros2_message_handling using outside dependencies

In our lab, this package is mainly used to save ros2 data, and thus turning ros2 messages to dictionaries is very common. The ros2_message_handling module therefore requires some ros2 packages to be installed, and is outside of the scope of most uses.

_The `test_ros2_message_handling.py` will thus fail in environments without ROS2.
\_We will likely remove this module before the stable release. the ros2_message handling should be integrated in it's own ros packages_
