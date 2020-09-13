
## Output File Description

### folder path: /Output/(Country Code)/
---

### Model results summaries - all time periods

#### 0_(Country Code)_ProcessGeneration.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | generation from every processes and transmission links |  |
| Spatial coverage | zones, country wide |  |
| Temporal resolution | time period steps |  |
| Data unit | GWh (annual) |  |
| Data in column | time period steps |  |
| Data in row | zone > technology > output |  |

#### 0_(Country Code)_Summary.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | summary information on energy, capacity, fuel, emissions and cost |  |
| Spatial coverage | single country/district |  |
| Temporal resolution | time period steps |  |
| Data unit | various (shown in the second column) |  |
| Data in column | time period steps |  |
| Data in row | various information on: electricity supply and demand, capacity by technology, fuel consumption, carbon emissions, annual cost, electricity generation by technology  |  |

#### 0_(Country Code)_ZoneBalance.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | energy supply, demand, spill and transmission |  |
| Spatial coverage | zones, country wide |  |
| Temporal resolution | time period steps |  |
| Data unit | GWh (annual) |  |
| Data in column | time period steps |  |
| Data in row | various information on (by zones): electricity demand, supply, spill, import and export  |  |

#### 0_(Country Code)_ZoneCapacity.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | capacity by technologies and transmission links |  |
| Spatial coverage | zones, country wide |  |
| Temporal resolution | time period steps |  |
| Data unit | MW (annual) |  |
| Data in column | time period steps |  |
| Data in row | zone > technology > output tranche  |  |

#### 0_(Country Code)_ZoneInfo.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | summary information on fuel, emissions and costs |  |
| Spatial coverage | zones, country wide |  |
| Temporal resolution | time period steps |  |
| Data unit | various (shown in the third column) |  |
| Data in column | time period steps |  |
| Data in row | zone > information on fuel consumption, emissions and costs  |  |

---

### Electricity dispatch model results

#### (Year)_ED_ProcessOutput.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | (ED model) generation from every processes and transmission links in specific year |  |
| Spatial coverage | zones, market wide |  |
| Temporal resolution | time-slices |  |
| Data unit | MW |  |
| Data in column | time-slices |  |
| Data in row | zone > technology > output/reserve services/transmission |  |

#### (Year)_ED_ZoneBalance.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | (ED model) energy supply, demand, spill and transmission in specific year |  |
| Spatial coverage | zones, market wide |  |
| Temporal resolution | time-slices |  |
| Data unit | GWh (representing hours aggregation) |  |
| Data in column | time-slices |  |
| Data in row | zone > information on: electricity demand, supply, spill, import and export  |  |

#### (Year)_ED_ZoneInfo.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | summary information on fuel consumption, emissions and costs in every zones in specific year |  |
| Spatial coverage | zones, market wide |  |
| Temporal resolution | time-slices |  |
| Data unit | various (shown in the third column) |  |
| Data in column | time-slices |  |
| Data in row | zone > information on fuel consumption, emissions and costs  |  |

---

### Capacity expansion model results

#### (Year)_CE_ProcessOutput.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | (CE model) generation from every processes and transmission links in specific year |  |
| Spatial coverage | zones, market wide |  |
| Temporal resolution | time-slices |  |
| Data unit | MW |  |
| Data in column | time-slices |  |
| Data in row | zone > technology > output/reserve services/transmission |  |

#### (Year)_CE_ZoneBalance.csv
| Item | Value | Note |
| ------ | ------ | ------ |
| Content | (CE model) energy supply, demand, spill and transmission in specific year |  |
| Spatial coverage | zones, market wide |  |
| Temporal resolution | time-slices |  |
| Data unit | GWh (representing hours aggregation) |  |
| Data in column | time-slices |  |
| Data in row | zone > information on: electricity demand, supply, spill, import and export  |  |

