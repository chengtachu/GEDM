#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Define country class
#


class Country:
    """ country class  """

    def __init__(self, Country, TechCostGroup, CarbonCostGroup, AncillaryGroup):
        
        self.sCountry = Country
        self.sZone_ZN = list()          # list of zone ID in this country
        self.lsProcessAssump = list()   # list of process in this country
        
        self.sTechCostGroup = TechCostGroup
        self.sCarbonCostGroup = CarbonCostGroup
        self.sAncillaryGroup = AncillaryGroup
        self.CountryOutput = CountryOutput()
        
        self.lsCommodity = list()       # a list of commodity in the country
        
        # policy requirement
        self.fCarbonCost_YS = list()    # USD/tCO2e
        self.fASFirst_YS = list()       # 0-1, percentage to power demand
        self.fASSecond_YS = list()      # 0-1, percentage to power demand
        self.fASThird_YS = list()       # 0-1, percentage to power demand

        # RE policy target (country level)
        # [Zone_Code, Target_type, Process_type, Year, Value]
        #self.lsRenewableTarget = list()
        
        # base year data  # MW
        self.dicBaseYearData = {}
        
        # renewable minimum installation MW
        self.dicRenMinInstall = {}
        # renewable maximum installation MW
        self.dicRenMaxInstall = {}
        
        # hydropower capacity limit MW
        self.fTotalHydroCapLimit = 0
        
        # available biomass in TJ
        self.fBiomassLimit_YS = []
        
        # max renewable capacity addition  # MW
        self.dicRenewMaxCapAdd = {}
        # min renewable capacity addition  # MW
        self.dicRenewMinCapAdd = {}
                
        return
    
    
class CountryOutput:
    """ a class defines result data of a country """
    
    def __init__(self):

        self.dicGenCapacity_YS_PR = {}
        self.dicGenNewCapacity_YS_PR = {}

        self.dicPowerGen_YS_TS_PR = {}
        self.dicPowerOutput_YS_TS_PR = {}
        self.dicHeatGen_YS_TS_PR = {}
        self.dicHeatOutput_YS_TS_PR = {}
        self.dicStrgInput_YS_TS_ST = {}
        self.dicStrgOutput_YS_TS_ST = {}

        self.dicFuelConsum_YS_TS_PR = {}

        self.dicAncSerRegulation_YS_TS = {}
        self.dicAncSer10MinReserve_YS_TS = {}
        self.dicAncSer30MinReserve_YS_TS = {}

        self.dicPctCapacityCommit_YS_TS_PR = {}
        self.dicPctCapacityGenerate_YS_TS_PR = {}
        self.dicPctCapacityAncSer_YS_TS_PR = {}
        
        ## transmission
        self.dicCrossBorderTrading_YS_TS = {}
        self.dicDomesticTrading_YS_TS = {}

        ##### model endogenous output

        self.dicCountryPowerOutput_YS_TS = {}
        self.dicCountryPowerGen_YS_TS = {}
        self.dicCountryHeatOutput_YS_TS = {}
        self.dicCountryHeatGen_YS_TS = {}
        self.dicProcessLCOE_YS_PR = {}
        self.dicPowerGenCost_YS_TS = {}
        self.dicPowerWholeSalePrice_YS_TS = {}

        self.dicCO2Emission_YS = {}
        self.dicCO2Emission_YS_TS = {}
        self.dicEmissionCaptured_YS_TS = {}
        self.dicFuelConsum_YS_TS_CM = {}        

        return

