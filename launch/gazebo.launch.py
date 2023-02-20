
import os
import launch
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess

def generate_launch_description():
    
    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    world_path = os.path.join(pkg_share, 'world/worldd.sdf')


    # Robotu gazeboya aktarmak için
    spawn_entity =Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', '/robot_description'],
        output='screen'
    )

    return launch.LaunchDescription([

        ExecuteProcess(cmd=['gazebo', '--verbose', world_path,'-s', 'libgazebo_ros_factory.so'], output='screen'),

        spawn_entity
    ])
