import os
import launch
from launch_ros.actions import Node
import launch_ros
from launch.substitutions import Command, LaunchConfiguration


def generate_launch_description():

    pkg_share = launch_ros.substitutions.FindPackageShare(
        package='my_robot').find('my_robot')
    
    twist_mux_params  = os.path.join(pkg_share , 'config', 'twist_mux.yaml')

    twist_mux_node= Node(
        package= 'twist_mux',
        executable= 'twist_mux',
        parameters= [twist_mux_params ,{'use_sim_time' : LaunchConfiguration('use_sim_time')}],
        remappings= [('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
    )

    twist_stamper_node = Node(
        package= 'twist_stamper',
        executable='twist_stamper',
        parameters= [{'use_sim_time':  LaunchConfiguration('use_sim_time')}],
        remappings= [('/cmd_vel_in','/cmd_vel'),
                     '/cmd_vel_out','/diff_cont/cmd_vel']
    )

    return launch.LaunchDescription([

        # twist_mux_node,
        twist_stamper_node
    ])
