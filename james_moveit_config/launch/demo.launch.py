# Simulated James (crate + OpenManipulator-X) with MoveIt and RViz: plan and try motions
# without the real arm.
#
#   ros2 launch james_moveit_config demo.launch.py
#
# Runs in its own ROS domain (77, localhost only), so it cannot interfere with the real arm on
# the network: the simulated arm also publishes /joint_states and accepts trajectories.
#
# Arm kinematics and joint limits come from open_manipulator_x_moveit_config, the ros2_control
# controller configuration from open_manipulator_x_bringup. James-specific are the robot model
# (james_description) and the SRDF (config/james.srdf).

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    robotis_moveit = get_package_share_directory('open_manipulator_x_moveit_config')
    robotis_bringup = get_package_share_directory('open_manipulator_x_bringup')

    moveit_config = (
        MoveItConfigsBuilder('james', package_name='james_moveit_config')
        .robot_description(mappings={'use_fake_hardware': 'true'})
        .robot_description_kinematics(
            file_path=os.path.join(robotis_moveit, 'config', 'kinematics.yaml'))
        .joint_limits(file_path=os.path.join(robotis_moveit, 'config', 'joint_limits.yaml'))
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    controller_spawners = [
        Node(package='controller_manager', executable='spawner', arguments=[controller])
        for controller in ('joint_state_broadcaster', 'arm_controller', 'gripper_controller')
    ]

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Start RViz'),

        SetEnvironmentVariable('ROS_DOMAIN_ID', '77'),
        SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[moveit_config.robot_description]),
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                moveit_config.robot_description,
                os.path.join(robotis_bringup, 'config', 'hardware_controller_manager.yaml')]),
        *controller_spawners,
        Node(
            package='moveit_ros_move_group',
            executable='move_group',
            output='screen',
            parameters=[moveit_config.to_dict()]),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(
                get_package_share_directory('james_moveit_config'), 'config', 'moveit.rviz')],
            parameters=[
                moveit_config.robot_description,
                moveit_config.robot_description_semantic,
                moveit_config.robot_description_kinematics,
                moveit_config.planning_pipelines,
                moveit_config.joint_limits],
            condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
