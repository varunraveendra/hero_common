#ifndef __TOF_H__
#define __TOF_H__

#include "Wire.h"
#include "VL53L1X.h" /* Include VL53L1X library */

/* ROS Library */
#define ROSSERIAL_ARDUINO_TCP
#include <ros.h>

/* Message types */
#include <std_msgs/Float32.h> /* Message type for distance */

class TOFSensor {
  private:
    ros::NodeHandle *nh_;
    String heroName;
    /* TOF publisher */
    std_msgs::Float32 tofMessage;  /* Message Type */
    String tofTopic;               /* Topic name */
    ros::Publisher *tofPub;        /* Publisher */
    String tofFrame;               /* TOF sensor frame */
    unsigned long rate = 20, timer;

    /* VL53L1X sensor instance */
    VL53L1X *tof;

    char stream[100];
    bool TOFSensorEnable = true;

  public:
    TOFSensor(unsigned long rate);
    void init(ros::NodeHandle &nh, String heroName);
    void update();
    void update(unsigned long rate);
    void enable(void);
    void disable(void);
    bool isEnable(void);
    void setRate(unsigned long rate);
    void readSensor();
    bool configModeCheck();
    float get(void);
};

#endif
