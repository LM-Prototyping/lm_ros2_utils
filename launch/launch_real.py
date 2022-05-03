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

from lm_ros2_utils.utils import parse_launch_arguments, build_arguments_dict

def get_configuration_file_path(robot_name):
    package_dir = get_package_share_directory("lm_ros2_utils")
    filepath = os.path.join(package_dir, "resource", robot_name + ".urdf")

    return filepath

port_mapping = {
    "PORT_A": 0x01,
    "PORT_B": 0x02,
    "PORT_C": 0x03,
    "PORT_D": 0x04,

    "PORT_1": 0x01,
    "PORT_2": 0x02,
    "PORT_3": 0x03,
    "PORT_4": 0x04,
}

def parse_urdf(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    compass_matcher = re.compile("CompassPlugin")
    distance_matcher = re.compile("DistancePlugin")
    light_matcher = re.compile("LightPlugin")
    touch_matcher = re.compile("TouchPlugin")

    print(root[0][0])
    print(root[0][0].attrib)

    nodes = []

    for node in root[0]:
        plugin_name = node.attrib['type']
        node_name = None
        print(node)

        if compass_matcher.search(plugin_name):
            print("Compass", plugin_name)
            node_name = "compass_sensor"
        if distance_matcher.search(plugin_name):
            node_name = "distance_sensor"
        if light_matcher.search(plugin_name):
            node_name = "light_sensor"
        if touch_matcher.search(plugin_name):
            node_name = "touch_sensor"
        if re.compile("MotorPlugin").search(plugin_name):
            node_name = "motor_node"
        if re.compile("ClockPlugin").search(plugin_name):
            continue

        print(node[0], node[1])

        if not node_name:
            continue

        nodes.append(
            Node(
                package="brickpi3_ros2",
                executable=node_name,
                output="screen",
                emulate_tty=True,
                namespace=node[0].text + "/" + port_mapping[node[1].text],
                parameters=[{
                    "port": port_mapping[node[1].text],
                    "robot_name": node[0].text,
                    "timestep": 32
                }]
            )
        )

    return nodes
    


def generate_launch_description():
    args = parse_launch_arguments()
    arguments_dict = build_arguments_dict(args.arguments)
    arg_roboter_name = DeclareLaunchArgument("robot_name")

    robot_name = arguments_dict["robot_name"]
    os.environ["WEBOTS_ROBOT_NAME"] = robot_name

    config_file = get_configuration_file_path(robot_name)
    nodes = parse_urdf(config_file)

    robot_description = pathlib.Path(config_file).read_text()
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    return LaunchDescription([
        arg_roboter_name, 
        *nodes
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