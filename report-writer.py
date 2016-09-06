# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:06:19 2016

@author: Aaron
"""
import sys
import xlsxwriter as xlsx
import CSVreader as csvr
import datetime as dt
reload(sys)
sys.setdefaultencoding('utf8')

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
            self.headers.append(item)
        ## get data of all youth
        data = csvr.readWriteRows(datafile).data
        self.data={}
        for key in data:
            key = key.rstrip()
            self.data[key]={}
            for key2 in data[key]:
                key2 = key2.rstrip()
                self.data[key][key2]=data[key][key2].rstrip()
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
        ws.merge_range('A1:F1', title, titlestyle)
#        ws.write(row, col, title, titlestyle)
        # write date of report
        row += 1
        ws.write(row, col, 'Report generated: ' + str(dt.date.today()))
        # name format
        namestyle = self.wb.add_format({'bold': True})
        # get names and attendance
        col = 0
        row = 2 + skiprow
        for nameID in self.nameIDlist:
            rowi = row
            ID = nameID[2]
            dic = self.data[ID]
            name = dic['First Name'] +' '+ dic['Middle Name'] +' '+ dic['Last Name']
            DOB = dic['Date of Birth']
            attendance = dic['Attendance'].strip('[').strip(']').split(', ')
            # write name
            ws.write(rowi, col, name, namestyle)
            rowi += 1
            # write 'Date of Birth'
            ws.write(rowi, col, 'Date of Birth:')
            rowi += 1
            # write DOB
            ws.write(rowi, col, DOB)
            rowi += 1
            # write 'Attendance'
            ws.write(rowi, col, 'Attendance:')
            # write dates of attendance
            for date in attendance:
                rowi += 1
                ws.write(rowi, col, date.strip("'"))
            col += 1
        ws.set_column(0, col, 21)


    def ServicePointReport(self, title, titlesize=24, titlebg='#C390D4',
                           skiprow=1, verbose=False):
        """input data and formatting into Access Report worksheet"""
        col = 0
        row = 0
        headers = self.headers
        headers.remove('First Name')
        headers.remove('Middle Name')
        headers.remove('Last Name')
        headers.remove('Attendance')
        # title format
        titlestyle = self.wb.add_format({'bold': True, 'font_color': '#000000',
                                     'bg_color': titlebg,
                                     'font_size': titlesize})
        # write title
        ws = self.worksheets[1]
        ws.merge_range('A1:F1', title, titlestyle)
#        ws.write(row, col, title, titlestyle)
        # write date of report
        row += 1
        ws.write(row, col, 'Report generated: ' + str(dt.date.today()))
        row += 1
        ws.write(row, col, 'Only youth who have answered all required'\
                            ' questions are shown here')
        row += 1
        # name format
        namestyle = self.wb.add_format({'bold': True})
        # get names and attendance
        col = 0
        row += skiprow
        for nameID in self.nameIDlist:
            rowi = row
            ID = nameID[2]
            if self.checkComplete(ID):
                if verbose: print '\nID: %s complete. Writing ID information to report' % ID
                dic = self.data[ID]
                name = dic['First Name'] +' '+ dic['Middle Name'] +' '+ dic['Last Name']
                DOB = dic['Date of Birth']
                attendance = self.stripAttendance(dic['Attendance'])
                # write name
                if verbose: print name
                ws.write(rowi, col, name, namestyle)
                rowi += 1
                # write Service Point questions and answers
                ## style for SP questions
                if col % 2 == 0: bgcolor = '#006666'
                if col % 2 == 1: bgcolor = '#800000'
                queststyle = self.wb.add_format({'bold': True, 'font_color': '#FFFFFF',
                                     'bg_color': bgcolor})
                for key in headers:
                    if verbose: print key, ': ', dic[key]
                    ws.write(rowi, col, key, queststyle)
                    rowi += 1
                    ws.write(rowi, col, dic[key])
                    rowi += 1
                # write 'Attendance'
                if verbose: print 'Attendance: ', attendance
                ws.write(rowi, col, 'Attendance:', queststyle)
                # write dates of attendance
                for date in attendance:
                    rowi += 1
                    ws.write(rowi, col, date)
              
                col += 1
        ws.set_column(0, col, 35)

    def stripAttendance(self, attendance):
        """takes the attendance string, and converts it to a list of strings"""
        attendance = attendance.strip('[').strip(']').split(', ')
        newList = []
        for date in attendance:
            newList.append(date.strip("'"))
        return newList

    def checkComplete(self, ID):
        """checks to see if all needed information for Service Point is present"""
        dic = self.data[ID]
        complete = 1
        for key in dic:
            if dic[key]=='':
                complete = 0
                if key == 'Middle Name':
                    complete = 1
            if complete == 0:
                return False
        if complete == 1:
            return True
                

    def close(self):
        self.wb.close()




if __name__=="__main__":
    datafile = "CYOC-YouthDatabase.csv"
    date = str(dt.date.today())
    wbname = "Youth Database Report %s.xlsx" % date
    wsnames = ["Access Report", "Service Point Report"]
    # create report instance
    thisreport =  report(datafile, wbname, wsnames)
    thisreport.AccessReport('ACCESS: Albany Drop-in Monthly Youth Report')
    thisreport.ServicePointReport('SERVICE POINT: Albany Drop-in Monthly Youth Report',
                                  verbose=True)
    thisreport.close()
    print '\nopen report under %s' % wbname
