#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from hero_common.msg import location
from cv_bridge import CvBridge,CvBridgeError

class CameraNode:
    def __init__(self):
        self.bridge = CvBridge()
        self.camera_pub = rospy.Publisher('camera/camera_feed', Image, queue_size=60)
        self.camera_sub = rospy.Subscriber('camera/image_raw', Image, self.camera_callback)
        self.circle_diameter_cm=6.7
        self.pub = rospy.Publisher('hero_1/cam_curr',location, queue_size=5)
        self.msg = location()

    def find_arena(self,econtours):
        for n in econtours:
            i,j,k,l=cv2.boundingRect(n)
            if (k*l)>600000 and (k*l)<730000:
                
                print('found',(k*l))
                return n
        
        
    def camera_callback(self, msg):
        try:
          cv_image = self.bridge.imgmsg_to_cv2(msg)
        except CvBridgeError as e:
          print(e)
        
        img_width, img_height = cv_image.shape[1], cv_image.shape[0]
        scale_factor=0.5
# Define the source and destination points for the perspective transformation
        src_points = np.float32([[0, 0], [img_width, 0], [img_width, img_height], [0, img_height]])
        dst_points = np.float32([[0, 0], [img_width, 0], [img_width * 0.88, img_height], [img_width * 0.12, img_height]])

# Calculate the perspective transformation matrix M
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        print(M)

        
        cv_image=cv2.warpPerspective(cv_image,M,(cv_image.shape[1], cv_image.shape[0]))    
        
        gray_image= cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        gray_image= cv2.bilateralFilter(gray_image,9,75,75)
        
       
        edges= cv2.Canny(gray_image,20,80)
        econtours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        _, binary_image=cv2.threshold(gray_image,250,255,cv2.THRESH_BINARY)
        contours,_ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        print(gray_image.shape)
        recontour= self.find_arena(econtours)
        i,j,k,l=cv2.boundingRect(recontour)
        cv2.rectangle(cv_image,(i,j), (i+k,j+l), (0,255,0), 2)
        #cv2.drawContours(cv_image,[recontour], -1, (0,255,0), 2)
        text1="Arena (0 cm,0 cm)"
        text2="Hero 1"
        font= cv2.FONT_HERSHEY_SIMPLEX
        font_scale=0.5
        font_thickness=1
        text_colour=(0,0,255)
        text_pos1=(i,j-10)
        cv2.putText(cv_image,text1,text_pos1,font,font_scale,text_colour, font_thickness)
        for contour in contours:
        
            if cv2.contourArea(contour)>10000 and cv2.contourArea(contour)<20000:
                epsilon=0.1*cv2.arcLength(contour,True)
                approx= cv2.approxPolyDP(contour,epsilon,True)
            
                x,y,w,h= cv2.boundingRect(approx)
                cv2.rectangle(cv_image, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.rectangle(binary_image, (x,y), (x+w,y+h), (0,255,0), 2)
                text_pos2=(x,y-10)
                
            
                print('focal is:',max(w,h))#focal length
                print(cv2.contourArea(contour))
                circle_diameter_pixels= max(w,h)
                circle_center_x= x+w//2
                circle_center_y= y+h//2
                focal=circle_diameter_pixels/self.circle_diameter_cm
                circle_diameter_cm= (circle_diameter_pixels / focal)
                self.msg.x=circle_center_x
                self.msg.y=circle_center_y
                self.pub.publish(self.msg)
                position_x= (circle_center_x - i)/focal
                position_y= (circle_center_y - j)/focal
                cv2.putText(cv_image,text2+" "+"("+str(position_x)+" cm"+","+str(position_y)+" cm"+")",text_pos2,font,font_scale,text_colour, font_thickness)
                
                print("Circle Diameter:",circle_diameter_cm)
                print("Robot Position:",circle_center_x, circle_center_y)
                
        
        #cv2.namedWindow("Image window", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("Image window",1200,1000)
        #cv2.imshow("Image window",cv_image)
        #cv2.waitKey(3)
        
        try:
          self.camera_pub.publish(self.bridge.cv2_to_imgmsg(cv_image))
        except CvBridgeError as e:
          print(e)

if __name__ == '__main__':
    rospy.init_node('camera_node')
    camera_node = CameraNode()
    rospy.spin()

