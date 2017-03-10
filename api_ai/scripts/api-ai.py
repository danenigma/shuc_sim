#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import sys
import argparse
import rospy
import json
from std_msgs.msg import String
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '295946fac8694c639fa7c95b2d3a8d6b'

class Ai():
    def __init__(self):

        rospy.init_node("APIAI")
        self.speech_pub = rospy.Publisher("/chatbot_responses",String,queue_size = 1)
        self.action_pub = rospy.Publisher("/action_response",String,queue_size = 1)
        self.chat_pub 	= rospy.Publisher("/chat_input",String,queue_size = 1)
        self.ai         = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        self.rate       = rospy.Rate(1)
        rospy.Subscriber("/speech",String,self.speech_callback)
    def speech_callback(self,command):
        rospy.loginfo("user intent : "+command.data)
        request = self.ai.text_request()      
        request.lang = 'en'  # optional, default value equal 'en'
        
        request.session_id = '65e79928'
        request.query = command.data
        try:
            response  = request.getresponse()
            try:
                value     = response.read()
                data      = json.loads(value)
                speech    = data['result']['fulfillment']['speech']
                action    = data['result']['action']
		if action!= "smalltalk.greetings":
			self.speech_pub.publish(str(speech))#publish on tts
			self.action_pub.publish(action+'.'+str(data['result']['parameters']))
		else:
                	self.chat_pub.publish(command.data)#publish to chatbot			
          
                rospy.loginfo("action: "+action)
                rospy.loginfo("parameters: "+str(data['result']['parameters']))
                
            except: 
                rospy.loginfo("parsing error!!!")           
        except:
            rospy.loginfo("connection error!")
if __name__ == '__main__': 
    ai = Ai()
    try:
        rospy.spin()
    except:
        rospy.loginfo("error!!!!!")


