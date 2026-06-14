from rclpy.node import Node
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist

class TeleopNode(Node):
    def __init__(self):
        super().__init__("teleop_node")
        self.acc_sub = self.create_subscription(Vector3, "/acc", self.acc_callback, 10)
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Teleop Node started")

    def acc_callback(self, msg):
        twist = Twist()
        ax = msg.x
        ay = msg.y
        az = msg.z
        self.get_logger().info(f"Received Acc: {ax:.2f}, {ay:.2f}, {az:.2f}")
        twist.linear.x = ax 
        twist.angular.z = ay 
        self.publisher.publish(twist)

def main(args=None):
    import rclpy
    rclpy.init(args=args)
    node = TeleopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
