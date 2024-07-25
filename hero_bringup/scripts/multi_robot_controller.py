#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg  import Float32

class MultiRobotController:
    def __init__(self):
        rospy.init_node('multi_robot_controller',anonymous=True)
        self.robot_names=rospy.get_param('/robot_names',[])
        self.subscribers=[]
        self.publishers={}
        
        self.linear_true=rospy.get_param('~linear_true',0.1)
        self.angular_true=rospy.get_param('~angular_true',0.5)
        self.linear_false=rospy.get_param('~linear_false',0.1)
        self.angular_false=rospy.get_param('~angular_false',0.5)
        
        
        for robot_name in self.robot_names:
            topic_name=f"/{robot_name}/distance"
            self.subscribers.append(rospy.Subscriber(topic_name,Float32,self.callback,robot_name))
            self.publishers[robot_name]=rospy.Publisher(f"/{robot_name}/velocity_controller/cmd_vel",Twist,queue_size=10)
            
        rospy.spin()
    
    def callback(self,data,robot_name):
        if self.condition_met(data)==1:
            self.send_velocity_1(robot_name)
        elif self.condition_met(data)==3:
            self.send_velocity_2(robot_name)
        elif self.condition_met(data)==2:
            self.send_velocity_stop(robot_name)
    
    def condition_met(self,data):
        if data<0.37:
            return 1
        elif data<0.1:
            return 1
        else:
            return 3
    
    
    def send_velocity_1(self,robot_name):
        cmd=Twist()
        cmd.linear.x=self.linear_true
        cmd.angular.z=self.angular_true
        self.publishers[robot_name].publish(cmd)  
        
    def send_velocity_2(self,robot_name):
        cmd=Twist()
        cmd.linear.x=self.linear_false
        cmd.angular.z=self.angular_false
        self.publishers[robot_name].publish(cmd)
        
    def send_velocity_stop(self,robot_name):
        cmd=Twist()
        cmd.linear.x=0.0
        cmd.angular.z=0.0
        self.publishers[robot_name].publish(cmd)
        
if __name__=='__main__':
    try:
        MultiRobotController()
    except rospy.ROSInterruptException:
        pass
        


