#!/usr/bin/env python3 

#opens bag files, puts GPS UTM clock to all the topics in a bag file, puts all the topics in a bag file

import json
import rosbag
import rospy
import sys

config_file = "/home/akin/local/src/utilities/config.json"


with open(config_file, "r") as read_file:
    config = json.load(read_file)

    if "output_bag" in config:
        out_bag = rosbag.Bag(config['output_bag'], 'w')
    else:
        out_bag = rosbag.Bag("out.bag", 'w')

    if "files" in config:
        for file in config['files']:
            bag = rosbag.Bag(file['name'])

            print("Processing " + file['name'])

            # Calculate the time difference to UTC
            time_diff = rospy.Duration()
            if file['sync_to_utc'] == True:
                for topic, msg, t in bag.read_messages():
                    if topic == file['utc_topic']:   
                        time_diff = msg.time_ref - msg.header.stamp
                        break

                print("UTC time difference: " + str(time_diff.to_sec()))

            # Get the prefix

            prefix = file['prefix']

            print("Adding prefix: " + prefix)

            #go over each message, add prefix, fix time, and write output

            for topic, msg, t in bag.read_messages():

                msg.header.stamp = msg.header.stamp + time_diff
                msg.header.frame_id = prefix + '/' + msg.header.frame_id
                topic = "/" + prefix + topic

                out_bag.write(topic, msg, msg.header.stamp)
               
