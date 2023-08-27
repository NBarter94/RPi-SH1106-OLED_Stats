import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import subprocess
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import sh1106

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

# Define your font
font_path = "PixelOperator.ttf"  # Change this to the path of your font file
font = ImageFont.truetype(font_path, 16)

# Set up OLED display using luma
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=WIDTH, height=HEIGHT, rotate=0)

# Create a blank image for drawing
image = Image.new("1", (device.width, device.height))

while True:
    # Clear the image
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)

    # Your data collection and display logic
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True)

    # Draw text on the image
    draw.text((0, 0), "IP: " + str(IP, 'utf-8'), font=font, fill="white")
    draw.text((0, 16), str(CPU, 'utf-8') + "LA", font=font, fill="white")
    draw.text((80, 16), str(Temp, 'utf-8'), font=font, fill="white")
    draw.text((0, 32), str(MemUsage, 'utf-8'), font=font, fill="white")
    draw.text((0, 48), str(Disk, 'utf-8'), font=font, fill="white")

    # Display the updated image
    device.display(image)
    time.sleep(LOOPTIME)
