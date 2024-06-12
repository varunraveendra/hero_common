#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from hero_common.msg import location
from cv_bridge import CvBridge
import cv2
import numpy as np
import tkinter as tk
from PIL import Image as PImage
from PIL import ImageTk

class ImageGUI:
    def __init__(self):
        rospy.init_node('image_gui', anonymous=True)
        self.bridge = CvBridge()
        self.image = None
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        rospy.Subscriber('/camera/camera_feed', Image, self.image_callback)
        
        self.pub = rospy.Publisher('hero_1/cam_dest',location, queue_size=5)
        self.msg = location()

    def image_callback(self, msg):
        self.image = self.bridge.imgmsg_to_cv2(msg)
        self.update_image()

    def update_image(self):
        if self.image is not None:
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image_pil = PImage.fromarray(image_rgb)
            self.photo = ImageTk.PhotoImage(image=image_pil)
            self.canvas.config(width=self.image.shape[1], height=self.image.shape[0])
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
    
        
    def on_click(self, event):
        if self.image is not None:
            x, y = event.x, event.y
            self.msg.x=x
            self.msg.y=y
            self.pub.publish(self.msg)
            
            if hasattr(self, 'box_id'):
                self.canvas.delete(self.box_id)
        
        # Draw a new box centered at the clicked position
            box_size = 50  # Size of the box
            x1, y1 = max(0, x - box_size), max(0, y - box_size)  # Top-left corner of the box
            x2, y2 = min(self.image.shape[1] - 1, x + box_size), min(self.image.shape[0] - 1, y + box_size)  # Bottom-right corner of the box
            self.box_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")

            pixel_value = self.image[y, x]  # OpenCV uses (y, x) indexing
            print("Pixel value at (x={}, y={}): {}".format(x, y, pixel_value))

    def run(self):
        self.root.mainloop()





if __name__ == "__main__":
    app = ImageGUI()
    app.run()

