import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
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
TEXT_UPDATE_INTERVAL = 2.0  # Update text every 2 seconds

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
font_path = "/path/to/your/font.ttf"  # Change this to the path of your font file
font = ImageFont.truetype(font_path, 16)
icon_font = ImageFont.truetype('lineawesome-webfont.ttf', 18)

# Define different screen contents
screens = [
    [
        ("Temperature: ", ""),
        ("Memory Usage: ", ""),
        ("Disk Usage: ", "")
    ],
    [
        ("CPU Load: ", ""),
        ("IP Address: ", ""),
        ("WiFi Icon: ", chr(61931))
    ]
]

current_screen = 0
screen_change_time = time.time() + 15  # Change screen every 15 seconds
text_update_time = 0

while True:
    # Clear the image
    draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)

    # Get the current screen content
    screen_content = screens[current_screen]

    y_position = 5
    for label, value in screen_content:
        # Icons
        if "Icon:" in label:
            draw.text((0, y_position), value, font=icon_font, fill=255)
        else:
            # Update text at the specified interval
            if time.time() - text_update_time > TEXT_UPDATE_INTERVAL:
                if "Temperature" in label:
                    value = subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True)
                elif "Memory" in label:
                    value = subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'", shell=True)
                elif "Disk" in label:
                    value = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'", shell=True)
                elif "CPU" in label:
                    value = subprocess.check_output("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True)
                elif "IP" in label:
                    value = subprocess.check_output("hostname -I | cut -d\' \' -f1 | head --bytes -1", shell=True)
                    
                text_update_time = time.time()
                
            # Text
            draw.text((0, y_position), label, font=font, fill=255)
            draw.text((80, y_position), str(value, 'utf-8'), font=font, fill=255)
        
        y_position += 20

    # Display the updated image
    device.display(image)
    time.sleep(LOOPTIME)

    # Check if it's time to change the screen
    if time.time() > screen_change_time:
        current_screen = (current_screen + 1) % len(screens)  # Cycle through screens
        screen_change_time = time.time() + 15
