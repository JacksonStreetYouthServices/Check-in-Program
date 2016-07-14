# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 05:06:03 2016

@author: Aaron
"""

import Tkinter as tk
import tkFont
import datetime as dt
from CYOC_data_entry import CYOC_questions
import CYOC_GUI4 as gui
import ast




def checkInScreen(App, ID):
    """
    This is a new window that opens for a check-in for a specific youth.
    After they click their name and Begin Check-in on the main client screen, \
    this new window opens to confirm the spelling of their first, middle, and \
    last names and asks them one of the questions that they have not answered \
    yet.
    On saving, the app updates their name and answer to the question to the \
    client database.
    On closing, no information is updated, and the main client screen should \
    be open.
    """
    subApp = tk.Toplevel(master=App)
    subApp.ID = ID
    # create instance of CYOC questions class
    subApp.questions = CYOC_questions(App.optionsFile, App.clientFile)
    subApp.grid()
    # Create Widget
    createQuestionsWidget(App, subApp)
    
    
def createQuestionsWidget(App, subApp):
    """
    stuff
    """
    # namelist = [First, Middle, Last], questionKey=key to the question in the
    # dictionary of question options.
    namelist, subApp.questionKey = loadClientInfo(App, subApp)
    # get full question text and the associated options
    (question, options) = subApp.questions.ask_question(subApp.questionKey)
    print 'Question: %s' % question
    # create variables/widget lists
    subApp.name_vars = []
    subApp.name_entrys = []
    subApp.name_labels = []
    # labels for name entry boxes
    subApp.name_labeltext = ['First Name', 'Middle Name', 'Last Name']
    i = 0
    # Create variable, entrys, and labels for client's name
    for name in namelist:
        # make StringVar
        subApp.name_vars.append(tk.StringVar(value=name, master=subApp))
        # make Entry and show it
        subApp.name_entrys.append(tk.Entry(subApp, 
                                textvariable=subApp.name_vars[-1]))
        subApp.name_entrys[-1].grid(row=2, column=i)
        # make label for name and show it
        subApp.name_labels.append(tk.Label(subApp, text=subApp.name_labeltext[i]))
        subApp.name_labels[-1].grid(row=1, column=i)
        i += 1
    rowi=3  # row counter variable
    # Add title to window
    subApp.title('Check-in for '+namelist[0]+' '+namelist[2])
    # Please answer below label:
    subApp.PAB = tk.Label(subApp, text='Please Answer Below:\n', font=App.titleFont)
    subApp.PAB.grid(row=rowi, columnspan=3, sticky=tk.W)
    rowi += 1
    # Create and show label for question
    subApp.Q = tk.Label(subApp, text=question, font=App.medFont)
    subApp.Q.grid(row=rowi, column=0, columnspan=3)
    rowi += 1
    # Create variable for answer to question
    subApp.answer = tk.StringVar(master=subApp)
    # Create list to hold Radiobutton objects
    subApp.buttonlist = []
    # if the question is Date of Birth, then create drop-down menues with the
    # appropraite options
    if question == 'Date of Birth':
        DOB = App.clients.data[subApp.ID]['Date of Birth']
        print DOB
#            self.CIdobVar = tk.StringVar(master=self)
        # labels for day, month, year
        subApp.monthLabel = tk.Label(subApp, text='Month')
        subApp.monthLabel.grid(row=rowi, column=0)
        subApp.dayLabel = tk.Label(subApp, text='Day')
        subApp.dayLabel.grid(row=rowi, column=1)
        subApp.yearLabel = tk.Label(subApp, text='Year')
        subApp.yearLabel.grid(row=rowi, column=2)
        rowi += 1
        # month listbox
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                  'Sep', 'Oct', 'Nov', 'Dec']
        subApp.monthDict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        subApp.monthVar = tk.StringVar(master=subApp)
        subApp.monthList = tk.OptionMenu(subApp, subApp.monthVar, *months) 
        subApp.monthList.grid(row=rowi, column=0)
        # day listbox
        days = range(1,32)
        subApp.dayVar = tk.StringVar(master=subApp)
        subApp.dayList = tk.OptionMenu(subApp, subApp.dayVar, *days) 
        subApp.dayList.grid(row=rowi, column=1)
        # year listbox
        currentYear = dt.date.today().year
        years = range(currentYear-25, currentYear)
        subApp.yearVar = tk.StringVar(master=subApp)
        subApp.yearList = tk.OptionMenu(subApp, subApp.yearVar, *years) 
        subApp.yearList.grid(row=rowi, column=2)
        # inscrease row counter
        rowi+=1
        # Create and show Finish Check-in Button
        subApp.checkinButton = tk.Button(subApp, text='Save Check-in',
                                         command=lambda: setDate(App, subApp))
        subApp.checkinButton.grid(row=rowi+1, column=2)
    else:
        # Create radio buttons for options in question if not Date of Birth
        for value in options:
            # create and show radio buttons for all options
            subApp.buttonlist.append(tk.Radiobutton(subApp, text=value,
                                    variable=subApp.answer, value=value))
            subApp.buttonlist[-1].grid(row=rowi, column=0, columnspan=3, sticky=tk.W)
            rowi += 1
        # Create and show Finish Check-in Button
        subApp.checkinButton = tk.Button(subApp, text='Save Check-in',
                                     command=lambda: submitClientInfo(App, subApp))
        subApp.checkinButton.grid(row=rowi+1, column=2)
    # Create label to show answer
    subApp.label = tk.Label(subApp, textvariable=subApp.answer)
    subApp.label.grid(row=rowi)
    rowi += 1
    # Create and show Cancel/MainScree  Button
    subApp.mainScreenButton = tk.Button(subApp, text='Cancel',
                                        command=lambda: mainScreen(subApp))
    subApp.mainScreenButton.grid(row=rowi, column=0)
    
    name = ''
    for var in subApp.name_vars:
        name += var.get()+' '
    print 'Displaying question for %s' % name


def setDate(App, subApp):
    if subApp.monthVar.get() == '' or subApp.dayVar.get() == '' or\
    subApp.yearVar.get() == '':
        subApp.answer.set('')
    else:
        s = ''
        mylist= [subApp.monthDict[subApp.monthVar.get()], '/', subApp.dayVar.get(),
                 '/', subApp.yearVar.get()]
        for item in mylist:
            s += str(item)
        subApp.answer.set(s)
    submitClientInfo(App, subApp)


def loadClientInfo(App, subApp):
    """
    Return namelist and questionKey
    namelist is a list of the client's first, middle, and last names.
    questionKey is the key for the appropriate question in the question dict.
    """
    clientDict = App.clients.data
    client = clientDict[subApp.ID]
    namelist = [client['First Name'], client['Middle Name'], client['Last Name']]
    questionKey = subApp.questions.which_question(subApp.ID)
    return namelist, questionKey


def mainScreen(subApp):
    """Return to main screen without saving"""
    print 'Returning to main screen without saving changes.'
    # open clientScreen
#        ClientScreen(clientFile)
    # close checkInScreen
    subApp.destroy()


def submitClientInfo(App, subApp):
    """
    Saves new client info to csv, closes Checkin app, and returns to \
    client screen.
    """
    print 'answer to question: ', subApp.answer.get()
    # save client info to dictionary
    App.clients.update_client_answer(subApp.ID, subApp.questionKey,
                                     subApp.answer.get())
    # save client names to dictionary
    i = 0
    for var in subApp.name_vars:
        App.clients.update_client_answer(subApp.ID, subApp.name_labeltext[i],
                                         var.get())
        i += 1
    # append date of check-in to attendance list in dictionary
    date = str(dt.date.today().month) + '/' + str(dt.date.today().day) + '/' +\
           str(dt.date.today().year)
    # If attendance list for client is empty, add date
    datelist = App.clients.data[subApp.ID]['Attendance']
    print 'attendance list: ', datelist
    if datelist == '':
        print 'datelist empty: ', datelist
        datelist = [date]
    # If attendance list for client has today's date already in it, keep the
    # list the same
    else:
        if type(datelist) is str:
            datelist = ast.literal_eval(datelist)
        if date in datelist:
            print 'datelist has today: ', datelist
        # If attendance list for client has other dates, append today's date
        else:
            print 'appending todays date %s to datelist ' % date, datelist
            datelist.append(date)
            print 'datelist: ', datelist
    # Update client dictionary with attendance list
    App.clients.update_client_answer(subApp.ID, 'Attendance', datelist)
    # save overwrite file with current client dictionary
    App.clients.save()
#    App.namebox.delete(0, len(App.clients.data)-1)
    gui.showNames(App)
    # open clientScreen
#        ClientScreen(self.clientFile, self.optionsFile)
    # close CheckIn app
    subApp.destroy()

if __name__ == "__main__":
    # Questions/options file
    optionsFile = "ServicePointRequired-Options.csv"
    # Client records file
    clientFile = "sample-CYOC-YouthDatabase.csv"
    ID = 'CYOC0004'
    app = checkInScreen(clientFile, optionsFile)
    app.mainloop()
