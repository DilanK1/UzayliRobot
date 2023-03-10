import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    goalpose = Node(
        package='my_robot',
        executable='goalpose_pub',
        name='goalpose_pub',
        output='screen'
    )

    return LaunchDescription([
        goalpose
    ])
