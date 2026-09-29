"""Verify live Noetic tf and visualization messages for MIT VNAV Lab 2."""
import math
import time

import rospy
import tf2_ros
from visualization_msgs.msg import MarkerArray


def main():
    rospy.init_node("lab2_noetic_runtime_verifier", anonymous=True)
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)
    marker_sizes = []
    rospy.Subscriber("/visuals", MarkerArray,
                     lambda msg: marker_sizes.append(len(msg.markers)))
    errors = {name: 0.0 for name in (
        "av1_radius", "av1_yaw", "av2_parabola", "relative_plane",
        "relative_ellipse", "relative_composition")}
    samples = 0
    deadline = time.monotonic() + 20.0
    while time.monotonic() < deadline and samples < 30 and not rospy.is_shutdown():
        try:
            w1 = buffer.lookup_transform("world", "av1", rospy.Time(0),
                                         rospy.Duration(0.2))
            w2 = buffer.lookup_transform("world", "av2", rospy.Time(0),
                                         rospy.Duration(0.2))
            a12 = buffer.lookup_transform("av1", "av2", rospy.Time(0),
                                          rospy.Duration(0.2))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException):
            continue
        x1, y1 = w1.transform.translation.x, w1.transform.translation.y
        x2, y2, z2 = (w2.transform.translation.x,
                      w2.transform.translation.y, w2.transform.translation.z)
        xr, yr, zr = (a12.transform.translation.x,
                      a12.transform.translation.y, a12.transform.translation.z)
        q = w1.transform.rotation
        cos_yaw = 1.0 - 2.0 * q.z * q.z
        sin_yaw = 2.0 * q.z * q.w
        xp = xr + 1.0
        yp = (yr + 0.5 + 2.0 * zr) / math.sqrt(5.0)
        predicted_xr = x1 * (x2 - x1) + y1 * (y2 - y1)
        predicted_yr = -y1 * (x2 - x1) + x1 * (y2 - y1)
        current = {
            "av1_radius": abs(x1 * x1 + y1 * y1 - 1.0),
            "av1_yaw": max(abs(cos_yaw - x1), abs(sin_yaw - y1)),
            "av2_parabola": max(abs(y2), abs(z2 - (1.0 - 2.0 * x2 * x2))),
            "relative_plane": abs(zr - 2.0 * yr - 1.0),
            "relative_ellipse": abs((xp / 0.5) ** 2 +
                                    (yp / (math.sqrt(5.0) / 2.0)) ** 2 - 1.0),
            "relative_composition": max(abs(xr - predicted_xr),
                                        abs(yr - predicted_yr), abs(zr - z2)),
        }
        for key, value in current.items():
            errors[key] = max(errors[key], value)
        samples += 1
        rospy.sleep(0.1)
    print("samples={} marker_arrays={} marker_count_set={}".format(
        samples, len(marker_sizes), sorted(set(marker_sizes))))
    for key, value in errors.items():
        print("max_{}_error={:.9g}".format(key, value))
    assert samples >= 10, "Too few live tf samples"
    assert marker_sizes and 5 in marker_sizes, "Expected two meshes and three trails"
    for key in ("av1_radius", "av1_yaw", "av2_parabola", "relative_plane",
                "relative_ellipse"):
        assert errors[key] < 1e-5, key
    assert errors["relative_composition"] < 0.15
    print("PASS: live ROS 1 Noetic transforms and visualization markers")
    del listener


if __name__ == "__main__":
    main()
