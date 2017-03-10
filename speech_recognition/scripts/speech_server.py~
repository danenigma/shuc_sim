#!/usr/bin/env python
#-*- coding:utf-8 -*-
	
from flask import Flask,render_template,request
import rospy
from std_msgs.msg import String
import socket
import fcntl
import struct

app = Flask(__name__)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

@app.route('/speech/',methods=['POST'])
def speech():
	rospy.loginfo(request.form)
	speech_pub.publish(request.form['text'])
	return render_template('index.html')

rospy.init_node("speech_server")
speech_pub    = rospy.Publisher(rospy.get_param('~publish_to', '/chat_input'),String,queue_size = 1)  
current_ip    = get_ip_address(rospy.get_param('~interface', 'wlan0'))
current_port  = rospy.get_param('~s_port','9000')
rospy.loginfo("WEB SERVER RUNNING ON THIS ADDRESS : "+current_ip)

	
if __name__ == "__main__":
	try:
		app.run(debug = True,host=current_ip,port=int(current_port))
	except:
		rospy.loginfo("connection error!")


