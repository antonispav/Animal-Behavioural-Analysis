#A python script to calculate the duration and the quantity of Sheep behaviours

from pandas import read_excel #pip3 install odfpy
import pandas as pd
import numpy as np
import datetime

import time

#convert string to TimeDelta
def make_delta(entry):
    entry = entry[:8]
    h , m , s = entry.split(':')
    return datetime.timedelta(hours = int(h) , minutes = int(m) , seconds = int(s))

def CalculateTotal(df):

    #In new column("changed_individual") mark with 1 when SheepID is different than previews
    df['changed_individual'] = df['SheepID'].rolling(2).apply(lambda x: x[0] != x[1]).fillna(1)

    #Count how many SheepID changes we have in the dataset
    df["value_group"] = df["changed_individual"].cumsum()

    #Make 2 new DataFrames with the starting & ending Date/Time/SheepID/Behaviour of an observation
    startD = df.groupby(['Date',"value_group"],as_index=False).nth(0)
    endD = df.groupby(['Date',"value_group"],as_index=False).nth(-1)

    #print('\n Time : \n', startD.loc[:,"Time"].subtract(endD.loc[:,"Time"]) )#pd.Series(delta.seconds for delta in (startD.Time - endD.Time) ))

    #Make a DataFrame with the Date/StartTime/EndTime/SheepID of an observation
    start_end = pd.DataFrame(
        {
            "start": startD.Time,
            "end": endD.Time ,
            "SheepID": startD.SheepID
        }
    )

    # convert timedeltas to seconds (float)
    start_end["Total"] = (
        (start_end["end"] - start_end["start"]) / np.timedelta64(1, 's')
    )

    return start_end

# dataset = read_excel("test.ods", engine="odf")
dataset = pd.read_csv("allatlibitum.csv")
durations = pd.read_csv("durations-not-overlapping.csv")
points = pd.read_csv("list-of-point-behaviours.csv")

#make a dataframe with columns the unique point/duration behaviours
pointsEmpty = pd.DataFrame(columns=points.Point.tolist())
durationsEmpty = pd.DataFrame(columns=durations.columns.tolist())

#convert dataframe to 2d list->1d list ->numpy array-> keep the unique values
#np.unique(np.array([j for sub in [durations[i].tolist() for i in durations.columns] for j in sub]))

#In every row we have the date , time , start(the sheep id), Behaviour and 0-1 Values(0 if new sheep id is starting)

#Keep in a new column all the values of a row in list format (drop all Null cells)
dataset['New'] = dataset.apply(lambda x: [val for val in x if not pd.isnull(val)] , axis=1)

#make a new dataframe with the above values
dfdata = dataset.New.apply(pd.Series).rename(columns={0: "Date", 1: "Time", 2: "SheepID", 3: "Value"}, errors="raise").set_index('Date')
dfdata['Time'] = dfdata['Time'].astype(str).map(lambda entry: make_delta(entry))#this line is stupid, probably the ods format has the Time column in datetime.time format(it was written in first place because csv makes every column into str)

#Convert SheepID to a Unique Category Number
dfdata["SheepID"] = dfdata["SheepID"].astype('category')
OriginalSheepID = dict( enumerate(dfdata['SheepID'].cat.categories ) )# keep a dictionary for real sheepID and it's numeric value

dfdata["SheepID"] = dfdata["SheepID"].cat.codes#replace the original SheepID with the equivalent category ID
dfdata['SheepID'] = pd.to_numeric(dfdata.SheepID, errors='coerce').fillna(0, downcast='infer')

#Call CalculateTotal for total observation time
dftotal = CalculateTotal(dfdata)

#Initialise points and duration DataFrame
dfpoints = pd.DataFrame({"Date":dftotal.index,"SheepID":dftotal.SheepID})
dfpoints = pd.merge(dfpoints,pointsEmpty,how="left",right_index=True,left_index=True).fillna(0).drop('Date', axis=1)#.reset_index()#.set_index('Date')
dfdata = dfdata.reset_index()
dfdurations = pd.DataFrame(
    {
        "Date":dftotal.index,
        "SheepID":dftotal.SheepID,
        "TotalObservation(sec)":dftotal.Total,
    }
)
dfdurations = pd.merge(dfdurations,durationsEmpty,how="left",right_index=True,left_index=True).fillna(0).drop('Date', axis=1).reset_index()

found = False#Flag for first Duration behaviour
for _,row in dfdata.iterrows():
    #calculate points
    if row['Value'] in points.Point.tolist():
        dfpoints.loc[dfpoints.SheepID == row['SheepID'],row['Value']] += 1
    #calculate durations
    if (row['Value'] in durations.columns.tolist() ) and not found:#if Value is a Duration
        start_behaviour = row['Value']
        startB_time = row['Time']
        found = True
    elif (found and row['Value'] in durations.columns.tolist()) and (start_behaviour in durations[start_behaviour].tolist()):#check if a behaviour stops the start_behaviour
        stopB_time = row['Time']
        stop_behaviour = row['Value']
        total_seconds = (stopB_time - startB_time).total_seconds()
        dfdurations.loc[(dfdurations.SheepID == row['SheepID']) & (dfdurations.Date == row['Date']) , start_behaviour] += total_seconds
        dfdurations.loc[(dfdurations.SheepID == row['SheepID']) & (dfdurations.Date == row['Date']) , "Behaviours"] = str(start_behaviour) + "-" +str(stop_behaviour)
        start_behaviour = row['Value']
        startB_time = row['Time']

#Convert category ID to the original SheepID
dfdurations['SheepID'] = dfdurations['SheepID'].map(OriginalSheepID)
dfpoints['SheepID'] = dfpoints['SheepID'].map(OriginalSheepID)

#check if dataset containts an Actor and a Recipient & split them to 2 columns
if ( dfpoints['SheepID'].str.contains(';', na=False, regex=True).sum() > 0 ) or ( dfdurations['SheepID'].str.contains(';', na=False, regex=True).sum() > 0 ):
    dfpoints[['SheepID1(Actor)','SheepID2(Recipient)']] = dfpoints.SheepID.str.split(pat=";",expand=True,)
    dfdurations[['SheepID1(Actor)','SheepID2(Recipient)']] = dfdurations.SheepID.str.split(pat=";",expand=True,)
else:#Other Datasets indicate the end of an observation with the 'end' value, so remove it as we don't need it
    dfdurations = dfdurations.drop(['end',"Behaviours"], axis=1).set_index('Date')

print("Results \n",,dfpoints,"\n\n",dfdurations)
dfpoints.to_csv("Points.csv" , sep='\t' , encoding='utf-8')
dfdurations.to_csv("Durations.csv" , sep='\t' , encoding='utf-8')
