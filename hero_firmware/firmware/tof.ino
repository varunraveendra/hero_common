#include "tof.h"

TOFSensor::TOFSensor(unsigned long rate) {
  this->timer = millis();
  this->setRate(rate);
}

void TOFSensor::init(ros::NodeHandle &nh, String heroName) {
  this->nh_ = &nh;   /* ROS Node Handle */
  this->heroName = (heroName.charAt(0) == '/') ? heroName.substring(1) : heroName;

  /* Address TOF publisher */
  this->tofTopic = String("/") + this->heroName + String("/distance");          /* Update topic name */
  this->tofPub = new ros::Publisher(this->tofTopic.c_str(), &this->tofMessage); /* Instantiate publisher */
  this->tofFrame = this->heroName + String("/tof_frame");                       /* Update frame name */
  this->nh_->advertise(*this->tofPub);                                          /* Advertise the topic */

  /* Setup TOF I2C communication */
  Wire.pins(I2C_SDA, I2C_SCL); // Set custom I2C pins if required
  Wire.begin();               // Initialize I2C bus
  Wire.setClock(400000);      // Set I2C clock to 400kHz
  this->tof = new VL53L1X();  // Instantiate VL53L1X object
 
  if (!this->tof->init()) {   // Initialize the sensor
    sprintf(this->stream, "\33[91m[%s] TOF sensor initialization failed!\33[0m", this->heroName.c_str());
    this->nh_->loginfo(this->stream);
    this->TOFSensorEnable = false;
    return;
  }
  this->tof->setDistanceMode(VL53L1X::Medium);
  this->tof->setMeasurementTimingBudget(30000);
  this->tof->setROICenter(199);
  this->tof->setROISize(4,4);
  this->tof->setTimeout(500); // Set timeout to 500ms
  this->tof->startContinuous(50); // Start continuous measurement mode

  sprintf(this->stream, "\33[92m[%s] TOF sensor initialized!\33[0m", this->heroName.c_str());
  this->nh_->loginfo(this->stream);
}

bool TOFSensor::isEnable(void) {
  return this->TOFSensorEnable;
}

void TOFSensor::enable(void) {
  this->TOFSensorEnable = true;
}

void TOFSensor::disable(void) {
  this->TOFSensorEnable = false;
}

void TOFSensor::setRate(unsigned long rate) {
  this->rate = rate;
}

void TOFSensor::update(unsigned long rate) {
  if (((millis() - this->timer) > (1000 / rate)) && TOFSensorEnable) {
    this->readSensor();
    /* Send TOF message to be published into ROS */
    this->tofMessage.data = this->get(); // Set the data to the message
    this->tofPub->publish(&this->tofMessage);
    this->timer = millis();
  }
}

void TOFSensor::update() {
  this->update(this->rate);
}

/* Read TOF data and publish it */
void TOFSensor::readSensor(void) {
  if (this->tof->timeoutOccurred()) {
    sprintf(this->stream, "\33[91m[%s] TOF sensor timeout!\33[0m", this->heroName.c_str());
    this->nh_->loginfo(this->stream);
  } else {
    float distance = this->tof->readRangeContinuousMillimeters();
    if (distance == 0) {
      sprintf(this->stream, "\33[91m[%s] TOF sensor failed to read distance!\33[0m", this->heroName.c_str());
      this->nh_->loginfo(this->stream);
    } else {
      this->tofMessage.data = distance / 1000.0; // Convert mm to meters
    }
  }
}

float TOFSensor::get(void) {
  return this->tofMessage.data;
}
