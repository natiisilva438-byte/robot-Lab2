cmake_minimum_required(VERSION 3.1)
project(two_drones_pkg)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(catkin REQUIRED COMPONENTS roscpp rospy geometry_msgs visualization_msgs tf2 tf2_ros)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

add_executable(frames_publisher_node src/frames_publisher_node.cpp)
target_link_libraries(frames_publisher_node ${catkin_LIBRARIES})

add_executable(plots_publisher_node src/plots_publisher_node.cpp)
target_link_libraries(plots_publisher_node ${catkin_LIBRARIES})
