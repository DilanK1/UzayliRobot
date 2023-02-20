import os
import launch
from launch.actions import IncludeLaunchDescription
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/my_robot3.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/my_robot.rviz')

    launch_file_dir = os.path.join(get_package_share_directory('my_robot'),'launch')
    slam_launch_file_dir = os.path.join(get_package_share_directory('slam_toolbox'),'launch')
    params_file_dir = os.path.join(pkg_share,'config/mapper_params_online_async.yaml')

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([slam_launch_file_dir, '/online_async_launch.py']),
        launch_arguments = {'use_sim_time' : 'true', 'params_file' : params_file_dir}.items(),
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/rviz.launch.py'])
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/gazebo.launch.py'])
    )

    map_server = Node(
        package = 'nav2_map_server',
        executable = 'map_saver_server',
        name = 'map_server',
        emulate_tty=False,
        parameters=[{'save_map_timeout': 2000},
                        {'free_thresh_default': 0.25},
                        {'occupied_thresh_default': 0.65}]

    )
    start_lifecycle_manager_cmd = launch_ros.actions.Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            emulate_tty=False, 
            parameters=[{'use_sim_time': 'True'},
                        {'autostart': 'True'},
                        {'node_names': 'my_map_save'}])

    return launch.LaunchDescription([

        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        gazebo_launch,
        rviz_launch,
        # map_server,
        # start_lifecycle_manager_cmd
        slam_launch,
    ])

