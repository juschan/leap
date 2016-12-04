# Note: This software is for educational purposes only. 
#       Use at your own risk.
#       The author does not take any liability or responsibility with the use of the code.

import unittest
import csv
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

#Definte some settings here
#TODO: Shift to a config.ini in future
studyenddate=date(2016, 12, 31)


#Method to calculate number of days between 2 dates
def DaysBetweenDates(startdate, enddate):
    return (enddate-startdate).days

#Method to calculate complete years betwen 2 dates
def YearsBetweenDates(startdate, enddate):
    return relativedelta(enddate, startdate).years

#Method to calculate exposure by lives
#Basically, number of days between to dates, divided by days in a year
#TODO: Adjust for leap year
def ExposureByLives(startdate, enddate):
    return DaysBetweenDates(startdate, enddate)/365.0

def GetDate(datestring):
    dt = list(map(int, datestring.split('/')))
    return date(dt[2], dt[1], dt[0])
    
#calculate the dates leading to change in age, calendar year and duration
def CreatePeriods(startdate, enddate, birthdate):
    nextdate=startdate
    result = [startdate]
    while nextdate != enddate:
        policyanniversary = date(nextdate.year+1, startdate.month, startdate.day)
        #print(policyanniversary)
        newyear=date(nextdate.year+1, 1, 1)

        currentyearbirthday = date(nextdate.year, birthdate.month, birthdate.day)
        
        #TODO: Make refactor in future
        if(currentyearbirthday < policyanniversary):
            currentyearbirthday = date(nextdate.year+1, birthdate.month, birthdate.day)
            
            if(enddate>newyear):
                result.append(newyear)
            else:
                result.append(enddate)
                return result
            if(enddate>currentyearbirthday): 
                result.append(currentyearbirthday)
            else:
                result.append(enddate)
                return result
            if(enddate>policyanniversary):
                result.append(policyanniversary)
            else:
                result.append(enddate)
                return result
        else:
            if(enddate>currentyearbirthday): 
                result.append(currentyearbirthday)
            else:
                result.append(enddate)
                return result
            if(enddate>newyear):
                result.append(newyear)
            else:
                result.append(enddate)
                return result
            if(enddate>policyanniversary):
                result.append(policyanniversary)
                return result
            else:
                result.append(enddate)
    
        nextdate=policyanniversary
    
    return result

#Calculate the exposures
def CalculateExposure(record):
    #initialise dates
    policystartdate=GetDate(record['PolicyStart'])
    if record['PolicyEnd'] == "nan":
        policyenddate=studyenddate
    policyenddate=GetDate(record['PolicyEnd'])
    birthdate=GetDate(record['DateOfBirth'])

    #calculate the various dates that change age/calendar year/duration in a list
    periods = CreatePeriods(policystartdate, policyenddate, birthdate)

    result=[]
    lastdate=None
    #iterate through all periods
    for dt in periods:
        if (lastdate==None):
            lastdate = dt
            continue;    
        
        #for each period, store the exposure by lives and amounts with 
        #age(last birthday), calendar year and duration
        age= YearsBetweenDates(birthdate, dt)
        calendaryear=lastdate.year
        duration=YearsBetweenDates(policystartdate, dt)
        exposurelives=ExposureByLives(lastdate, dt)
        exposureamts = exposurelives * record['SumAssured']
        claimlives = 0.0
        claimamts = 0.0
        lapselives = 0.0
        lapseamts = 0.0
        if(dt == policyenddate):
            if (record['Decrement']==1): # death
                claimlives=1.0
                claimamts=record['SumAssured']
            elif (record['Decrement']==-1): #lapse
                lapselives=1.0
                lapseamts= record['SumAssured']
            
        result.append([age, calendaryear, duration, exposurelives, exposureamts, 
            claimlives, claimamts, lapselives, lapseamts])

    #return result
    return result

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
        self.assertEqual(YearsBetweenDates(startdate,enddate),1)

        #test GetDate
        testdate='02/01/2014'
        self.assertEqual(GetDate(testdate), date(2014,1,2))

        #test CreatePeriods
        periods = CreatePeriods(date(2012,6,1), date(2016,2,1), date(1970,3,1))
        expectedperiods = [date(2012,6,1), 
            date(2013,1,1), date(2013,3,1), date(2013,6,1),
            date(2014,1,1), date(2014,3,1), date(2014,6,1),
            date(2015,1,1), date(2015,3,1), date(2015,6,1),
            date(2016,1,1), date(2016,2,1)]
        self.assertEqual(periods, expectedperiods)


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
        'DateOfBirth': '01/03/1970', 'Gender': 'M', 'PolicyNumber': 'AA001', 
        'SumAssured': 100000, 'PolicyEnd': '01/02/2016', 'Decrement': 1}
        
        #do calcs
        result = CalculateExposure(record)

        #test results
        firstresult=result[0]
        expectedfirstresult = [42,2012,0,(214/365.0), ((214/365.0)*100000), 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(firstresult, expectedfirstresult)
        lastresult=result[-1]
        expectedfirstresult = [45,2016,3,(32/365.0), ((32/365.0)*100000), 1.0, 100000, 0.0, 0.0]


if __name__ == '__main__':
    #unittest.main()

    #create the actual, output to stdout
    records = CreateDataFrame('test.csv')
    
    #output header
    header = ['PolicyNumber', 'Gender', 'Smoker', 'SumAssured', 'Age', 'Year', 'Duration', 'ExposureLives',
        'ExposureAmts', 'ClaimLives', 'ClaimAmts', 'LapseLive', 'LapseAmts']
    print(",".join(header))
    
    #output records
    for record in records:
        results = CalculateExposure(record)
        for resultline in results:
            combineresult = [ record['PolicyNumber'], record['Gender'], record['Smoker'], record['SumAssured']] + resultline
            formattedoutput = ','.join(map(str,combineresult))
            print(formattedoutput)
        

