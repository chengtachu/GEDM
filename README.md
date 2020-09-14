
## General Electricity sector Decarbonization Model (GEDM)
GEDM is a Python package developed to estimate the capacity and generation mixes of technologies in large-scale electricity systems, with a focus on renewable energy. It consists of an electricity dispatch model and a capacity expansion model which are formulated as mathematical programming problems. A framework is developed to control the program flow, access an external solver, and convert input and output data. This tool offers flexibility in the structure of the electricity market considered, time-slices, time periods and time horizon configuration, and all assumptions can be modified.

### Main features
A model instance consists of a collection of CSV files that define the market structure, commodities/fuels, technologies/processes, resource potentials and assumptions and so on. This model framework imports these files, builds optimization problems, solves the problems, constructs result tables and exports to CSV files.

Key features of this framework:
- Flexibilities on structuring the model
- The integration of power system flexibility measures, e.g. storage system operation, interconnection and reserve services.
- The tests on system reliability with extreme supply and demand cases
- The dedicated input/output modules that convert the data into more readable table format
- The integration of VRE potential and hourly generation data based on an existing open access dataset provided by the author
- Freely available under the MIT license

This framework offers flexibility on configuring the following:
- market structure (market -> countries/districts -> zones)
- time-slices (for CE model up to 288)
- time period steps (the interval doesn't need to be constant)
- time horizon and base year
- most assumptions: techno-economic, fuel price, carbon cost, emission limits, development potentials etc.

---

### Requirements
GEDM has been tested on Windows. Running GEDM requires the following environment:
- the [Python3](https://www.python.org/downloads/release/python-368/) programming language (version 3.6 or greater)
- Python modules and their dependencies: [Numpy](https://github.com/numpy/numpy), [Pyomo](https://github.com/Pyomo/pyomo)
- installing a mathematical problem solver: GEDM has been tested with [GAMS](https://www.gams.com/) and [GLPK](https://www.gnu.org/software/glpk/) (It is possible to use other solvers in this framework if Pyomo supports the interface.)
- installing [Python API for GAMS](https://www.gams.com/latest/docs/API_PY_TUTORIAL.html) when using GAMS

### Getting started
Using this tool by following these steps:
1. install the requirements above
2. download or clone the GEDM repository
3. check the solver option file "/Input/1_model_config/01_SolverConfig.csv"
4. construct a case by editing the input files (you can start with the sample case)
5. run the model `$ Python scripts/GEDM.py`
6. check the output files

Users are expected to have experiences on Python. The main reason is that when infeasible solutions returned, the users may want greater control over the program flow and the models to find the causes, more than changing the settings and assumption. In addition, Pyomo and solvers may occasionally have compatible issues. It would require some Python experience and change the codes to solve it.

---

### Main components
The overall framework and program flow is shown below. The electricity dispatch (ED) model (md_main.py, md_ED_\*.py) deals with the generation dispatch decisions for all generators, taking into account operation constraints of conventional thermal plants and storage systems, variability of renewable generation, and inter-zone transmission. The ED model solves each daily dispatch problem individually. Essential outputs include CO2 emissions, fuel consumption, electricity flows, and cost etc.

The capacity expansion (CE) model (md_CE_\*.py) decides the optimal new installation investment in each time period step. The results will be fed to the ED model for dispatch optimization. A critical feature is the mechanism of identifying extreme cases for testing system reliability. Before the program builds the CE problem, this framework selects the most extreme supply and demand hour in each calendar month, i.e. the hour with the highest residual demand. Therefore, this model optimizes the problem with configured time-slices plus these 12 cases.

An input data processing module (impt_\*.py) is developed to convert the inputs according to the market structure, temporal resolution, time zone etc. Base year, time horizon, time periods and time-slices are configurable. The original system demand and renewable generation have to be given in hourly resolution to allow such conversion. Another data processing module is constructed to extract model solutions and convert the results into readable tables (\*_output.py) in CSV files.

![Program Flow](/img/program_flow.jpg)


### Formulation of the core models
The ED and CE models are the core components formulated into linear programming problems.
Details about the model formulation can be seen in [this document]().

---
### Input files and settings

Most settings and assumptions are separated from the codes. Users can freely design theirs models. The tables below summarize the purpose of the inputs files which set up the models.

**Model configuration**

folder path: /Input/1_model_config/
| File | Description |
| ------ | ------ |
| 01_SolverConfig.csv | Pyomo and solver options |
| 02_ModelConfig.csv | scenario and miscellaneous model assumptions |
| 03_YearStep.csv | time period steps |
| 04_TimeSlice_ED.csv | time-slice of the ED model |
| 05_TimeSlice_CE.csv | time-slice of the CE model |
| 11_MarketStruct.csv | define market structure (market > country/district > zone) |
| 21_CountryAssumpGroup.csv | define the main assumption groups to a country/district |
| 22_Zone_TimeZone.csv | set the time zone for each zone |

**Commodity/fuel assumptions**

folder path: /Input/2_commodity/
| File | Description |
| ------ | ------ |
| 01_MainCommodity.csv | define the main types of commodity |
| 02_CostGroup.csv | set the cost group of main types of commodity in each country/district |
| 03_CommodityCost.csv | set the cost projection of the commodity groups |

**Process/technology assumptions**

folder path: /Input/3_process/
| File | Description |
| ------ | ------ |
| 01_MainProcess.csv | define main default technologies, and their fuel type, operation mode and reserve provision |
| 02_Tech_coal.csv | set technical assumptions of coal-fired technologies |
| 02_Tech_gas.csv | set technical assumptions of gas-fired technologies |
| 02_Tech_other.csv | set technical assumptions of other technologies |
| 02_Tech_renewable.csv | set technical assumptions of renewable technologies |
| 03_Cost_coal.csv | set cost assumptions of coal-fired technologies |
| 03_Cost_gas.csv | set cost assumptions of gas-fired technologies |
| 03_Cost_other.csv | set cost assumptions of other technologies |
| 03_Cost_renewable.csv | set cost assumptions of renewable technologies |
| 04_Transmission.csv | set technical and cost assumptions of transmission links |

**Policy assumptions**

folder path: /Input/4_policy/
| File | Description |
| ------ | ------ |
| 01_RE_Target.csv | set specific renewables development target (for future model extension, currently not used) |
| 02_CarbonCost.csv | set carbon cost projections |
| 03_AncillaryService.csv | set ancillary service requirements (percentage to power demand) |
| 04_FixedNewBuild_dispatch.csv | set fixed new installation capacity of dispatchable technologies  |
| 05_CNS_EmissionLimits.csv | set the CO2 emissions limits in the CNS scenario  |
| /RE_MCP/\*.csv | set the optimal renewable mix projections of each country/district applied in MCP scenario |

**Existing capacity and calibration**

folder path: /Input/5_calibration/
| File | Description |
| ------ | ------ |
| 01_BaseYear_Generation.csv | generation and energy flow in base year (country/district) |
| /Zone_BaseYear_CF/\*.csv | capacity factor of dispatchable processes in the zones in base year |
| /Zone_Exist_Process/\*.csv | set the capacity and lifetime of existing processes in terrestrial zones |
| /Zone_Exist_Process_offshore/\*.csv | set the capacity and lifetime of existing processes in offshore zones |

**Transmission**

folder path: /Input/6_transmission/
| File | Description |
| ------ | ------ |
| 01_Zone_conn_base.csv | set transmission links: zone connection, length, base year capacity |
| 02_Zone_conn_base_offshore.csv | set offshore links: zone connection, length, base year capacity |

**Electricity demand profile**

folder path: /Input/7_demand/
| File | Description |
| ------ | ------ |
| /Zone_288/\*.csv | zonal demand profile projections in default 288 time-slices |
| /Zone_8760/\*.csv | zonal demand profile projections in hourly resolution |

**Renewables**

folder path: /Input/8_VRE/
| File | Description |
| ------ | ------ |
| 01_RE_Min_Install.csv | set minimum installation capacity of renewables by year |
| 02_RE_Max_Install.csv | set maximum installation capacity of renewables by year |
| 03_RE_Hydro_Max_Cap.csv | set maximum installation capacity of hydropower |
| 04_RE_Biomass_Max_Pot.csv | set maximum supply of total biofuel supply by year |
| /CF288/\*.csv | capacity factors of renewables in default 288 time-slices |
| /CF8760/\*.csv | capacity factors of renewables in hourly resolution |
| /DevLimit/\*.csv | maximum installation capacity of renewables by tranches |
| /SolarAreaLimit/\*.csv | maximum available areas for solar technologies deployment |

---
### Output files

The data processing module extracts solutions returned from the solver, summarizes the results, and exports as readable tables in CSV files. Every model instance has coorresponding output files. There are also files to summarize the results through the time horizon. 

/Output/(Country Code)/
| File | Description |
| ------ | ------ |
| 0_(Country Code)_ProcessGeneration.csv | annual generation from every processes and transmission links |
| 0_(Country Code)_Summary.csv | annual summary information on energy, capacity, fuel, emissions and cost |
| 0_(Country Code)_ZoneBalance.csv | annual energy supply, demand, spill and transmission in every zones |
| 0_(Country Code)_ZoneCapacity.csv | annual capacity by technologies and transmission links in every zones |
| 0_(Country Code)_ZoneInfo.csv | annual summary information on fuel, emissions and costs in every zones |
| (Year)_ED_ProcessOutput.csv | (ED model) generation from every processes and transmission links in specific year |
| (Year)_ED_ZoneBalance.csv | (ED model) energy supply, demand, spill and transmission in every zones in specific year |
| (Year)_ED_ZoneInfo.csv | (ED model) summary information on fuel consumption, emissions and costs in every zones in specific year |
| (Year)_CE_ProcessOutput.csv | (CE model) generation from every processes and transmission links in specific year |
| (Year)_CE_ZoneBalance.csv | (CE model) energy supply, demand, spill and transmission in every zones in specific year |
  
---
### License
This package is licensed under the [MIT License](/LICENSE).
