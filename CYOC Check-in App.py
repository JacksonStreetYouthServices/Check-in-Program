# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 11:44:13 2016

@author: Aaron
"""
import os

try:
    from CheckInProgram import CYOC_GUI4 as gui
except ImportError:
    import CYOC_GUI4 as gui

if __name__ == "__main__":
    currentdir = os.path.dirname(__file__)
    # Questions/options file
    optionsFile = currentdir+"\CheckInProgram\ServicePointRequired-Options.csv"
    # Client records file
#    clientFile = "sample-CYOC-YouthDatabase.csv"
    clientFile = currentdir+"\CheckInProgram\CYOC-YouthDatabase.csv"
    # Instantiating the Application class
    gui.ClientScreen('Sample Application', clientFile, optionsFile)
    