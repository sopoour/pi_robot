import os
import sys
import signal
import threading
import time
#import io
#import json
#import asyncio
from sanic import Sanic
from sanic import response
import config as cfg
import io_wrapper as hw
#import io_wrapper_dummy as hw

app = Sanic(__name__)
app.static('/static', './static')
app.static('/favicon.ico', './static/favicon.ico')

# Immobilizes sytem (chocks on) after 'timeout' seconds 
def watchdog_timer():
    while cfg.watchdog_active:
        time.sleep(1)
        if cfg.watchdog_running:
            cfg.watchdog += 1
            if cfg.watchdog > cfg.timeout and not cfg.chocks:
                chocks_on()
            if cfg.watchdog <= cfg.timeout and cfg.chocks:
                chocks_off()

# Handler for a clean shutdown when pressing Ctrl-C
def signal_handler(signal, frame):
    hw.light_blue_blink(0.1)
    cfg.watchdog_active = False
    brakes_on()
    wd.join()
    app.stop()
    hw.light_blue_off()
    sys.exit(0)

# Handler for explorer-hat touchpads
def touch_handler(channel, event):
    if channel == 1:
        cfg.blue = not cfg.blue
        if cfg.blue:
            hw.light_blue_on()
            hw.output_one_on()
        else:
            hw.light_blue_off()
            hw.output_one_off()
    if channel == 2:
        cfg.yellow = not cfg.yellow
        if cfg.yellow:
            hw.light_yellow_on()
            hw.output_two_on()
        else:
            hw.light_yellow_off()
            hw.output_two_off()
    if channel == 3:
        cfg.chocks = not cfg.chocks
        if cfg.chocks:
            cfg.watchdog_running = False
            chocks_on()
        else:
            cfg.watchdog_running = True
            chocks_off()
    if channel == 4:
        hw.light_green_blink(0.1)
        cfg.green = True
        time.sleep(5)
        if cfg.chocks:
            hw.light_green_on()
            os.system("sudo -s shutdown -h now")
        else:
            hw.light_green_off()
            cfg.green = False
    
def brakes_on():
    cfg.brakes = True
    cfg.left_motor = 0
    cfg.right_motor = 0
    hw.motor_one_speed(cfg.right_motor)
    hw.motor_two_speed(cfg.left_motor)
    
def brakes_off():
    cfg.brakes = False
    cfg.watchdog = 0
    
def chocks_on():
    cfg.chocks = True
    brakes_on()
    hw.light_red_blink(0.2)
    
def chocks_off():
    cfg.chocks = False
    brakes_off()
    hw.light_red_off()


# Base URL / - loads web interface        
@app.route('/')
def index(request):
    video = request.args.get('video')
    if video == 'n':
        cfg.video_status = False
    else:
        if video == None:
            cfg.video_status = True
        elif float(video) > 0:
            cfg.video_status = float(video)
    return response.file('./static/sanic_index.html')

# URL to remote control touchpads 1-4 on explorer-hat
@app.route('/touchpad')
def touchpad(request):
    pad = request.args.get('pad')
    if pad:
        touch_handler(int(pad), True)
    return response.text('ok')

# URL for heartbeat requests (resets watchdog timer)    
# Returns JSON object with status data
@app.route('/heartbeat')
def heartbeat(request):
    cfg.watchdog = 0
    output = {}
    output['b'] = cfg.blue
    output['y'] = cfg.yellow
    output['c'] = cfg.chocks
    output['g'] = cfg.green
    output['v'] = cfg.video_status
    output['l'] = cfg.left_motor
    output['r'] = cfg.right_motor
    output['i1'] = hw.input_one_read()
    output['i2'] = hw.input_two_read()
    output['i3'] = hw.input_three_read()
    output['i4'] = hw.input_four_read()
    output['a1'] = hw.analog_one_read()
    output['a2'] = hw.analog_two_read()
    output['a3'] = hw.analog_three_read()
    output['a4'] = hw.analog_four_read()
    return response.json(output)

# URL for motor control - format: /motor?l=[speed]&r=[speed]
@app.route('/motor')
def motor(request):
    left = request.args.get('l')
    right = request.args.get('r')
    if left and not cfg.chocks:
        left = int(left)
        if left >= -100 and left <= 100:
            cfg.left_motor = left
            hw.motor_two_speed(cfg.left_motor)
    if right and not cfg.chocks:
        right = int(right)
        if right >= -100 and right <= 100:
            cfg.right_motor = right
            hw.motor_one_speed(cfg.right_motor)
    return response.text('ok')

# URL for joystick input - format: /joystick?x=[x-axis]&y=[y-axis]
@app.route('/joystick')
def joystick(request):
    cfg.watchdog = 0
    x_axis = int(request.args.get('x'))
    y_axis = int(request.args.get('y'))
    x_axis = -1 * max( min(x_axis, 100), -100)
    y_axis = max( min(y_axis, 100), -100)
    v = (100-abs(x_axis)) * (y_axis/100) + y_axis
    w = (100-abs(y_axis)) * (x_axis/100) + x_axis
    r = int((v+w) / 2)
    l = int((v-w) / 2)
    if not cfg.chocks:
        cfg.right_motor = r
        cfg.left_motor = l
        hw.motor_one_speed(cfg.right_motor)
        hw.motor_two_speed(cfg.left_motor)
    return response.text('ok')


if __name__ == '__main__':
    hw.light_green_blink(0.1)
    time.sleep(1)
    hw.light_green_off()
    
    # register signal handler for a clean exit    
    signal.signal(signal.SIGINT, signal_handler)

    # register handler for touchpads
    if hw.explorerhat:
        hw.xhat.touch.released(touch_handler)
        
    # prepare and start watchdog
    wd = threading.Thread(name='watchdog_timer', target=watchdog_timer)
    wd.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False, access_log=False)
