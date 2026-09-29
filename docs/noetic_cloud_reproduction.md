# ROS Noetic on the supplied AutoDL host

The cloud host is Ubuntu 22.04.3 with ROS 2 Humble. The course's ROS 1 package instead targets Ubuntu 20.04 and ROS Noetic. A Focal root filesystem was created at `/root/autodl-tmp/vnav_lab2/focal-rootfs` on the host data disk with `debootstrap`. Its APT sources use Ubuntu Focal and the ROS Noetic repository. The following packages were installed in that root filesystem: `ros-noetic-ros-base`, `ros-noetic-rviz`, `ros-noetic-turtlesim`, `ros-noetic-tf`, `ros-noetic-tf2-tools`, `python3-catkin-tools`, and `build-essential`.

The completed course package is in the root filesystem at `/root/vnav_ws/src/two_drones_pkg`. The tested build command was:

```bash
f=/root/autodl-tmp/vnav_lab2/focal-rootfs
proot -r "$f" -w /root -b /dev -b /proc -b /sys -b /tmp \
  /usr/bin/env -i HOME=/root \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  TERM=xterm LC_ALL=C /bin/bash -c \
  'source /opt/ros/noetic/setup.bash; cd /root/vnav_ws; catkin build -j1 --no-status'
```

The build reported `All 2 packages succeeded` and zero failures. Both executable nodes were checked in `/root/vnav_ws/devel/lib/two_drones_pkg`. A separate workspace at `/root/vnav_make_ws` also passed `catkin_make -j1`. PRoot supplies the pseudo-terminal and mounted `/dev` that `catkin build` requires on this host. The compiled ROS nodes run through an ordinary `chroot`.

For a cloud session, start `roscore` in one sourced Focal shell. To launch the dynamic or static scene in another sourced shell, use this pattern (the static mode adds `static:=true`):

```bash
f=/root/autodl-tmp/vnav_lab2/focal-rootfs
chroot "$f" /usr/bin/env -i HOME=/root \
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  TERM=xterm LC_ALL=C ROS_HOSTNAME=localhost \
  DISPLAY=127.0.0.1:100 LIBGL_ALWAYS_SOFTWARE=1 \
  /bin/bash -c \
  'source /opt/ros/noetic/setup.bash; source /root/vnav_ws/devel/setup.bash; exec roslaunch two_drones_pkg two_drones.launch'
```

The test used an Xvfb server on display `:100` with TCP enabled so the Focal RViz and turtlesim windows could start. The accompanying `evidence/noetic` logs show `rosnode` and topic connections, 30 live dynamic tf samples, 139 marker arrays, the static tf values, and turtlesim movement. The checker scripts in `checks/` can be run from a sourced Noetic shell while each scene is active. The Focal root filesystem remains on the cloud host; it is not included in the submission ZIP because it contains the installed operating system and ROS packages.
