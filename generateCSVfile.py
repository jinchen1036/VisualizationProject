import pycountry
import csv
import numpy as np
import math

# Country Code Dict
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3



# Read CSV File
csvfile = open('master.csv', 'r')
fieldnames = ("country","year","sex","age","suicides_no","population","suicides/100k pop",
              "country-year", "HDI for year","gdp_for_year ($)","gdp_per_capita ($)","generation")
reader = csv.DictReader( csvfile, fieldnames)

allData = []

# Get Data for CSV File and save to allData
# currentDict= {'country','code', 'year','GDP','population','malePopulation','femalePopulation','totalRate','maleRate','femaleRate',
#               '5-14','15-24','25-34','35-54','55-74','75+','male_5-14','male_15-24','male_25-34','male_35-54',
#               'male_55-74','male_75+','female_5-14','female_15-24','female_25-34','female_35-54', 'female_55-74','female_75+'}

age_groups = ["5-14 years","15-24 years","25-34 years","35-54 years","55-74 years","75+ years"]
currentDict = {}
age_groups_data = np.zeros((6, 4))
for row in reader:
    if row['year'] == 'year':
        continue

    country = row["country"]
    # Check for update current country and year
    if country == "Republic of Korea":
        country = "Korea, Republic of"

    if country not in countries:
        print("Country without code %s" % country)
        continue
    else:
        countryCode = countries[country]

    # Parameters form csv:
    sex = row["sex"]
    age_index = age_groups.index(row["age"])


    if 'year' not in currentDict:
        # male_rate, female_rate = 0, 0
        # male_pop, female_pop = 0,0

        currentDict ={'country':country,'code':countryCode,'year':int(row["year"]),
                    'GDP':int(row["gdp_per_capita ($)"].replace(',', '')),}


    elif int(row['year']) != currentDict['year']:
        # finalize the data
        sums = np.sum(age_groups_data,axis=0)
        currentDict['population'] = sums[1]+sums[3]
        currentDict['malePopulation'] = sums[1]
        currentDict['femalePopulation'] = sums[3]
        currentDict['maleRate'] = sums[0]/sums[1] * 100000
        currentDict['femaleRate'] = sums[2] / sums[3] * 100000
        currentDict['totalRate'] = (sums[0]+sums[2])/(sums[1]+sums[3])* 100000

        sum_suicide = age_groups_data[:,0]+age_groups_data[:,2]
        sum_pop = age_groups_data[:,1]+age_groups_data[:,3]
        currentDict['5-14'] = sum_suicide[0] / sum_pop[0] * 100000
        currentDict['15-24'] = sum_suicide[1] / sum_pop[1] * 100000
        currentDict['25-34'] = sum_suicide[2] / sum_pop[2] * 100000
        currentDict['35-54'] = sum_suicide[3] / sum_pop[3] * 100000
        currentDict['55-74'] = sum_suicide[4] / sum_pop[4] * 100000
        currentDict['75+'] = sum_suicide[5] / sum_pop[5] * 100000

        k =[]
        for val in currentDict.values():
            try:
                k.append(math.isnan(val))
            except TypeError:
                pass
            # if val.isdigit():
            #     k.append(math.isnan(val))

        if not any(k):
            allData.append(currentDict)

        # male_rate, female_rate = 0,0
        # male_pop, female_pop = 0, 0
        age_groups_data = np.zeros((6, 4))
        currentDict ={'country':country,'code':countryCode,'year':int(row["year"]),
                    'GDP':int(row["gdp_per_capita ($)"].replace(',', '')),}


    if sex == 'male':
        age_groups_data[age_index, 0] += int(row["suicides_no"])
        age_groups_data[age_index, 1] += int(row["population"])
        if age_index == 0:
            currentDict['male_5-14'] = float(row["suicides/100k pop"])
        elif age_index == 1:
            currentDict['male_15-24'] = float(row["suicides/100k pop"])
        elif age_index == 2:
            currentDict['male_25-34'] = float(row["suicides/100k pop"])
        elif age_index == 3:
            currentDict['male_35-54'] = float(row["suicides/100k pop"])
        elif age_index == 4:
            currentDict['male_55-74'] = float(row["suicides/100k pop"])
        elif age_index == 5:
            currentDict['male_75+'] = float(row["suicides/100k pop"])
    else:
        age_groups_data[age_index, 2] += int(row["suicides_no"])
        age_groups_data[age_index, 3] += int(row["population"])
        if age_index == 0:
            currentDict['female_5-14'] = float(row["suicides/100k pop"])
        elif age_index == 1:
            currentDict['female_15-24'] = float(row["suicides/100k pop"])
        elif age_index == 2:
            currentDict['female_25-34'] = float(row["suicides/100k pop"])
        elif age_index == 3:
            currentDict['female_35-54'] = float(row["suicides/100k pop"])
        elif age_index == 4:
            currentDict['female_55-74'] = float(row["suicides/100k pop"])
        elif age_index == 5:
            currentDict['female_75+'] = float(row["suicides/100k pop"])


# if not any(np.isnan(val) for val in currentDict.values()):
#     allData.append(currentDict)


with open('suicideDataset2.csv', mode='w') as csv_file:
    # currentDict= {'country','code', 'year','GDP','population','malePopulation','femalePopulation','totalRate','maleRate','femaleRate',
    #               '5-14','15-24','25-34','35-54','55-74','75+','male_5-14','male_15-24','male_25-34','male_35-54',
    #               'male_55-74','male_75+','female_5-14','female_15-24','female_25-34','female_35-54', 'female_55-74','female_75+'}

    fieldnames = ['country','code', 'year','GDP','population','malePopulation','femalePopulation','totalRate',
                  'maleRate','femaleRate', '5-14','15-24','25-34','35-54','55-74','75+','male_5-14','male_15-24',
                  'male_25-34','male_35-54', 'male_55-74','male_75+','female_5-14','female_15-24','female_25-34',
                  'female_35-54', 'female_55-74','female_75+']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in allData:
        writer.writerow(row)
        # print(row)
    # writer.writerow(currentDict)


print("DONE")