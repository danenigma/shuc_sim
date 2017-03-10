#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'daniel'

import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge, CvBridgeError

class TakePic():
	NODE_NAME = "take_pic"
	def __init__(self):
	
		rospy.init_node(self.NODE_NAME)
		self.sub = rospy.Subscriber('/take_pic',String,self.cmd_callback)
		self.bridge = CvBridge()
		#for simulation 
		self.data_path = rospy.get_param('~data_path','data')
		self.sub_frame = rospy.Subscriber('/rgbd_camera/rgb/image_raw',Image,self.frame_callback)
		try:
			self.final_pic_no = open(self.data_path+'/latest.txt', 'rw')#latest image taken
			self.count = int(self.final_pic_no.readline())
		except:
			rospy.loginfo("file read error")
		self.frame = None
	def frame_callback(self,frame):

		try:
			self.frame = self.bridge.imgmsg_to_cv2(frame, "bgr8")
		except CvBridgeError as e:
			rospy.loginfo(e)

		#print self.frame
	def cmd_callback(self,data):
		
		if data.data == "take pic":
			if self.frame is not None:
				cv2.imwrite(self.data_path+'/' + str(self.count) +'.png',self.frame)
				self.count+=1
				open(self.data_path+'/latest.txt', 'w').write(str(self.count))
				cv2.imshow("image",self.frame)
				cv2.waitKey(0)	
if __name__ == "__main__":
	t = TakePic()
	try:
		rospy.spin()
	except:
		print "Error!"
