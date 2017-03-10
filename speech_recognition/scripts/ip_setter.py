#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import socket
import fcntl
import struct
class IpSetter():
	def __init_(self):
		rospy.init_node('speech_ip_setter')
	def get_ip_address(self,ifname):
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	    )[20:24])

	def set_ip(self):	
		self.ifname =rospy.get_param('~interface', 'lo')
		self.ip = self.get_ip_address(self.ifname)
		rospy.set_param('~address',self.ip)
		rospy.loginfo('running on ip' + self.ip)
if __name__ == "__main__":
	ips = IpSetter()
	ips.set_ip()
