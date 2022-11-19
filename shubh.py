from thefuzz import fuzz, process
import pandas as pd
import numpy as np
import json

df1 = pd.read_csv("Metadata.csv")
df2 = pd.read_csv("Clubs_data.csv")
df3 = pd.read_csv("Organisers_In_Fests.csv")
df4 = pd.read_csv("Participants_In_Fests.csv")

truthvalues = df1.iloc[:, 0].values
clubsvalues = df2.iloc[:, 1].values
organisersvalues = df3.iloc[:, 1].values
participantsvalues = df4.iloc[:, 1].values

# print(truthvalues)
# print(clubsvalues)
# print(organisersvalues)
# print(participantsvalues)

participantsmap = {}
# for realname in truthvalues:
#     closest = [-1, ""]
#     for participantname in participantsvalues:
#         fuzzval = fuzz.partial_ratio(realname, participantname)
#         # if fuzzval >= closest[0] and fuzzval < 90:
#         if fuzzval > 50:
#             closest[0] = fuzzval
#             closest[1] = participantname
#     participantsmap[closest[1]] = realname

for participantname in participantsvalues:
    mx=-1
    name=""
    for realname in truthvalues:
        fuzzscore = fuzz.ratio(participantname, realname)
        if fuzzscore > mx :
            mx = fuzzscore
            name = realname
    participantsmap[participantname] = name

# print(participantsmap)
# print(len(participantsmap))



organisersmap = {}
for organisername in organisersvalues:
    mx=-1
    name=""
    for realname in truthvalues:
        fuzzscore = fuzz.ratio(organisername, realname)
        if fuzzscore > mx :
            mx = fuzzscore
            name = realname
    organisersmap[organisername] = name
# print(organisersmap)
# print(len(organisersmap))

clubsmap = {}
for clubname in clubsvalues:
    mx=-1
    name=""
    for realname in truthvalues:
        fuzzscore = fuzz.ratio(clubname, realname)
        if fuzzscore > mx :
            mx = fuzzscore
            name = realname
    clubsmap[clubname] = name
# print(clubsmap)
# print(len(clubsmap))

# for realname in truthvalues:
#     closest = [-1, ""]
#     for organisername in organisersvalues:
#         fuzzval = fuzz.partial_ratio(realname, organisername)
#         if fuzzval >= closest[0] and fuzzval > 50:
#             closest[0] = fuzzval
#             closest[1] = organisername
#     organisersmap[closest[1]] = realname

# print(organisersmap)

######   Replace the Faulty Values of names in the CSVs according to the hashmaps   ######

# replace the 2nd column values of df4 with the mapped values in participantsmap
print(df1)
df4.iloc[:, 1] = df4.iloc[:, 1].map(participantsmap)
# remove deplicate rows
df4 = df4.drop_duplicates()
# print(df4)
print("")
df3.iloc[:, 1] = df3.iloc[:, 1].map(organisersmap)
# print(df3)
print("")
df2.iloc[:, 1] = df2.iloc[:, 1].map(clubsmap)
# print(df2)
# if there are same Name values make them unique 


# df2.iloc[:, 1] = df2.iloc[:, 1].map(clubsmap)
# print(df2)


#####  Creating final dataframe 1 #####
df5 = pd.merge(df1, df3, how='inner', on='Name')
print(df5)
# df6 = df5.groupby(['ID', 'Name', 'Fest_Name'])[['Role']].sum()
# print(df6)
# flatdf6 = df6.reset_index()                                 # flatten the multi-indexed dataframe
# print(flatdf6)



#####  Creating final dataframe 2 #####
df7 = pd.merge(df1, df4, how='inner', on='Name')
# df8 = df7.groupby(['ID', 'Name'])[['Fest_Name', 'Event']]
df7.sort_values(by=['ID', 'Fest_Name'], inplace=True)
print(df7)
df8 = pd.merge(df7, df5, how='left', on=['ID', 'Name', 'Fest_Name'])
# where Role = NaN, replace with 'Participant'
df8['Role'].fillna('Participant', inplace=True)
print(df8)
# df8 to json
# find where Name is Starr Hammond
# print(df8.loc[df8['Name'] == 'Starr Hammond'])

st = 'organiser_'

df9 = pd.merge(df1, df2, how='inner', on='Name')
print(df9)

res = []
currid = ""
currfest = ""
clubs = {}
fests = {}
for i, row in df8.iterrows():
    # fest_i_event_j = {row['Event']: {'participated': True}}
    fest_i_event_j = row['Event']
    if row['Fest_Name'] != currfest or row['ID'] != currid:
        currfest = row['Fest_Name']
        # if row['Role'] is a string like organiser_1 or organiser_2
        if row['Role'].startswith(st):
            print(row['Role'])
            fest_i_obj = {'isOrganiser': True}
        else:
            fest_i_obj = {'isOrganiser': False}
        # fest_i_obj = {'isOrganizer': ''}
    fest_i_obj[fest_i_event_j] = {'participated': True}
    if row['ID'] != currid:
        res.append(fests)
        fests = {}
        currid = row['ID']
        fests = {'name': row['Name'], 'id': currid, 'fests': {}}
    fests['fests'][currfest] = fest_i_obj
res.append(fests)
del res[0]

# print(res)
file = open("output1.json", "w")
# file.write(str(res))
json.dump(res, file, indent=4)
file.close()


# print(df2)


# df8 = df7.groupby(['ID', 'Name', 'Fest_Name'])[['Event']].agg(",".join)
# df8 = df7.groupby(['ID', 'Name', 'Fest_Name'])[['Event']].sum()
# 
# print(df8)
# flatdf8 = df8.reset_index()                                 # flatten the multi-indexed dataframe
# df8['Event'] = df8['Event'].str.split(',').str.join(', ')
# print(flatdf8)
# eventjson = []
# for i, group in df8.iterrows():
#     print(group)
#     for j, row in group.items():
#         eventjson.append(row)
    # eventjson.append({"name": row["Name"], "id": row["ID"], "fests": 10})
# df8.to_csv('test.csv')
# print(eventjson)



#####  Creating final dataframe 3 #####
# df2 = df2.groupby(['Name', 'Club_Name', 'Event'])[['Role']].sum()
# print(df2)
# df9 = pd.merge(df1, df2, how='inner', on='Name')
# df9 = df9.groupby(['ID', 'Name', 'Club_Name', 'Event'])[['Role']].sum()
# print(df9)
# flatdf9 = df9.reset_index()                                 # flatten the multi-indexed dataframe
# flatdf9 = flatdf9.groupby(['ID', 'Name', 'Club_Name', 'Event'])[['Role']].sum()
# print(flatdf9)
# print(flatdf9.query('Role == "Participant"'))
# for one ID and Name there can be multiple Club_Name values, Event values, Role values
# so we need to group them together
# df10 = df9.groupby(['ID', 'Name'])[['Club_Name', 'Event', 'Role']].sum()
# df10 = df9.groupby(['ID', 'Name', 'Club_Name', 'Event'])[['Role']].sum()
# print(df10)
# flatdf10 = df10.reset_index()                                 # flatten the multi-indexed dataframe
# print(flatdf10)


# [
#     {'name': 'Dummy',
#  'id': 'id000',
#  'clubs': {'club_i': {'isOrganiser': 'Organiser',
#             'club_i_event_j': {'participated': False},
#             },
#         },
#  'fests': {'fest_i': {'isOrganiser': '',
#             'fest_i_event_j': {'participated': True},
#             },
#         }
#     }
# ]

# for name in truthvalues:
    # df1.query the id of the name
    # print(name, df1.query('Name == @name')['ID'].values[0])
    # make a json file with fields