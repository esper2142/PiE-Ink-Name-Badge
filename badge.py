#!/usr/bin/env python

import os
import sys
import re
import time
from commands import *
from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO

user = os.getuid()
if user != 0:
    print "Please run script as root"
    sys.exit()

# Command line usage
# papirus-buttons

WHITE = 1
BLACK = 0

L_SIZE = 25
M_SIZE = 20
S_SIZE = 15

SW1 = 21
SW2 = 16
SW3 = 20
SW4 = 19
SW5 = 26

projectPath = '/home/pi/Desktop/badge/'

def draw(papirus, imagePath="", text="", size=20, partial=0):
    # initially set all white background
    if imagePath=="":
        image = Image.new('1', papirus.size, WHITE)
    else:
        image = Image.open(projectPath + imagePath)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

    # Calculate the max number of char to fit on line
    line_size = (papirus.width / (size * 0.65))

    current_line = 0
    for l in re.split(r'[\r\n]+', text):
        current_line += 1
        draw.text((0, ((size * current_line) - size)), l, font=font, fill=BLACK)

    papirus.display(image)
    if partial == 1:
        papirus.partial_update()
    else:
        papirus.update()

def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)
    GPIO.setup(SW5, GPIO.IN)

    papirus = Papirus()

    draw(papirus, text="Booting up\r\nJosh's Linux\r\nName Badge...", size=L_SIZE)

    while True:
        if GPIO.input(SW1) == False or GPIO.input(SW2) == False or GPIO.input(SW3) == False or GPIO.input(SW4) == False or GPIO.input(SW5) == False:
            while 1:
                draw(papirus, 'josh-name-job.bmp')
                sleep(5)
                draw(papirus, 'cisco.bmp')
                sleep(2)
                draw(papirus, imagePath='josh-blank.bmp')
                sleep(0.3)
                draw(papirus, imagePath='josh-1.bmp', partial=1)
                sleep(0.3)
                draw(papirus, imagePath='josh-2.bmp', partial=1)
                sleep(0.3)
                draw(papirus, imagePath='josh-3.bmp', partial=1)
                sleep(0.3)
                draw(papirus, imagePath='josh-2.bmp', partial=1)
                sleep(0.3)
                draw(papirus, imagePath='josh-1.bmp', partial=1)
                sleep(0.3)
                draw(papirus, imagePath='cisco.bmp', partial=1)
                sleep(1)

if __name__ == '__main__':
    main()


