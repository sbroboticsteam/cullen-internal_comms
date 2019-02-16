
import sdl2
import sdl2.ext
from Node import Node
import json
import time

node = Node("controls_send.json")

sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

arm_joy = sdl2.SDL_JoystickOpen(0)
drive_joy = sdl2.SDL_JoystickOpen(1)

pressed14 = False

while True:
    sdl2.SDL_PumpEvents()

    arm_data = []
    for i in range(0, 6):
        arm_data.append(sdl2.SDL_JoystickGetAxis(arm_joy, i))
    for i in range(0, 11):
        arm_data.append(sdl2.SDL_JoystickGetButton(arm_joy, i))
    arm_data.append(sdl2.SDL_JoystickGetHat(arm_joy, 0))

    drive_data = []
    for i in range(0, 6):
        drive_data.append(sdl2.SDL_JoystickGetAxis(drive_joy, i))
    for i in range(0, 11):
        drive_data.append(sdl2.SDL_JoystickGetButton(drive_joy, i))
    drive_data.append(sdl2.SDL_JoystickGetHat(drive_joy, 0))

    if ((arm_data[14] or drive_data[14]) and not pressed14):
        pressed14 = True
    if (not arm_data[14] and not drive_data[14] and pressed14):
        pressed14 = False
        arm_joy, drive_joy = drive_joy, arm_joy

    arm_msg = json.dumps(arm_data)
    node.send("arm", arm_msg)
    drive_msg = json.dumps(drive_data)
    node.send("drive", drive_msg)

    time.sleep(0.01)

    # Data array format:
    ## 16 bit signed ints:
    # 0  | right joystick x
    # 1  | right joystick y
    # 2  | right trigger
    # 3  | left joystick x
    # 4  | left joystick y
    # 5  | left trigger
    ## 1 bit (0 = unpressed, 1 = pressed)
    # 6  | A
    # 7  | B
    # 8  | X
    # 9  | Y
    # 10 | left bumper
    # 11 | right bumper
    # 12 | view (left center button)
    # 13 | menu (right center button)
    # 14 | xbox (center button)
    # 13 | left joystick button
    # 14 | right joystick button
    ## 4 bit
    # 17 | hat switch / dpad
    #    | (1 = N, 3 = NE, 2 = E, 6 = SE, 4 = S, 12 = SW, 8 = W, 9 = NW)
