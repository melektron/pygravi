"""
ELEKTRON (c) 2022
Written by melektron (Matteo Reiter)
www.elektron.work
02.05.22 20:20

Microsecond delay function that works on Windows, Linux and OSX.
Windows implementation was adopted from the GS_timing.py file
by By Gabriel Staples from http://www.ElectricRCAircraftGuy.com.
His code: https://github.com/ElectricRCAircraftGuy/eRCaGuy_PyTime/

This file only contains a microsecond delay function (usleep) and not any
of the other functions provided by GS_timing.py for Windows and Linux.

The usleep() function does however work for Windows, Linux and OSX.
"""

import platform
import ctypes

plat = platform.system().lower()
if plat.startswith("windows"):
    """ The following code is copied from GS_timing.py"""
    def micros():
        "return a timestamp in microseconds (us)"
        tics = ctypes.c_int64() #use *signed* 64-bit variables; see the "QuadPart" variable here: https://msdn.microsoft.com/en-us/library/windows/desktop/aa383713(v=vs.85).aspx 
        freq = ctypes.c_int64()

        #get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics)) 
        #get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))  
        
        t_us = tics.value*1e6/freq.value
        return t_us
    
    #Private module function
    #-see here for use of underscore to make "module private": http://stackoverflow.com/questions/1547145/defining-private-module-functions-in-python/1547160#1547160
    #-see here for example of constrain function: http://stackoverflow.com/questions/34837677/a-pythonic-way-to-write-a-constrain-function/34837691
    def _constrain(val, min_val, max_val):
        "constrain a number to be >= min_val and <= max_val"
        if (val < min_val): 
            val = min_val
        elif (val > max_val): 
            val = max_val
        return val
    
    # renamed from delayMicroseconds to usleep
    def usleep(delay_us: int):
        "delay for delay_us microseconds (us)"
        #constrain the commanded delay time to be within valid C type uint32_t limits 
        delay_us = _constrain(delay_us, 0, (1<<32)-1)
        t_start = micros()
        while ((micros() - t_start)%(1<<32) < delay_us): #use modulus to force C uint32_t-like underflow behavior
            pass #do nothing 
        return 

elif plat.startswith("linux"):
    libc = ctypes.CDLL("libc.so.6") # linux c standard library is contained in shared objects file libc.so.6

    def usleep(delay_us: int):
        "delay for delay_us microseconds (us)"
        libc.usleep(ctypes.c_int(int(delay_us)))
    
elif plat.startswith("darwin"):
    libc = ctypes.CDLL("libSystem.dylib")   # macos c standard library is contained in dynamic library libSystem.dylib
    
    def usleep(delay_us: int):
        "delay for delay_us microseconds (us)"
        libc.usleep(ctypes.c_int(int(delay_us)))