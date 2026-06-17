import tkinter as tk

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3, Twist


class DashboardNode(Node):

    def __init__(self):
        super().__init__("dashboard_node")

        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0

        self.linear_x = 0.0
        self.angular_z = 0.0

        self.create_subscription(
            Vector3,
            "/acc",
            self.acc_callback,
            10
        )

        self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmd_callback,
            10
        )

        self.root = tk.Tk()
        self.root.title("ROMI Telemetry Dashboard")
        self.root.geometry("400x250")

        self.acc_label = tk.Label(
            self.root,
            text="ACC",
            font=("Arial", 14)
        )
        self.acc_label.pack(pady=10)

        self.vel_label = tk.Label(
            self.root,
            text="VEL",
            font=("Arial", 14)
        )
        self.vel_label.pack(pady=10)

        self.update_gui()

    def acc_callback(self, msg):
        self.ax = msg.x
        self.ay = msg.y
        self.az = msg.z

    def cmd_callback(self, msg):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def update_gui(self):

        self.acc_label.config(
            text=f"AX: {self.ax:.2f}\n"
                 f"AY: {self.ay:.2f}\n"
                 f"AZ: {self.az:.2f}"
        )

        self.vel_label.config(
            text=f"Linear X: {self.linear_x:.2f}\n"
                 f"Angular Z: {self.angular_z:.2f}"
        )

        self.root.after(100, self.update_gui)


def main(args=None):

    rclpy.init(args=args)

    node = DashboardNode()

    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.01)
        node.root.update()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()