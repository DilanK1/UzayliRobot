
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    package_name='my_robot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'myRobot'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
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


    # map_server = Node(
    #     package = 'nav2_map_server',
    #     executable = 'map_saver_server',
    #     name = 'map_server',
    #     emulate_tty=False,
    #     parameters=[{'save_map_timeout': 2000},
    #                     {'free_thresh_default': 0.25},
    #                     {'occupied_thresh_default': 0.65}]

    # )
    # start_lifecycle_manager_cmd = launch_ros.actions.Node(
    #         package='nav2_lifecycle_manager',
    #         executable='lifecycle_manager',
    #         name='lifecycle_manager',
    #         output='screen',
    #         emulate_tty=False, 
    #         parameters=[{'use_sim_time': True},
    #                     {'autostart': True},
    #                     {'node_names': lifecycle_nodes}])

    # slam_node = launch_ros.actions.Node(
    #     package = 'slam_toolbox',
    #     executable = 'async_slam_toolbox_node',
    #     name = 'slam',
    #     output ='screen',
    #     parameters = [{'map_file_name': '/home/dilan/foxy_ws/my_map_serial','use_sim_time': LaunchConfiguration('use_sim_time')}]
    #     # parameters=[os.path.join(pkg_share, 'config/mapper_params_online_async.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    # ) 