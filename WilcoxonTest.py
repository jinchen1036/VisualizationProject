# Reference: https://gist.github.com/mblondel/1761714
import csv
import numpy as np
from collections import defaultdict
from scipy.stats import ttest_1samp, wilcoxon
from Functions import get_pValue

columns = defaultdict(list) # each value in each column is appended to a list
with open('suicideNormalizebyYear.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k


years = np.array(range(1985,2016)).astype('str')
allpValues = []
for year in years:
    pValues = {}
    print(year)
    index  = np.where(np.array(columns['year']) == year)[0]

    # Get the data from the normalized data
    GDP = np.array(columns['GDP'])[index].astype(np.float32)
    totalRate = np.array(columns['totalRate'])[index].astype(np.float32)
    Population = np.array(columns['population'])[index].astype(np.float32)
    maleRate = np.array(columns['maleRate'])[index].astype(np.float32)
    femaleRate = np.array(columns['femaleRate'])[index].astype(np.float32)


    # Calculate the pValues
    pValues['year'] = year
    pValues['GDP_Rate']= get_pValue(values1=GDP,values2=totalRate)
    pValues['Population_Rate']= get_pValue(values1=Population,values2=totalRate)
    pValues['male_female']= get_pValue(values1=maleRate,values2=femaleRate)

    allpValues.append(pValues)


# Save coefficient to csv file
with open('yearlyPvalue.csv', mode='w') as csv_file:
    fieldnames = ['year', 'GDP_Rate','Population_Rate','male_female']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in allpValues:
        writer.writerow(row)

print('Done')




# wilcoxon test  for not normal distributed data
# t-test data for normal distribution data

