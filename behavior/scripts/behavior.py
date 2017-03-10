#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import ast
from std_msgs.msg import String

class Behavior():
    def __init__(self):

        rospy.init_node("BEHAVIOR")
        rospy.Subscriber("/action_response",String,self.action_callback)
        self.take_pic_pub  = rospy.Publisher("/take_pic",String,queue_size=1)
        self.goto_pub      = rospy.Publisher("/go_to",String,queue_size=1)
        self.get_loc_coord = rospy.Publisher("/get_it",String,queue_size=1)

    def action_callback(self,data):
        #OUR USECASE
        data         = data.data.split('.')
        action,param = data[0],data[1] 
	try:
        	param        = ast.literal_eval(param)
	except:
		rospy.loginfo("!error")
        if action == "call.call":
                rospy.loginfo('calling')
        if action == "move":
                rospy.loginfo('moving-command')
        if action == "map-house":
                rospy.loginfo('slam that ')
        if action == "go_to":
            if param['household-locations'] != []: 
                rospy.loginfo("navigate to the : "+str(param['household-locations']))
                self.goto_pub.publish(str(param['household-locations']))
        if action == "remember-location":
            if param['household-locations']!=[]:
                rospy.loginfo("remember: "+str(param['household-locations']))
                self.get_loc_coord.publish(str(param['household-locations']))                
        if action == "take-a-pic":
                self.take_pic_pub.publish("take pic")
                rospy.loginfo("take a picture")
        if action == "look for intruder ":
                rospy.loginfo("look for intruder")
        if action == "set a reminder ":
                rospy.loginfo("set a reminder ")
if __name__ == '__main__': 
    b = Behavior()
    try:
        rospy.spin()
    except:
        rospy.loginfo("error")


