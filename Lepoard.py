#(December 2018)
import csv,time
import pandas as pd
import datetime
import numpy as np
import re

#gia na stoixizeis fraseis se lista
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#calculate time difference
def make_delta(entry):
    entry = entry[:8]
    h , m , s = entry.split(':')
    return datetime.timedelta(hours = int(h) , minutes = int(m) , seconds = int(s))

path1 = "/home/bewater/Desktop/kal/evening.csv"
path2 = "/home/bewater/Desktop/kal/relations.csv"
path3 = "/home/bewater/Desktop/kal/ANTWNIS1.csv"
path4 = "/home/bewater/Desktop/kal/durationsM.csv"
path5 = "/home/bewater/Desktop/kal/pointsM.csv"
path6 = "/home/bewater/Desktop/kal/durationsF.csv"
path7 = "/home/bewater/Desktop/kal/pointsF.csv"
dfdata = pd.read_csv(path1 )
dfcounts = pd.read_csv(path2)
dfrelations = pd.read_csv(path3)
dfMdurations = pd.read_csv(path4)
dfMpoints = pd.read_csv(path5)
dfFdurations = pd.read_csv(path6)
dfFpoints = pd.read_csv(path7)

dfdata['Time'] = dfdata['Time'].map(lambda entry: make_delta(entry))

dfdata['New'] = dfdata.apply(lambda x: [val for val in x if not pd.isnull(val)] , axis=1)
df1 = dfdata.set_index('New')

list = []
for name , values in dfdata['New'].iteritems():
    list.append(values)
dfLast = pd.DataFrame.from_records(list , columns=["Date" , "Time" , "Day" , "Sex" , "Value1" , "Value2"])
print(dfLast)

#pare tis diaforetikes imerominies
dfFpoints['Date'] = dfLast.Date.unique()
dfMpoints['Date'] = dfLast.Date.unique()
dfFdurations['Date'] = dfLast.Date.unique()
dfMdurations['Date'] = dfLast.Date.unique()
#vale ws index thn imerominia
dfFpoints = dfFpoints.set_index('Date')
dfMpoints = dfMpoints.set_index('Date')
dfFdurations = dfFdurations.set_index('Date')
dfMdurations = dfMdurations.set_index('Date')
#gemise ta NaN me 0
dfFpoints = dfFpoints.fillna(0)
dfMpoints = dfMpoints.fillna(0)
dfFdurations = dfFdurations.fillna(0)
dfMdurations = dfMdurations.fillna(0)

date = ""
startdurationM = 'eat'
startdurationF = 'eat'
#apo to keno mexri to Focal_end vres to duration
#apo to prwto duration point ews to epomeno vres to duration
vrikeM2 = True
vrikeF2 = True
#vres ta durations
for index , row in dfLast.iterrows():
    if row['Sex'] == "Male":
        #durations
        #vres sinoliko xrono parakolouthisis ana mera
        if row['Value2'] == None and row['Value1'] == None:
            starttimeM = row['Time']
        if row['Value1'] == "FOCAL_END":
            dfMdurations.at[row['Date'] , 'Total'] = pd.to_timedelta(dfMdurations.at[row['Date'] , 'Total']) + (row['Time'] - starttimeM)

        #vres sinoliko xrono gia kathe duration an mera
        if (row['Value2'] in dfrelations.columns.tolist()) and vrikeM2:
            startdurationM = row['Value2']
            startdurationtimeM = row['Time']
            print("koitame an to %s stamataei apo kapoio duration kai ti wra xekinise:%s  " %(startdurationM , startdurationtimeM))
            #vrike to prwto tou Male,mhn xana mpei
            vrikeM2 = False
        if row['Value2'] in dfrelations[startdurationM].tolist():
            print("MOU LES OTI to %s stamataei to %s me xrono %s kai eixe prin %s" %(row['Value2'],startdurationM,(row['Time']-startdurationtimeM), pd.to_timedelta(dfMdurations.at[row['Date'] , startdurationM])))
            dfMdurations.at[row['Date'] , startdurationM] = pd.to_timedelta(dfMdurations.at[row['Date'] , startdurationM]) + (row['Time'] - startdurationtimeM)
            startdurationM = row['Value2']
            startdurationtimeM = row['Time']

    elif row['Sex'] == "Female":
    #durations
        #vres sinoliko xrono parakolouthisis ana mera
        if row['Value2'] == None and row['Value1'] == None:
            starttimeF = row['Time']
        if row['Value1'] == "FOCAL_END":
            dfFdurations.at[row['Date'] , 'Total'] = pd.to_timedelta(dfFdurations.at[row['Date'] , 'Total']) + (row['Time'] - starttimeF)

        #vres sinoliko xrono gia kathe duration an mera
        if (row['Value2'] in dfrelations.columns.tolist()) and vrikeF2:
            startdurationF = row['Value2']
            startdurationtimeF = row['Time']
            #vrike to prwto tou Female,mhn xana mpei
            vrikeF2 = False
            print("koitame an to %s stamataei apo kapoio duration kai ti wra xekinise:%s  " %(startdurationF , startdurationtimeF))
        if row['Value2'] in dfrelations[startdurationF].tolist() :
            print("MOU LES OTI to %s stamataei to %s me xrono %s kai eixe prin %s" %(row['Value2'],startdurationF,(row['Time']-startdurationtimeF), pd.to_timedelta(dfFdurations.at[row['Date'] , startdurationF])))
            dfFdurations.at[row['Date'] , startdurationF] = pd.to_timedelta(dfFdurations.at[row['Date'] , startdurationF]) + (row['Time'] - startdurationtimeF)
            startdurationF = row['Value2']
            startdurationtimeF = row['Time']

#vres ta points
for index , row in dfLast.iterrows():
    if row['Sex'] == "Male":
        if (row['Value2'] in dfcounts.Points.values):
            dfMpoints.at[row['Date'] , row['Value2']] = dfMpoints.at[row['Date'] , row['Value2']] + 1
        if (row['Value1'] in dfcounts.Points.values):
            dfMpoints.at[row['Date'] , row['Value1']] = dfMpoints.at[row['Date'] , row['Value1']] + 1
    elif row['Sex'] == "Female":
        if (row['Value2'] in dfcounts.Points.values):
            dfFpoints.at[row['Date'] , row['Value2']] = dfFpoints.at[row['Date'] , row['Value2']] + 1
        if (row['Value1'] in dfcounts.Points.values):
            dfFpoints.at[row['Date'] , row['Value1']] = dfFpoints.at[row['Date'] , row['Value1']] + 1

dfFpoints.to_csv("/home/bewater/Desktop/kal/points/FemalePointsevening.csv" , sep='\t' , encoding='utf-8')
dfMpoints.to_csv("/home/bewater/Desktop/kal/points/MalePointsevening.csv" , sep='\t' , encoding='utf-8')
dfFdurations.to_csv("/home/bewater/Desktop/kal/durations/FemaleDurationsevening.csv" , sep='\t' , encoding='utf-8')
dfMdurations.to_csv("/home/bewater/Desktop/kal/durations/MaleDurationsevening.csv" , sep='\t' , encoding='utf-8')
