
import os
import launch
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    
    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    world_path = os.path.join(pkg_share, 'world/my_world.sdf')

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

    # Robotu gazeboya aktarmak için
    spawn_entity =Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', '/robot_description'],
        output='screen'
    )

    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world_path,'-s', 'libgazebo_ros_factory.so'], output='screen')

    return launch.LaunchDescription([

        robot_state_publisher_node,
        joint_state_publisher_node,
        gazebo,
        spawn_entity
    ])