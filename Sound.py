import Blocky.uasyncio as asyncio
from Blocky.Button import *

from machine import *
from time import *

dir = Pin(25 , Pin.OUT)
clk = Pin(26 , Pin.OUT)
button = Button('D3')

tar_pos = 0
cur_pos = 0

tar_angle = 0
cur_angle = 0 #float



def step_to_angle(step):
	return step/(3969*2/289/1.8)
	
def angle_to_step(angle):
	return int(angle*(3969*2/289/1.8))
STEP_ANGLE_RATIO = angle_to_step(1)	
def handler(source):
	global cur_pos , tar_pos , tar_angle , cur_angle
	if abs(cur_pos - tar_pos ) < STEP_ANGLE_RATIO:
		for x in range(abs(cur_pos-tar_pos)):
			dir.value(1 if tar_pos > cur_pos else 0)
			clk.value(not clk.value())
			cur_pos = cur_pos + 1 if tar_pos > cur_pos else cur_pos - 1
			sleep_ms(1)
		return 
	if tar_pos > cur_pos :
		dir.value(1)
		for x in range(STEP_ANGLE_RATIO):
			sleep_ms(1)
			clk.value(not clk.value())
			cur_pos += 1
	if tar_pos < cur_pos :
		dir.value(0)
		for x in range(STEP_ANGLE_RATIO):
			sleep_ms(1)
			clk.value(not clk.value())
			cur_pos -= 1 
			
def angle(ang= None):
	if ang == None :
		return step_to_angle(cur_pos)
	else :
		step = angle_to_step( ang - angle())
		global tar_pos ; tar_pos += step 
		
#Timer(-1).init(mode = Timer.PERIODIC , period = 10 , callback  = handler)

async def execute():
  angle(angle() + 45)
async def handler_async():
	while True :
		await asyncio.sleep_ms(1)
		handler(1)
		
button.event('pressed' , 1 , execute)

loop = asyncio.get_event_loop()
loop.call_soon(handler_async())
loop.run_forever()