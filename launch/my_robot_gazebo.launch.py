import os
import launch
from launch.actions import IncludeLaunchDescription
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/my_robot3.urdf')

    launch_file_dir = os.path.join(get_package_share_directory('my_robot'),'launch')

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/slam_toolbox.launch.py'])
    ) 

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/rviz.launch.py'])
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/gazebo.launch.py'])
    )

    map_server_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/map_server.launch.py'])
    )

    amcl_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/amcl.launch.py'])
    )


    return launch.LaunchDescription([

        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        gazebo_launch,
        rviz_launch,
        map_server_launch,
        amcl_launch,
        # slam_launch,
    ])

