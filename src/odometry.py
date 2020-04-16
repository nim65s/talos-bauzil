#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import PoseWithCovarianceStamped
from gazebo_msgs.srv import GetModelState, GetModelStateRequest

# Init node
rospy.init_node('odometry_pub')

# Init Publisher
publisher = rospy.Publisher('/odom', Odometry, queue_size=1)
publisher_aicp = rospy.Publisher('/odom_aicp', PoseWithCovarianceStamped, queue_size=1)

rospy.wait_for_service('/gazebo/get_model_state')
get_mod_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)


odom = Odometry()
headodom = Header()
headodom.frame_id = '/world'

posecova = PoseWithCovarianceStamped()
headcova = Header()
headcova.frame_id = '/world'

model = GetModelStateRequest()
model.model_name = 'talos'

watch = rospy.Rate(2)

while not rospy.is_shutdown():
    state = get_mod_srv(model)

    odom.pose.pose = state.pose
    odom.twist.twist = state.twist
    odom.child_frame_id = '/base_link'

    posecova.pose.pose = state.pose

    stamp = rospy.Time.now()
    headodom.stamp = stamp
    headcova.stamp = stamp
    
    odom.header = headodom
    posecova.header = headcova

    publisher.publish(odom)
    publisher_aicp.publish(posecova)

    watch.sleep()
