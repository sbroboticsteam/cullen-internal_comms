
import sdl2
import sdl2.ext
from Node import Node
import json
import time

# Basic initialization stuff for the node and joysticks
node = Node("controls_send.json")
sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
arm_joy = sdl2.SDL_JoystickOpen(0)
drive_joy = sdl2.SDL_JoystickOpen(1)

# Whether or not the xbox button of either controller is pressed
pressed14 = False

# Processes input from the arm controller
def handle_arm_input(data):
    arm_rotation = (data[5] - data[2]) // 64
    linear_actuator = data[0] // 32
    elbow = data[1] // 32
    wrist_left = (data[4] + data[3]) // 32
    wrist_right = (-data[4] - data[3]) // 32
    return [arm_rotation, linear_actuator, elbow, wrist_left, wrist_right]

while True:

    # Update the xbox controller events
    sdl2.SDL_PumpEvents()

    # Grabs data from both joysticks and stores them in arrays
    arm_data = []
    drive_data = []
    for i in range(0, 6):
        arm_data.append(sdl2.SDL_JoystickGetAxis(arm_joy, i))
        drive_data.append(sdl2.SDL_JoystickGetAxis(drive_joy, i))
    for i in range(0, 11):
        arm_data.append(sdl2.SDL_JoystickGetButton(arm_joy, i))
        drive_data.append(sdl2.SDL_JoystickGetButton(drive_joy, i))
    arm_data.append(sdl2.SDL_JoystickGetHat(arm_joy, 0))
    drive_data.append(sdl2.SDL_JoystickGetHat(drive_joy, 0))
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

    # Handles switching xbox controllers by clicking the xbox button (14)
    if ((arm_data[14] or drive_data[14]) and not pressed14):
        pressed14 = True
    if (not arm_data[14] and not drive_data[14] and pressed14):
        pressed14 = False
        arm_joy, drive_joy = drive_joy, arm_joy

    # Actually sends the data
    arm_msg = json.dumps(handle_arm_input(arm_data))
    drive_msg = json.dumps(drive_data)
    node.send("arm", arm_msg)
    node.send("drive", drive_msg)

    # Small time delay so nothing freaks out
    time.sleep(0.01)

