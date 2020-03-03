#A python script to calculate the duration and the quantity of Sheep behaviours
#Dataset :
#Head of dataset example(start : sheep id)
# Date	Time	START	Other	Activity	Affiliative	Aggressive	Body posture	Object	Fear	Feeding	Inactive	Maintenance	Reproductive	Focal end
# 16/1/2020	10:31:24	2150
# 16/1/2020	10:31:27	2150		Walking

#In order to calculate the duration and the quantity of sheep behaviours we need 2 tables:
#the durations not overlapping each other for the duration
#and the list of point behaviours for the quantity

#ex durations not overlaping :
# Walking	Running       Trotting	Circling
# standing	standing     standing	standing
# Running	Walking	      Walking	Walking
# Trotting	Trotting	    Running	Running
# Circling	Circling	Circling	Trotting
# Walking	Running	      Trotting	Circling

#ex points :
# defecate,standing,Walking,Running,Trotting,Circling,urinate,tail wave,ears back,ears erect,ears flat,lick object,object sniff,observing,attention to man,attention to sheep,Leap,Foot stamp,Turn back
import csv
import pandas as pd
import numpy as np
import datetime

#convert string to TimeDelta
def make_delta(entry):
    entry = entry[:8]
    h , m , s = entry.split(':')
    return datetime.timedelta(hours = int(h) , minutes = int(m) , seconds = int(s))

def CalculateTotal(df):
    #In new column("changed_individual") mark with 1 when SheepID is different than previews
    df['changed_individual'] = df['SheepID'].rolling(2).apply(lambda x: x[0] != x[1]).fillna(1)

    df["value_group"] = df["changed_individual"].cumsum()
    startD = df.groupby("value_group",as_index=False).nth(0)
    endD = df.groupby("value_group",as_index=False).nth(-1)

    start_end = pd.DataFrame(
        {
            "start": startD.Time,
            # add freq to get when the state ended
            "end": endD.Time ,#+ pd.Timedelta(freq),
            "SheepID": df.SheepID.unique(),
        }
    )
    # convert timedeltas to seconds (float)
    start_end["Total"] = (
        (start_end["end"] - start_end["start"]) / np.timedelta64(1, 's')
    )

    return start_end

dataset = pd.read_csv("dataset.csv")
durations = pd.read_csv("durations-not-overlapping.csv")
points = pd.read_csv("list-of-point-behaviours.csv")

#make a dataframe with columns the unique point/duration behaviours
pointsEmpty = pd.DataFrame(columns=points.Point.tolist())
durationsEmpty = pd.DataFrame(columns=durations.columns.tolist())

#convert dataframe to 2d list->1d list ->numpy array-> keep the unique values
#np.unique(np.array([j for sub in [durations[i].tolist() for i in durations.columns] for j in sub]))

#In every row we have the date , time , start(the sheep id) and 0-1 Values(0 if new sheep id is starting)
#we want to keep only the above columns

#Keep in a new column all the values of a row in list format (drop all Null cells)
dataset['New'] = dataset.apply(lambda x: [val for val in x if not pd.isnull(val)] , axis=1)

#make a new dataframe with the above values
dfdata = dataset.New.apply(pd.Series).rename(columns={0: "Date", 1: "Time", 2: "SheepID", 3: "Value"}, errors="raise").set_index('Date')

dfdata['Time'] = dfdata['Time'].map(lambda entry: make_delta(entry))

#we have only 1 "bad" entry in START("xwris" instead of INT)
#Replace values that are not INT with 0
dfdata['SheepID'] = pd.to_numeric(dfdata.SheepID, errors='coerce').fillna(0, downcast='infer')
dfdata['changed_individual'] = dfdata['SheepID'].rolling(2).apply(lambda x: x[0] != x[1]).fillna(1)

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
        # print("1st IF : \n",row['Value'],row['Time'])
        start_behaviour = row['Value']
        startB_time = row['Time']
        found = True
    elif (found and row['Value'] in durations.columns.tolist()) and (start_behaviour in durations[start_behaviour].tolist()):#check if a behaviour stops the start_behaviour
        stopB_time = row['Time']
        stop_behaviour = row['Value']
        total_seconds = (stopB_time - startB_time).total_seconds()
        # print("2nd IF : \n",start_behaviour,startB_time,row['Value'],row['Time'],str(start_behaviour)+str(row['Value']),total_seconds)
        dfdurations.loc[(dfdurations.SheepID == row['SheepID']) & (dfdurations.Date == row['Date']) , start_behaviour] += total_seconds
        dfdurations.loc[(dfdurations.SheepID == row['SheepID']) & (dfdurations.Date == row['Date']) , "Behaviours"] = str(start_behaviour) + "-" +str(stop_behaviour)
        start_behaviour = row['Value']
        startB_time = row['Time']
dfdurations = dfdurations.drop(['end',"Behaviours"], axis=1).set_index('Date')
print("non 0 values in points : \n",dfpoints.iloc[:,2:].astype(bool).sum(axis=0),dfpoints,"\n\n",dfdurations.iloc[:20,:13])
dfpoints.to_csv("Points.csv" , sep='\t' , encoding='utf-8')
dfdurations.to_csv("Durations.csv" , sep='\t' , encoding='utf-8')
