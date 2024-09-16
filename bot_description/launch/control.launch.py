from launch import LaunchDescription
from launch_ros.actions import Node 
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    teleop_twist_keyboard_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        output="screen",
        prefix='xterm -e',  # Optional: opens in a new terminal if desired
    )


    return LaunchDescription([
        teleop_twist_keyboard_node,
    ])