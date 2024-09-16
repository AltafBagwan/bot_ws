import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (Command, LaunchConfiguration)
from launch_ros.actions import (Node, SetParameter)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

# ROS2 Launch System will look for this function definition #
def generate_launch_description():

    # Get Package Description and Directory #
    package_description = "bot_description"
    package_directory = get_package_share_directory(package_description)


    # Load URDF File #
    urdf_file = 'my_bot.urdf'
    robot_desc_path = os.path.join(package_directory, "urdf", urdf_file)
    with open(robot_desc_path,'r') as f:
        robot_desc = f.read()
    print("URDF Loaded !")


    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
                    launch_arguments={
                        'pause' : 'True',
                        'gz_args' :'-v 4'+ ' -r ' + package_directory + '/world/empty.sdf',
                    }.items(),
                )

    rviz = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('bot_description'), 'launch'), '/rviz.launch.py']),)

    # Robot State Publisher (RSP) #
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        output="screen",
        emulate_tty=True,
        parameters=[{
                     'robot_description': Command(['xacro ', robot_desc_path])}]  #'robot_description': Command(['xacro ', robot_desc_path]) use this if file use any type of 
                                                        #xacro functionality
    )

    gz_spawn_entity = Node(package='ros_gz_sim',
                    executable='create',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'robot'],
                    output='screen')

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                   '/imu@sensor_msgs/msg/Imu@ignition.msgs.IMU',
                   '/lidar@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan' ,
                   '/rgbd_camera@std_msgs/msg/ColorRGBA@gz.msgs.Color'
                    ],
        output='screen'
    )

    # Create and Return the Launch Description Object #
    return LaunchDescription(
        [   gazebo,
            # Sets use_sim_time for all nodes started below (doesn't work for nodes started from ignition gazebo) #
            # SetParameter(name="use_sim_time", value=True),
            bridge,
            robot_state_publisher_node,
            gz_spawn_entity,
            # rviz

        ]
    )