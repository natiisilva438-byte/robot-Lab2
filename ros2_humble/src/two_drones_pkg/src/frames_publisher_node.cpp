#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.h>

#include <geometry_msgs/msg/transform_stamped.hpp>
#include <cmath>
#include <iostream>
#include <memory>
#include <rclcpp/create_timer.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/timer.hpp>

class FramesPublisherNode : public rclcpp::Node {
  rclcpp::Time startup_time;

  rclcpp::TimerBase::SharedPtr heartbeat;

  std::unique_ptr<tf2_ros::TransformBroadcaster> broadcaster_;

 public:
  FramesPublisherNode() : Node("frames_publisher_node") {

    broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    startup_time = now();
    heartbeat = create_timer(this,
                             get_clock(),
                             rclcpp::Duration::from_seconds(0.02),
                             std::bind(&FramesPublisherNode::onPublish, this));
    heartbeat->reset();
  }

  void onPublish() {

    const double time = (now() - startup_time).seconds();

    geometry_msgs::msg::TransformStamped world_T_av1;
    geometry_msgs::msg::TransformStamped world_T_av2;

    const auto stamp = now();
    world_T_av1.header.stamp = stamp;
    world_T_av1.header.frame_id = "world";
    world_T_av1.child_frame_id = "av1";
    world_T_av1.transform.translation.x = std::cos(time);
    world_T_av1.transform.translation.y = std::sin(time);
    world_T_av1.transform.translation.z = 0.0;
    // Yaw aligns AV1's y axis with its circular tangent.
    tf2::Quaternion av1_rotation;
    av1_rotation.setRPY(0.0, 0.0, time);
    av1_rotation.normalize();
    world_T_av1.transform.rotation.x = av1_rotation.x();
    world_T_av1.transform.rotation.y = av1_rotation.y();
    world_T_av1.transform.rotation.z = av1_rotation.z();
    world_T_av1.transform.rotation.w = av1_rotation.w();

    world_T_av2.header.stamp = stamp;
    world_T_av2.header.frame_id = "world";
    world_T_av2.child_frame_id = "av2";
    world_T_av2.transform.translation.x = std::sin(time);
    world_T_av2.transform.translation.y = 0.0;
    world_T_av2.transform.translation.z = std::cos(2.0 * time);
    world_T_av2.transform.rotation.w = 1.0;

    broadcaster_->sendTransform(world_T_av1);
    broadcaster_->sendTransform(world_T_av2);
  }
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FramesPublisherNode>());
  return 0;
}
