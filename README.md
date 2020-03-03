# Animal Behavioural Analysis
Python scripts for animal behavioural analysis
## Discription
In this study a wide range of animal behaviours were scored on a daily base.
The goal of this program was to calculate the mean frequency of each behaviour per day of observations.

###The basic input
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

##Leopard
Observational data of two captive leopards was selected.
##Sheep
Observational data of a group of sheeps.

###Input Examples
1. Dataset

`
| Date        | Time           | Day  | START  | Behaviour  | Aggressive  | Stereotypic  |  Inactive  | Body posture  | Affiliative  | Activity  | Stress  | Marking  | Reproductive  | Exploratory  |  Maintenance   | Other  | Feeding  | Fear  | Focal end  |  Observer note |
| ------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|
| 12/3/2018      | 16:30:20 | Monday | Female |
| 12/3/2018      | 16:30:25      |  Monday | Male | Inactive |   |   | sleeping

`

`
| Date        | Time           | START  | Other  | Activity  | Affiliative  | Aggressive  |  Body posture  | Object  | Fear  | Feeding  | Inactive  | Maintenance  | Reproductive  | Focal end |
| ------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|------------- |:-------------:| -----:|
| 16/1/2020      | 10:31:24 | 2150 |
| 16/1/2020      | 10:31:27      |   2150 |  | Walking |

`
***

2. Points and Durations

`
| Point |
| ------------- |
| standing |
| Walking |
| Running |
| Trotting |
| Circling |
| urinate |
| tail wave |
| ears back |
| ears erect |
| ears flat |
| lick object |
| object sniff |
| observing |
| attention to man |
| attention to sheep |
| Leap |
| Foot stamp |
| Turn back |
| object eat |
| defecate |

`
`
| Walking        | Running  | Trotting  | Circling  |
| ------------- |:-------------:| -----:|------------- |
| standing  | standing | standing | standing |
| Running   | Walking      |   Walking |  | Walking |
| Trotting  | Trotting | Running | Running |
| Circling   | Circling      |   Circling |  | Circling |
| Walking  | Running | Trotting | Circling |
`
