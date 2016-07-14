# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:43:57 2016

@author: Aaron
"""
import Tkinter as tk
import CSVreader as csvr
from CYOC_data_entry import CYOC_questions as quest
import numpy as np
import datetime as dt
from dateutil.parser import parse as dpp
import CYOC_GUI4 as gui


def newClient(App):
    """
    This creates a new window and app that asks for a new client's name and DOB
    It saves the client info to the
    Upon closing, it opens a new instance of the CYOC GUI.
    """
    subApp = tk.Toplevel(master=App)
    subApp.grid()
    # Create Widget
    createQuestionsWidget(App, subApp)

        
        
def createQuestionsWidget(App, subApp):
    """
    stuff
    """
    # create variables lists
    subApp.name_vars = []
    subApp.name_entrys = []
    subApp.name_labels = []
    subApp.name_labeltext = ['First Name', 'Middle Name', 'Last Name']
    subApp.date = tk.StringVar()
    i = 0
    rowi=0
    # Create and show label for title of New Client, Add title to window
    subApp.title('New Client')
    subApp.title = tk.Label(subApp, text='New Client')
    subApp.title.grid(row=rowi, columnspan=len(subApp.name_labeltext))
    rowi += 1
    # Create variable, entrys, and labels for name
    for name in subApp.name_labeltext:
        # make label for names and show it
        subApp.name_labels.append(tk.Label(subApp, text=subApp.name_labeltext[i]))
        subApp.name_labels[-1].grid(row=rowi, column=i, ipady=10, sticky=tk.S)
        # make StringVars
        subApp.name_vars.append(tk.StringVar())
        # make name Entrys and show it
        subApp.name_entrys.append(tk.Entry(subApp, 
                                textvariable=subApp.name_vars[-1]))
        subApp.name_entrys[-1].grid(row=rowi+1, column=i)
        i += 1
    rowi += 2
    # Create label, variable, and entry for Date of Birth
    ## labels
    subApp.monthLabel = tk.Label(subApp, text='Month')
    subApp.monthLabel.grid(row=rowi, column=0)
    subApp.dayLabel = tk.Label(subApp, text='Day')
    subApp.dayLabel.grid(row=rowi, column=1)
    subApp.yearLabel = tk.Label(subApp, text='Year')
    subApp.yearLabel.grid(row=rowi, column=2)
    rowi += 1
    ## month listbox
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
              'Sep', 'Oct', 'Nov', 'Dec']
    subApp.monthDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    subApp.monthVar = tk.StringVar(master=subApp)
    subApp.monthList = tk.OptionMenu(subApp, subApp.monthVar, *months) 
    subApp.monthList.grid(row=rowi, column=0)
    ## day listbox
    days = range(1,32)
    subApp.dayVar = tk.StringVar(master=subApp)
    subApp.dayList = tk.OptionMenu(subApp, subApp.dayVar, *days) 
    subApp.dayList.grid(row=rowi, column=1)
    ## year listbox
    currentYear = dt.date.today().year
    years = range(currentYear-25, currentYear)
    subApp.yearVar = tk.StringVar(master=subApp)
    subApp.yearList = tk.OptionMenu(subApp, subApp.yearVar, *years)
    subApp.yearList.grid(row=rowi, column=2)
    ## inscrease row counter
    rowi+=1
    


    

#        print subApp.name_vars[0].get()
    
    # Blank row
#        blank1 = tk.Label(self)
#        blank1.grid(row=rowi)
#        rowi += 1
    rowi += 1
    # Create and show Cancel/MainScree  Button
    subApp.mainScreenButton = tk.Button(subApp, text='Cancel',
                                        command=lambda: mainScreen(subApp))
    subApp.mainScreenButton.grid(row=rowi, column=0, pady=10)
    # Create and show Finish Check-in Button
    subApp.saveButton = tk.Button(subApp, text='Save Check-in',
                                 command=lambda: submitClientInfo(App, subApp))
    subApp.saveButton.grid(row=rowi, column=2, pady=10)
    # change tab order
    subApp.saveButton.lower()
    subApp.mainScreenButton.lower()



        
def mainScreen(subApp):
    """Return to main screen without saving"""
    print 'Returning to main screen without saving changes.'
    # open clientScreen
#        ClientScreen(clientFile)
    # close checkInScreen
    subApp.destroy()

def newID(App):
    """
    Reads the IDs that exist, strips the CYOC off, the finds the highest ID
    Returns a new ID, which is one integer higher than the previous largest ID
    """
    # build list of client IDs
    idlist = App.clients.data.keys()
    nums = []
    # build list of ID numbers
    for ID in idlist:
        try:
            nums.append(int(ID.strip('cyoc')))
        except ValueError:
            print 'oh no! ID misunderstood ', ID
    # find highest number
    nums.sort()
    highid = nums[-1]
    # add one to the highest number
    newid = highid + 1
    # return new ID number with leading zeros on the number
    return 'cyoc%04d' % (newid)

def submitClientInfo(App, subApp):
    """
    Saves new client info to csv, closes Checkin app, and returns to \
    client screen.
    """
    # convert Date of Birth entries to usable format if DOB is filled out
    if subApp.monthVar.get() != '' and subApp.dayVar.get() != '' and \
    subApp.yearVar.get() != '':
        s = ''
        mylist= [subApp.monthDict[subApp.monthVar.get()], '/', subApp.dayVar.get(),
                 '/', subApp.yearVar.get()]
        for item in mylist:
            s += str(item)
        subApp.date.set(s)
    # get new ID
    ID = newID(App)
    # get First, Middle, Last name from string variables attached to boxes
    names = []
    for var in subApp.name_vars:
        names.append(var.get())
    # get date
    date = subApp.date.get()
    # save client info dictionary to file
    App.clients.add_new_client(ID, {'ID':ID,
                                        'First Name': names[0],
                                        'Middle Name': names[1],
                                        'Last Name': names[2],
                                        'Date of Birth': date})
    App.clients.save()
    # refresh name boxes
    gui.showNames(App)
    # open clientScreen
#        ClientScreen(clientFile)
    # close CheckIn app
    subApp.destroy()

if __name__=="__main__":
    # Questions/options file
#    optionsFile = "ServicePointRequired-Options.csv"
    # Client records file
    clientFile = "sample-CYOC-YouthDatabase.csv"
    # Instantiating the Application class
    ID = 'CYOC0001'
    app = newClient(clientFile, ID)
    app.mainloop()