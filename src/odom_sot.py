#!/usr/bin/env python2

import rospy
import tf
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, TwistStamped
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from dynamic_graph_bridge_msgs.msg import Vector
from dynamic_graph_bridge_msgs.msg import Matrix



#def callbacks
twist = Vector([0.0,0.0,0.0,0.0,0.0,0.0])
def process_twist(data):
    global twist
    twist = data
    
pose = Vector([0.0,0.0,0.0,0.0,0.0,0.0,0.0])
def process_pose(data):
    global pose
    pose = data
    

# Init node
rospy.init_node('sot_odometry_pub')


# Init Publisher
publisher = rospy.Publisher('/odom_sot', Odometry, queue_size=1)
publisher_aicp = rospy.Publisher('/odom_sot_aicp', PoseWithCovarianceStamped, queue_size=1)
publisher_tf = tf.TransformBroadcaster()

odom = Odometry()
headodom = Header()
headodom.frame_id = '/world'

posecova = PoseWithCovarianceStamped()
headcova = Header()
headcova.frame_id = '/world'

# Init subscribers
# The topics subscribed to are created in appli_online_walking.py and are sot dynamic-graph messages 
# that contain the necessary for odometry. The callbacks allow to store the data in order to be converted in the loop. 
v = rospy.Subscriber("/sot/base_estimator/v", Vector, process_twist)
quat = rospy.Subscriber("/sot/e2q/quaternion", Vector, process_pose)

watch = rospy.Rate(10)

while not rospy.is_shutdown():
    
   
    #defining pose part of odom
    odom.pose.pose.position.x = pose.data[0]
    odom.pose.pose.position.y = pose.data[1]
    odom.pose.pose.position.z = pose.data[2]
    odom.pose.pose.orientation.x = pose.data[3]
    odom.pose.pose.orientation.y = pose.data[4]
    odom.pose.pose.orientation.z = pose.data[5]
    odom.pose.pose.orientation.w = pose.data[6]

    #defining twist part of odom
    odom.twist.twist.linear.x = twist.data[0]
    odom.twist.twist.linear.y = twist.data[1]
    odom.twist.twist.linear.z = twist.data[2]
    odom.twist.twist.angular.x = twist.data[3]
    odom.twist.twist.angular.y = twist.data[4]
    odom.twist.twist.angular.z = twist.data[5]

    #pose cova
    posecova.pose.pose=odom.pose.pose
    #defining child frame
    odom.child_frame_id = '/base_link'


    #timestamp in headers
    stamp = rospy.Time.now()
    headodom.stamp = stamp
    headcova.stamp = stamp
    
    odom.header = headodom
    posecova.header = headcova

    publisher_tf.sendTransform((odom.pose.pose.position.x, odom.pose.pose.position.y, odom.pose.pose.position.z),
                               (odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w),
                                stamp,
                                "base_link",
                                "world")
    publisher.publish(odom)
    publisher_aicp.publish(posecova)

    try:
        watch.sleep()
    except rospy.ROSInterruptException:
        rospy.logwarn("Stopped sot odom")
        exit()
