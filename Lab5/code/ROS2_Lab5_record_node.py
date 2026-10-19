import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import csv
import os

class RecordNode(Node):
    def __init__(self):
        super().__init__('record_node')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        # Файл для збереження сценарію
        self.filename = os.path.expanduser('~/ros2_ws/scenario.csv')
        self.start_time = time.time()
        self.recording = True

        # Створюємо файл і записуємо заголовок
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'linear_x', 'angular_z'])

        self.get_logger().info(f'Запис розпочато → {self.filename}')
        self.get_logger().info('Керуй роботом. Для зупинки запису натисни Ctrl+C')

    def cmd_callback(self, msg):
        if not self.recording:
            return

        current_time = time.time() - self.start_time
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Записуємо у файл
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([f'{current_time:.3f}', f'{linear_x:.3f}', f'{angular_z:.3f}'])

        self.get_logger().info(
            f'Записано: t={current_time:.2f}s | linear.x={linear_x:.2f} | angular.z={angular_z:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RecordNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Запис зупинено')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
