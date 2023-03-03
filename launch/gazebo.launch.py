
import os
import launch
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(
        package='my_robot').find('my_robot')
    world_path = os.path.join(pkg_share, 'world/my_world.sdf')

    world_file_name = 'my_world.model'
    world = os.path.join(get_package_share_directory(
        'my_robot'), 'world', world_file_name)

    xacro_urdf_path = os.path.join(get_package_share_directory(
        'my_robot'), 'urdf_amr', 'amr_mini.xacro')

    robot_description_config = xacro.process_file(xacro_urdf_path)
    robot_desc = robot_description_config.toxml()

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items(),
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}
                    ]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # Robotu gazeboya aktarmak için
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-topic', '/robot_description'],
        output='screen'
    )

    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_path, '-s', 'libgazebo_ros_factory.so'], output='screen')

    return launch.LaunchDescription([

        gzserver,
        gzclient,
        joint_state_publisher_node,
        robot_state_publisher_node,
        # # gazebo,
        # spawn_entity
    ])
