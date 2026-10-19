import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import random
from collections import deque

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')

        # Публікатор сирих та відфільтрованих даних
        self.raw_pub = self.create_publisher(Float32, '/sensor_data', 10)
        self.filtered_pub = self.create_publisher(Float32, '/sensor_data_filtered', 10)

        # (Опціонально) можливість зупиняти робота
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Параметри
        self.threshold = 80.0          # порогове значення
        self.window_size = 5           # розмір вікна для усереднення
        self.values = deque(maxlen=self.window_size)

        # Таймер 10 Гц (0.1 секунди)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info('Sensor Node запущено (10 Гц)')

    def timer_callback(self):
        # 1. Генерація тестових даних (симуляція сенсора)
        # Базове значення + шум
        raw_value = 50.0 + random.uniform(-15.0, 40.0)
        raw_value = max(0.0, min(100.0, raw_value))   # обмеження 0-100

        # Публікуємо сирі дані
        raw_msg = Float32()
        raw_msg.data = raw_value
        self.raw_pub.publish(raw_msg)

        # 2. Усереднення (фільтрація)
        self.values.append(raw_value)
        filtered_value = sum(self.values) / len(self.values)

        # Публікуємо відфільтровані дані
        filtered_msg = Float32()
        filtered_msg.data = filtered_value
        self.filtered_pub.publish(filtered_msg)

        # 3. Перевірка порогу
        if filtered_value > self.threshold:
            self.get_logger().warning(
                f'УВАГА! Перевищено поріг: {filtered_value:.2f} > {self.threshold}'
            )
            # (Опціонально) зупиняємо робота
            self.stop_robot()
        else:
            self.get_logger().info(
                f'Сире: {raw_value:.2f} | Відфільтроване: {filtered_value:.2f}'
            )

    def stop_robot(self):
        """Зупинка робота при критичному значенні"""
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        self.cmd_pub.publish(stop_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
