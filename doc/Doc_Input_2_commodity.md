
## Input Files Description

### folder path: /Input/
---

### Commodity/fuel assumptions
#### folder path: /Input/2_commodity

###### &nbsp;
#### Main Commodity
#### file: 001_MainCommodity.csv
Define the main fuel categories in the model.
- commodity/fuel in data row 
- column 1 Commodity Name
- column 2 Category
- column 3 Heat Rate (currently not used)
- column 4 CO2 Emission Factor, in MTon/PJ (=kg/MJ)
- column 5 Default unit in the model

###### &nbsp;
#### Cost Group
#### file: 02_CostGroup.csv
Assign cost group by fuel category to each country/district.
- country/district in data row 
- column 1 Country/District name (arbitrary)
- column 2 Country/District code
- column 3 cost group - oil
- column 4 cost group - coal
- column 5 cost group - uranium
- column 6 cost group - biomass (for power generation only)

###### &nbsp;
#### Commodity Cost
#### file: 03_CommodityCost.csv
Assumptions on fuel cost projections associated to the cost groups.
| Item | Value | Note |
| ------ | ------ | ------ |
| Spatial coverage | cost groups assigned to each country in the market |  |
| Temporal resolution | annual value |  |
| Unit | USD/GJ |  |
| Data in column | time period steps | cover the time horizon, longer projection is recommended |
| Data in row | cost groups |  |

