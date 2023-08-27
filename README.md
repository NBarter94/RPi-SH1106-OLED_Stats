# OLED Stats

SH1106 OLED Stats Display Script for Raspberry Pi

Based off of mklements OLED_Stats, this is a display script for SH1106 boards unlike the mklements original which is for SSD1306 displays.

This script is pre-configured for the SH1106 128x64 I2C OLED Display ONLY, but can easily be modified to run on a 128x32 I2C OLED Display.

## Display Issues using mklements OLED_Stats:

When you're following mklements OLED_Stats steps, unfortunately if your display shows jumbled pixels/symbols instead of actual text - you more than likely have a display which supports the SH1106 driver instead of the more common SSD1306 driver. It's an easy mistake to make as many SH1106 boards are advertised/labelled as the common SSD1306.

mklements script ONLY works for SSD1306 displays BUT this script will help you with issues using his script with SH1106 displays. 

A similar process can be followed to get the SH1106 displays setup BUT you'll need to alter mklements original script to get it working or just use my scripts instead. Video: https://www.youtube.com/watch?v=LdOKXUDw2NY


## Screenshots:

<table align="center" style="margin: 0px auto;">
  <tr>
    <th>Stats-SH1106.py</th>
    <th>Monitor-SH1106.py</th>
  </tr>
  <tr>
    <td><img align="right" src="https://i.ytimg.com/vi/lRTQ0NsXMuw/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLA2eFunUPnMf_Cveih2-b_JEXZxig" height="220"></img></td>
    <td><img align="right" src="https://i.ytimg.com/vi/94ZjxjmhBrY/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBTY9ptxf2VqzErucUVVxqmK3Pw6g" height="220"></img></td>
  </tr>
  </table>

## Installation Steps:

1. Connect **GND, VCC(3.3v), SCL, & SDA** ports of the display according to mklements picture shown below:

<img src="https://www.the-diy-life.com/wp-content/uploads/2021/11/Screenshot-2021-11-14-at-22.16.39-1024x576.jpg">

```shell
    $ VDD/VCC (Power) = PIN1 or any other 3V3 power
    $ GND (Ground) = PIN9 or any other ground
    $ SCK/SCL (Serial Clock) = PIN5
    $ SDA (Serial Data) = PIN3
```

2. Upgrade your Raspberry Pi firmware and reboot:

```shell
    $ sudo apt-get update
    $ sudo apt-get full-upgrade
    $ sudo reboot
```

3. Install python3-pip & upgrade the setuptools

```shell
    $ sudo apt-get install python3-pip
    $ sudo pip3 install --upgrade setuptools
```

4. Next, we’re going to retrieve all of the dependencies luma.oled requires and install them automatically using the following command:

```shell
    $ sudo -H pip3 install --upgrade luma.oled
```

NOTE: If pip is unable to automatically install its dependencies you will have to add them manually. To resolve the issues you will need to add the appropriate development packages to continue.

If you are using Raspberry Pi OS you should be able to use the following commands to add the required packages:

```shell
    $ sudo apt-get update
    $ sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
    $ sudo -H pip3 install luma.oled
```

5. Allowing the Raspberry Pi to use I2C interface via raspi-config

   Open raspi-config via cli/command,

   ```shell
        $ sudo raspi-config
   ```
   Go to Section 3. "Interface Options" & hit enter.
   Go down to I2C & hit enter, you'll then be asked if you want to enable I2C interface, Choose Yes.
   Once enabled you can then finish Raspi-Config

5. Check the `I2C` status using the command:

```shell
    $ sudo i2cdetect -y 1

        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:                         -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --
```

6. Next, we need to install psutil & python3-pil. Start by entering the following commands:

```shell
    $ sudo pip3 install psutil
    $ sudo reboot
    $ sudo apt-get install python3-pil
```

7. Now we need to download the python script from our github:

```shell
    $ git clone https://github.com/NBarter94/RPi-SH1106-OLED_Stats.git

    $ cd RPi-SH1106-OLED_Stats
    $ cp PixelOperator.ttf ~/PixelOperator.ttf
    $ cp lineawesome-webfont.ttf ~/lineawesome-webfont.ttf
    $ cp Stats-SH1106.py ~/stats.py   
    $ cp Monitor-SH1106.py ~/monitor.py

```

8. For activating the `crontab` follow the procedure:

```shell
    $ crontab -e
```

**Add this at the bottom:**

Remember to change your username (pi below) if you're not using the default username

```
    @reboot python3 /home/pi/stats.py &

    OR
    
    @reboot python3 /home/pi/psutilstats.py &
    
    OR

    @reboot python3 /home/pi/monitor.py &
```

9. At the end DELETE the OLED_Stats folder and reboot

```shell
    $ sudo rm -rf RPi-SH1106-OLED_Stats
    $ sudo reboot
```

## Display Issues:
<img src="https://www.the-diy-life.com/wp-content/uploads/2021/11/Screenshot-2021-11-14-at-22.16.39-1024x576.jpg">
If your display shows jumbled pixels/symbols as shown above instead of actual text - you may have a display which supports the SSD1306 driver instead of less common SH1106 driver. This script ONLY works for SH1106 displays.
If you have this issue, follow mkelements guide which this script is based off https://github.com/mklements/OLED_Stats

<h3><p align="center">THE  END</p></h3>
