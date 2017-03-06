#ifndef _ROS_variant_msgs_VariantHeader_h
#define _ROS_variant_msgs_VariantHeader_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace variant_msgs
{

  class VariantHeader : public ros::Msg
  {
    public:
      const char* publisher;
      const char* topic;
      bool latched;

    VariantHeader():
      publisher(""),
      topic(""),
      latched(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_publisher = strlen(this->publisher);
      memcpy(outbuffer + offset, &length_publisher, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->publisher, length_publisher);
      offset += length_publisher;
      uint32_t length_topic = strlen(this->topic);
      memcpy(outbuffer + offset, &length_topic, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->topic, length_topic);
      offset += length_topic;
      union {
        bool real;
        uint8_t base;
      } u_latched;
      u_latched.real = this->latched;
      *(outbuffer + offset + 0) = (u_latched.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->latched);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_publisher;
      memcpy(&length_publisher, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_publisher; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_publisher-1]=0;
      this->publisher = (char *)(inbuffer + offset-1);
      offset += length_publisher;
      uint32_t length_topic;
      memcpy(&length_topic, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_topic; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_topic-1]=0;
      this->topic = (char *)(inbuffer + offset-1);
      offset += length_topic;
      union {
        bool real;
        uint8_t base;
      } u_latched;
      u_latched.base = 0;
      u_latched.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->latched = u_latched.real;
      offset += sizeof(this->latched);
     return offset;
    }

    const char * getType(){ return "variant_msgs/VariantHeader"; };
    const char * getMD5(){ return "e4adbe277ed51d50644d64067b86c73d"; };

  };

}
#endif