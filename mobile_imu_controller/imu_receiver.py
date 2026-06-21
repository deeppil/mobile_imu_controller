import socket
import json

from rclpy.node import Node
from geometry_msgs.msg import Vector3


class IMUReceiver(Node):
    def __init__(self):
        super().__init__("imu_receiver")

        self.acc_pub = self.create_publisher(Vector3, "/acc", 10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 1212))
        self.sock.setblocking(False)

        self.timer = self.create_timer(0.01, self.update)

        self.prev_x = 0.0
        self.prev_y = 0.0
        self.prev_z = 0.0

        self.log_count = 0

        self.get_logger().info("IMU Receiver started")

    def low_pass_filter(self, current, previous, alpha=0.5):
        return alpha * current + (1 - alpha) * previous

    def update(self):
        latest_data = None

        while True:
            try:
                latest_data, _ = self.sock.recvfrom(4096)
            except BlockingIOError:
                break

        if latest_data is None:
            return

        try:
            packet = json.loads(latest_data.decode("utf-8"))
            ax = packet["data"]["x"]
            ay = packet["data"]["y"]
            az = packet["data"]["z"]
        except json.JSONDecodeError:
            groups = latest_data.decode("utf-8").strip().split("|")
            acc = [float(v) for v in groups[0].split(",")]
            ax = acc[0]
            ay = acc[1]
            az = acc[2]

        ax = self.low_pass_filter(ax, self.prev_x)
        ay = self.low_pass_filter(ay, self.prev_y)
        az = self.low_pass_filter(az, self.prev_z)

        deadzone = 0.1

        if abs(ax) < deadzone:
            ax = 0.0
        if abs(ay) < deadzone:
            ay = 0.0
        if abs(az) < deadzone:
            az = 0.0    

        self.prev_x = ax
        self.prev_y = ay
        self.prev_z = az

        msg = Vector3()
        msg.x = ax
        msg.y = ay
        msg.z = az

        self.acc_pub.publish(msg)

        if self.log_count % 20 == 0:
            self.get_logger().info(
                f"Filtered Acc: {ax:.3f}, {ay:.3f}, {az:.3f}"
            )

        self.log_count += 1


def main(args=None):
    import rclpy

    rclpy.init(args=args)

    node = IMUReceiver()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()