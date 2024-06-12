#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from hero_common.msg import location
import tf.transformations as tf
import numpy as np
import math
import time

class NavListener:
    def __init__(self):
        rospy.init_node('nav_listener', anonymous=True)
        self.reference_orientation = None
        self.imu_subscriber = rospy.Subscriber('/hero_1/imu', Imu, self.imu_callback)
        self.dest_subscriber= rospy.Subscriber('/hero_1/cam_dest', location, self.dest_callback)
        self.curr_subscriber= rospy.Subscriber('/hero_1/cam_curr', location, self.curr_callback)
        self.director_pub= rospy.Publisher('hero_1/velocity_controller/cmd_vel', Twist, queue_size = 1)
        self.current_pos_x,self.current_pos_y = None, None
        self.destination_pos_x, self.destination_pos_y= self.current_pos_x,self.current_pos_y

    def goal_check(self):
        if self.destination_pos_x == self.current_pos_x and self.destination_pos_y == self.current_pos_y:
            return True
        distance= math.sqrt(((self.current_pos_x - self.destination_pos_x)**2) + ((self.current_pos_y - self.destination_pos_y)**2))
        if distance < 130:
            print('distance',distance)
            return True
        return False
    
    def imu_callback(self, imu_msg):
        if self.reference_orientation is None:
            # Extract orientation quaternion from IMU message
            orientation = imu_msg.orientation
            orientation_quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]

            # Convert quaternion to Euler angles (roll, pitch, yaw)
            self.reference_orientation = tf.euler_from_quaternion(orientation_quaternion)

            rospy.loginfo("Reference orientation set: Roll=%f, Pitch=%f, Yaw=%f",
                          self.reference_orientation[0], self.reference_orientation[1], self.reference_orientation[2])

        if  self.goal_check():
            stop_msg=Twist()
            self.director_pub.publish(stop_msg)
        if not self.goal_check():
            stop_msg=Twist()
            self.director_pub.publish(stop_msg)
            # Process subsequent IMU readings relative to the reference orientation
            current_degrees= self.process_imu_data(imu_msg)        
            if self.destination_pos_x < self.current_pos_x and self.destination_pos_y > self.current_pos_y: #bottomleft quad
                raw_degree_required=math.degrees( math.atan((self.destination_pos_y - self.current_pos_y) / (self.current_pos_x - self.destination_pos_x)))
                req_degrees= -180 + raw_degree_required
                print("req1",req_degrees,raw_degree_required)
            
            if self.destination_pos_x > self.current_pos_x and self.destination_pos_y > self.current_pos_y: #bottomright quad
                raw_degree_required= math.degrees(math.atan((self.destination_pos_y - self.current_pos_y) / (self.destination_pos_x - self.current_pos_x)))
                req_degrees= -raw_degree_required
                print("req2",req_degrees,raw_degree_required)
            
            if self.destination_pos_x < self.current_pos_x and self.destination_pos_y < self.current_pos_y: #topleft quad
                raw_degree_required= math.degrees(math.atan((self.current_pos_y - self.destination_pos_y) / (self.current_pos_x - self.destination_pos_x)))
                req_degrees= 180 - raw_degree_required
                print("req3",req_degrees,raw_degree_required)
            
            if self.destination_pos_x > self.current_pos_x and self.destination_pos_y < self.current_pos_y: #topright quad
                raw_degree_required= math.degrees(math.atan((self.current_pos_y - self.destination_pos_y) / (self.destination_pos_x - self.current_pos_x)))
                req_degrees= raw_degree_required
                print("req4",req_degrees,raw_degree_required)
            
            if current_degrees > (req_degrees - 15.0) and current_degrees < (req_degrees + 15.0):
                # move the robot front
                print("moving front")
                twist_msg=Twist()
                twist_msg.linear.x=0.1
                self.director_pub.publish(twist_msg)
                
                
            
            if current_degrees < (req_degrees - 15.0) or current_degrees > (req_degrees + 15.0):
                # fix the orientation
                stop_msg=Twist()
                self.director_pub.publish(stop_msg)
                urrent_degrees = current_degrees if current_degrees > 0 else current_degrees + 360
                eq_degrees = req_degrees if req_degrees > 0 else req_degrees + 360
                if urrent_degrees - eq_degrees > 0 and urrent_degrees - eq_degrees < 180:
                    #right turn
                    print("moving r")
                    twist_msg=Twist()
                    twist_msg.angular.z= -1.5
                    self.director_pub.publish(twist_msg)
                    
                    
                if urrent_degrees - eq_degrees < 0 and urrent_degrees - eq_degrees > -180:
                    #left turn
                    print("moving l")
                    twist_msg=Twist()
                    twist_msg.angular.z= 1.5
                    self.director_pub.publish(twist_msg)
                    
                    
                if urrent_degrees - eq_degrees > 0 and urrent_degrees - eq_degrees > 180:
                    #left turn
                    print("moving l")
                    twist_msg=Twist()
                    twist_msg.angular.z= 1.5
                    self.director_pub.publish(twist_msg)
                    
                    
                if urrent_degrees - eq_degrees < 0 and urrent_degrees - eq_degrees < -180:
                    #right turn
                    print("moving r")
                    twist_msg=Twist()
                    twist_msg.angular.z= -1.5
                    self.director_pub.publish(twist_msg)
                    
                    
                
                
    def dest_callback(self,dloc_msg):
        self.destination_pos_x, self.destination_pos_y = dloc_msg.x, dloc_msg.y
    
    def curr_callback(self,cloc_msg):
        self.current_pos_x, self.current_pos_y = cloc_msg.x, cloc_msg.y

    def process_imu_data(self, imu_msg):
        # Extract orientation quaternion from IMU message
        orientation = imu_msg.orientation
        orientation_quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]

        # Convert quaternion to Euler angles (roll, pitch, yaw)
        current_orientation = tf.euler_from_quaternion(orientation_quaternion)

        # Calculate relative orientation (difference from reference orientation)
        relative_orientation = np.array(current_orientation) - np.array(self.reference_orientation)

        # Example calculation: convert relative orientation to degrees
        relative_orientation_degrees = np.degrees(relative_orientation)

        # Example usage: print relative orientation in degrees
        rospy.loginfo("Relative orientation (degrees): Roll=%f, Pitch=%f, Yaw=%f",
                      relative_orientation_degrees[0], relative_orientation_degrees[1], relative_orientation_degrees[2])

        
        return relative_orientation_degrees[2]

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    nav_listener = NavListener()
    nav_listener.run()



