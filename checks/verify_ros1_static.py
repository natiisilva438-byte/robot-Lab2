"""Verify the ROS Noetic Lab 2 static tf tree and marker stream."""
import rospy
import tf2_ros
from visualization_msgs.msg import MarkerArray


def main():
    rospy.init_node("lab2_noetic_static_verifier", anonymous=True)
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)
    expected = {"av1": (1.0, 0.0, 0.0), "av2": (0.0, 0.0, 1.0)}
    for frame, position in expected.items():
        transform = buffer.lookup_transform("world", frame, rospy.Time(0),
                                            rospy.Duration(5.0))
        tr = transform.transform.translation
        rotation = transform.transform.rotation
        actual = (tr.x, tr.y, tr.z)
        print("{} translation={} rotation=({}, {}, {}, {})".format(
            frame, actual, rotation.x, rotation.y, rotation.z, rotation.w))
        assert all(abs(a - b) < 1e-12 for a, b in zip(actual, position))
        assert all(abs(a - b) < 1e-12 for a, b in zip(
            (rotation.x, rotation.y, rotation.z, rotation.w), (0, 0, 0, 1)))
    markers = rospy.wait_for_message("/visuals", MarkerArray, timeout=5.0)
    print("marker_count={}".format(len(markers.markers)))
    assert len(markers.markers) == 5
    print("PASS: static ROS 1 Noetic transforms and visualization markers")
    del listener


if __name__ == "__main__":
    main()
