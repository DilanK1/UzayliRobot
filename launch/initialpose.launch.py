import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    initialpose = Node(
        package='my_robot',
        executable='initialpose_pub',
        name='initialpose_pub',
        output='screen'
    )

    return LaunchDescription([
        initialpose
    ])
