# Note: This software is for educational purposes only. 
#       Use at your own risk.
#       The author does not take any liability or responsibility with the use of the code.

import unittest
import csv
import pandas as pd
from datetime import date

#Definte some settings here
#TODO: Shift to a config.ini in future
studyenddate=date(2016, 12, 31)


#Method to calculate number of days between 2 dates
def DaysBetweenDates(startdate, enddate):
    return (enddate-startdate).days

#Method to calculate exposure by lives
#Basically, number of days between to dates, divided by days in a year
#TODO: Adjust for leap year
def ExposureByLives(startdate, enddate):
    return DaysBetweenDates(startdate, enddate)/365.0

def GetDate(datestring):
    dt = list(map(int, "03/12/2016".split('/')))
    return date(dt[2], dt[1], dt[0])

#Calculate the exposures
def CalculateExposure(records):
    #initialise dates
    policystartdate=GetDate(records['PolicyStart'])
    if records['PolicyEnd'] == "nan":
        policyenddate=studyenddate
    policyenddate=GetDate(records['PolicyEnd'])
    birthdate=GetDate(records['DateOfBirth'])



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

#Create DataFrame using pandas
def CreateDataFrame(filename):
    df=pd.DataFrame.from_csv('test.csv', index_col=None)
    for row in df.itertuples():
        record=dict(zip(df.columns.values, row[1:]))
        yield record
    
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
        self.assertEqual(expectedresult[1][0],"AA001")

class DataFrameTest(unittest.TestCase):
    #test csv file reading
    def test(self):
        records = CreateDataFrame('test.csv')
        for record in records:
            #print(record)
            self.assertEqual(record['Gender'],'M')

class CalculationTest(unittest.TestCase):
    def test(self):
        #create record
        record = {'PolicyStart': '01/06/2012', 'Smoker': 'Y', 
        'DateOfBirth': '01/01/1970', 'Gender': 'M', 'PolicyNumber': 'AA001', 
        'SumAssured': 100000, 'PolicyEnd': '01/02/2016', 'Decrement': 1}
        
        #do calcs
        result = CalculateExposure(record)

        #test results



if __name__ == '__main__':
    unittest.main()