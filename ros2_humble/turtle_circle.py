#!/usr/bin/env python3
"""ROS 2 Humble turtlesim velocity command example."""
import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class CircleController(Node):
    def __init__(self):
        super().__init__("turtle_circle_controller")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.05, self.publish_command)

    def publish_command(self):
        command = Twist()
        command.linear.x = 1.0
        command.angular.z = 1.0
        self.publisher.publish(command)


def main():
    rclpy.init()
    node = CircleController()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
