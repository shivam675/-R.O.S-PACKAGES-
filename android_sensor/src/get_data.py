#!/usr/bin/env python

import rospy
from android_sensor.msg import sensorData
import json
import requests

def talker():
	
    #create a new publisher. we specify the topic name, then type of message then the queue size
	pub = rospy.Publisher('android_sensor_data', sensorData, queue_size=20)
	#we need to initialize the node
	# In ROS, nodes are uniquely named. If two nodes with the same
	# node are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'talker' node 
	rospy.init_node('data_grabber', anonymous=False)
	#set the loop rate
	rate = rospy.Rate(1) # 1hz
	#keep publishing until a Ctrl-C is pressed
	i = 0
	while not rospy.is_shutdown():
		data = sensorData()
		url = "http://192.168.0.101:8080/sensors.json"
		json_data=requests.get(url).json()
		json_status = json_data['battery_level'] 
		bat_per = json_status['data'][0][1][0]  #battery percentage value in bat_per
		json_accel = json_data['accel']
		Ax = json_accel['data'][0][1][0]
		Ay = json_accel['data'][0][1][1]
		Az = json_accel['data'][0][1][2]
		json_btemp= json_data['battery_temp']
		bat_temp = json_btemp['data'][0][1][0]
		json_voltage= json_data['battery_voltage']
		voltage = json_voltage['data'][0][1][0]
		
		data.battery_percentage = bat_per 
		data.Ax = Ax
		data.Ay = Ay
		data.Az = Az
		data.battery_temp = bat_temp
		data.voltage = voltage
		
		rospy.loginfo(data)
		pub.publish(data)
		rate.sleep()
       

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


#data = "incomming data \nBattery Percentage : {} \nAccel \n    {}\n    {}\n    {}\nBattery Temp : {}\nVoltage : {}".format(bat_per,Ax,Ay,Az,bat_temp,voltage)
