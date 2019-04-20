import csv
import numpy as np
from scipy import stats
from collections import defaultdict


def normalize(array):
    return (array-np.min(array))/np.ptp(array)

columns = defaultdict(list) # each value in each column is appended to a list
with open('suicideDataset2.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

codes = set(columns['year'])
fieldnames = ['country', 'code', 'year', 'GDP', 'population', 'malePopulation', 'femalePopulation', 'totalRate',
              'maleRate', 'femaleRate', '5-14', '15-24', '25-34', '35-54', '55-74', '75+', 'male_5-14', 'male_15-24',
              'male_25-34', 'male_35-54', 'male_55-74', 'male_75+', 'female_5-14', 'female_15-24', 'female_25-34',
              'female_35-54', 'female_55-74', 'female_75+']

allNormal = []
for year in range(1985,2016):

    index = list(np.where(np.array(columns['year']) == str(year))[0])
    dataHold = np.zeros((len(fieldnames)-3,len(index)))
    print(year)

    for i in range(3,len(fieldnames)):
        dataHold[i-3] = normalize(np.array(columns[fieldnames[i]])[index].astype(np.float32))



    for i in range(len(index)):
        normal = {}
        j = 0
        for name in fieldnames:
            if j < 3:
                normal[name] = columns[name][index[i]]
            else:
                normal[name] = dataHold[j-3][i]
            j+=1
        allNormal.append(normal)


with open('suicideNormalizebyYear.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in allNormal:
        writer.writerow(row)
print('Done')




