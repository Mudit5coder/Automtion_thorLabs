 
import time
import clr
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\ThorLabs.MotionControl.KCube.DCServoCLI.dll")
import os
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI, SimulationManager
from Thorlabs.MotionControl.KCube.DCServoCLI import KCubeDCServo
from System import Decimal

from ctypes import c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_double

controller = None
controller1 = None
def initialize_motor():
    global controller
    global controller1
    serial_num = '27267676'
    serial_num1 = '27267869'
    DeviceManagerCLI.BuildDeviceList()
    controller = KCubeDCServo.CreateKCubeDCServo(serial_num)
    controller1 = KCubeDCServo.CreateKCubeDCServo(serial_num1)
    if controller is not None and controller1 is not None:
        controller.Connect(serial_num)
        controller1.Connect(serial_num1)
        if not controller.IsSettingsInitialized():
            controller.WaitForSettingsInitialized(3000)
        if not controller1.IsSettingsInitialized():
            controller1.WaitForSettingsInitialized(3000)    
        controller.StartPolling(50)
        time.sleep(0.1)
        controller.EnableDevice()
        time.sleep(0.1)
        config = controller.LoadMotorConfiguration(serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = 'PRM1-Z8'
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)
        print('Homing Motor')
        controller.Home(60000)
        print('Motor Homed')
        time.sleep(0.5)
        controller1.StartPolling(50)
        time.sleep(0.1)
        controller1.EnableDevice()
        time.sleep(0.1)
        config1 = controller1.LoadMotorConfiguration(serial_num1, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config1.UpdateCurrentConfiguration()
        controller1.SetSettings(controller1.MotorDeviceSettings, True, False)
        print('Homing Motor 2')
        controller1.Home(60000)
        print('Motor Homed  2')
    else:
        raise Exception("Motor not found or couldn't connect.")

def move_motor(x, y):
    global controller
    global controller1
    print('Homing Motor')
    controller.Home(60000)
    print('Motor Homed')
    time.sleep(2)
    print('Homing Motor 2')
    controller1.Home(60000)
    print('Motor Homed  2')
    time.sleep(2)
    jog_params = controller.GetJogParams()
    jog_params.StepSize = Decimal(x)
    jog_params.MaxVelocity = Decimal(10)
    jog_params.JogMode = JogParametersBase.JogModes.SingleStep
    controller.SetJogParams(jog_params)
    print(f'Moving motor by {x} angle')
    controller.MoveJog(MotorDirection.Forward, 60000)
    print('moving motor 1 done')
    time.sleep(2)
    jog_params1 = controller1.GetJogParams()
    jog_params1.StepSize = Decimal(y)
    jog_params1.MaxVelocity = Decimal(10)
    jog_params1.JogMode = JogParametersBase.JogModes.SingleStep
    controller1.SetJogParams(jog_params1)
    print(f'Moving motor by {y} angle')
    controller1.MoveJog(MotorDirection.Forward, 60000)
    print('moving motor 2 done')
    time.sleep(2)
    
initialize_motor()  # Call this ONCE
LP_Motor1_s = [0, 0, 99, 79, 41, -39, 69, -21, 69, -69, -39, 39]
QWPs_motor2 = [45, 135, 0, 0, 30, 30, -30, 60, 30, -30, -60]
for angle, angle1 in zip(LP_Motor1_s, QWPs_motor2):
    move_motor(angle, angle1)
    
    time.sleep(2)
    
