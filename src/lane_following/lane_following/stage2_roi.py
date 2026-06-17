import rclpy # ROS2 Python library lets Python talk to ROS
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

import cv2
import numpy as np

class LaneFollower(Node):
    def __init__(self):
        super().__init__('lane_follower')

        # Convert ROS images -> OpenCV
        self.bridge = CvBridge()

        # Subscribe to camera, run image callback everytime Image is published
        self.sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publish motion commands
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Control gain
        self.kp = 0.8
        self.prev_angular = 0.0
        self.alpha = 0.6 # Smoothing factor for angular velocity

        self.get_logger().info("Lane follower started")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        error = self.detect_lane_error(frame)
        twist = Twist()

        # P-controller
        twist.linear.x = 0.05
        new_angular = -self.kp * error
        # Exponential smoothing to prevent jerky movements
        twist.angular.z = self.alpha * self.prev_angular + (1 - self.alpha) * new_angular
        self.prev_angular = twist.angular.z
        self.pub.publish(twist)

        cv2.imshow("camera", frame)
        cv2.waitKey(1)

    def detect_lane_error(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Removes color for easier processing
        blur = cv2.GaussianBlur(gray, (5, 5), 0) # Removes noise
        edges = cv2.Canny(blur, 50, 150) # Finds strong boundaries

        height, width = edges.shape

        # Focus on bottom 40%
        roi_top = int(height * 0.6)
        roi = edges[roi_top:height, :]

        lines = cv2.HoughLinesP( # Finds straight line segments in image
            roi,
            1,
            np.pi / 180,
            threshold=50,
            minLineLength=40,
            maxLineGap=100
        )

        center_frame = width / 2

        if lines is None: # If no lines identified
            return 0.0

        left_x, right_x = [], []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)

            if abs(slope) > 5: # Filter out nearly horizontal or vertical lines
                continue
            if slope < 0:
                left_x += [x1, x2]
            else:
                right_x += [x1, x2]

        if len(left_x) == 0 or len(right_x) == 0: # Assume robot is centered if we can't see either left or right lane
            return 0.0
        print("Left x:", len(left_x), "Right x:", len(right_x))
        lane_center = (np.mean(left_x) + np.mean(right_x)) / 2

        error = (lane_center - center_frame) / center_frame # Negative means we want to turn left
        return error


def main():
    rclpy.init()
    node = LaneFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()