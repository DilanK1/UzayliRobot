from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    urdf_tutorial_path = get_package_share_path('my_robot')
    default_model_path = urdf_tutorial_path / 'urdf/my_robot3.urdf'
    default_rviz_config_path = urdf_tutorial_path / 'rviz/my_robot.rviz'

    # world_path = urdf_tutorial_path/ 'world/my_world.sdf'

    
    gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return LaunchDescription([
        gui_arg,
        model_arg,
        rviz_arg,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
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
