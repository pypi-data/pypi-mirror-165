from collections import OrderedDict
import numpy as np
import pytest
from event_data_logging.data_handling import flatten_dictionary


def test_flatten_dictionary():
    """Use dictionary with variety of types, validate with test_data and test_header"""
    input_dict = {
        "header": {
            "timestamp": {"sec": 3, "nanosec": 123},
            "frameID": 3,
        },
        "voltages": [
            {"voltage": 0.2},
            {"voltage": 3.1},
        ],
        "single_fly": [{"x": 1.0, "y": 2.0, "r": 0.2}],
        "flies": [{"x": 1.0, "y": 2.0, "r": 0.2}, {"x": 4.0, "y": 5.0, "r": 0.4}],
        "amps": np.array([3.2, 1.1]),
        "testlist": ["a", "b", "c"],
        "username": "John Doe",
    }

    computed_header, computed_data = flatten_dictionary(input_dict)

    test_header = [
        "header_timestamp_sec",
        "header_timestamp_nanosec",
        "header_frameID",
        "voltages_0_voltage",
        "voltages_1_voltage",
        "single_fly_0_x",
        "single_fly_0_y",
        "single_fly_0_r",
        "flies_0_x",
        "flies_0_y",
        "flies_0_r",
        "flies_1_x",
        "flies_1_y",
        "flies_1_r",
        "amps_0",
        "amps_1",
        "testlist_0",
        "testlist_1",
        "testlist_2",
        "username",
    ]
    test_data = [
        3,
        123,
        3,
        0.2,
        3.1,
        1.0,
        2.0,
        0.2,
        1.0,
        2.0,
        0.2,
        4.0,
        5.0,
        0.4,
        3.2,
        1.1,
        "a",
        "b",
        "c",
        "John Doe",
    ]

    assert computed_header == test_header
    assert computed_data == test_data


def test_flatten_dictionary_bad_input():
    """test whether exception is raised for unsupported type"""
    input_dict = {"example_input": (1, 2)}

    with pytest.raises(Exception) as exception_info:
        computed_header, computed_data = flatten_dictionary(input_dict)

    assert str(exception_info.value) == "Message format is not implemented"


def test_flatten_ordered_dict():
    """Test functionality for ordered dict"""
    input_dict = OrderedDict(
        [
            (
                "header",
                OrderedDict(
                    [
                        (
                            "timestamp",
                            OrderedDict([("sec", 3), ("nanosec", 123)]),
                        ),
                        ("frameID", 3),
                    ]
                ),
            ),
            (
                "voltages",
                [OrderedDict([("voltage", 0.2)]), OrderedDict([("voltage", 3.1)])],
            ),
        ]
    )

    computed_header, computed_data = flatten_dictionary(input_dict)

    goal_header = [
        "header_timestamp_sec",
        "header_timestamp_nanosec",
        "header_frameID",
        "voltages_0_voltage",
        "voltages_1_voltage",
    ]
    goal_data = [3, 123, 3, 0.2, 3.1]
    assert computed_header == goal_header

    assert computed_data == goal_data
