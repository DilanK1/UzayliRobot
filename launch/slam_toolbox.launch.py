import os
import launch
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource



def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/my_robot3.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/my_robot.rviz')
    world_path = os.path.join(pkg_share, 'world/worldd.sdf')

    launch_file_dir = os.path.join(get_package_share_directory('slam_toolbox'),'launch')
    params_file_dir = os.path.join(pkg_share,'config/mapper_params_online_async.yaml')

 
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}
        ]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])},{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # Robotu gazeboya aktarmak için
    spawn_entity =Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', '/robot_description'],
        output='screen'
    )


    print(params_file_dir)

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_dir, '/online_async_launch.py']),
        launch_arguments = {'use_sim_time' : 'true', 'params_file' : params_file_dir}.items(),
    )


    return launch.LaunchDescription([

        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        ExecuteProcess(cmd=['gazebo', '--verbose', world_path,'-s', 'libgazebo_ros_factory.so'], output='screen'),
        spawn_entity,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node,
        slam_launch,
    ])

