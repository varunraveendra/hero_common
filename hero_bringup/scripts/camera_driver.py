#!/usr/bin/env python3

import rospy
import subprocess
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError


class cameradrive:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=60)
        self.capture = cv2.VideoCapture(0)

    def capture_image(self):
        returnValue, image_data_cv= self.capture.read()
        if returnValue==True:
            rospy.loginfo('Captured Successfully')
            image_data=self.bridge.cv2_to_imgmsg(image_data_cv)
            self.image_pub.publish(image_data)

if __name__ == '__main__':
    rospy.init_node('cameradrive')
    node = cameradrive()
    rate = rospy.Rate(60)  # 10 Hz
    while not rospy.is_shutdown():
        node.capture_image()
        rate.sleep()

