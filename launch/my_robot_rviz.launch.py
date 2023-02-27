import os
import launch
from ament_index_python.packages import get_package_share_path

# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import ExecuteProcess

import launch_ros

from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/my_robot3.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/my_robot.rviz')
    world_path = os.path.join(pkg_share, 'world/worldd.sdf')

    
    # gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
    #                                 description='Flag to enable joint_state_publisher_gui')
    # model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
    #                                   description='Absolute path to robot urdf file')
    # rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
    #                                  description='Absolute path to rviz config file')

    
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

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     condition=IfCondition(LaunchConfiguration('gui'))
    # )

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

    return launch.LaunchDescription([


        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        # ExecuteProcess(cmd=['gazebo', '--verbose', world_path,'-s', 'libgazebo_ros_factory.so'], output='screen'),


        # spawn_entity,
        joint_state_publisher_node,
        # joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
    ])


# ---------------------------------------------------
# 
# import launch
# import launch_ros.actions

# def generate_launch_description():
#     urdf_file = launch.substitutions.LaunchConfiguration('urdf_file', default='$(find my_robot_description)/urdf/my_robot.urdf')
#     xacro_file = launch.substitutions.LaunchConfiguration('xacro_file', default='$(find my_robot_description)/urdf/my_robot.xacro')

#     xacro_node = launch_ros.actions.Node(
#         package='xacro',
#         node_executable='xacro',
#         output='screen',
#         arguments=[xacro_file, 'output=' + urdf_file]
#     )

#     robot_state_publisher = launch_ros.actions.Node(
#         package='robot_state_publisher',
#         node_executable='robot_state_publisher',
#         parameters=[{'use_tf_static': True},
#                     {'publish_frequency': 50},
#                     {'robot_description': urdf_file}
#                     ]
#     )

#     return launch.LaunchDescription([xacro_node, robot_state_publisher])


# import os

# import launch
# import launch.actions
# import launch_ros.actions


# def generate_launch_description():
#     urdf = launch.substitutions.LaunchConfiguration('model', default=os.path.join(
#         launch.substitutions.ThisLaunchFileDir(),
#         'urdf', 'my_robot.urdf'
#     ))

#     use_gui = launch.substitutions.LaunchConfiguration('use_gui', default='true')

#     robot_state_publisher = launch_ros.actions.Node(
#         package='robot_state_publisher',
#         node_executable='robot_state_publisher',
#         output='screen',
#         arguments=[urdf],
#         parameters=[{'publish_frequency': 50.0}]
#     )

#     joint_state_publisher = launch_ros.actions.Node(
#         package='joint_state_publisher',
#         node_executable='joint_state_publisher',
#         output='screen',
#     )

#     rviz = launch_ros.actions.Node(
#         package='rviz2',
#         node_executable='rviz2',
#         output='screen',
#         arguments=['-d', urdf],
#         condition=launch.conditions.IfCondition(use_gui),
#         parameters=[{'fixed_frame': 'base_link'}]
#     )

#     return launch.LaunchDescription([
#         robot_state_publisher,
#         joint_state_publisher,
#         rviz,
#     ])
