import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')

        # Підписка на зображення з камери
        # Можливі назви топіків: /image_raw, /camera/image_raw, /camera/image
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',          # зміни, якщо у тебе інший топік
            self.image_callback,
            10
        )

        self.bridge = CvBridge()
        self.get_logger().info('Vision Node запущено. Чекаю зображення...')

    def image_callback(self, msg):
        try:
            # Конвертація ROS Image → OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Помилка cv_bridge: {e}')
            return

        # === Базова обробка ===
        # 1. Grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # 2. Gaussian Blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 3. Threshold
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        # 4. (Опціонально) Edge Detection
        edges = cv2.Canny(blurred, 50, 150)

        # === Відображення ===
        cv2.imshow('Original', cv_image)
        cv2.imshow('Grayscale + Blur', blurred)
        cv2.imshow('Threshold', thresh)
        cv2.imshow('Edges (Canny)', edges)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
