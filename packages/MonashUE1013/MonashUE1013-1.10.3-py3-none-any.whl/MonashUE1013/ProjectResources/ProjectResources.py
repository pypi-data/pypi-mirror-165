'''
Purpose: This module provides the basic functionality required for the completion of the projects B and C of ENG1013
Functions included: 
            Main driver functionality:
                1. 8 segment control with single SR without scrolling
                2. 8 segment control with single SR with scrolling
                2. 8 segment control with single SR and parallel SR for other output drive without scrolling
                3. 8 segment control with single SR and parallel SR for other output drive with scrolling
                4. 8 segment control with two SRs in series without scrolling
                5. 8 segment control with two SRs in series with scrolling
                6. 8 segment control with two SRs in series and parallel SR for other output drive without scrolling
                7. 8 segment control with two SRs in series and parallel SR for other output drive with scrolling
                8. Motor drive
            Supporting:
                1. Get Pymana4 instance
                2. Initalize SR pins
                3. Initialize 8 seg pins (for digit pin control via arduino)
                4. Initialize 8 seg pins (for digit pin control via 2nd SR)
                5. On/Off SRs
                6. Get binary mapping for value
                7. Convert input to binary mapping
                8. Write to single 8 seg display
                9. Write to 4 8 seg displays without scrolling 
                10. Write to 4 8 seg displays with scrolling

Copyright (C) 2022 Monash University
Author: Sachinthana Pathiranage and Jessica Woolley
Date Created: 08/07/2022
Last Modified: 19/08/2022
Version: 1.10.1
'''
import time
from pymata4 import pymata4

# a-g,dp
# 1 - on, 0 - off
PIN_MAP = {
    "A": int("11101110", 2),
    "B": int("00111110", 2),
    "C": int("10011100", 2),
    "D": int("01111010", 2),
    "E": int("10011110", 2),
    "F": int("10001110", 2),
    "G": int("10111100", 2),
    "H": int("01101110", 2),
    "I": int("10001000", 2),
    "J": int("01110000", 2),
    "K": int("10101110", 2),
    "L": int("00011100", 2),
    "M": int("10101010", 2),
    "N": int("00101010", 2),
    "O": int("00111010", 2),
    "P": int("11001110", 2),
    "Q": int("11100110", 2),
    "R": int("00001010", 2),
    "S": int("10110110", 2),
    "T": int("00011110", 2),
    "U": int("00111000", 2),
    "V": int("01111100", 2),
    "W": int("01010110", 2),
    "X": int("01101110", 2),
    "Y": int("01110110", 2),
    "Z": int("11010010", 2),
    "0": int("11111100", 2),
    "1": int("01100000", 2),
    "2": int("11011010", 2),
    "3": int("11110010", 2),
    "4": int("01100110", 2),
    "5": int("10110110", 2),
    "6": int("10111110", 2),
    "7": int("11100000", 2),
    "8": int("11111110", 2),
    "9": int("11110110", 2)
}
DIGIT_CODES = {
    0:int("1110",2),
    1:int("1101",2),
    2:int("1011",2),
    3:int("0111",2),
    'off':int("1111",2)
}

PIN_MASK = 0b00000001
PIN_MASK_EX = 0b000000000001
# digit pins for the four 8 seg
# DIGIT_PINS[0] - left-most, DIGIT_PINS[3] - right-most
DIGIT_PINS = []

DISTANCE_CM = 2
sonarData = -1

# default speed calibration for motor
calibration = {
    0:0, 
    1:50, 
    2:100, 
    3:150, 
    4:200, 
    5:255
}

class ENG1013ProjectResources:
    '''
    Initialize ENG1013 Project Resources.

    :param digitPins: Arduino pins for 4 digit 8 seg display.
    :type digitPins: List[int]

    :param pinMap: Binary dictionary mapping for alpha numeric characters.
    :type pinMap: dict[int]

    :return: None
    '''

    def __init__(self) -> None:

        self.board = None #pymata4.Pymata4() # initialize board
        
    def get_board(self):
        '''
        Get arduino board instance.

        :param: None

        :return: Arduino board instance.
        :rtype: Pymata4
        '''
        return self.board

#---------------------------------------START PIN SETUP FUNCTIONALITY---------------------------------------------#
    def setup_shiftreg(self, data, srclk, rclk): # setup the board and pin modes
        '''
        Initialize the arduino pins connected to shift register.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param rclk: Latch pin.
        :type rclk: int

        :return: None
        '''
        # set the pin mode
        self.board.set_pin_mode_digital_output(data)
        self.board.set_pin_mode_digital_output(srclk)
        self.board.set_pin_mode_digital_output(rclk)
        
        # reset the input pins
        self.board.digital_write(data,0)
        self.board.digital_write(srclk,0)
        self.board.digital_write(rclk,0)

    # setup 8 seg pins separately
    def setup_8seg(self,digitPins,pinMap = None):
        '''
        Initialize the pins connected to 4 digit 8 seg display.

        :param: None

        :return: None
        '''
        if digitPins:
            global DIGIT_PINS
            DIGIT_PINS = digitPins
        if pinMap:
            global PIN_MAP
            PIN_MAP = pinMap

        # set the pin mode
        for pin in DIGIT_PINS:
            self.board.set_pin_mode_digital_output(pin)

        # turn off all digits
        for pin in DIGIT_PINS:
            self.board.digital_write(pin,1)


    def setup_8seg_extended(self, srPins):
        '''
        Initialize the arduino pins for series 8 seg control.

        :param srPins: Arduino pins connected to shift register.
        :type srPins: List[int]

        :return: None
        '''
        for _ in range(8):
            self.board.digital_write(srPins[0], 1)

            # toggle srclk to shift next
            self.board.digital_write(srPins[1], 1)
            self.board.digital_write(srPins[1], 0)
        
        for _ in range(8):
            self.board.digital_write(srPins[0], 0)
            
            # toggle srclk to shift next
            self.board.digital_write(srPins[1], 1)
            self.board.digital_write(srPins[1], 0)
        
        # toggle rclk to store the data to register 
        self.board.digital_write(srPins[2],1)
        self.board.digital_write(srPins[2],0)
    
        # DO NOT REMOVE
        time.sleep(1) # this should be at least 1s

    def toggle_sr_on(self, latchPin): # turn off SR bank if selected
        '''
        Reset shift register latch.

        :param latchPin: Arduino pin connected to shift register latch.
        :type latchPin: int

        :return: None
        '''
        self.board.digital_write(latchPin,0)
#---------------------------------------END OF PIN SETUP FUNCTIONALITY---------------------------------------------#


#---------------------------------------START 8 SEG FUNCTIONALITY---------------------------------------------#
    def get_codes(self, c): # retrieve binary code from pin map
        '''
        Get binary mapping for character.

        :param c: Character to be converted.
        :type c: string

        :return: Binary mapping from dictionary.
        :rtype: int
        '''

        return PIN_MAP[c.upper()]

    def convert_input(self, displayInput): # convert the input values to binary codes
        '''
        Convert given input to 8-bit binary.

        :param displayInput: Value to be converted.
        :type displayInput: string or List[int]

        :return: Integer mapping to given input.
        :rtype: List[List[int]]
        '''
        # all upper case or all lower case?
        digitCodes = []
        if type(displayInput) == str: # return a 2D array, however will have always 1 sub array - scroll if sub array length > 4
            valToBinary = []
            for c in displayInput:
                if c.isalnum():
                    valToBinary.append(self.get_codes(c)) # error handling for unavailable chars?
                elif c == '.': # assumption - there will always be an alphanumeric proceeding a dot.
                    prev = bin(valToBinary.pop())
                    prev = prev[:len(prev)-1] + '1'
                    valToBinary.append(int(prev,2))
                else:
                    print(f'ERROR: Invalid character found. Ignoring {c} in the output.')
            # append 0s to make the length equals to 4
            codeLen = len(valToBinary)
            prefix = [0]*(4-codeLen)
            valToBinary = prefix + valToBinary
            digitCodes.append(valToBinary)
        elif type(displayInput) == list: # return a 2D array - displayed one value after the other
            for num in displayInput:
                chars = str(num)
                numToBinary = []
                for c in chars:
                    if c.isnum():
                        numToBinary.append(self.get_codes(c))
                    elif c == '.': # assumption - there will always be an number proceeding a dot.
                        prev = bin(numToBinary.pop())
                        prev = prev[:len(prev)-1] + '1'
                        numToBinary.append(int(prev,2))
                    else:
                        print(f'ERROR: Invalid character found. Ignoring {c} in the output.')
                # append 0s to make the length equals to 4
                codeLen = len(numToBinary)
                prefix = [0]*(4-codeLen)
                numToBinary = prefix + numToBinary
                digitCodes.append(numToBinary)
        else:
            print('ERROR: Invalid input type received. Input should be a string or a list of numbers.')
        return digitCodes

    # first register maps to pin Q7 -> value written first is pushed to pin Q7, second value pushed to Q6 etc. Pin Q7 is connected to DP of 8-seg
    def write_single_seg(self, val, srPins, digit,default = True): # write to single digit
        '''
        Write to single 8-seg display.

        :param val: Value to be written.
        :type val: int

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param digit: Digit to be written.
        :type digit: int

        :param default: sets if 7 seg digit pins being used 
        :type default: bool

        :return: None
        '''
        for i in range(8):
            if (val) & (PIN_MASK << i): # if 1, write 1 to serial pin
                self.board.digital_write(srPins[0], 1)
            else: # if 0, write 0 to serial pin
                self.board.digital_write(srPins[0], 0)
            
            # toggle srclk to shift next
            self.board.digital_write(srPins[1], 1)
            self.board.digital_write(srPins[1], 0)

        # toggle rclk to store the data to register 
        self.board.digital_write(srPins[2],1)
        self.board.digital_write(srPins[2],0)
        if default:
            # turn on the display
            self.board.digital_write(DIGIT_PINS[digit], 0)
            # DO NOT REMOVE
            time.sleep(0.005) # do not make this too small (input is in seconds). It will cause output to queue and not display a sequence of numbers
            # disable output
            self.board.digital_write(DIGIT_PINS[digit], 1)
        else:
             time.sleep(0.005) # do not make this too small (input is in seconds). It will cause output to queue and not display a sequence of numbers

    # in the first SR, first register maps to pin Q7 -> value written first is pushed to pin Q7, second value pushed to Q6 etc. Pin Q7 is connected to DP of 8-seg
    # in the second SR, Q4-Q7 will be always zero. Q0 maps to digit one (left most), Q3 maps to digit 4 (right most)
    # first 8 bits written will be written to the second SR
    def write_single_seg_extended(self, val, srPins, digit):
        '''
        Write to single 8-seg display for series 8 seg control.

        :param val: Value to be written.
        :type val: int

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param digit: Digit to be written.
        :type digit: int

        :return: None
        '''
        val = val<<4|DIGIT_CODES[digit] #adds the digit code to the digit for series SRs

        for i in range(12):
            if (val) & (PIN_MASK_EX << i): # if 1, write 1 to serial pin
                self.board.digital_write(srPins[0], 1)
            else: # if 0, write 0 to serial pin
                self.board.digital_write(srPins[0], 0)
            
            # toggle srclk to shift next
            self.board.digital_write(srPins[1], 1)
            self.board.digital_write(srPins[1], 0)
        
        # toggle rclk to store the data to register 
        self.board.digital_write(srPins[2],1)
        self.board.digital_write(srPins[2],0)
        # DO NOT REMOVE - fixes serial output queing issue.
        time.sleep(0.005) # we will use the time taken to write the next 16 bits as the wait time

    def write_four_digits_no_scroll(self, digitCodes, srPins, wait, sleepTime, default = True): # 4 or less chars per array
        '''
        Write to to 4 8 seg digits without scrolling.

        :param digitCodes: Value(s) converted to 8-bit binary.
        :type digitCodes: int or List[List[int]]

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param wait: Display duration for each value.
        :type wait: int

        :param sleepTime: Sleep time between single digit dispay to avoid output buffering.
        :type sleepTime: int

        :param default: True for series control, False otherwise.
        :type default: boolean

        :return: None
        '''
        n = len(digitCodes)

        # iterate and draw
        for i in range(n): # function will return after all values in digitCodes are displayed
            start = time.time()
            while True:
                for j in range(4):
                    if digitCodes[i][j]:
                        if default:
                            self.write_single_seg(digitCodes[i][j], srPins, j) # digit j from left to right
                        else:
                            self.write_single_seg_extended(digitCodes[i][j], srPins, j)
                        # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
                        time.sleep(sleepTime)
                # wait for time specified by wait (in seconds) and move to the next value
                if time.time() - start > wait:
                    break

    def write_four_digits_scroll(self, digitCodes, srPins, delay, duration, sleepTime, default = True): # for strings with more than 4 characters
        '''
        Write to to 4 8 seg digits with scrolling.

        :param digitCodes: Value(s) converted to 8-bit binary.
        :type digitCodes: int or List[List[int]]

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param delay: Scrolling speed.
        :type delay: int
        
        :param duration: Display duration.
        :type duration: int

        :param sleepTime: Sleep time between single digit dispay to avoid output buffering.
        :type sleepTime: int

        :param default: True for series control, False otherwise.
        :type default: boolean

        :return: None
        '''
        digitCodes = digitCodes[0] # we will receive only one array for scrolling
        n = len(digitCodes) # original length of the string
        digitCodes.append(0) # to distinguish the end
        digitCodes += digitCodes[:3] # to display the 4 digits when 1st digit is off (digitCode = 0)
        startDisplay = time.time()

        while True:
            for i in range(n+1): # length of string + 1 for seperator
                start = time.time()
                while True:
                    pin = 0
                    for j in range(i,i+4): # display one set of 4 characters at a time
                        if default:
                            self.write_single_seg( digitCodes[j], srPins, pin)
                        else:
                            self.write_single_seg_extended(digitCodes[j], srPins, pin)
                        pin += 1
                    # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
                    time.sleep(sleepTime)
                    # wait for the time specified by delay and shift left
                    if time.time() - start > delay:
                        break
            # exit functionality if specified duration exceeded
            if time.time() - startDisplay > duration:
                break
            # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
            time.sleep(sleepTime)

    def write_four_digits_par_no_scroll(self, digitCodes, srPins, wait, sleepTime): # 4 or less chars per array
        '''
        Write to to 4 8 seg digits without scrolling for parallel connection.

        :param digitCodes: Value(s) converted to 8-bit binary.
        :type digitCodes: int or List[List[int]]

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param wait: Display duration for each value.
        :type wait: int

        :param sleepTime: Sleep time between single digit dispay to avoid output buffering.
        :type sleepTime: int

        :return: None
        '''

        n = len(digitCodes)

        # iterate and draw
        for i in range(n): # function will return after all values in digitCodes are displayed
            start = time.time()
            while True:
                for j in range(4):
                    if digitCodes[i][j]:
                        self.write_to_sr2(DIGIT_CODES['off'],srPins)#make sure all digits off
                        self.write_single_seg(digitCodes[i][j], srPins, j, False) # digit j from left to right
                        self.write_to_sr2(DIGIT_CODES[j],srPins)
                        # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
                        time.sleep(sleepTime)
                # wait for time specified by wait (in seconds) and move to the next value
                if time.time() - start > wait:
                    break

    def write_four_digits_par_scroll(self, digitCodes, srPins, delay, duration, sleepTime): # for strings with more than 4 characters
        '''
        Write to to 4 8 seg digits with scrolling for parallel connection.

        :param digitCodes: Value(s) converted to 8-bit binary.
        :type digitCodes: int or List[List[int]]

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :param delay: Scrolling speed.
        :type delay: int
        
        :param duration: Display duration.
        :type duration: int

        :param sleepTime: Sleep time between single digit dispay to avoid output buffering.
        :type sleepTime: int

        :return: None
        '''
        digitCodes = digitCodes[0] # we will receive only one array for scrolling
        n = len(digitCodes) # original length of the string
        digitCodes.append(0) # to distinguish the end
        digitCodes += digitCodes[:3] # to display the 4 digits when 1st digit is off (digitCode = 0)
        startDisplay = time.time()

        while True:
            for i in range(n+1): # length of string + 1 for seperator
                start = time.time()
                while True:
                    pin = 0
                    for j in range(i,i+4): # display one set of 4 characters at a time
                        self.write_to_sr2(DIGIT_CODES['off'],srPins)
                        self.write_single_seg( digitCodes[j], srPins, pin,False)
                        self.write_to_sr2(DIGIT_CODES[pin],srPins)
                        pin += 1
                    # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
                    time.sleep(sleepTime)
                    # wait for the time specified by delay and shift left
                    if time.time() - start > delay:
                        break
            # exit functionality if specified duration exceeded
            if time.time() - startDisplay > duration:
                break
            # DO NOT REMOVE - fixes serial output queing issue - give like 0.02s for chained SR, 0.001 otherwise
            time.sleep(sleepTime)
#---------------------------------------END OF 8 SEG FUNCTIONALITY---------------------------------------------#


#---------------------------------------START SR2 FUNCTIONALITY---------------------------------------------#
    def write_to_sr2(self, vals, srPins): # vals is expected to be a list of exactly 8 values
        '''
        Write values to second shift register.

        :param vals: Values to be written.
        :type vals: List[int]

        :param srPins: Arduno pins connected to shift register.
        :type srPins: List[int]

        :return: None
        '''
        for i in range(4):
            if (vals) & (PIN_MASK << i): # if 1, write 1 to serial pin
                self.board.digital_write(srPins[0], 1)
            else: # if 0, write 0 to serial pin
                self.board.digital_write(srPins[0], 0)
            # toggle srclk to shift next
            self.board.digital_write(srPins[1], 1)
            self.board.digital_write(srPins[1], 0)
        
        #toggle rclk to store the data to register 
        self.board.digital_write(srPins[3],1)
        self.board.digital_write(srPins[3],0)
#---------------------------------------END OF SR2 FUNCTIONALITY---------------------------------------------#


#---------------------------------------START MOTOR FUNCTIONALITY---------------------------------------------#
    def setup_motor(self, enA, inA1, inA2, minimum, pwmMapping):
        '''
        Setup single motor drive.

        :param enA: Enable pin connected to arduino.
        :type enA: int

        :param inA1: Input 1 connected to arduino for direction control.
        :type inA1: int

        :param inA2: Input 2 connected to arduino for direction control.
        :type inA2: int

        :param minimum: lowest bound for the mapping.
        :type minimum: int

        :param pwmMapping: PWM mapping for speed control.
        :type pwmMapping: int

        :return: None
        '''
        global calibration
        
        # setup pin modes
        self.board.set_pin_mode_pwm_output(enA)
        self.board.set_pin_mode_digital_output(inA1)
        self.board.set_pin_mode_digital_output(inA2)

        # set motor off
        self.board.digital_write(inA1, 0)
        self.board.digital_write(inA2, 0)
        

        if pwmMapping is not None and (pwmMapping >= 6 or pwmMapping < 2):
            print('ERROR: Incorrect PWM mapping size. Default mapping used! Please between 2 and 6.')
        elif pwmMapping is not None:
            if pwmMapping == 2:
                calibration = {0:minimum,1:255}
            elif pwmMapping == 3:
                calibration = {0:minimum,1:int((255-(255-minimum))/2),2:255}
            elif pwmMapping == 4:
                calibration = {0:minimum,1:int((255-(255-minimum))/3),2:int(2*(255-(255-minimum))/3),3:255}
            elif pwmMapping == 6:
                calibration = {0:minimum,1:int((255-(255-minimum))/5),2:int(2*(255-(255-minimum))/5),3:int(3*(255-(255-minimum))/5),4:int(4*(255-(255-minimum))/5),5:255}
            else:
                calibration = {0:minimum,1:int((255-(255-minimum))/4),2:int(2*(255-(255-minimum)))/4,3:int(3*(255-(255-minimum))/4),4:255}
        self.board.pwm_write(enA,0)

    # user should have run setup_motor before running this method
    def run_motor_bi(self, enA, inA1, inA2, forward, speed): # forward: 1- True, 0 - False (backward)
        '''
        Run single DC motor.

        :param enA: Enable pin value.
        :type enA: int

        :param inA1: Input 1 for direction control.
        :type inA1: int

        :param inA2: Input 2 for direction control.
        :type inA2: int

        :param forward: Running direction. True if forward, False otherwise.
        :type forward: boolean

        :param speed: Running speed.
        :type speed: int

        :return: None
        '''
        try:
            # speed control
            self.board.pwm_write(enA,calibration[speed])

            # direction control
            if forward:
                self.board.digital_write(inA1, 1)
                self.board.digital_write(inA2, 0)
            else:
                self.board.digital_write(inA1, 0)
                self.board.digital_write(inA2, 1)

        except RuntimeError:
            print('ERROR: Please make sure you have run setup_motor function before running this method!')

    def run_motor_uni(self, enA, inA1, inA2, motorID, speed): # forward: 1- True, 0 - False (backward)
        '''
        Run 1 or 2 uni DC motor.

        :param enA: Enable pin value.
        :type enA: int

        :param inA1: Input 1 for direction control.
        :type inA1: int

        :param inA2: Input 2 for direction control.
        :type inA2: int

        :param motorID: Which mtor to run. True if A, False otherwise.
        :type motorID: boolean

        :param speed: Running speed.
        :type speed: int

        :return: None
        '''
        try:
            # speed control
            self.board.pwm_write(enA,calibration[speed])

            # direction control
            if motorID==1:
                self.board.digital_write(inA1, 1)
                self.board.digital_write(inA2, 0)
            else:
                self.board.digital_write(inA1, 0)
                self.board.digital_write(inA2, 1)

        except RuntimeError:
            print('ERROR: Please make sure you have run setup_motor function before running this method!')
#---------------------------------------END OF MOTOR FUNCTIONALITY---------------------------------------------#

#---------------------------------------SINGLE SHIFT REGISTER FO 8-SEG FUNCTIONALITY---------------------------------------------#
    def write_8seg_default_no_scroll(self, data, srclk, rclk, value, wait, sleepTime): # running 8 seg display by default without scrolling
        '''
        Default function for 8 seg control with a shift register without scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param rclk: Latch pin.
        :type rclk: int

        :param value: Value to display on 8 seg.
        :type value: String/ List[float]

        :param wait: Display time per value.
        :type wait: int

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''
        if type(value)==str:
            # map the value to 8-seg display format
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value
        
        srPins = [data, srclk, rclk]

        try:
            # display values
            self.write_four_digits_no_scroll( digitCodes, srPins, wait, sleepTime)
        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()

    def write_8seg_default_scroll(self, data, srclk, rclk, value, wait, duration, sleepTime): # running 8 seg display by default with scrolling
        '''
        Default function for 8 seg control with a shift register with scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param rclk: Latch pin.
        :type rclk: int

        :param value: Value to display on 8 seg.
        :type value: String/ List[float]

        :param wait: Scrolling speed.
        :type wait: int

        :param duration: Display duration.
        :type duration: int

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''

        # map the value to 8-seg display format
        if type(value)==str:
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value
        
        srPins = [data, srclk, rclk]

        try:
            # display values
            self.write_four_digits_scroll(digitCodes, srPins, wait, duration, sleepTime)
        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()
#---------------------------------------END OF SINGLE SHIFT REGISTER FO 8-SEG FUNCTIONALITY---------------------------------------------#


#---------------------------------------PARALLEL SHIFT REGS (TWO BANKS) FUNCTIONALITY---------------------------------------------#
    # uses different latches - fast writing to multiple SRs sharing same data and clock
    # latchSelect a dictionary representing the [pin, on/off status] of each register bank
    def write_parallel_no_scroll(self, data, srclk, rclk1, rclk2, value, wait,sleepTime): # switch between two SR banks as specified by the user - without scrolling
        '''
        Control 8 seg and other outputs parallely with two shift registers without scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param value: Value to write to shift register.
        :type value: String/ List[float]

        :param wait: Display time per value.
        :type wait: int

        :param latchSelect: Shift register selection.
        :type latchSelect: dict[List[int]]

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''
        # set up the board
        srPins = [data, srclk, rclk1,rclk2]

        # map the value to 8-seg display format
        if type(value)==str:
            # map the value to 8-seg display format
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value

        try:
            # display values
            self.write_four_digits_par_no_scroll(digitCodes, srPins, wait,sleepTime)

        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()


    def write_parallel_scroll(self, data, srclk,rclk1,rclk2, value, wait, duration, sleepTime): # switch between two SR banks as specified by the user - with scrolling
        '''
        Control 8 seg and other outputs parallely with two shift registers with scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param value: Value to write to shift register.
        :type value: String/ List[float]

        :param wait: Scrolling speed.
        :type wait: int

        :param duration: Scrolling speed.
        :type duration: int

        :param latchSelect: Shift register selection.
        :type latchSelect: dict[List[int]]

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''
        # set up the board
        srPins = [data, srclk, rclk1,rclk2]

        # map the value to 8-seg display format
        if type(value)==str:
            # map the value to 8-seg display format
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value

        try:
            # display values
            self.write_four_digits_par_scroll(digitCodes, srPins, wait,duration,sleepTime)

        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()
#---------------------------------------END OF PARALLEL SHIFT REGS (TWO BANKS) FUNCTIONALITY---------------------------------------------#


#---------------------------------------CHAINED SHIFT REGISTERS - SINGLE BANK FUNCTIONALITY---------------------------------------------#
    # uses a common - slow writing to multiple SRs sharing same data and clock
    def write_series_no_scroll(self, data, srclk, rclk, value, wait, sleepTime): # running 8 seg display by default without scrolling, second SR used for digit pins
        '''
        Control 8 seg in series with two shift registers without scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param rclk: Latch pin.
        :type rclk: int

        :param value: Value to write to shift register.
        :type value: String/ List[float]

        :param wait: Display time per value.
        :type wait: int

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''

        # map the value to 8-seg display format
        if type(value)==str:
            # map the value to 8-seg display format
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value
        
        srPins = [data, srclk, rclk]

        try:
            # display values
            self.write_four_digits_no_scroll(digitCodes, srPins, wait, sleepTime, default = False)
        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()

    def write_series_scroll(self, data, srclk, rclk, value, wait, duration, sleepTime): # running 8 seg display by default with scrolling, second SR used for digit pins
        '''
        Control 8 seg and other outputs parallely with two shift registers with scrolling.

        :param data: Serial data pin.
        :type data: int

        :param srclk: Clock pin.
        :type srclk: int

        :param rclk: Latch pin.
        :type rclk: int

        :param value: Value to write to shift register.
        :type value: String/ List[float]

        :param wait: Scrolling speed.
        :type wait: int

        :param duration: Scrolling speed.
        :type duration: int

        :param sleepTime: Sleep time after writing to single digit.
        :type sleepTime: int

        :return: None
        '''

        # map the value to 8-seg display format
        if type(value)==str:
            # map the value to 8-seg display format
            digitCodes = self.convert_input(value)
        else:
            digitCodes = value
            
        srPins = [data, srclk, rclk]

        try:
            # display values
            self.write_four_digits_scroll(digitCodes, srPins, wait, duration, sleepTime, default = False)
        except KeyboardInterrupt:
            # interrupt functionality
            self.board.shutdown()
#---------------------------------------END OF CHAINED SHIFT REGISTER - SINGLE BANK FUNCTIONALITY---------------------------------------------#
