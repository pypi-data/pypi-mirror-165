import filecmp
import json
import pytest

from event_data_logging import JSONWriter, StampedJSONWriter, TimestampModes


def test_JSONWriter():
    """Write to file and see that it matches the goalfile. Then delete created file"""
    test1 = {
        "timestamp": 1661110000123456789,
        "bar_color": [1, 2, 3],
    }
    test2 = {"timestamp": 1661110010123456789, "bar_width_degrees": 10}
    test3 = {"timestamp": 1661110020123456789, "example_float": 0.1}

    filename = "data/json_data.json"
    writer = JSONWriter(filename)
    writer.save_event(test1)
    writer.save_event(test2)
    writer.save_event(test3)

    try:
        assert filecmp.cmp("data/json_data.json", "test_data/goal_json_data.json")
    finally:
        writer.filename.unlink()


def test_StampedJSONWriter():
    """Test writing file, and see that it matches. Since timestamps cannot be reproduced, they are set to zero before checking"""
    test_events = [
        {"bar_color": [1, 2, 3]},
        {"bar_width_degrees": 10},
        {"example_float": 0.1},
    ]

    filename = "data/stamped_json_data.json"
    writer = StampedJSONWriter(filename)

    validate_json = []
    for event in test_events:
        writer.save_event(event)
        validate_json.append({"timestamp": 0.0, **event})

    try:
        with open(filename) as f:
            saved_json = json.load(f)

        for saved_dict, validate_dict in zip(saved_json, validate_json):
            validate_dict["timestamp"] = saved_dict["timestamp"]

        assert saved_json == validate_json

        with pytest.raises(Exception) as e_info:
            writer = StampedJSONWriter(filename, timestamp_mode=1.2)
        assert str(e_info.value) == "timestamp mode must be int"

        with pytest.raises(Exception) as e_info:
            writer = StampedJSONWriter(filename, timestamp_mode=5)
        assert str(e_info.value) == "Invalid timestamp integer"

    finally:
        writer.filename.unlink()


def test_StampedJSONWriter_stamp_options():
    """test if nanosecond writer also works"""
    test_events = [
        {"bar_color": [1, 2, 3]},
        {"bar_width_degrees": 10},
        {"example_float": 0.1},
    ]

    filename = "data/stamped_json_data.json"
    writer = StampedJSONWriter(filename, timestamp_mode=TimestampModes.NANOSECONDS)

    validate_json = []
    for event in test_events:
        writer.save_event(event)
        validate_json.append({"timestamp": 0.0, **event})

    try:
        with open(filename) as f:
            saved_json = json.load(f)

        for saved_dict, validate_dict in zip(saved_json, validate_json):
            validate_dict["timestamp"] = saved_dict["timestamp"]

        assert saved_json == validate_json

    finally:
        writer.filename.unlink()


def test_StampedJSONWriter_setters():
    """test getting and setting if timestamp mode, and see if errors are correctly raised"""

    filename = "data/stamped_json_data.json"
    writer = StampedJSONWriter(filename, timestamp_mode=TimestampModes.NANOSECONDS)

    # should work the setter
    writer.timestamp_mode = TimestampModes.SECONDS
    writer.timestamp_mode = TimestampModes.NANOSECONDS

    # use get getter
    timestamp_mode = writer.timestamp_mode

    with pytest.raises(Exception) as e_info:
        writer.timestamp_mode = 1.1
    assert str(e_info.value) == "timestamp mode must be int"

    with pytest.raises(Exception) as e_info:
        writer.timestamp_mode = 3
    assert str(e_info.value) == "Invalid timestamp integer"
