# Mobile IMU Controller for TurtleBot3

A ROS 2 package that enables real-time control of a TurtleBot3 robot in Gazebo using smartphone IMU data streamed over UDP.

---

## Overview

This project uses a smartphone as a wireless motion controller for a TurtleBot3 robot. IMU data is transmitted over UDP to a ROS 2 node, filtered, and converted into velocity commands that drive the robot in simulation.

The system demonstrates:

- UDP communication
- Sensor data processing
- ROS 2 publishers and subscribers
- Real-time robot teleoperation
- TurtleBot3 integration in Gazebo
- Telemetry monitoring

---

## Features

- Real-time smartphone-to-robot control
- UDP-based IMU data streaming
- Accelerometer data filtering
- ROS 2 topic-based architecture
- TurtleBot3 simulation support
- Modular node design

---

## Nodes

### IMU Receiver Node

Receives IMU data from a smartphone over UDP, applies filtering, and publishes accelerometer values.

---

### Teleop Node

Subscribes to accelerometer data and converts phone motion into robot velocity commands.

---

### Dashboard Node

Subscribes to accelerometer data as well as velocity commands topic to display telemetry data to user. 

---

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- TurtleBot3 Packages
- Gazebo
- Smartphone capable of streaming IMU data over UDP

---

## Installation

Clone the repository into your ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/deeppil/mobile_imu_controller.git
```

Build the package:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

## Running

Start the IMU receiver:

```bash
ros2 run mobile_imu_controller imu_receiver
```

Start the teleoperation node:

```bash
ros2 run mobile_imu_controller teleop_node
```

Start the dashboard node:

```bash
ros2 run mobile_imu_controller dashboard_node
```

Verify accelerometer data:

```bash
ros2 topic echo /acc
```

Verify velocity commands:

```bash
ros2 topic echo /cmd_vel
```

---
