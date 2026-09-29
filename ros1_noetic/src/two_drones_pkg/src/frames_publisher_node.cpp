#include <ros/ros.h>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/TransformStamped.h>

#include <iostream>
#include <cmath>

class FramesPublisherNode {
 private:
  ros::NodeHandle nh;
  ros::Time startup_time;

  ros::Timer heartbeat;
  tf2_ros::TransformBroadcaster broadcaster;

 public:
  FramesPublisherNode() {
    startup_time = ros::Time::now();
    heartbeat =
        nh.createTimer(ros::Duration(0.02), &FramesPublisherNode::onPublish, this);
    heartbeat.start();
  }

  void onPublish(const ros::TimerEvent&) {
    const double time = (ros::Time::now() - startup_time).toSec();

    geometry_msgs::TransformStamped AV1World;
    geometry_msgs::TransformStamped AV2World;

    AV1World.transform.rotation.w = 1.0;
    AV2World.transform.rotation.w = 1.0;

    const ros::Time stamp = ros::Time::now();
    AV1World.header.stamp = stamp;
    AV1World.header.frame_id = "world";
    AV1World.child_frame_id = "av1";
    AV1World.transform.translation.x = std::cos(time);
    AV1World.transform.translation.y = std::sin(time);
    AV1World.transform.translation.z = 0.0;
    // Yaw aligns AV1's y axis with its circular tangent.
    tf2::Quaternion av1_rotation;
    av1_rotation.setRPY(0.0, 0.0, time);
    av1_rotation.normalize();
    AV1World.transform.rotation.x = av1_rotation.x();
    AV1World.transform.rotation.y = av1_rotation.y();
    AV1World.transform.rotation.z = av1_rotation.z();
    AV1World.transform.rotation.w = av1_rotation.w();

    AV2World.header.stamp = stamp;
    AV2World.header.frame_id = "world";
    AV2World.child_frame_id = "av2";
    AV2World.transform.translation.x = std::sin(time);
    AV2World.transform.translation.y = 0.0;
    AV2World.transform.translation.z = std::cos(2.0 * time);

    broadcaster.sendTransform(AV1World);
    broadcaster.sendTransform(AV2World);
  }
};

int main(int argc, char** argv) {
  ros::init(argc, argv, "frames_publisher_node");
  FramesPublisherNode node;
  ros::spin();
  return 0;
}
