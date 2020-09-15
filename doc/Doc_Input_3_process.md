
## Input Files Description

### folder path: /Input/
---

### Process/technology assumptions
#### folder path: /Input/3_process

###### &nbsp;
#### Define Process/technology
#### file: 01_MainProcess.csv
Define the main processes/technologies in the model.
- Process/technology in data row 
- column 1: Process Name (key index)
- column 2: Process Type
- column 3: Process Full Name (not used in the modelling)
- column 4: Fuel - associated with fuel category
- column 5: Operation Mode - "Dispatch", "NonDispatch" or "Storage"
- column 6: CCS - enable (0 or 1) carbon capture and sequestration integration
- column 7: AS_T1 - enable (0 or 1) tier one ancillary service
- column 8: AS_T2 - enable (0 or 1) tier two ancillary service
- column 9: AS_T3 - enable (0 or 1) tier three ancillary service

###### &nbsp;
#### Technical Assumptions
#### file: 02_Tech_\*.csv
The technical assumptions of the tech-cost groups.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | tech-cost groups assigned to each country in the market |  |
| Temporal resolution | annual value |  |
| Unit | various, shown in the fourth column |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | technology > tech-cost group > assumptions\* |  |

\* The necessary assumptions are: **UnitCapacity**: capacity of a single generator; **Gross_Eff**: gross efficiency of power generation; **RampRate**: power ramp rate of the generator; **EquAvailFactor**: equivalent available factor; **AuxiliaryCon**: auxiliary consumption; **CaptureRate**(SSC only): CCS capture rate; **Duration**(storage technology only): storage system duration hour;

###### &nbsp;
#### Cost Assumptions
#### file: 03_Cost_\*.csv
The cost assumptions of the tech-cost groups.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | tech-cost groups assigned to each country in the market |  |
| Temporal resolution | annual value |  |
| Unit | various, shown in the fourth column |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | technology > tech-cost group > assumptions\* |  |

\* The necessary assumptions are: **CAPEX**: capital cost; **OPEX**: fixed operation and maintenance cost; **varOPEX**: variable operation and maintenance cost; **Lifetime**: service life of a generator; 

###### &nbsp;
#### Technical and Cost Assumptions of Transmission
#### file: 04_Transmission.csv
An universal technical and cost assumptions of transmission applied in the model. The items listed in the sample file are all necessary, though the projection value is changeable.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | NA |  |
| Temporal resolution | annual value |  |
| Unit | various, shown in the third column |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | assumption items | transmission losses, converter losses, CAPEX, OPEX |


