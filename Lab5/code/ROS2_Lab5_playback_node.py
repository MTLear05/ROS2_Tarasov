import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import csv
import time
import os

class PlaybackNode(Node):
    def __init__(self):
        super().__init__('playback_node')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.filename = os.path.expanduser('~/ros2_ws/scenario.csv')

        if not os.path.exists(self.filename):
            self.get_logger().error(f'Файл не знайдено: {self.filename}')
            return

        self.get_logger().info(f'Відтворення сценарію з файлу: {self.filename}')
        self.play_scenario()

    def play_scenario(self):
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        if not data:
            self.get_logger().warning('Файл порожній')
            return

        previous_time = 0.0

        for row in data:
            current_time = float(row['time'])
            linear_x = float(row['linear_x'])
            angular_z = float(row['angular_z'])

            # Затримка між командами (синхронізація часу)
            delay = current_time - previous_time
            if delay > 0:
                time.sleep(delay)

            # Публікуємо команду
            msg = Twist()
            msg.linear.x = linear_x
            msg.angular.z = angular_z
            self.publisher_.publish(msg)

            self.get_logger().info(
                f'Відтворено: t={current_time:.2f}s | linear.x={linear_x:.2f} | angular.z={angular_z:.2f}'
            )

            previous_time = current_time

        # Зупинка в кінці
        stop_msg = Twist()
        self.publisher_.publish(stop_msg)
        self.get_logger().info('Відтворення завершено')

def main(args=None):
    rclpy.init(args=args)
    node = PlaybackNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
