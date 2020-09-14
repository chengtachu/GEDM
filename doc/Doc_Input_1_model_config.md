
## Input Files Description

### folder path: /Input/
---

### Model configuration
#### folder path: /Input/1_model_config

###### &nbsp;
#### Solver Configurations
#### file: 01_SolverConfig.csv
Pyomo and solver options. The options and values will be sent to the solver.
- The second data row is to set the solver. The default solver is "**gams**".
- There are two solver option groups: Pyomo option and Solver option. **Pyomo options** are the configurations on Pyomo. You can also send additional options to the solver with **Solver options**. Useful references: [Pyomo Solver Interfaces](https://pyomo.readthedocs.io/en/stable/library_reference/solvers/index.html), [GAMS Solver Options](https://www.gams.com/latest/docs/UG_SolverUsage.html)
- The second column "Item" is option name. The third column "Value" is the option value applied. 
- The options can be activate/deactivate by filling a "1 or 0" in the fourth column. Useful feature.
- **Be sure to create a cooresponding Pyomo file folder pointed to the Pyomo option "tmpdir"**.

###### &nbsp;
#### Model Configurations
#### file: 02_ModelConfig.csv
Addition model settings that are covered in other files.
| Item | Value (default) | Note |
| ------ | ------ | ------ |
| ReDevSen | DEF | Renewable development senario. **DEF**: default scenario; **MCP**: constraints applied on minimum capacity of every renewable options in every time periods, through the file at /Input/4_policy/RE_MCP70/; **CNS**: emissions limit, a ratio to base year, applied on every time period, through this file /Input/4_policy/05_CNS_EmissionLimits.csv |
| MinExistUnitCF | 0-1 (or empty) | **Minimum generation ratio** of existing generators in each time period step **compared to base year generation**. This minimum generation setting is to aviod unreasonable drop or surge of generation from existing generators. This setting link to base year generation assumption in **/Input/5_calibration/Zone_BaseYear_CF/**. The first argument is the base year. It is not recommend to set **1** for base year, because improper base year generation assumptions will make the problem unsolvable. This configuration can be applied up to 8 periods. However, they can be **left empty to ignore base year calibration**. |
| ImportPrice | 0.3 | Electricity import price in USD per kWh. The electricity **imports from other markets** are variables in the model. This can ensure most problem can be solvable, if there exists transmission links with other zones outside the current market. (This import **should not be confused with the transmission between the zones within the current market**.) |
| EnergySpillCost | 0.01 | Energy spill cost in USD per kWh. This parameter can reduce excessive spill in most cases. |

###### &nbsp;
#### Time Period Steps
#### file: 03_YearStep.csv
- one row; the second column is **base year**, other steps follow
- the step interval can be variable, e.g. 2015, 2018, 2020, 2022, 2025, 2030
- **make sure the setting in other assumption files can cover this time horizon** (the steps don't need to be aligned)

###### &nbsp;
#### Time-Slices in ED model
#### file: 04_TimeSlice_ED.csv
Currently, the time-slices in ED model is **fixed at 288**, as configured in this file.
It is possible to customize this setting, as it has been done for the CE model. However, this will require more work in developing a conversion mechanism if base year calibration is applied.

###### &nbsp;
#### Time-Slices in CE model
#### file: 05_TimeSlice_CE.csv
Users are free to restructure the time-slices. Starting from the existing example is recommended.
- time-slices in data row 
- column 1 TSIndex: index of time-slices **in numerical order**, integer 1 ~
- column 2 Month: use bracketed number to represent the month e.g. [2] or [4][5][6] or [12][1]
- column 3 Day: use bracketed number to represent the day of the month. The default value "**Weekday**" means no separation on the day of the month.
- column 4 Hour: use bracketed number to represent the hour in the day e.g. [0][1][2] or [18]
- column 5 DayIndex: index of the representative day in this time-slice configurations, **in numerical order**
- column 6 RepDayInYear: number of days this representative days represent in a year
- column 7 RepHoursInDay: number of hours this time-slice represents in its representative days
- column 8 RepHoursInYear: total representative hours of this time-slice in a year. The value equal to **RepDayInYear x RepHoursInDay**.

###### &nbsp;
#### Market Structure
#### file: 11_MarketStruct.csv
The modelling instance is on market basis. A market may consists of several countries/districts and sub-country zones. The smallest geographical representation area is defined as a “zone”. The hierarchy is: market > country/district > zone. 
- zones in data row 
- column 1 Country/District code
- column 2 Zone_Code: critical index, in the form "**(country code).(zone code)**", e.g. GBR.Scotland or GBR.OffRgn1
- column 3 Zone_Type: can only be Terrestrial or Offshore
- column 4 Market_Code: arbitrary name of this market

###### &nbsp;
#### Assumption Group
#### file: 21_CountryAssumpGroup.csv
Several assumptions are configured at country level, including techno-economic assumptions of the technologies, carbon cost projection, fuel costs and reserve requirements. Users should assign these assumptions in groups. The grouping allows changing the assumptions in a big market or region easier.
- country/district in data row 
- column 1 Country/District name (arbitrary)
- column 2 Country/District code
- column 3 Region (currently not used)
- column 4 TechCostGroup: techno-economic assumptions group
- column 5 CarbonCostGroup: carbon cost assumptions group
- column 6 AncillaryGroup: reserve services assumptions group

###### &nbsp;
#### Time Zone
#### file: 22_Zone_TimeZone.csv
set the time zone for every zone in the market. Note that all modelling work and the outputs is based on GMT time or UTC+0.
- zone in data row 
- column 1 Country/District code
- column 2 zone code
- column 3 time zone: a number **between -12 and 12**, the UTC time zone


