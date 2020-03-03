# Animal Behavioural Analysis
Python scripts for animal behavioural analysis
## Discription
In this study a wide range of animal behaviours were scored on a daily base.
The goal of this program was to calculate the mean frequency of each behaviour per day of observations.

##Leopard
Observational data of two captive leopards was selected

######The basic input
A table of all the scored data including each individual, the date of the
observation and the behaviours that were scored together with the time they occurred.
The behaviours that were scored were divided in **point** and **duration** behaviours.
+**Point behaviours** are the behaviours that do not have a duration and thus their presence in the dataset automatically means that they occurred for one second.
+**Duration behavours** are the behaviour that may start at a specific time and finish at a different time
with point behaviours occurring in between.
------
For that the input of the program included a list of the
point behaviours and a table of all the duration behaviours indicating which of them do not overlap.
For each individual we received two tables. The first one included the frequency of the point
behaviours just by counting the times they were present and the second included the durations
behaviours and their frequency in seconds per day.
###Example
`
| Date        | Time           | Day  | START  | Behaviour  | Aggressive  | Stereotypic  |  Inactive  | Body posture  | Affiliative  | Activity  | Stress  | Marking  | Reproductive  | Exploratory  |  Maintenance   | Other  | Feeding  | Fear  | Focal end  |  Observer note |
| ------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|
| 12/3/2019      | 16:30:20 | Tuesday | Female |
| 12/3/2019      | 16:30:25      |   Tuesday | Male | Inactive |   |   | sleeping
														

`
