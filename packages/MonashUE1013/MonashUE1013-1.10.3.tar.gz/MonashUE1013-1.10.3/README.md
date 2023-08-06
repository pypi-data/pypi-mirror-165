# MonashUE1013 
MonashUE1013 is a python package that uses pymata4 to allow for specific Arduino functionality for use as part of Monash University's ENG1013 course as part of the department of Engineering. 
  
This module requires the pymata4 module with FirmataExpress installed on an associated Arduino Board. It should be included in files as:
```py
  from MonashUE1013 import MonashUE1013
```
  
## Main functionality includes 
- Setting up a 7 segment display using 1 or 2 shift registers running 1 or 2 clocks, see more information on the function parameters for specific call instructions 
- Running a 7 segment display using 1 or 2 shift registers running 1 or 2 clocks, see more information on the function parameters for specific call instructions 
- Setting up a 3V motor using a Motor driver chip, see more information on the function parameters for specific call instructions
- Running a 3V motor using a Motor driver chip, see more information on the function parameters for specific call instructions
  
## Requirements
MonashUE1013 requires `pymata4`. 

## LICENSING
  See license.txt for licencing information for this module 
