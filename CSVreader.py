# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 03:53:07 2015

@author: Aaron
"""

import csv

#variables



def readRows(Myfile):
    """read a csv file and return its rows in a list of rows."""
    data = []
    with open(Myfile, 'rb') as csvfile:
        data1 = csv.reader(csvfile, delimiter=',')
        for row in data1:
            data.append(row)
    return data
    
def readCols(Myfile, method='rb'):
    """read a csv file and return its columns in a dict of columns (the headers are the keys)."""
    data = []
    dic = {}
    with open(Myfile, method) as csvfile:
        data1 = csv.reader(csvfile, delimiter=',')
        for row in data1:
            data.append(row)
            
    trans= zip(*data) #transpose of data - row-to=column operation
    for col in trans:
        dic[col[0]]=list(col[1:])
    return dic

def lineToRead(myFile, recordNum, args):
    Dic = readCols(myFile)
    myList = []
    for key in args:
        myList.append(Dic[key][recordNum])
    return myList

class readWriteCols(object):
    
    def __init__(self, MyFile):
        self.data = readCols(MyFile)
        self.file = MyFile
        self.firstNameKey = 'First Name'
        self.lastNameKey = 'Last Name'
        
    
    def save(self):
        """Earases old file and writes new data"""
        print('writing data to file')
        with open(self.file, 'r+') as f:
            f.write(self.data)
        
    
    def pull_info(self,firstName, lastName):
        """dumps info about client from self.data into a dictionary for that client"""
        record = {}
        try: a,b = self.data[self.firstNameKey],self.data[self.lastNameKey]
        except KeyError: print('first and/or lastname key incorrect--change \
        name keys used to search by redefining self.firstNameKey or self.lastNameKey')
        alst = [i for i,x in enumerate(a)  if x==firstName]
        blst = [i for i,x in enumerate(b)  if x==lastName]
        [i]=[i for i, j in zip(alst, blst) if i == j]
        
        for key in self.data.keys():
            record[key] = self.data[key][i]
        return record
        
    def update_client_record(self, dict):
        """writes info from input dict to self.data dict\
        make sure to have matching keys"""
#        for key in self.data.keys():
#            try: 
#                self.data
        

class readWriteRows(object):
    """
    Take a CSV file name
    readWriteRows.data returns a dictionary like:
      {x01: {header1: x01, header2: x11, header3: x21},
       x02: {header1: x02, header2: x12, header3: x22}}
    """
    
    def __init__(self, MyFile):
        self.rawData = readRows(MyFile)
        self.headers = self.rawData[0]
        self.data = {}
        self.file = MyFile
        self.firstNameKey = 'First Name'
        self.lastNameKey = 'Last Name'
        for row in self.rawData[1:]:
            i=0
            dic = {}
            for entry in row:
                dic[self.headers[i]] = entry
                i+=1
            self.data[row[0]] = dic
        
        
    def print_all(self):
        """prints file"""
        for key in self.data:
            print('\n ID = %s'%key)
            print(self.data[key])
    
        
    
    def pull_ID_info(self,ID):
        """dumps info about client from self.data into a dictionary for that client"""
        print '\n info on ID ',ID,self.data[ID]
        
    def update_client_answer(self, ID, key, answer):
        """writes status to the key in a particular ID record
        ID of the client, key=information type, status=answer to information type"""
        
        print '\n writing %s=%s to %s record'%(key,answer,ID)
        self.data[ID][key] = answer
        
    def update_client_answers(self, ID, dic):
        """writes answers to questions in a particular ID record
        ID of the client, dic={keys of questions: client's anwers}"""
        print '\n writing ', dic, ' to local record of ', ID
        for key in dic:
            self.data[ID][key] = dic[key]
    
    def add_new_client(self, ID, dic):
        """
        Adds a new record to the dictionary that will be saved
        {ID: {dictionary of info}}
        """
        # check if the ID is already in use
        try:
            if self.data[ID]:
                # if already in use, print and exit
                print "ID already in dictionary, ID: %s" % ID
                print "Exiting without adding new client"
        # if not in use, add to dictionary
        except KeyError:
                self.data[ID] = dic
                print 'adding record to dictionary \n %s: %s' %(ID, dic)
            
            
            
    def save(self):
        """Earases old file and writes new data"""
        print('\n writing data to file')
        with open(self.file, 'wb') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            for key in self.data:
#                print 'writing this: ',self.data[key]
                writer.writerow(self.data[key])
    
    



#print dic['NameFirst'][0]
#NameLast
#Nickname
#FirstEncounterAge
#FirstEncounterDate
#GenderID
    
if __name__ == "__main__":
    myFile = 'CYOC/sample-CYOC-YouthDatabase - Copy.csv'
    sample = readWriteRows(myFile)
    print sample.data['CYOC0001']['Middle Name']
    sample.update_client_answer('CYOC0001','Middle Name', 'Jake')
    sample.save()
    print sample.data['CYOC0001']['Middle Name']
#    SOdata = readWriteRows(myFile)
#    SOdata.print_all()
#    steveDic={'Mental Health Status':'Good', \
#    'Formerly a Ward of Juvenile Justice System': 'Yes',\
#    'Last Grade Completed': 'Some College', \
#    'Dental Health Status': 'Good', \
#    'General Health Status': 'Good'}
##    SOdata.update_client_answers('0002',steveDic)
##    SOdata.update_client_answer('0002', 'Sexual Orientation', 
#                                'Data not collected')
#    SOdata.save()
    

    
