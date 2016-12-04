# Note: This software is for educational purposes only. 
#       Use at your own risk.
#       The author does not take any liability or responsibility with the use of the code.

import unittest
import csv
from datetime import date


#Method to calculate number of days between 2 dates
def DaysBetweenDates(startdate, enddate):
    return (enddate-startdate).days

#Method to calculate exposure by lives
#Basically, number of days between to dates, divided by days in a year
#TODO: Adjust for leap year
def ExposureByLives(startdate, enddate):
    return DaysBetweenDates(startdate, enddate)/365.0

#Read record from filename provided. CSV format.
def ReadRecord(filename):
    f = open(filename, 'rt')
    result=[]
    try:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            result.append(row)
    finally:
        f.close() 
    return result


#unit tests
class DateTest(unittest.TestCase):
    def test(self):
        #test dates, same year
        startdate = date(2008,8,1)
        enddate = date(2008,12,1)
        self.assertEqual(DaysBetweenDates(startdate, enddate), 122)
        self.assertEqual(ExposureByLives(startdate,enddate), 122/365.0)

        #test dates, different year
        startdate = date(2008,8,1)
        enddate = date(2009,12,1)
        self.assertEqual(DaysBetweenDates(startdate, enddate), 487)

class CSVTest(unittest.TestCase):
    #test csv file reading
    def test(self):
        expectedresult = ReadRecord('test.csv')
        self.assertEqual(expectedresult[0][0],"PolicyNumber")
        self.assertEqual(expectedresult[1][0],"A001")


if __name__ == '__main__':
    unittest.main()