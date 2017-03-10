#!/usr/bin/env python
#-*- coding:utf-8 -*-
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64,Header
from geometry_msgs.msg import PointStamped, Point, Pose, PoseStamped
from math import radians
import tf
import os, thread
import time
class FaceTracker():
	NODE_NAME = "FaceTracker"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.tf = tf.TransformListener()
		self.state_pub = rospy.Publisher('joint_states',JointState,queue_size=1)
		self.js_sub = rospy.Subscriber('joint_states', JointState, self.update_joint_state)
		self.ts_sub = rospy.Subscriber('/target_pose', PoseStamped, self.face_location_callback)
		self.pan_joint = 'pan_joint'
		self.tilt_joint = 'tilt_joint'
		self.joint_state = JointState()
		self.state  = JointState()
		self.state.header = Header()
		self.state.name = ["pan_joint", "tilt_joint"]
		self.state.velocity = []
		self.state.effort = []	
		self.face_link = 'face_link'
		self.max_pan  = 90
		self.min_pan  = -90
		self.max_tilt = 90
		self.min_tilt = -90
		self.lock = thread.allocate_lock()

	def update_joint_state(self,joint_pos):
		
		try:
			
            		self.joint_state = joint_pos
			
       		except:
            		pass
        
	def face_location_callback(self,target_pos):	
		self.lock.acquire()
		try:
			if target_pos == PointStamped():
			        return
		    	target = PointStamped()
		    	target.header.frame_id = target_pos.header.frame_id
		    	target.point = target_pos.pose.position
			face_target  = self.tf.transformPoint(self.face_link, target)
		        pan = face_target.point.y
		        tilt = -face_target.point.z
		        # Compute the distance to the target in the x direction
		        distance = float(abs(face_target.point.x))
		        try:
		 	       pan /= distance
		 	       tilt /= distance
			except:
		 	       pan /= 0.5
		 	       tilt /= 0.5
		        
		        if abs(pan) > 0.0:
	    
	    	            current_pan = self.joint_state.position[self.joint_state.name.index(self.pan_joint)]
	    	            
	    	            delta_pan = min(0.5, 0.25 * 2.5 * abs(pan))
	    	            rospy.loginfo("delta pan : "+str(delta_pan))
	    		                
	    	            if pan > 0:
	    	                self.pan_position = max(self.min_pan, current_pan - delta_pan)
	    	            else:
	    	                self.pan_position = min(self.max_pan, current_pan + delta_pan)
		            
	    	        else:
	    	            self.pan_position = max(self.min_pan, min(self.max_pan, pan)) 
 		        if abs(tilt) > 0.0:
	    
	    	            current_tilt = self.joint_state.position[self.joint_state.name.index(self.tilt_joint)]
	    	            
	    	            delta_tilt = min(0.5, 0.25 * 2.5 * abs(tilt))
	    	            rospy.loginfo("delta tilt : "+str(delta_tilt))
	    		                
	    	            if tilt > 0:
	    	                self.tilt_position = max(self.min_tilt, current_tilt - delta_tilt)
	    	            else:
	    	                self.tilt_position = min(self.max_tilt, current_tilt + delta_tilt)
		            
	    	        else:
	    	            self.tilt_position = max(self.min_tilt, min(self.max_tilt, tilt)) 
			self.state.position=[self.pan_position,self.tilt_position]
			self.state.header.stamp = rospy.Time.now()
			self.state_pub.publish(self.state)         
			
				        
	        finally:
         	   self.lock.release()
if __name__=="__main__":
	ft =FaceTracker()
	nodes  = os.popen("rosnode list").readlines()

	try:
		time.sleep(3)
		os.system("rosnode kill " + '/joint_state_publisher\n' )	#kill joint state publisher
		time.sleep(1) 
		rospy.spin()
	except:
		rospy.loginfo("error!!")
