#include <thread>
#include "ros/ros.h"
#include "can_msgs/Frame.h"
#include <ros/callback_queue.h>

int read_rate = 10;

void can1_callback(const can_msgs::Frame::ConstPtr &can_msg)
{

  ROS_INFO("CAN1 Callback");
  ROS_INFO_STREAM(can_msg->header.stamp);
}

void can0_callback(const can_msgs::Frame::ConstPtr &msg)
{
  ROS_INFO("CAN0 Callback");
  ROS_INFO_STREAM(msg->header.stamp);


}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "can_decode_node");
  ros::NodeHandle nh;
  ros::NodeHandle can1_nh;

  ros::CallbackQueue can1_queue;
  can1_nh.setCallbackQueue(&can1_queue);
  ros::Subscriber sub_can1 = can1_nh.subscribe("/received_messages_can3", 1, can1_callback);

  std::string dbc_file = "/home/akin/local/src/opendbc/toyota_prius_2017_pt_generated.dbc";

  nh.getParam("read_rate", read_rate);
  nh.getParam("dbc_file", dbc_file);

  std::thread can1_spin_thread([&can1_queue]() {
    ros::Rate r(read_rate);
    while(ros::ok()) {
      can1_queue.callAvailable(); 
      r.sleep();
    }

  });

  ros::Subscriber sub = nh.subscribe("/received_messages_can5", 1, can0_callback);
  
  ros::Rate r(read_rate); 
  while(ros::ok()) {
    ros::spinOnce();
    r.sleep();
  }
  can1_spin_thread.join();


  return 0;

}
