# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 19:22:21 2022

@author: https://github.com/XanOpiat
@modified: YaMaSei
"""

import sys
import subprocess
import os

# Vars
missingPkgs = 0

def setup():
    global missingPkgs
    # Testing imports
    try:
        import pymem
        print(pymem.__name__)
    except ImportError:
        missingPkgs += 1

    try:
        import keyboard
        print(keyboard.__name__)
    except ImportError:
        missingPkgs += 1

    try:
        import numpy
        print(numpy.__name__)
    except ImportError:
        missingPkgs += 1
        
    try:
        import pynput
        print(pynput.__name__)
    except ImportError:
        missingPkgs += 1
        
    try:
        import win32api
        print(win32api.__name__)
    except ImportError:
        missingPkgs += 1
    try:
        import re
        print(re.__name__)
    except ImportError:
        missingPkgs += 1

    # Ask to install missing packages!
    if missingPkgs == 0:
        os.system("cls")
        print("You already installed the required packages!")
        quit(0)
    else:
        os.system("cls")
        print(f"You are missing [{missingPkgs}] packages! \n\tWould you like to install them? \n\t(Y/N)")
        installSTR = str(input("Install? > "))
        if installSTR.lower() == "y":
            os.system("cls")
            try:
                import pymem
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymem'])
            try:
                import keyboard
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'keyboard'])
            try:
                import numpy
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
            try:
                import pynput
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pynput'])
            try:
                import win32api
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])
            try:
                import re
            except ImportError:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'regex'])
            os.system("cls")
            print("Finished installing packages!")
            quit(0)
        elif installSTR.lower() == "n":
            os.system("cls")
            print("Process aborted!")
            quit(0)
        else:
            os.system("cls")
            print("Process aborted! \n\t(Y/N) Y = Yes | N = No")
            quit(0)


if __name__ == '__main__':
    setup()
else:
    print("Installer Is not allowed to be ran, by other programs!")
    quit(0)