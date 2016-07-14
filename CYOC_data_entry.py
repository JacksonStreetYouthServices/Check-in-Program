# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 10:20:36 2015

@author: Aaron
"""

import CSVreader as csvr
import random




class CYOC_questions():
    """
    Takes an optionsFile to build a questions dict used in CYOC check-in GUI.
    CYOC_data_strut.clients.data returns a dict of dicts of client data.
    {'ID number': {'infotype': 'info', 'infotype': 'info'}, 'ID number': {...}}
    """
    def __init__(self, optionsFile, clientFile):
        self.options = csvr.readCols(optionsFile) #list of options for the questions
        for key in self.options.keys():    #stripping empty entries from list of options
            self.options[key] = filter(None, self.options[key])
        self.clients = csvr.readWriteRows(clientFile)
        self.currentClientID = ''
        
        
    def ask_question(self, questionKey):
        """based on the questionKey provide, this prompts the user with a
        question, records the answer, and updates client's record.
        This must match the header in the options file."""
#        print(question)
#        print('ID  Option')
        Ops = self.options[questionKey]
#        numbered = enumerate(Ops)
#        for option in numbered:
#            print option[0],' ',option[1]
#        answer = int(raw_input('\n Please enter the ID of your answer:'))
#        print('Thank you for your input! Updating file...')
        
#        
#        self.clients.update_client_answer(ID,questionKey,O[answer])
#        self.clients.save()
        return questionKey, Ops

    def which_question(self, ID):
        """
        Returns a question that has not been answered.
        If all have answers, returns a random question.
        """
        client = self.clients.data[ID]
        ask = []
        for question in client:
            if question != 'Last Name' and question != 'Middle Name' and\
               question != 'First Name' and question !='ID' and\
               question != 'Gender' and question != 'Age' and\
               question != 'Attendance':
#                print question
                if client[question] == '':
                    ask.append(question)
#        print 'missing question: ', ask
        if ask == []:
            ask.append(random.choice(self.options.keys()))
        return random.choice(ask)




if __name__ == "__main__":
    optionsFile = "ServicePointRequired-Options.csv"
    CYOC = CYOC_questions(optionsFile)
    clientList = csvr.readWriteRows(clientFile).data
    nameList = []
    for key in clientList:
        name = clientList[key]['Last Name'] + ', ' +\
               clientList[key]['First Name'] + ' ' + 'MiddleName'
        print(name)
        nameList.append(name)
#    print CYOC.options['Sexual Orientation']
    print [CYOC.which_question('CYOC0002')]
#    CYOC.ask_question('0002','Sexual Orientation')

    
    
    