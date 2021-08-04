from m5stack import *
from m5stack_ui import *
from uiflow import *
import urequests
import time
import json

import wifiCfg
import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
dual_button_0 = unit.get(unit.DUAL_BUTTON, unit.PORTA)
servo_0 = unit.get(unit.SERVO, (25,25))
servo_1 = unit.get(unit.SERVO, (26,26))


foodQuantity = None
status = None
DataMap = None
lastFoodTime = None
json_data = None
buttonPressed = None

wifiCfg.autoConnect(lcdShow=True)
label0 = M5Label('Red Button', x=43, y=143, color=0xff0000, font=FONT_MONT_14, parent=None)
label1 = M5Label('Blue Button', x=193, y=143, color=0x2a43ff, font=FONT_MONT_14, parent=None)
image0 = M5Img("res/cat-food.png", x=51, y=57, parent=None)
image1 = M5Img("res/cat-food-fish.png", x=203, y=63, parent=None)
image2 = M5Img("res/pawprint.png", x=67, y=165, parent=None)
image3 = M5Img("res/pawprint.png", x=219, y=165, parent=None)
label2 = M5Label('Last fed:', x=43, y=26, color=0x000, font=FONT_MONT_14, parent=None)
label3 = M5Label('Text', x=108, y=26, color=0x000, font=FONT_MONT_14, parent=None)
label4 = M5Label('seconds ago', x=144, y=26, color=0x000, font=FONT_MONT_14, parent=None)
ps = M5Label('Waiting', x=21, y=217, color=0x000, font=FONT_MONT_14, parent=None)
HttpStatus = M5Label('Status', x=249, y=217, color=0x000, font=FONT_MONT_14, parent=None)

import math


# Describe this function...
def PetFeeder():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  foodQuantity = 150
  DataMap = {'FoodQuantity':foodQuantity,'ButtonPressed':buttonPressed}
  json_data = json.dumps(DataMap)

# Describe this function...
def SendPOST():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  status = 'No StatusCode'
  try:
    req = urequests.request(method='POST', url='Replace_With_Your_Webscript_Address',data=json_data, headers={'Content-Type':'application/json'})
    ps.set_text_color(0x006600)
    wait(2)
    status = req.status_code
    ps.set_text('Data sent')
  except:
    ps.set_text_color(0xcc0000)
    wait(2)
    ps.set_text('Not sent')
  wait(2)
  HttpStatus.set_text(str(status))


def btnRed0_wasPressed():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  image2.set_hidden(False)
  image3.set_hidden(True)
  label3.set_text(str(round(((time.ticks_ms()) - lastFoodTime) / 1000)))
  lastFoodTime = time.ticks_ms()
  buttonPressed = 'red'
  servo_0.write_angle(-90)
  wait_ms(10)
  servo_0.write_us(0) 
  PetFeeder()
  wait_ms(100)
  SendPOST()
  pass
dual_button_0.btnRed.wasPressed(btnRed0_wasPressed)
def btnRed0_wasReleased():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  red.set_text('Released')
  pass
dual_button_0.btnRed.wasReleased(btnRed0_wasReleased)
def btnBlue0_wasPressed():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  image2.set_hidden(True)
  image3.set_hidden(False)
  label3.set_text(str(round(((time.ticks_ms()) - lastFoodTime) / 1000)))
  lastFoodTime = time.ticks_ms()
  buttonPressed = 'blue'
  servo_0.write_angle(-90)
  wait_ms(10)
  servo_1.write_us(0)
  PetFeeder()
  wait_ms(100)
  SendPOST()
  pass
dual_button_0.btnBlue.wasPressed(btnBlue0_wasPressed)
def btnBlue0_wasReleased():
  global foodQuantity, status, DataMap, lastFoodTime, json_data, buttonPressed
  blue.set_text('Released')
  pass
dual_button_0.btnBlue.wasReleased(btnBlue0_wasReleased)

image2.set_hidden(True)
image3.set_hidden(True)
lastFoodTime = time.ticks_ms()
label3.set_text(str(0))
import custom.urequests as urequests
