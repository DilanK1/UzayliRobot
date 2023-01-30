import os
import launch
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
import launch_ros
from launch.actions import ExecuteProcess

def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(package='my_robot').find('my_robot')
    default_model_path = os.path.join(pkg_share, 'urdf/my_robot3.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/my_robot.rviz')
    world_path = os.path.join(pkg_share, 'world/worldd.sdf')
   
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

    # diff_node = Node(
    #     package='diff_drive_controller',
    #     node_executable='diff_drive_controller_node',
    #     node_name='diff_drive_controller',
    #     parameters=[{'tf_prefix': 'my_robot'}],
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

    # robot_localization_node = launch_ros.actions.Node(
    #      package='robot_localization',
    #      executable='ekf_node',
    #      name='ekf_filter_node',
    #      output='screen',
    #      parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    # )

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
        # robot_localization_node,
        rviz_node,
        # diff_node
    ])

    # gzserver = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
    #     ),
    #     launch_arguments={'world': world_path}.items(),
    # )

    # gzclient = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
    #     ),
    # )
