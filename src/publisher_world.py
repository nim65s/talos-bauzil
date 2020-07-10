#! /usr/bin/env python

import rospy
import tf
from gazebo_msgs.srv import GetModelState, GetModelStateRequest

rospy.init_node('world_pub')

publisher = tf.TransformBroadcaster()

rospy.wait_for_service('/gazebo/get_model_state')
get_mod_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

model = GetModelStateRequest()
model.model_name = 'talos'

watch = rospy.Rate(100)

while not rospy.is_shutdown():
    state = get_mod_srv(model)

    publisher.sendTransform((state.pose.position.x, state.pose.position.y, state.pose.position.z),
                            (state.pose.orientation.x, state.pose.orientation.y, state.pose.orientation.z, state.pose.orientation.w),
                            rospy.Time.now(),
                            "base_link",
                            "world")

    try:
        watch.sleep()
    except rospy.ROSInterruptException:
        rospy.logwarn("%s stopped in 'watch.sleep()'.", rospy.get_name())
        exit()
