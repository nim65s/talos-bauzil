#!/usr/bin/env python
# O. Stasse 17/01/2020
# LAAS, CNRS
# from package robotpkg-talos-data
# Modified by T. Lasguignes 06/03/2020
# LAAS, CNRS

import os
import rospy
import time
import roslaunch
import rospkg

from std_srvs.srv import Empty

# Start roscore
import subprocess
roscore = subprocess.Popen('roscore')
time.sleep(1)

# Get the path to talos_data
arospack = rospkg.RosPack()
talos_data_path = arospack.get_path('talos_data')
talos_bauzil_path = arospack.get_path('talos_bauzil')

# Start talos_gazebo
rospy.init_node('starting_talos_gazebo', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

cli_args = [talos_bauzil_path+'/launch/script_talos_gazebo_bauzil.launch',
            'world_name:=bauzil_skins',
            'robot:=full_v2_ouster',
            'enable_leg_passive:=false'
           ]
roslaunch_args = cli_args[1:]
roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

launch_gazebo_alone = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
launch_gazebo_alone.start()
rospy.loginfo("talos_gazebo_bauzil started")

rospy.wait_for_service("/gazebo/pause_physics")
gazebo_pause_physics = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
gazebo_pause_physics()

time.sleep(10)
# Spawn talos model in gazebo
# "Barbaric" spawn for special pose in gazebo
spawn_file = [talos_data_path+'/launch/talos_spawn.launch']
#params for half-sitting pause
left_leg_pose='-J leg_left_1_joint 0.0 -J leg_left_2_joint 0.0 -J leg_left_3_joint -0.411354 -J leg_left_4_joint 0.859395 -J leg_left_5_joint -0.448041 -J leg_left_6_joint -0.001708'
right_leg_pose='-J leg_right_1_joint 0.0 -J leg_right_2_joint 0.0 -J leg_right_3_joint -0.411354 -J leg_right_4_joint 0.859395 -J leg_right_5_joint -0.448041 -J leg_right_6_joint -0.001708'
left_arm_pose='-J arm_left_1_joint 0.25847 -J arm_left_2_joint 0.173046 -J arm_left_3_joint -0.0002 -J arm_left_4_joint -0.525366 -J arm_left_5_joint 0.0 -J arm_left_6_joint 0.0 -J arm_left_7_joint 0.1'
right_arm_pose='-J arm_right_1_joint -0.25847 -J arm_right_2_joint -0.173046 -J arm_left_3_joint 0.0002 -J arm_right_4_joint -0.525366 -J arm_right_5_joint 0.0 -J arm_right_6_joint 0.0 -J arm_right_7_joint 0.1'
torso_pose='-J torso_1_joint 0.0 -J torso_2_joint 0.006761'
gzpose='-x -4.2 -y 0.0 -z 1.21 -R 0.0 -P 0.0 -Y 3.14 '+left_leg_pose+' '+right_leg_pose+' '+left_arm_pose+' '+right_arm_pose+' '+torso_pose
spawn_args = ['gzpose:='+gzpose]
spawn_roslaunch = [(roslaunch.rlutil.resolve_launch_arguments(spawn_file)[0], spawn_args)]
launch_gazebo_spawn_hs = roslaunch.parent.ROSLaunchParent(uuid,
                                                          spawn_roslaunch)
launch_gazebo_spawn_hs.start()
rospy.loginfo("talos_spawn half-sitting started")

rospy.wait_for_service("/gains/arm_left_1_joint/set_parameters")
time.sleep(10)
gazebo_unpause_physics = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
gazebo_unpause_physics()

# Start roscontrol
launch_bringup = roslaunch.parent.ROSLaunchParent(uuid,
                                                  [talos_data_path+'/launch/talos_bringup.launch'])
launch_bringup.start()
rospy.loginfo("talos_bringup started")

time.sleep(10)

# Start sot
roscontrol_sot_talos_path=arospack.get_path('roscontrol_sot_talos')
launch_roscontrol_sot_talos =roslaunch.parent.ROSLaunchParent(uuid,
                                                              [roscontrol_sot_talos_path+'/launch/sot_talos_controller_gazebo.launch'])
launch_roscontrol_sot_talos.start()
rospy.loginfo("roscontrol_sot_talos started")

time.sleep(10)

# Publish odometry
launch_odom = roslaunch.parent.ROSLaunchParent(uuid,
                                               [talos_bauzil_path+'/launch/talos_odometry.launch'])
launch_odom.start()
rospy.loginfo("Talos odometry started")

rospy.spin()

