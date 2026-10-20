import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class HeartbeatNode(Node):
    def __init__(self):
        super().__init__('heartbeat_node')

        self.publisher_ = self.create_publisher(String, '/heartbeat', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # кожну секунду
        self.counter = 0

        self.get_logger().info('Heartbeat Node запущено')

    def timer_callback(self):
        msg = String()
        msg.data = f'alive | count={self.counter} | time={time.time():.0f}'
        self.publisher_.publish(msg)

        self.get_logger().info(f'Heartbeat: {msg.data}')
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
