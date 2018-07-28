
#1.First step , check for json file
try :
	from ujson import loads
	f = open('config.json','r')
	config = loads(f.read())
	f.close()
	if not config.get('auth_key',False)\
	or not config.get('known_networks',False):
		raise KeyError('Missing key information')
except Exception:
	print('Missing required info in config. Enter config mode')
	import Blocky.ConfigManager#exec(open('Blocky/ConfigManager.py').read())
	
print('Finished loading config file' , config)




from Blocky.Timer import *
from Blocky.Network import network
from Blocky.Indicator import indicator
import Blocky.uasyncio as asyncio

from machine import Pin
if  Pin(12,Pin.IN,Pin.PULL_UP).value():
	import Blocky.ConfigManager#exec(open('Blocky/ConfigManager.py').read())

FLAG_UPCODE = False
import Blocky.Global
async def service():
	while True :
		await asyncio.sleep_ms(300)
		
		if Blocky.Global.flag_UPCODE == True:
			print('Ran by Flag')
			exec(open('user_code.py').read())
			
			Blocky.Global.flag_UPCODE= False
		network.process()
		
def require_network():
	network.connect()
	loop = asyncio.get_event_loop()
	loop.call_soon(service())

try :
  network_required = open('user_code.py','r').read().find('network.') > 0
except :
  network_required = True
network_required = True
if network_required :
	require_network()
	
else :
	from Blocky.Button import *
	button  = Button(12)
	from Blocky.Network import network
	button.event('pressed' , 1 , require_network)
	




# network will do the wifi and broker
from Blocky.MQTT import *
from Blocky.Network import *

GLOBAL_CAPTURE = list(globals().keys())

try :
	exec(open('user_code.py').read())
except Exception as err:
	network.log('Your code crashed because of "' + str(err) + '"')
	
# TODO :
"""
 If inside the setup block contains a blocking operation , the chip will be bricked
 
"""
import _thread
loop = asyncio.get_event_loop()
def atte():
  while True :
    try :
      loop.run_forever()
    except Exception as err:
      print(err)
      
   
_thread.start_new_thread(atte,())


async def cancelall():
    await asyn.Cancellable.cancel_all()
    
def cancel():
    loop = asyncio.get_event_loop()
    loop.call_soon(cancelall())



