"""ros2_message_handling

Extra utility to turn ros2 messages into a dictionary with custom timestamp format. 
This module has dependencies outside of the scope of the package, 
and cannot be run or tested without having ROS2 installed

This will be removed from the package in the future 
"""

from rosidl_runtime_py.convert import message_to_ordereddict
from collections import OrderedDict
from typing import Any


def convert_ros2_msg_to_nanosecond_stamped_dict(message: Any) -> dict:
    """

    Args:
        message (Any): ros2 message with header (without header will give error).
            For dictionary without header, simply use message_to_ordereddict.

    Returns:
        dict: dictionary with header turned to nanoseconds timestamp
    """
    # convert message in our format of dictionary
    ordered_dict: OrderedDict = message_to_ordereddict(message)
    timestamp: int = (
        int(ordered_dict["header"]["stamp"]["sec"] * 1e9)
        + ordered_dict["header"]["stamp"]["nanosec"]
    )
    custom_dict = OrderedDict(
        [("timestamp", timestamp), ("frame_id", ordered_dict["header"]["frame_id"])]
    )
    del ordered_dict["header"]
    custom_dict.update(ordered_dict)
    return custom_dict
