
## Input Files Description

### folder path: /Input/
---

### Power Demand Profile
#### folder path: /Input/7_demand

###### &nbsp;
#### Zone power demand (for default ED model)
#### file: /Zone_288/(zone code).csv
Zonal power demand profile projections in default 288 time-slices used in the ED model. This is **end-use power demand** derived from the end-use sectors. **All data in local time**.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | one zone |  |
| Temporal resolution | 288 time-slices  |  |
| Unit | MW |  |
| Data in column | time period steps |  |
| Data in row | 288 time-slices | a day of 24 hours for each calendar month |

###### &nbsp;
#### Zone power demand (8760 hourly)
#### file: /Zone_8760/(zone code).csv
Zonal power demand profile projections in hourly temporal resolution. This is **end-use power demand** derived from the end-use sectors. The first column is for indexing. **All data in local time**.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | one zone |  |
| Temporal resolution | 8760 hours |  |
| Unit | MW |  |
| Data in column | time period steps |  |
| Data in row | 8760 hours |  |






