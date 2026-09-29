#!/usr/bin/env python3
"""ROS Noetic turtlesim velocity-command demonstration."""
import rospy
from geometry_msgs.msg import Twist


def main():
    rospy.init_node("turtle_circle_controller")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        command = Twist()
        command.linear.x = 1.0
        command.angular.z = 1.0
        pub.publish(command)
        rate.sleep()
    pub.publish(Twist())


if __name__ == "__main__":
    main()
