        # Логування
        if limited:
            self.get_logger().warning(
                f'Швидкість обмежено! '
                f'linear.x={linear_x:.2f}, angular.z={angular_z:.2f}'
            )
        else:
            self.get_logger().info(
                f'Отримано: linear.x={linear_x:.2f}, angular.z={angular_z:.2f}'
            )
