import rclpy
from rclpy.node import Node

class CountdownNode(Node):
    def __init__(self):
        super().__init__('countdown')
        self.ticks = 5
        self.timer = self.create_timer(1.0, self.counting)
        self.get_logger().info('Нода отсчета запущена щас будем считать 0о0')
    
    def counting(self):
        if self.ticks > 0:
            self.get_logger().info(f'{self.ticks}')
            self.ticks -= 1
        elif self.ticks == 0:
            self.get_logger().info('Поехали!')
            self.ticks = -1


def main():
    rclpy.init()
    node = CountdownNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        ...
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()