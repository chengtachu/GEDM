

## Input Files Description

### folder path: /Input/
---

### Renewable
#### folder path: /Input/8_VRE

###### &nbsp;
#### Renewable minimum addition
#### file: 01_RE_Min_Install.csv
Set minimum capacity addition of renewables in every period steps. Leave the cell empty to ignore the constraints. The constraints will be ignored in **MCP** scenario.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | countries/districts | country-wide assumption |
| Temporal resolution | annual |  |
| Unit | MW |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | country > renewable technologies | all output tranches of the a technology are aggregated |

###### &nbsp;
#### Renewable maximum addition
#### file: 02_RE_Max_Install.csv
Set minimum capacity addition of renewables in every period steps. Leave the cell empty to ignore the constraints. The constraints will be ignored in **MCP** scenario.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | countries/districts | country-wide assumption |
| Temporal resolution | annual |  |
| Unit | MW |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | country > renewable technologies | all output tranches of the a technology are aggregated |

###### &nbsp;
#### Hydropower maximum capacity
#### file: 03_RE_Hydro_Max_Cap.csv
Set maximum installation capacity of hydropower, applies on large and small hydropower counted together. 
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | countries/districts | country-wide assumption |
| Temporal resolution | NA |  |
| Unit | MW |  |
| Data in column | NA |  |
| Data in row | country |  |

###### &nbsp;
#### Biomass maximum supply
#### file: 04_RE_Biomass_Max_Pot.csv
Set maximum supply of biomass (only for power generation) in a country/district.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | countries/districts | country-wide assumption |
| Temporal resolution | annual |  |
| Unit | TJ |  |
| Data in column | time period steps | the periods is flexible, 5-years interval is suggested |
| Data in row | country |  |

###### &nbsp;
#### Renewable output profile (for default ED model)
#### file: /CF288/(zone code).csv
Renewable output profile in default 288 time-slices used in the ED model. Profiles are separated by output trahcnes. **All data is in GMT (UTC+0) time**.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones in a country/district |  |
| Temporal resolution | 288 time-slices |  |
| Unit | Capacity factor (0-1) |  |
| Data in column | zones > technologies > output tranches |  |
| Data in row | 288 time-slices | a day of 24 hours for each calendar month |

###### &nbsp;
#### Renewable output profile (8760 hourly)
#### file: /CF8760/(zone code).csv
Renewable output profile in hourly temporal resolution. Profiles are separated by output tranches. **All data is in GMT (UTC+0) time**.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones in a country/district |  |
| Temporal resolution | 8760 hours |  |
| Unit | Capacity factor (0-1) |  |
| Data in column | zones > technologies > output tranches |  |
| Data in row | 8760 hours |  |

###### &nbsp;
#### Renewable installation limits
#### file: /DevLimit/(country code).csv
Maximum installation capacity of renewables by tranches.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones in a country/district |  |
| Temporal resolution | NA |  |
| Unit | MW |  |
| Data in column | zones > technologies > output tranches |  |
| Data in row | assumptions from different sources | the program only imports the data row "**Cap_GEDM**" |

###### &nbsp;
#### Area for Solar technologies
#### file: /SolarAreaLimit/(country code).csv
Maximum available areas for solar technologies deployment.
| Table structure | Setting | Note |
| ------ | ------ | ------ |
| Spatial coverage | zones in a country/district |  |
| Temporal resolution | NA |  |
| Unit | Kilometer square |  |
| Data in column | single column |  |
| Data in row | zones in the country |  |



