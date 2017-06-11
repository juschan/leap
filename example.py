import leap

#create the actual, output to stdout
records = leap.CreateDataFrame('test.csv')
   
#output header
header = ['PolicyNumber', 'Gender', 'Smoker', 'SumAssured', 'Age', 'Year', 'Duration', 'ExposureLives',
    'ExposureAmts', 'ClaimLives', 'ClaimAmts', 'LapseLive', 'LapseAmts']
print(",".join(header))
    
#output records
for record in records:
    results = leap.CalculateExposure(record)
    for resultline in results:
        combineresult = [ record['PolicyNumber'], record['Gender'], record['Smoker'], record['SumAssured']] + resultline
        formattedoutput = ','.join(map(str,combineresult))
        print(formattedoutput)