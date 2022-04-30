import os
import sys
import pathlib

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

from lm_ros2_utils.utils import parse_launch_arguments, build_arguments_dict


def get_configuration_file_path(robot_name):
    package_dir = get_package_share_directory("lm_ros2_utils")
    filepath = os.path.join(package_dir, "resource", robot_name + ".urdf")

    return filepath


def generate_launch_description():
    args = parse_launch_arguments()
    arguments_dict = build_arguments_dict(args.arguments)
    arg_roboter_name = DeclareLaunchArgument("robot_name")

    robot_name = arguments_dict["robot_name"]
    os.environ["WEBOTS_ROBOT_NAME"] = robot_name

    config_file = get_configuration_file_path(robot_name)

    robot_description = pathlib.Path(config_file).read_text()
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    return LaunchDescription([
        arg_roboter_name, 
        Node(
            package='webots_ros2_driver',
            executable='driver',
            output='screen',
            emulate_tty=True, # For showing stdout,
            namespace=robot_name,
            parameters=[
                {'robot_description': robot_description,
                'use_sim_time': use_sim_time,
                'set_robot_state_publisher': True},
            ],
        )
    ])