from setuptools import setup
import os


PATH = f"{os.getenv('LM_FRAMEWORK_PATH')}ros2Workspace/src/lm_ros2_utils"

files_in_dir = (
    lambda dir: 
        [
            f"{dir}/{file}" for file in 
            os.listdir(f"{PATH}/{dir}")
            if os.path.isfile(f"{PATH}/{dir}/{file}")
        ]
    )


package_name = "lm_ros2_utils"
data_files = []

launch_files = files_in_dir("launch")
data_files.append(("share/" + package_name + "/launch", launch_files))

resources_files = files_in_dir("resource")
data_files.append(("share/" + package_name + "/resource", resources_files))

script_files = files_in_dir("lm_ros2_utils")
data_files.append(("share/" + package_name + "/lm_ros2_utils", script_files))

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        *data_files
    ],
    install_requires=["setuptools", "launch"],
)