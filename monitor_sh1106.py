import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.oled.device import sh1106

import subprocess

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Set up OLED display using luma with sh1106
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=WIDTH, height=HEIGHT, reset=oled_reset)

# Create a blank image for drawing
image = Image.new('1', (device.width, device.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Define your font
font_path = "PixelOperator.ttf"
font = ImageFont.truetype(font_path, 16)
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

while True:
    # Clear the image
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)

    # Your data collection and display logic
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell=True)

    cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)

    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell=True)

    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True)

    # Icons
    draw.text((0, 5), chr(62609), font=icon_font, fill=255)
    draw.text((65, 5), chr(62776), font=icon_font, fill=255)
    draw.text((0, 25), chr(63426), font=icon_font, fill=255)
    draw.text((65, 25), chr(62171), font=icon_font, fill=255)
    draw.text((0, 45), chr(61931), font=icon_font, fill=255)

    # Text
    draw.text((19, 5), str(Temperature, 'utf-8'), font=font, fill=255)
    draw.text((87, 5), str(MemUsage, 'utf-8'), font=font, fill=255)
    draw.text((19, 25), str(Disk, 'utf-8'), font=font, fill=255)
    draw.text((87, 25), str(CPU, 'utf-8'), font=font, fill=255)
    draw.text((19, 45), str(IP, 'utf-8'), font=font, fill=255)

    # Display the updated image
    device.display(image)
    time.sleep(LOOPTIME)
