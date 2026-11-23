"""Читает из библиотеки TF, где стоит лидар, и публикует это тремя числами.

Раз в секунду спрашивает трансформацию от base_link к lidar и отправляет
её в топик /lidar_offset как [x, y, yaw]: смещение вперёд, смещение влево
и угол поворота вокруг вертикальной оси.
"""

import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


def quat_to_yaw(x, y, z, w):
    """Угол поворота вокруг вертикальной оси из четырёх чисел кватерниона."""
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

class GeometryMonitor(Node):
    def __init__(self):
        super().__init__("geometry_monitor")

        # buffer хранит известные трансформации,
        # listener наполняет его, читая /tf и /tf_static
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.offset_pub = self.create_publisher(Float32MultiArray, "/lidar_offset", 10)
        self.timer = self.create_timer(1.0, self.report)

        self.get_logger().info("geometry_monitor запущен")

    def report(self):
        try:
            tf = self.tf_buffer.lookup_transform("base_link", "lidar", rclpy.time.Time())
        except TransformException as error:
            self.get_logger().warn(f"Трансформация пока недоступна: {error}")
            return

        t = tf.transform.translation
        q = tf.transform.rotation
        yaw = quat_to_yaw(q.x, q.y, q.z, q.w)

        out = Float32MultiArray()
        out.data = [float(t.x), float(t.y), float(yaw)]
        self.offset_pub.publish(out)


def main():
    rclpy.init()
    node = GeometryMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
