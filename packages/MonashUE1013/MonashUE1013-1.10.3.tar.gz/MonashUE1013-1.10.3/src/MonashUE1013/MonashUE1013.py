'''
Purpose: This module provides the basic functionality required for the completion of the projects B and C of ENG1013
Functions included: 
            Set-Up:
                1. Initialise motor drive
                    a. Unidirecional control
                    b. Bidirectional control 
                    c. Mapping

                2. Initialise 7 segment control 
                    a.  with 1 or 2 clock connections
                    b.  with single SR 
                    c.  with single SR and parallel SR 
                    d.  with two SRs in series 
                    
            Main driver functionality:
                1. 7 segment control 
                    a. with scrolling
                    b. without scrolling
                    
                2. Motor driver
'''
#Copyright (C) 2022 Monash University
#Author: Sachinthana Pathiranage and Jessica Woolley
#Date Created: 08/07/2022
#Last Modified: 19/08/2022
#Version: 1.10.3

from MonashUE1013.ProjectResources import ProjectResources

CF = ProjectResources.ENG1013ProjectResources()

#global vairables
TUNING = 0 #sets the tuning value
SCROLL = 0 #set the scroll speed of the 7 seg 
MODEM = ''#set the motor mode type
MODES = ''#set the shift register mode 
SPEEDNUMBER = 0 #sets the range for the motor speeds based on calibration 

MOTORPINS = [] #save the motor pins for use
SRPINS = [] #save the shift register pins for use
 

#---------------------------------------START PIN SETUP FUNCTIONALITY---------------------------------------------#
#motor_setup function is used to set up the motor connections and mode to the Arduino
#Inputs
#   board = pymata board for use with function
#   pinList = list of integers which link to pins for control in order [enablePin,input1,input2]
#   mapping = integer which determines the minimum set for the speed, between 0 and 255. default = 0
#   mode = string of either 'uni' (uni-directional) or 'bi' (bi-directional) which sets the motor mode depending on wiring. default = 'uni'
#   speedNumber = integer which determines the range of speed options, between 2 and 6. default = 2
#Return
#   None

def motor_setup(board, pinList, mapping, mode='uni', speedNumber=2):
    '''
    board = pymata board for use with function
    pinList = list of integers which link to pins for control in order [enablePin,input1,input2]\n
    mapping = integer which determines the minimum set for the speed, between 0 and 255.\n
    mode = string of either 'uni' (uni-directional) or 'bi' (bi-directional) which sets the motor mode depending on wiring. default = 'uni'\n
    speedNumber = integer which determines the range of speed options, between 2 and 6. default = 2
    '''
    #board alignment:
    CF.board = board
    #set file globals for updating 
    global SPEEDNUMBER, MODEM, MOTORPINS

    #make sure pinlist is valid
    if len(pinList)!= 3 or type(pinList) == str:
        print("Invalid number of pins pinList, please make sure there are 3 pins and it is a list")
        exit()

    #make sure mapping is valid
    try:
        mapping = int(str(mapping))    
        if mapping<0 or mapping>255:
            print("Invalid value for mapping, it must be between 0 and 255")
            exit()
    except ValueError:
        print("Invalid type for mapping, it must be an integar")
        exit()

    #make sure type is valid
    if mode!= 'uni' and mode!='bi':
        print("Invalid value for mode, it must be either uni or bi")
        exit()

    #make sure speed number is valid
    try:
        speedNumber = int(str(speedNumber))
        if (speedNumber<2 or speedNumber>6):
            print("Invalid value for speedNumber, it must be between 2 and 6")
            exit()
    except ValueError:
        print("Invalid type for speedNumber, it must be an integar")
        exit()
        
    #run setup
    CF.setup_motor(pinList[0], pinList[1], pinList[2], mapping,speedNumber)
    #update globals
    SPEEDNUMBER = speedNumber
    MODEM = mode
    MOTORPINS = pinList
    print("INFO: Motor setup done!")


#seven_seg_setup function is used to set up the seven-segment display connections and mode to the Arduino
#Inputs
#   board = pymata board for use with function
#   controlPinList = list of integers that link to pins for control in order [SRCLK,RCLK]. If length = 1 then 1 clock mode
#   dataPinList = list of integers that link to pins for data in order [SRDATA,DIGIT1,DIGIT2,DIGIT3,DIGIT4]. If length = 5 then 1 SR, if length = 1 then 2 SR
#   scrollSpeed = float which determines how fast the message scrolls in seconds. default = 1
#   tuning = float which determines how long the digit is on in seconds for brightness/flicker tuning. default = 0.01
#Return
#   None
def seven_seg_setup(board,controlPinList, dataPinList, scrollSpeed=1, tuning=0.01):
    '''
    board = pymata board for use with function
    controlPinList = list of integers that link to pins for control in order [SRCLK,RCLK]. If length = 1 then 1 clock mode\n
    dataPinList = list of integers that link to pins for data in order [SRDATA,DIGIT1,DIGIT2,DIGIT3,DIGIT4]. If length = 5 then 1 SR, if length = 1 then 2 SR\n
    scrollSpeed = float which determines how fast the message scrolls in seconds. default = 1\n
    tuning = float which determines how long the digit is on in seconds for brightness/flicker tuning. default = 0.01
    '''
    #board alignment:
    CF.board = board
    #define globals for updating
    global SRPINS, SCROLL, TUNING, MODES

    #check input is valid for parameters
    try:
        tuning = float(tuning)
        if tuning <0:
            print("Invalid tuning value, it must be above 0")
            exit()
    except ValueError:
        print("Invalid tuning value, it must be an float")
        exit()
    try:
        scrollSpeed = float(scrollSpeed)
        if scrollSpeed <0:
            print("Invalid scrollSpeed value, it must be above 0")
            exit()
    except ValueError:
        print("Invalid scrollSpeed value, it must be an float")
        exit()

    #use length to determine numbre of shift registers 
    if len(dataPinList)==5 and type(dataPinList)!=str: 
        #one shift register
        MODES = 'sing'
        #set up seven seg
        CF.setup_8seg(dataPinList[1:5])
        print("INFO: 7 seg setup done!")
        if len(controlPinList)==2 and type(dataPinList)!=str:
            #if 2 clocks
            CF.setup_shiftreg(dataPinList[0], controlPinList[0], controlPinList[1])
            srPins = [dataPinList[0],controlPinList[0],controlPinList[1]]
            print("INFO: Shift register setup done!")
        elif len(controlPinList) ==1 and type(dataPinList)!=str:
            #if 1 clock
            CF.setup_shiftreg(dataPinList[0], controlPinList[0], controlPinList[0])
            srPins = [dataPinList[0],controlPinList[0],controlPinList[0]]
            print("INFO: Shift register setup done!")
        else:
            print("Invalid number of controlPins in List, please make sure it is either 1 or 2 and a list")
            exit()

    elif len(dataPinList)==1 and type(dataPinList)!=str:
        #if 2 shift registers 
        if len(controlPinList) == 2 and type(dataPinList)!=str: 
            #in series mode
            srPins = [dataPinList[0],controlPinList[0],controlPinList[1]]
            #set up
            CF.setup_shiftreg(srPins[0], srPins[1], srPins[2])
            CF.setup_8seg_extended(srPins)
            print("INFO: Shift registers 1 & 2 setup done!")
            MODES = 'ser'
        elif len(controlPinList) == 3 and type(dataPinList)!=str: 
            #in parrallel mode
            srPins = [dataPinList[0],controlPinList[0],controlPinList[1],controlPinList[2]]
            #set up 
            CF.setup_shiftreg(srPins[0], srPins[1], controlPinList[1])
            CF.setup_8seg_extended([srPins[0],srPins[1],srPins[2]])
            print("INFO: Shift register 1 setup done!")
            CF.setup_shiftreg(srPins[0], srPins[1], controlPinList[2])
            CF.setup_8seg_extended([srPins[0],srPins[1],srPins[3]])
            print("INFO: Shift register 2 setup done!")
            MODES = 'par'
        else:
            print("Invalid number of controlPins in List, please make sure it is either 2 or 3 and a list")
            exit()
    else:
        print("Invalid number of dataPins in List, please make sure it is either 1 or 5 and a list")
        exit()

    #update global variables 
    TUNING = tuning
    SCROLL = scrollSpeed
    SRPINS = srPins

#---------------------------------------END OF PIN SETUP FUNCTIONALITY---------------------------------------------#

#---------------------------------------START MAIN DRIVER FUNCTIONALITY--------------------------------------------#
#motor_running function is used to run the motors
#Inputs
#   board = pymata board for use with function
#   speed = integer which sets the current speed of the motor, between 0 and speedNumber (as per setup).
#   direction = integer which determines the direction the motor spins in bi-directional mode, either 1 (left) or 2 (right). default = 1
#   motorID = integer which determines which motor to spin in uni-directional mode, either 1 (A) or 2 (B). default = 1
#Return
#   None
def motor_running(board,speed, direction=1, motorID=1):
    '''
    board = pymata board for use with function
    speed = integer which sets the current speed of the motor, between 0 and speedNumber (as per setup).\n
    direction = integer which determines the direction the motor spins in bi-directional mode, either 1 (left) or 2 (right). default = 1\n
    motorID = integer which determines which motor to spin in uni-directional mode, either 1 (A) or 2 (B). default = 1\n
    '''
    #board alignment:
    CF.board = board
    #check speed is valid
    try:
        speed = int(str(speed))
        if 0>speed or speed >SPEEDNUMBER:
            print("Invalid speed option, please input between 0 and the set speedNumber (from setup)")
            exit()
    except ValueError:
        print("Invalid speed option, speed must be an integar")
        exit()

    #check direction is valid
    try:
        direction = int(str(direction))
        if direction ==1:
            forward = True 
        elif direction == 2:
            forward = False
        else:
            print("Invalid direction, please input 1 or 2")
            exit()
    except ValueError:
        print("Invalid direction, it must be an integar")
        exit()

    #check motorID is valid 
    try:
        motorID = int(str(motorID))

        if motorID!=1 and motorID!= 2:
            print("Invalid motor choice, please input 1 or 2")
            exit()
    except ValueError:
        print("Invalid motor choice, it must be an integar")
        exit()

    #use mode to determine which running function to use    
    if MODEM =='bi':
        CF.run_motor_bi(MOTORPINS[0], MOTORPINS[1], MOTORPINS[2], forward, speed)
    else:
        CF.run_motor_uni(MOTORPINS[0], MOTORPINS[1], MOTORPINS[2], motorID, speed)



#seven_seg_running function is used to display messages on the set up seven segment display
#Inputs
#   board = pymata board for use with function
#   message = string or list of integers which determines the message displayed on the 7 seg. if a string needs to be converted to digit code; if an integer is already in code form. length <=4 no scrolling or length >4 scrolling.
#   messagePersistance = float which determines how long the message is displayed in seconds. default = 1
#Return
#   None
def seven_seg_running(board,message,messagePersistance=1):
    '''
    board = pymata board for use with function
    message = string or list of integers which determines the message displayed on the 7 seg. if a string needs to be converted to digit code; if an integer is already in code form. length <=4 no scrolling or length >4 scrolling.\n
    messagePersistance = float which determines how long the message is displayed in seconds. default = 1\n
    '''
    #board alignment:
    CF.board = board
    #check message persistance is valid
    try:
        messagePersistance = float(messagePersistance)
        if messagePersistance<0:
            print("Invalid messagePersitance, must be greater than 0")
            exit()
    except ValueError:
        print('Invalid messagePersitance, it must be a float')
        exit()

    #use message length to determine if scrolling
    if type(message)==str:
        if len(message)<=4:
            #use mode to determine which function to use
            if MODES == 'sing':
                CF.write_8seg_default_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,messagePersistance,TUNING)
            elif MODES == 'ser':
                CF.write_series_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,messagePersistance,TUNING)
            elif MODES == 'par':
                CF.write_parallel_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],SRPINS[3],message,messagePersistance,TUNING)
        else:
            #use mode to determine which function to use
            if MODES =='sing':
                CF.write_8seg_default_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,SCROLL,messagePersistance,TUNING)
            elif MODES =='ser':
                CF.write_series_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,SCROLL,messagePersistance,TUNING)
            elif MODES =='par':
                CF.write_parallel_scroll(SRPINS[0],SRPINS[1],SRPINS[2],SRPINS[3],message,SCROLL,messagePersistance,TUNING)
    else:
        if len(message[0])<=4:
            #use mode to determine which function to use
            if MODES == 'sing':
                CF.write_8seg_default_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,messagePersistance,TUNING)
            elif MODES == 'ser':
                CF.write_series_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,messagePersistance,TUNING)
            elif MODES == 'par':
                CF.write_parallel_no_scroll(SRPINS[0],SRPINS[1],SRPINS[2],SRPINS[3],message,messagePersistance,TUNING)
        else:
            #use mode to determine which function to use
            if MODES =='sing':
                CF.write_8seg_default_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,SCROLL,messagePersistance,TUNING)
            elif MODES =='ser':
                CF.write_series_scroll(SRPINS[0],SRPINS[1],SRPINS[2],message,SCROLL,messagePersistance,TUNING)
            elif MODES =='par':
                CF.write_parallel_scroll(SRPINS[0],SRPINS[1],SRPINS[2],SRPINS[3],message,SCROLL,messagePersistance,TUNING)

