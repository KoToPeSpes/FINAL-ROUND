import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class FakeSensorNode(Node):
    def __init__(self):
        super().__init__('fake_sensor')
        self.pub = self.create_publisher(Float32, "my_sensor", 10)
        self.timer = self.create_timer(0.2, self.temperatura)
    
    def temperatura(self):
        otklonenie = random.uniform(-3.0, 3.0)
        msg = Float32()
        msg.data = 25 + otklonenie
        self.pub.publish(msg)
        self.get_logger().info(msg.data)

def main():
    rclpy.init()
    node = FakeSensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        ...
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()