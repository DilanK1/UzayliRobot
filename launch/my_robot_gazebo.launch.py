import os
import launch
from launch.actions import IncludeLaunchDescription
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import xacro


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(
        package='my_robot').find('my_robot')
    default_model_path = os.path.join(get_package_share_directory(
        'my_robot'), 'urdf_amr', 'amr_mini.xacro')


    launch_file_dir = os.path.join(
        get_package_share_directory('my_robot'), 'launch')
    

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/slam_toolbox.launch.py'])
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/rviz.launch.py'])
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/gazebo.launch.py'])
    )

    merge_laser_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/merge_laser.launch.py'])
    )

    map_server_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/map_server.launch.py'])
    )

    amcl_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/amcl.launch.py'])
    )

    initialpose_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/initialpose.launch.py'])
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/nav2.launch.py'])
    )

    twist_mux_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [launch_file_dir, '/twist_mux.launch.py'])
    )

    return launch.LaunchDescription([

            launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                                description='Absolute path to robot urdf file'),
            launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='true',
                                                description='Flag to enable use_sim_time'),
            gazebo_launch,
            rviz_launch,
            map_server_launch,
            merge_laser_launch,
            amcl_launch,
            initialpose_launch,
            nav2_launch,
            twist_mux_launch
            # slam_launch,
        ])
