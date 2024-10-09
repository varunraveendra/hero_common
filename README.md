# HeRo+ : An extended version of the [HeRo](https://github.com/verlab/hero_common) Robot.
<p align="justify">
Welcome to the HeRo+ project! This is an extension of the HeRo Robot, by VerLab.

The latest improvements after forking the repository include the following enhancements:
- **New Bump Shield**: The robots now have a circular bump shield, so the robot's encoders and wheels are safe even when they collide.
- **Encoder Placement**: The encoders have been repositioned outside the wheel to eliminate slippage between the previously used gear shaft encoder, enhancing accuracy. 
- **Encoder Reading**: There is no use of a Kalman filter for processing encoder data. The PID loop now utilizes the raw readings directly from the encoders, ensuring more immediate control adjustments. 
- **New TOF Sensor**: The HeRo+ robot now features a new Time-of-Flight (TOF) sensor placed on the hat. The IMU sensor has been removed but can be reintroduced by replacing the TOF sensor. 
- **Battery Upgrade**: The [battery](https://www.amazon.com/dp/B0CXSMLK8T?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) has been upgraded to prevent over-discharge cutoff, improving the overall durability and safety of the robot. 
- **STL Files Update**: Updated STL files for the new robot design are now available, reflecting the latest hardware improvements. 
</p>

For more in-depth information about HeRo, please visit the original documentation page [here](https://verlab.github.io/hero_common/).

<p align="center">
  <img alt="robot" width="400px" src="https://github.com/varunraveendra/hero_common/raw/master/Images/Screenshot%202024-09-19%20at%2012.12.53%E2%80%AFAM.png"/>
</p>

## HeRo+ Author
<a href="https://github.com/varunraveendra">
  <img src="https://github.com/varunraveendra.png" width="50" alt="Varun Raveendra"/>
</a>


## HeRo Authors
[![Paulo Rezeck](https://github.com/rezeck.png?size=50)](https://rezeck.github.io/)
[![Hector Azpurua](https://github.com/h3ct0r.png?size=50)](https://github.com/h3ct0r)
[![Maurício Ferrari](https://github.com/mauferrari.png?size=50)](https://github.com/mauferrari)


## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-ShareALike 4.0 International License</a>.
