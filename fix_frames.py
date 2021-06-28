#!/usr/bin/env python3 


## Removes leading / from the frame_id of all the topics. TF2 doesn't support frames starting with /


import rosbag
import sys

newfile = sys.argv[1].replace(".bag","")+"_fixed.bag"

with rosbag.Bag(newfile, 'w') as outbag:
	for topic, msg, t in rosbag.Bag(sys.argv[1]).read_messages():
		if msg._has_header:
			if len(msg.header.frame_id) > 0:
				if msg.header.frame_id[0] == '/':
					msg.header.frame_id = msg.header.frame_id[1:]
		
		outbag.write(topic, msg, t)


	outbag.close()
