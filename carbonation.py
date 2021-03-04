#!/usr/bin/env python3

### Implementation of idea presented by BevSense @ beveragesensors.com
### https://www.beveragesensors.com/wp-content/uploads/bevsense-methods-of-analysis-for-correcting-co2-content.pdf

import sys
from enum import Enum
from colorama import init, Fore, Back, Style

PSI_LOW = 1
PSI_HIGH = 35
TMP_LOW = 30
TMP_HIGH = 50 

class UNITS(Enum):
    F = 1
    C = 2

current_unit = UNITS.C
#current_unit = UNITS.F

def units_convert(temperature):
    if current_unit == UNITS.F:
        return temperature
    else:
        return (temperature - 32) * (5/9)


def units_ending():
    if current_unit == UNITS.F:
        return "F" 
    else:
        return "C" 
    

def color_volumes(volume):
   if volume < 1.40:
        print(Back.BLUE, end = '') 
   elif volume < 1.50:
        print(Back.CYAN, end = '') 
   elif volume < 2.20:
        print(Back.WHITE, end = '') 
   elif volume < 2.60:
        print(Back.GREEN, end = '') 
   elif volume < 4.0:
        print(Back.YELLOW, end = '') 
   elif volume < 6.0:
        print(Back.RED, end = '') 
        

def pressure_calc(SpecificGravity, percentByWeightAlcohol):
    ETHANOL_DENSITY = .789  # g/ml
    HENRYS_EXPERIMENTAL = 5.16  # ??
    TEMP_ADJ = 12.4  # ???:

    ALTITUDE_PSIA = 12  # 5280 feet
    #ALTITUDE_PSIA = 14.7  # sea level 

    init()  # colorama

    print(Fore.BLACK + Back.WHITE)
    print("")

    print("{:>26s}      atm@{:3.3f} psi     SG = {:4.3f}     %alc = {:2.1f}".format("CO2 Volume Chart", ALTITUDE_PSIA, SpecificGravity, percentByWeightAlcohol*100))
    print("")

    print("          ", end = '')
    for psi in range(PSI_LOW, PSI_HIGH, 1):
        print("[{:3d}]".format(psi), end = '')
    print("")

    for temperature in range(TMP_LOW, TMP_HIGH + 1, 1):

        
        print(" [{:>5.1f}{:1s}] ".format(units_convert(temperature), units_ending()), end = '')

        for psi in range(PSI_LOW, PSI_HIGH, 1):
            
            volumes = HENRYS_EXPERIMENTAL * (psi + ALTITUDE_PSIA) / \
                    (temperature + TEMP_ADJ) * SpecificGravity * (1 + (percentByWeightAlcohol/ETHANOL_DENSITY))
            
            # Standard chart
            # volumes = 4.85 * (psi + 14.7) / (temperature + TEMP_ADJ)
            color_volumes(volumes)
            if volumes < 6.0 and volumes >= 1.0:
                print("{:3.2f} ".format(volumes), end = '')
            else:
                #print("{:3.3s} ".format(" X   "), end = '')
                print(" X   ", end = '')

        print(Back.WHITE) 
    print("")
    print("")
    print("")

specific_gravity = None
percent_alcohol = None

# main
if len(sys.argv) != 3:
    print("Usage carbonation <SG> <%alc>") 
    sys.exit(0)
else:
    specific_gravity = float(sys.argv[1])
    percent_alcohol = float(sys.argv[2]) / 100.0
    
#pressure_calc(1.012, .06)
pressure_calc(specific_gravity, percent_alcohol)
