import csv
import numpy as np
from scipy import stats
from collections import defaultdict
from Functions import plot_correlation

columns = defaultdict(list) # each value in each column is appended to a list
with open('suicideNormalizebyYear.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k


years = np.array(range(1985,2016)).astype('str')
allCorrelation = []
for year in years:
    correlations = {}
    print(year)
    index  = np.where(np.array(columns['year']) == year)[0]

    # Get the data from the normalized data
    GDP = np.array(columns['GDP'])[index].astype(np.float32)
    totalRate = np.array(columns['totalRate'])[index].astype(np.float32)
    Population = np.array(columns['population'])[index].astype(np.float32)
    maleRate = np.array(columns['maleRate'])[index].astype(np.float32)
    femaleRate = np.array(columns['femaleRate'])[index].astype(np.float32)


    # Calculate the correlation coeifficients
    correlations['year'] = year
    correlations['GDP_Rate'],_ = stats.pearsonr(GDP,totalRate)
    correlations['Population_Rate'], _ = stats.pearsonr(Population, totalRate)
    correlations['male_female'], _ = stats.pearsonr(maleRate, femaleRate)

    # Plot the correlation and save the figure
    plot_correlation(variable1=GDP,variable2=totalRate,name1='GDP',name2='totalRate',
                     rValue=correlations['GDP_Rate'],year=year)
    plot_correlation(variable1=Population, variable2=totalRate, name1='Population', name2='totalRate',
                     rValue=correlations['Population_Rate'], year=year)
    plot_correlation(variable1=maleRate, variable2=femaleRate, name1='maleRate', name2='femaleRate',
                     rValue=correlations['male_female'], year=year)

    allCorrelation.append(correlations)


# Save coefficient to csv file
with open('yearlyCorrelation.csv', mode='w') as csv_file:
    fieldnames = ['year', 'GDP_Rate','Population_Rate','male_female']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in allCorrelation:
        writer.writerow(row)

print('Done')




# wilcoxon test  for not normal distributed data
# t-test data for normal distribution data

