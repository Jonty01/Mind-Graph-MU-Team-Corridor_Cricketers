from thefuzz import fuzz, process
import pandas as pd
import numpy as np
import json
import mysql.connector


# mydb = mysql.connector.connect(host='localhost', database='shubh', user='root', password='admin')


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
# print(df1)
df4.iloc[:, 1] = df4.iloc[:, 1].map(participantsmap)
# remove deplicate rows
df4 = df4.drop_duplicates()
# print(df4)
print("")
df3.iloc[:, 1] = df3.iloc[:, 1].map(organisersmap)
# print(df3)
print("")
df2.iloc[:, 1] = df2.iloc[:, 1].map(clubsmap)
df2 = df2.drop_duplicates()
# print(df2)
# if there are same Name values make them unique 


# df2.iloc[:, 1] = df2.iloc[:, 1].map(clubsmap)
# print(df2)


#####  Creating final dataframe 1    For Joined Fest Organiser Table #####
df5 = pd.merge(df1, df3, how='inner', on='Name')
# print(df5)                              
# df6 = df5.groupby(['ID', 'Name', 'Fest_Name'])[['Role']].sum()
# print(df6)
# flatdf6 = df6.reset_index()                                 # flatten the multi-indexed dataframe
# print(flatdf6)




st = 'organiser_'
st1 = "Participant"


#####  Creating final dataframe 2 #####
df7 = pd.merge(df1, df4, how='inner', on='Name')
# df8 = df7.groupby(['ID', 'Name'])[['Fest_Name', 'Event']]
df7.sort_values(by=['ID', 'Fest_Name'], inplace=True)
print(df7)
df8 = pd.merge(df7, df5, how='left', on=['ID', 'Name', 'Fest_Name'])
# where Role = NaN, replace with 'Participant'
df8['Role'].fillna('Participant', inplace=True)
df8.sort_values(by=['ID', 'Fest_Name'], inplace=True)
print(df8)
# df8 to json
# find where Name is Starr Hammond
# print(df8.loc[df8['Name'] == 'Starr Hammond'])


#find from df8 where Role is like organiser_% ans Fest_Name is fest_1
f1_organisers = len(df8.loc[(df8['Role'].str.contains(st)) & (df8['Fest_Name'] == 'fest_1')])
f2_organisers = len(df8.loc[(df8['Role'].str.contains(st)) & (df8['Fest_Name'] == 'fest_2')])
f1_participants = len(df8.loc[(df8['Role'].str.contains(st1)) & (df8['Fest_Name'] == 'fest_1')])
f2_participants = len(df8.loc[(df8['Role'].str.contains(st1)) & (df8['Fest_Name'] == 'fest_2')])
print("fest_1 organisers: ", f1_organisers)
print("fest_2 organisers: ", f2_organisers)
print("fest_1 participants: ", f1_participants)
print("fest_2 participants: ", f2_participants)

# fest_1 has 13 events 
# fest_2 has 15 events

for i in range(1, 3):
    if i==1 :
        fest_1_event = []
        for j in range(1, 14):
            stf = 'fest_1_event_' + str(j)
            se1 = len(df8.loc[(df8['Event'] == stf)])
            fest_1_event.append(se1)
            # print(se1)
            # find from df8 from 8 where fest_i_name_j is fest_1_event_j
    elif i==2:
        fest_2_event = []
        for j in range(1, 16):
            stf = 'fest_2_event_' + str(j)
            se1 = len(df8.loc[(df8['Event'] == stf)])
            fest_2_event.append(se1)
            # print(se1)

print("fest_1_event: ", fest_1_event)
print("fest_2_event: ", fest_2_event)





df9 = pd.merge(df1, df2, how='inner', on='Name')
df9.sort_values(by=['ID', 'Club_Name'], inplace=True)

print(df9)

#find from df9 where Role is like organiser_% ans Club_Name is club_1
print("")
print("")
print("club_1")
c1_organisers = len(df9.loc[(df9['Role'].str.contains(st)) & (df9['Club_Name'] == 'club_1')])
c2_organisers = len(df9.loc[(df9['Role'].str.contains(st)) & (df9['Club_Name'] == 'club_2')])
c3_organisers = len(df9.loc[(df9['Role'].str.contains(st)) & (df9['Club_Name'] == 'club_3')])
c1_participants = len(df9.loc[(df9['Role'].str.contains(st1)) & (df9['Club_Name'] == 'club_1')])
c2_participants = len(df9.loc[(df9['Role'].str.contains(st1)) & (df9['Club_Name'] == 'club_2')])
c3_participants = len(df9.loc[(df9['Role'].str.contains(st1)) & (df9['Club_Name'] == 'club_3')])
print("club_1 organisers: ", c1_organisers)
print("club_2 organisers: ", c2_organisers)
print("club_3 organisers: ", c3_organisers)
print("club_1 participants: ", c1_participants)
print("club_2 participants: ", c2_participants)
print("club_3 participants: ", c3_participants)

# participants who are students of 17th batch
print("")
print("")
print("17th batch")
batch_17 = len(df9.loc[(df9['Role'].str.contains(st1)) & (df9['ID'].str.contains('17XJ1A'))])
print("17th batch participants: ", batch_17)
batch_18 = len(df9.loc[(df9['Role'].str.contains(st1)) & (df9['ID'].str.contains('18XJ1A'))])
print("18th batch participants: ", batch_18)
print(len(df9.loc[(df9['Role'] == 'Participant')]))
print(len(df9.loc[(df9['Role'].str.contains('organiser'))]))


# club_1 has 3 events
# club_2 has 3 events
# club_3 has 3 events


for i in range(1,4):
    for j in range(1,4):
        # make list named as club_i_event
        stc = "club_" + str(i) + "_event_" + str(j)
        print(stc)


for i in range(1, 4):
    if i==1 :
        club_1_event = []
        for j in range(1, 4):
            stc = 'club_1_event_' + str(j)
            se2 = len(df9.loc[(df9['Event'] == stc)])
            club_1_event.append(se2)
            # print(se1)
            # find from df8 from 8 where fest_i_name_j is fest_1_event_j
    elif i==2:
        club_2_event = []
        for j in range(1, 4):
            stc = 'club_2_event_' + str(j)
            se2 = len(df9.loc[(df9['Event'] == stc)])
            club_2_event.append(se2)
            # print(se1)
    elif i==3:
        club_3_event = []
        for j in range(1, 4):
            stc = 'club_3_event_' + str(j)
            se2 = len(df9.loc[(df9['Event'] == stc)])
            club_3_event.append(se2)
            # print(se1)

print("club_1_event: ", club_1_event)
print("club_2_event: ", club_2_event)
print("club_3_event: ", club_3_event)













# df11 = pd.merge(df8, df9, how='inner', on=['ID', 'Name'])
df11 = pd.merge(df9, df8, how='outer', on=['ID', 'Name'])
# df11 = df11.drop_duplicates()
# print(df11)
print(df11.loc[df11['Fest_Name'] == 'fest_1'])

df12 = pd.merge(df8, df9, how='outer', on=['ID', 'Name'])
# df12 = df12.drop_duplicates()
# print(df12)
df12.to_csv('Joined_Fest_Organiser.csv', index=False)
df13 = pd.merge(df12, df11, how='inner', on=['ID', 'Name'])
# df13 = df13.drop_duplicates()
# print(df13)
df13.to_csv('Joined_Organiser.csv', index=False)
# df11 to csv
df11.to_csv('Final.csv', index=False)
# delete all rows where there is Nan in Club_Name or Event_y or Role_y
# df11.dropna(subset=['Club_Name', 'Event_y', 'Role_y'], inplace=True)
# print(df11)
# query from df11 where Role_y is like organiser_
# print(df11.loc[df11['Name'] == 'Starr Hammond'])


# Extract all names that are present in df8 and df9
# df8names = df8.iloc[:, 1].values
# df9names = df9.iloc[:, 1].values
# print(df8names)
# print(df9names)



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

# Main Joined Dataframe df11 

res1 = []
currid = ""
currclub = ""
clubs = {}
for i, row in df9.iterrows():
    # fest_i_event_j = {row['Event']: {'participated': True}}
    club_i_event_j = row['Event']
    if row['Club_Name'] != currclub or row['ID'] != currid:
        currclub = row['Club_Name']
        # if row['Role'] is a string like organiser_1 or organiser_2
        if row['Role'].startswith(st):
            print(row['Role'])
            club_i_obj = {'isOrganiser': 'Organiser'}
        else:
            club_i_obj = {'isOrganiser': 'Participant'}
        # fest_i_obj = {'isOrganizer': ''}
    club_i_obj[club_i_event_j] = {'participated': True}
    if row['ID'] != currid:
        res1.append(clubs)
        fests = {}
        currid = row['ID']
        clubs = {'name': row['Name'], 'id': currid, 'clubs': {}}
    clubs['clubs'][currclub] = club_i_obj
res1.append(clubs)
del res1[0]

# print("dccfgvbhfcvgbh  check check:  ")
# print(res1)
# find number of "isOrganiser": "Organiser" in res1
# print(res1[0]['clubs']['Dance Club']['isOrganiser'])
file = open("output2.json", "w")
# file.write(str(res))
json.dump(res1, file, indent=4)
file.close()


with open('output2.json') as f1:
    data1 = json.load(f1)
with open('output1.json') as f2:
    data2 = json.load(f2)


merged = [{**res1, **res} for res1, res in zip(data1, data2)]
file=open("output3.json", "w")
json.dump(merged, file, indent=4)



print("Names that have values in df8 but not in df9")
dfa = (df8.loc[~df8['Name'].isin(df9['Name'])])
print(dfa)

print("")
print("Names that have values in df9 but not in df8")
dfb = (df9.loc[~df9['Name'].isin(df8['Name'])])
print(dfb)




# put dfa(Name, ID, Fest_Name, Event, Role) in a json file, this is for fests
j1 = []
currid = ""
currfest = ""
clubs = {}
fests = {}
for i, row in dfa.iterrows():
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
        j1.append(fests)
        fests = {}
        currid = row['ID']
        fests = {'name': row['Name'], 'id': currid, 'fests': {}}
    fests['fests'][currfest] = fest_i_obj
j1.append(fests)
# del j1[0]

file = open("output6.json", "w")
# file.write(str(res))
json.dump(j1, file, indent=4)
file.close()


j2 = []
currid = ""
currclub = ""
clubs = {}
for i, row in dfb.iterrows():
    # fest_i_event_j = {row['Event']: {'participated': True}}
    club_i_event_j = row['Event']
    if row['Club_Name'] != currclub or row['ID'] != currid:
        currclub = row['Club_Name']
        # if row['Role'] is a string like organiser_1 or organiser_2
        if row['Role'].startswith(st):
            print(row['Role'])
            club_i_obj = {'isOrganiser': 'Organiser'}
        else:
            club_i_obj = {'isOrganiser': 'Participant'}
        # fest_i_obj = {'isOrganizer': ''}
    club_i_obj[club_i_event_j] = {'participated': True}
    if row['ID'] != currid:
        j2.append(clubs)
        fests = {}
        currid = row['ID']
        clubs = {'name': row['Name'], 'id': currid, 'clubs': {}}
    clubs['clubs'][currclub] = club_i_obj
j2.append(clubs)
del j2[0]

# print(res)
file = open("output7.json", "w")
# file.write(str(res))
json.dump(j2, file, indent=4)
file.close()



with open('output3.json') as f3:
    data3 = json.load(f3)
with open('output6.json') as f4:
    data4 = json.load(f4)


merged2 = [{**res, **res1} for res, res1 in zip(data3, data4)]
file=open("output8.json", "w")
json.dump(merged2, file, indent=4)



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

# find the number of "isOrganiser" = True from output2.json










# mycursor = mydb.cursor()

# insert data of df8 into table fests_records
# for i, row in df8.iterrows():
#     sql = "INSERT INTO fests_records (id, name, fests) VALUES (%s, %s, %s)"
#     val = (row['ID'], row['Name'], row['Fest_Name'])
#     mycursor.execute(sql, val)
#     mydb.commit()
#     print(mycursor.rowcount, "record inserted.")


# insert data of df9 into table clubs_records
# for i, row in df9.iterrows():
#     sql = "INSERT INTO clubs_records (id, name, clubs) VALUES (%s, %s, %s)"
#     val = (row['ID'], row['Name'], row['Club_Name'])
#     mycursor.execute(sql, val)
#     mydb.commit()
#     print(mycursor.rowcount, "record inserted.")

club_1=[]
club_2=[]
club_3=[]

c1f1=len(df11.loc[(df11['Club_Name'] == ('club_1')) & (df11['Fest_Name'] == 'fest_1')])
c1f2=len(df11.loc[(df11['Club_Name'] == ('club_1')) & (df11['Fest_Name'] == 'fest_2')])
club_sum1 = c1f1 + c1f2
c1f1per = (c1f1/club_sum1)*100
c1f2per = (c1f2/club_sum1)*100
print(c1f1per, c1f2per)

c2f1=len(df11.loc[(df11['Club_Name'] == ('club_2')) & (df11['Fest_Name'] == 'fest_1')])
c2f2=len(df11.loc[(df11['Club_Name'] == ('club_2')) & (df11['Fest_Name'] == 'fest_2')])
club_sum2 = c2f1 + c2f2
c2f1per = (c2f1/club_sum2)*100
c2f2per = (c2f2/club_sum2)*100
print(c2f1per, c2f2per)


c3f1=len(df11.loc[(df11['Club_Name'] == ('club_3')) & (df11['Fest_Name'] == 'fest_1')])
c3f2=len(df11.loc[(df11['Club_Name'] == ('club_3')) & (df11['Fest_Name'] == 'fest_2')])
club_sum3 = c3f1 + c3f2
c3f1per = (c3f1/club_sum3)*100
c3f2per = (c3f2/club_sum3)*100
print(c3f1per, c3f2per)



# print(len(df11.loc[(df11['Club_Name'] == ('club_1')) & (df11['Fest_Name'] == 'fest_1')]))
# print(len(df11.loc[(df11['Club_Name'] == ('club_1')) & (df11['Fest_Name'] == 'fest_2')]))

# print(len(df11.loc[(df11['Club_Name'] == ('club_2')) & (df11['Fest_Name'] == 'fest_1')]))
# print(len(df11.loc[(df11['Club_Name'] == ('club_2')) & (df11['Fest_Name'] == 'fest_2')]))

# print(len(df11.loc[(df11['Club_Name'] == ('club_3')) & (df11['Fest_Name'] == 'fest_1')]))
# print(len(df11.loc[(df11['Club_Name'] == ('club_3')) & (df11['Fest_Name'] == 'fest_2')]))

# df8 for fests and df9 for clubs