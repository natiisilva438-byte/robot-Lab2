# Runtime demonstrations

These are actual screen recordings of the ROS Noetic programs running in an Ubuntu 20.04 root filesystem on AutoDL. Both videos are silent, 15-second H.264 MP4 files with browser-compatible pixel format and fast-start metadata. The PNG files are frames extracted from the videos at 6 seconds.

| File | Scene | Capture size | Capture frame rate |
| --- | --- | --- | --- |
| [drones_rviz.mp4](drones_rviz.mp4) | Two drone markers and the world/relative trajectories in RViz | 1280 x 800 | 10 fps |
| [turtlesim_circle.mp4](turtlesim_circle.mp4) | A turtle moving on a circular path | 500 x 500 | 20 fps |

The RViz scene uses the dynamic transforms published by `two_drones_pkg`. Rendering on this CPU-only host can update more slowly than the video capture rate.

The turtle receives `geometry_msgs/Twist` commands at 20 Hz, with `linear.x = 1.0` m/s and `angular.z = 1.0` rad/s. Its circular path has radius approximately 1 m.

## Run the drone scene

From the repository root after building the ROS 1 package:

```bash
source /opt/ros/noetic/setup.bash
source ros1_noetic/devel/setup.bash
roslaunch two_drones_pkg two_drones.launch
```

## Run turtlesim

Start `roscore` in one terminal. In a second terminal:

```bash
source /opt/ros/noetic/setup.bash
rosrun turtlesim turtlesim_node
```

In a third terminal, from the repository root:

```bash
source /opt/ros/noetic/setup.bash
python3 ros1_noetic/turtle_circle.py
```

Stop the controller with Ctrl+C.
