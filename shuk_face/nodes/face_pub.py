#!/usr/bin/env python


import rospy
import sys
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PointStamped, Point, PoseStamped, Pose
from dynamic_reconfigure.server import Server
import dynamic_reconfigure.client
import math
import cv2

class Pub3DTarget():
    def __init__(self):
        rospy.init_node('shuk_face')
        
        self.rate = rospy.get_param('~rate', 20)
        target_frame = rospy.get_param('~target_frame', 'base_link')
        self.path    = rospy.get_param('~face_cascade_path','')
        self.capture_device = rospy.get_param('~capture_device','0')
    
        self.face_cascade = cv2.CascadeClassifier(self.path)
        self.cap = cv2.VideoCapture(int(self.capture_device))  
        self.r = rospy.Rate(self.rate)
        target_pub = rospy.Publisher('target_pose', PoseStamped, queue_size=5)
        
        marker_pub = rospy.Publisher('target_marker', Marker, queue_size=5)
        
        marker_scale = rospy.get_param('~marker_scale', 0.1)
        marker_lifetime = rospy.get_param('~marker_lifetime', 1/self.rate) # 0 = forever
        marker_ns = rospy.get_param('~marker_ns', 'target_point')
        marker_id = rospy.get_param('~marker_id', 0)
        marker_color = rospy.get_param('~marker_color', {'r': 0.5, 'g': 1.0, 'b': 0.0, 'a': 0.8})
        
        marker = Marker()
        marker.ns = marker_ns
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.lifetime = rospy.Duration(marker_lifetime)
        marker.scale.x = marker_scale
        marker.scale.y = marker_scale
        marker.scale.z = marker_scale
        marker.color.r = marker_color['r']
        marker.color.g = marker_color['g']
        marker.color.b = marker_color['b']
        marker.color.a = marker_color['a']
        
        target = PoseStamped()
        target.header.frame_id = target_frame
        
        target.header.frame_id = target_frame
        target.pose.orientation.x = 0
        target.pose.orientation.y = 0
        target.pose.orientation.z = 0
        target.pose.orientation.w = 1
        
        rospy.loginfo("Publishing target point on frame " + str(target_frame))
        

    def run(self):    
        while not rospy.is_shutdown():
            _,img   = self.cap.read()
            if img is None:continue
            self.detect_face(img);
            cv2.imshow("faces",img)
            if cv2.waitKey(10) == ord('q'):
                break
                    

    def detect_face(self,img):  
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
         hight,width, channels = img.shape

         for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.circle(img,(x+w/2,y+h/2),20,(255,0,0),2)
                target.pose.position.x = 0.0
                target.pose.position.y = float(y)/hight
                target.pose.position.z = float(x)/width
                                
                now = rospy.Time.now()
                        
                target.header.stamp = now
                
                marker.header.stamp = now
                marker.header.frame_id = target.header.frame_id
                marker.pose.position = target.pose.position
                marker.id = 0
                # Publish the target
                target_pub.publish(target)
                # Publish the marker for viewing in RViz
                marker_pub.publish(marker)                 
                   
if __name__ == '__main__':
    try:
        target = Pub3DTarget()
        target.run()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Target publisher is shut down.")
