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
    map_path = os.path.join(pkg_share, 'maps', 'my_map_save.yaml')

    lifecycle_nodes = ['map_server']
    autostart = True

    map_server = Node(
        package = 'nav2_map_server',
        executable = 'map_server',
        name = 'map_server',
        parameters=[{'yaml_filename': map_path},
                    {'use_sim_time' : LaunchConfiguration('use_sim_time')}]
    )

    start_lifecycle_manager_cmd = launch_ros.actions.Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')},
                    {'autostart': autostart},
                    {'node_names': lifecycle_nodes}])


    return launch.LaunchDescription([

        map_server,
        start_lifecycle_manager_cmd,
    ])

