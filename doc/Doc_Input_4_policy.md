
## Input Files Description

### folder path: /Input/
---

### Policy Assumptions
#### folder path: /Input/4_policy

###### &nbsp;
#### Renewables development target
#### file: 01_RE_Target.csv
Set specific renewables development target (for future model extension, **currently not used**)
- specific renewables target in a zone as data row 
- column 1: Country/District Code
- column 2: Zone Code
- column 3: Target type - "**Percentage**": percentage to total supply; "**Generation**": absolute generation; "**Capacity**": absolute capacity. 
- column 4: Process type
- column 5: Year - reach the target at this year
- column 6: Value - "**Percentage**": 0 - 100; "**Generation**": value in GWh; "**Capacity**": value in MW.

###### &nbsp;
#### Carbon Cost
#### file: 02_CarbonCost.csv
Set carbon cost projections for each cost group.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | assumption groups assigned to each country in the market |  |
| Temporal resolution | annual value |  |
| Unit | USD/tCO2e |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | carbon cost groups |  |

###### &nbsp;
#### Ancillary services (reserve services)
#### file: 03_AncillaryService.csv
Set the requirements of reserve services, which is  a percentage to power demand.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | assumption groups assigned to each country in the market |  |
| Temporal resolution | annual value |  |
| Unit | % |  normally between 0-10 |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | assumption groups > reserve types | three reserve types: "Primary", "Secondary" and "Tertiary". Their requirements on response time is configurable in the third column. |

###### &nbsp;
#### Fixed new installation for dispatchable technologies
#### file: 04_FixedNewBuild_dispatch.csv
Set fixed new installation capacity for dispatchable technologies for every period steps. An approach to consider technology readiness or political decisions. For example CCS power plant will not be commercially available in most country before 2025, and some countries have determined to be nuclear-free in the future. **If the value is empty, the model ignores this constraints. If the value if set 0, no new installation allowed at the year.** 
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | countries/districts |  |
| Temporal resolution | annual value |  |
| Unit | MW |  |
| Data in column | **specific year step** | **The constraints applied only when the year columns here match the time period steps**. |
| Data in row | country > technology |  |

###### &nbsp;
#### CO2 emission limits
#### file: 04_FixedNewBuild_dispatch.csv
Set the CO2 emissions limits in the **CNS** scenario. The default **DEF** scenario does not apply this restriction. This limit is market-wide. Countries in the market may have different level of contribution.  
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | market-wide |  |
| Temporal resolution | annual value |  |
| Unit | % | compared to base year emissions |
| Data in column | time period steps |  |
| Data in row | one market | only one row |

###### &nbsp;
#### Fixed new installation for renewable technologies
#### file: /RE_MCP/\*.csv
Set fixed new installation capacity for renewable technologies for every period steps. The constraints are only applied in **MCP** scenario. The data row should include every renewable options in the zones. 
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones |  |
| Temporal resolution | annual value |  |
| Unit | MW |  |
| Data in column | time period steps |  |
| Data in row | zone > technology |  |


