
## Input Files Description

### folder path: /Input/
---

### Calibration
#### folder path: /Input/5_calibration

###### &nbsp;
#### Base year calibration
#### file: 01_BaseYear_Generation.csv
Generation and energy flow in the countries/districts in base year. This input was used in a base year calibration model which produces the base year output for every types of dispatchable processes. **Most data are not used in current models**, except for the last two columns: "**industry own use**" and "**losses**" which are used to derive the power demand from end-use side.  

###### &nbsp;
#### Base year output (dispatchable generators)
#### file: /Zone_BaseYear_CF/(country code).csv
The assumptions on the output (capacity factor) from dispatchable technologies in base year. The assumptions are **crucial to keep the resulting generation mix and fuel consumptions consistent with historical records**. It also has influence on a few following period steps if the **Minimum generation ratio** of existing generators is configured in 02_ModelConfig.csv.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones in the market |  |
| Temporal resolution | time-slices |  |
| Unit | 0-1 | capacity factor |
| Data in column | time-slices |  |
| Data in row | zones > dispatchable processes | existing processes in the zones |

###### &nbsp;
#### Existing Process - terrestrial zone
#### file: /Zone_Exist_Process/(zone code).csv
Set the capacity and commission time of existing processes in terrestrial zones. The capacity of existing processes are aggregated into 5-years periods according to their commission time. This table indicates the capacity mix in a zone in base year, and the expected retire time of existing processes.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | one zone |  |
| Temporal resolution | 5-years periods |  |
| Unit | MW |  |
| Data in column | 5-years periods | from 1950 to 2020 |
| Data in row | processes | existing processes |

###### &nbsp;
#### Existing Process - offshore zone
#### file: /Zone_Exist_Process_offshore/(zone code).csv
Set the capacity and commission time of existing processes in offshore zones. The capacity of existing processes are aggregated into 5-years periods according to their commission time. This table indicates the capacity mix in a zone in base year, and the expected retire time of existing processes.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | one zone |  |
| Temporal resolution | 5-years periods |  |
| Unit | MW |  |
| Data in column | 5-years periods | from 1950 to 2020 |
| Data in row | processes | existing processes |


