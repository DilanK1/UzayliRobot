
import os
import launch
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro


def generate_launch_description():

    launch_file_dir = os.path.join(
        get_package_share_directory('merge_laser'), 'launch')

    merge_laser = Node(
        package='merge_laser',
        executable='merge_laser_scan',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments={'front_lidar_amr_mini_laser', 'back_lidar_amr_mini_laser'}
    )

    merge_laser_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/merge_laser.launch.py'])
    )
    
    
    return launch.LaunchDescription([
        merge_laser
        # merge_laser_launch
    ])
