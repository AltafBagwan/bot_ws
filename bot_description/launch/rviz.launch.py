from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkgPath= get_package_share_directory("bot_description")
    urdfModelPath=os.path.join(pkgPath,"urdf/my_bot.urdf")
    rvizConfigPath =os.path.join(pkgPath,"config/config.rviz")

    with open(urdfModelPath,'r') as f:
        robot_desc = f.read()
    params={"robot_description":robot_desc}

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],

    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        parameters=[params],

    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output ="screen",
        arguments=['-d', rvizConfigPath]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])

