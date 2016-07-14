# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 02:29:24 2016

@author: Aaron
"""

#!/usr/bin/env python
# Line above should make the script self-executing,
# if Python has been correctly installed
import Tkinter as tk
import tkFont as tkf
import CSVreader as csvr
import checkin as CI
import newClient as NC
from math import ceil


def ClientScreen(Title, clientFile, optionsFile):
    print "Starting CYOC Check-in Application"
    # Create main window
    App = tk.Tk()
    App.geometry("%dx%d+0+0" % (App.winfo_screenwidth(), App.winfo_screenheight()))
    App.overrideredirect(1)
    #### Variables ####
    App.BoxNum = 6 # number of listboxes for names
    Ipadx, Ipady = 50, 200  # internal padding of listboxes
    Padx, Pady = 10, 10  # external padding of listboxes
    # import client data
    App.clients = csvr.readWriteRows(clientFile)
    App.clientFile = clientFile
    App.optionsFile = optionsFile
    # Formatting variables
    App.titleFont = tkf.Font(family="Helvetica",size=18,weight="bold",
                              underline=True)
#    App.titleFont.configure(underline=True)
    App.medFont = tkf.Font(family="Helvetica",size=12,weight="bold")
#    App.grid()
    App.title('Test')
    # Create display title
    App.displayTitle = tk.Label(App,
                    text='Welcome to Jackson Street\'s Albany Drop-in!')
    # Create button labeled "Quit"
    App.quitButton = tk.Button(App, text='Quit',
                                command=lambda: Quit(App))
    # Create button labeled "Begin Check-in"
    App.beginCheckinButton = tk.Button(App,
                                        text='Begin Check-in',
                                        command=lambda: beginCheckIn(App))
    # Create button labeled "Edit Profile"
    App.editButton = tk.Button(App, text="Edit Profile",
                               command=lambda: editProfile(App))
    # Create button labeled "New Client"
    App.newClientButton = tk.Button(App, text="New Client",
                                    command=lambda: newClient(App))
    # Make listboxes for names
    makeNameboxes(App)
    clmcounter = 0  # counter to help scrollbar be placed
    # Place listboxes on screen
    for box in App.nameBoxes:
        box.grid(row=1, column=clmcounter, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W,
                     ipadx=Ipadx, ipady=Ipady, padx=Padx, pady=Pady)
        clmcounter += 2
    # Place other elements on screen
    App.displayTitle.grid(row=0, column=0, columnspan=clmcounter)
    App.yScroll.grid(row=1, column=clmcounter, sticky=tk.N+tk.S)
    App.quitButton.grid(row=4, column=1, sticky=tk.S+tk.W)
    App.beginCheckinButton.grid(row=4, column=3)
    App.editButton.grid(row=4, column=0, sticky=tk.E)
    App.newClientButton.grid(row=4, column=2)
    App.bind('<Double-1>', lambda x: App.beginCheckinButton.invoke())
    # Create list of tuples of names and corresponding IDs
    showNames(App)    
    # run application loop
    App.mainloop()



def makeNameboxes(App):
    """
    Creates Num number of Listbox objects to hold the namelists.
    """
    Num = App.BoxNum
    # Create Listbox objexts
    App.nameBoxes = []
    App.nameVars = []
    # scrollbar for all nameboxes
    App.yScroll = tk.Scrollbar(App, orient="vertical", command=lambda *args: OnScroll(App, args))
    # Create Listbox objects, tied to scrollbar and listVar
    for i in range(Num):
        App.nameVars.append(tk.StringVar())
        App.nameBoxes.append(tk.Listbox(App, selectmode=tk.SINGLE,
                             yscrollcommand=App.yScroll.set, width=10,
                             listvariable=App.nameVars[i]))
    # Bind Listboxes to mousewheel scrolling
    for box in App.nameBoxes:
        box.bind("<MouseWheel>", lambda event: OnMouseWheel(App, event))


def OnScroll(App, *args):
    """Connect scrollbar to vertical view of nameboxes"""
    if args[0][0]=='scroll':
        for box in App.nameBoxes:
#            print args, args[0][1:]
            apply(box.yview_scroll, args[0][1:])
    if args[0][0]=='moveto':
        for box in App.nameBoxes:
            thing = [args[0][1]]
#            print args, thing
            apply(box.yview_moveto, thing)


def OnMouseWheel(App, event):
    """Connect mousewheel activity to scrolling in nameboxes"""
    for box in App.nameBoxes:
        print event.delta
        box.yview("scroll", -(event.delta/len(App.nameIDlist)), "units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
    return "break"


def showNames(App):
    """
    Create list of tuples of names and corresponding IDs from client database.
    Clears the Listbox and adds the list of names.
    """
    Num = App.BoxNum
    App.nameIDlist = []
    data = App.clients.data
    for ID in data:
        client = data[ID]
        last = client['Last Name'].title()
        first = client['First Name'].title()
        middle = client['Middle Name'].title()
        name = '%s, %s %s' % (last, first, middle)
        App.nameIDlist.append((name, ID))
    # Place names into list
    clearNames(App)
    insertNames(App, Num)


def insertNames(App, Num):
    """
    Populates the namebox with names of clients to click on given a \
    list of name/ID tuples [(name1, ID1), (name2, ID2)].
    """
    namesID = App.nameIDlist[:]
    namesID.sort()  # alphabetizes the master names list
    namesLists = []  # lists of namelists to be put in Listboxes
    # Split names lists into roughly equal lists to be put in listboxes
    length = int(ceil(len(namesID)/Num))
    print 'Displaying %s clients to %s lists of about %s clients each' % \
           (len(namesID), Num, length)
    for i in range(Num):
        newlist = []
        if length <= len(namesID):
            for i in range(length):
                pair = namesID[0]
                newlist.append(pair)
                namesID.remove(pair)
        if length > len(namesID):
            for pair in namesID[:]:
                newlist.append(pair)
                namesID.remove(pair)
        namesLists.append(newlist)
    # Add each list of names to each listbox
#    for nameID in namesLists[0]:
#        App.nameBoxes[0].insert(tk.END, '%s' % nameID[0])
    for i in range(Num):
        for nameID in namesLists[i]:
            App.nameBoxes[i].insert(tk.END, '%s' % nameID[0])


def clearNames(App):
    """
    Clears the list so it can be repopulated.
    """
    for box in App.nameBoxes:
        length = box.size()-1
        box.delete(0, length)


def getID(App):
    """
    Returns the ID of the name selected
    """
    for box in App.nameBoxes:
        try:
            print 'trying box ', box
            sel = box.get(box.curselection())
            print 'get box.curselection ', box.get(box.curselection())
            tupl = [pair for pair in App.nameIDlist if sel in pair]
            print 'tupl = ', tupl
            ID = tupl[0][1]
            break
        except IndexError:
            print "Try double clicking on a name"
            return
        except tk.TclError:
            print 'this box not active, moving to next box'
            continue
    return ID


def beginCheckIn(App):
    """
    Action corrsponding to Begin Check-in button on main screen.
    Finds ID from selected text, and loads question frame for client ID.
    """
    try:
        ID = getID(App)
    except UnboundLocalError:
        return
    if ID==None:
        print "ID=None"
        return
    # open the Check-in app window for the client with ID=ID
    CI.checkInScreen(App, ID)
#    showNames(App)


def editProfile(App):
    """
    Action corresponding to Edit Profile button on main screen.
    Finds ID from selected text and loads basic profile interface and data.
    """


def newClient(App):
    """
    Opens new window to enter new client information
    """
    print "Opening New Client Window"
    newClientApp = NC.newClient(App)


def Quit(App):
    password = 'LinnCounty'
    root = tk.Tk()
    pwdVar = tk.StringVar()
    pwdbox = tk.Entry(root, textvariable=pwdVar, show = '*')
    def onpwdentry(evt):
        if pwdbox.get()==password:
            App.destroy()
            root.destroy()
        else:
            pwdbox.delete(0, 'end')
    def onokclick():
        if pwdbox.get()==password:
            App.destroy()
            root.destroy()
        else:
            pwdbox.delete(0, 'end')
    tk.Label(root, text = 'Password').pack(side = 'top')

    pwdbox.pack(side = 'top')
    pwdbox.bind('<Return>', onpwdentry)
    tk.Button(root, command=onokclick, text = 'OK').pack(side = 'right')
    tk.Button(root, command=root.destroy, text = 'Cancel').pack(side = 'left')

    root.mainloop()


    '''

class NewClientScreen(tk.Tk):
    """
    Opens new window where client can add their name, date of birth, and gender.
    Saving updates the client database.
    """


class GenerateReports(tk.Tk):
    """
    Generate reports of contacts: 1) of a specific youth and what days they \
    have checked in, 2) number of total contacts for a month or year, and 3) \
    number of unique individuals that checked in in a month or year.
    """
'''
if __name__ == "__main__":
    # Questions/options file
    optionsFile = "ServicePointRequired-Options.csv"
    # Client records file
#    clientFile = "sample-CYOC-YouthDatabase.csv"
    clientFile = "CYOC-YouthDatabase.csv"
    # Instantiating the Application class
    ClientScreen('Sample Application', clientFile, optionsFile)
    
