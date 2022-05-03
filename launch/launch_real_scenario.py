import os
import sys
import re
import pathlib
import xml.etree.ElementTree as ET

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from lm_ros2_utils.utils import parse_launch_arguments, build_arguments_dict

def generate_launch_description():
    args = parse_launch_arguments()
    arguments_dict = build_arguments_dict(args.arguments)
    arg_roboter_name = DeclareLaunchArgument("robot_name")

    robot_name = arguments_dict["robot_name"]
    scenario = arguments_dict["evaluation_scenario"]

    return LaunchDescription([
        arg_roboter_name, 
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory("lm_ros2_utils"), "launch", "launch_real.py"
                ),
            ),
            launch_arguments={
                "robot_name": robot_name
            }.items()
        ),
        Node(
            package="evaluation_scenarios",
            executable=scenario,
            output="screen",
            emulate_tty=True
        )
        # Node(
        #     package='webots_ros2_driver',
        #     executable='driver',
        #     output='screen',
        #     emulate_tty=True, # For showing stdout,
        #     namespace=robot_name,
        #     parameters=[
        #         {'robot_description': robot_description,
        #         'use_sim_time': use_sim_time,
        #         'set_robot_state_publisher': True},
        #     ],
        # )
    ])