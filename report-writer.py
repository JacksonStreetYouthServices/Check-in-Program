# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:06:19 2016

@author: Aaron
"""
import sys
import xlsxwriter as xlsx
import CSVreader as csvr
import datetime as dt
#reload(sys)
#sys.setdefaultencoding('utf8')

class report(object):
    """
    An excel workbook to display youth data for input into Microsoft Access
    and Service Point databases
    """
    def __init__(self, datafile, outputname, wsnames):
        """create a workbook and add a worksheet"""
        self.wb = xlsx.Workbook(outputname) # workbook
        self.worksheets = []
        for ws in wsnames:
            self.worksheets.append(self.wb.add_worksheet(ws)) # add Worksheets
        #import data from spreadsheet for the report
        ## get info tags for questions
        self.headers = []
        ls = csvr.readRows(datafile)[0]
        for item in ls:
            self.headers.append(item.decode('UTF-8'))
#        self.headers = csvr.readRows(datafile)[0]
        ## get data of all youth
        self.data = csvr.readWriteRows(datafile).data
        ## get list of names and IDs
        self.nameIDlist = []
        for ID in self.data:
            dic = self.data[ID]
            self.nameIDlist.append((dic['Last Name'],dic['First Name'],ID))
        ## sort the list of names alphabetially
        self.nameIDlist.sort()

    def AccessReport(self, title, titlesize=24, titlebg='#A1D490', skiprow=1):
        """input data and formatting into Access Report worksheet"""
        col = 0
        row = 0
        # title format
        titlestyle = self.wb.add_format({'bold': True, 'font_color': '#000000',
                                     'bg_color': titlebg,
                                     'font_size': titlesize})
        # write title
        ws = self.worksheets[0]
        ws.write(row, col, title, titlestyle)
        # write date of report
        row += 1
        ws.write(row, col, 'Report generated: ' + str(dt.date.today()))
        # name format
        namestyle = self.wb.add_format({'bold': True})
        # get names and attendance
        col = 0
        row = 1 + skiprow
        for nameID in self.nameIDlist:
            rowi = row
            ID = nameID[2]
            dic = self.data[ID]
            name = dic['First Name'] + dic['Middle Name'] + dic['Last Name']
            DOB = dic['Date of Birth']
            attendance = dic['Attendance']
            # write name
            ws.write(rowi, col, name, namestyle)
            # write dates of attendance
            for date in attendance:
                rowi += 1
                ws.write(rowi, col, date)
            col += 1
        

    def ServicePointReport(self, title, titlesize=24, titlebg='#C390D4'):
        """input data and formatting into Access Report worksheet"""


    def close(self):
        self.wb.close()




if __name__=="__main__":
    datafile = "CYOC-YouthDatabase.csv"
    wbname = "Youth Database Report.xlsx"
    wsnames = ["Access Report", "Service Point Report"]
    # create report instance
    thisreport =  report(datafile, wbname, wsnames)
    thisreport.AccessReport('Albany Drop-in Monthly Youth Report')
    thisreport.close()
