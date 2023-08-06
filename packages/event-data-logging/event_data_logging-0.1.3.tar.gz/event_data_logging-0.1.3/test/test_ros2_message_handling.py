"""
ros2_message_handling cannot be included in the test suite since it has dependencies on ros2, which are outside of the scope of the package
This file will be removed in the future


"""
# from collections import OrderedDict
# from geometry_msgs.msg import TwistStamped

# from event_data_logging.ros2_message_handling import (
#     convert_ros2_msg_to_nanosecond_stamped_dict,
# )


# def no_convert_ros2_msg_to_nanosecond_stamped_dict():

#     message = TwistStamped()
#     # custom_dict = convert_ros2_msg_to_maimon_dict(message)
#     custom_dict = convert_ros2_msg_to_nanosecond_stamped_dict(message)
#     print(f"Custom dict: {custom_dict}")
#     test_dict = OrderedDict(
#         [
#             ("timestamp", 0.0),
#             ("frame_id", ""),
#             (
#                 "twist",
#                 OrderedDict(
#                     [
#                         ("linear", OrderedDict([("x", 0.0), ("y", 0.0), ("z", 0.0)])),
#                         ("angular", OrderedDict([("x", 0.0), ("y", 0.0), ("z", 0.0)])),
#                     ]
#                 ),
#             ),
#         ]
#     )

#     assert custom_dict == test_dict
