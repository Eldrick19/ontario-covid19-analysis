### Dependencies
import pandas as pd

### Import data from CSV
df = pd.read_csv('positive-cases-detail/conposcovidloc.csv')
#print(df.head())

### Get Age-Gender Combinations (Method 1)
gender_age_list = []
for index, row in df.iterrows(): # Get all the existing unique combinations of age and gender
    list_search = [row['Age_Group'],row['Client_Gender']]
    if list_search not in gender_age_list:
        gender_age_list.append(list_search)
dfAB = pd.DataFrame.from_records(gender_age_list)

### Data clean-up & Formatting (1)
dfAB.columns = ['Age_Group', 'Client_Gender']
dfAB = dfAB.sort_values(by=['Client_Gender', 'Age_Group'], ascending=(True, True))
dfAB = dfAB.reset_index(drop=True)

### Distribute Combination Icons
icon_list = []
for index, row in dfAB.iterrows():
    if row['Age_Group'] == '<20' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/minor-f.png')
    elif row['Age_Group'] == '<20' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/minor-m.png')
    elif row['Age_Group'] == '20s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/20-f.png')
    elif row['Age_Group'] == '20s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/20-m.png')
    elif row['Age_Group'] == '30s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/30-f.png')
    elif row['Age_Group'] == '30s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/30-m.png')
    elif row['Age_Group'] == '40s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/middleaged-f.png')
    elif row['Age_Group'] == '40s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/middleage-m.png')
    elif row['Age_Group'] == '50s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/middleaged-f.png')
    elif row['Age_Group'] == '50s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/middleaged-m.png')
    elif row['Age_Group'] == '60s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/elderly-f.png')
    elif row['Age_Group'] == '60s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/elderly-m.png')
    elif row['Age_Group'] == '70s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/elderly-f.png')
    elif row['Age_Group'] == '70s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/elderly-m.png')
    elif row['Age_Group'] == '80s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/elderly-f.png')
    elif row['Age_Group'] == '80s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/elderly-m.png')
    elif row['Age_Group'] == '90s' and row['Client_Gender'] == 'FEMALE':
        icon_list.append('img/bar-chart-race/elderly-f.png')
    elif row['Age_Group'] == '90s' and row['Client_Gender'] == 'MALE':
        icon_list.append('img/bar-chart-race/elderly-m.png')
    else:
        icon_list.append('')

### Data clean-up & Formatting (2)
dfC = pd.DataFrame(icon_list)
dfC.columns = ['IMG_URL']

### Merge Columns A, B & C
dfABC = pd.concat([dfAB, dfC], axis=1)

### Add  date columns
dfABCZ = dfABC
dfbyDate = df.sort_values(by='Accurate_Episode_Date', ascending=True)
dfbyDate = dfbyDate.reset_index(drop=True)
values_dict = {}
prev_date = 0
for index, row in dfbyDate.iterrows():
    age_group = row['Age_Group']
    gender = row['Client_Gender']
    date = row['Accurate_Episode_Date']
    key = age_group + gender

    if key not in values_dict:
        values_dict[key] =  1
    else:
        values_dict[key] += 1

    if date not in dfbyDate.columns:
        dfABCZ[date] = prev_date
        age_condition = dfABCZ['Age_Group'] == age_group
        gender_condition = dfABCZ['Client_Gender'] == gender
        dfABCZ.loc[age_condition & gender_condition, date] = values_dict[key]
    else:
        age_condition = dfABCZ['Age_Group'] == age_group
        gender_condition = dfABCZ['Client_Gender'] == gender
        dfABCZ.loc[age_condition & gender_condition, date] = values_dict[key]

    prev_date = dfABCZ[date]

### Data clean-up & Formatting (3)
dfABCZ = dfABCZ[dfABCZ.Client_Gender != 'UNKNOWN']
dfABCZ = dfABCZ[dfABCZ.Client_Gender != 'OTHER']
dfABCZ = dfABCZ[dfABCZ.Client_Gender != '(blank)']

### Export to CSV
dfABCZ.to_csv('bar-chart-race-output.csv', index=False)