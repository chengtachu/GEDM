#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Insance class, functions to all import data
#

import impt_instance
import impt_country
import impt_zone


class Instance:
    """ simulation instance class """

    def __init__(self):
        """ import instance settings """
        
        # solver settings
        impt_instance.get_SolverSettings(self)
        
        # model senarios: "DEF", "MCP", "CNS"
        self.sPathway = impt_instance.get_ReDevScenario()

        # year steps (list of year, first value is base year)
        self.iAllYearSteps_YS = impt_instance.get_AllYearSteps()

        # time slice (Dispatch operation)
        self.lsTimeSlice = impt_instance.get_TimeSlice("ED")
        
        # time slice (capacity expansion)
        self.lsTimeSlice_CEP = impt_instance.get_TimeSlice("CE")
           
        # structure day time slice (Dispatch operation)
        self.lsDayTimeSlice = impt_instance.set_DayTimeSlice(self.lsTimeSlice)
        
        # structure day time slice (capacity expansion)
        self.lsDayTimeSlice_CEP = impt_instance.set_DayTimeSlice(self.lsTimeSlice_CEP)

        # energy commodity
        self.lsCommodity = impt_instance.get_CommodityDef()

        # process definition list
        self.lsProcessDefObjs = impt_instance.get_ProcessDef(self.iAllYearSteps_YS)

        # market structure
        self.lsMarket = impt_instance.get_Market(self)
        
        # country structure
        self.lsCountry = impt_instance.get_Country(self)
        
        ### other settings
        self.iMinExistUnitCF = impt_instance.get_MinExistUnitCF()
        self.iImportPrice = impt_instance.get_ImportPrice()
        self.iSpillCost = impt_instance.get_EnergySpillCost()
        
        # emission limits for CNS mode
        if self.sPathway  == "CNS":
            self.fEmissoinLimits_YS = impt_instance.get_EmissionLimits(self)

        return


    def get_CountryAssumption(self):
        """ get configurations on country level """
                        
        # import country techno-economic assumptions
        impt_country.get_CountryTechCostAssump(self)
        
        # commodity cost assumption
        impt_country.get_CountryCommodityAssump(self)
        
        # policy and new tech limit
        impt_country.get_CountryPolicyAndTechAssump(self)
        
        # base year data (only own use and loss are used now)
        impt_country.get_CountryBaseYearData(self)
                     
        # renewable installation limits
        impt_country.get_CountryRenInstallLimit(self)
        
        # hydropower capacity limits
        impt_country.get_CountryHydroCapLimit(self)
        
        # availalbe biomass by projection
        impt_country.get_CountryBiomassLimit(self)
                
        return


    def get_MarketSettings(self):
        """ get configurations on market level """
                        
        for objMarket in self.lsMarket:
            
            # transmission connection structure
            impt_country.get_MarketTransmission(self, objMarket)
            
            # transmission assumptions
            impt_country.get_TransTechEcoAssump(self, objMarket)
            
        return


    def get_ZoneAssumption(self):
        """ get assumptions on zone level """
                    
        for objMarket in self.lsMarket:
            
            for objZone in objMarket.lsZone:
                
                # import demand profile
                impt_zone.get_DemandProfile(self, objZone)
                
                # import demand profile 8760hr
                impt_zone.get_DemandProfile_8760(self, objZone)

                # import demand profile
                impt_zone.get_DemandProfile_CEP(self, objZone)

                ##### do not move the sequence of the following functions
                
                # copy process assumption, set up renewable development limit, capacity factor
                impt_zone.get_ZoneProcessAssump(self, objZone)
                
                # PV available land limit
                impt_zone.get_ZonePVLandLimit(self, objZone)
                
                # import existing processe
                impt_zone.get_ZoneExistingProcess(self, objZone)
                
                # import base year dispatchable unit CF
                impt_zone.get_ZoneProcessDispBaseCF(self, objZone)                    
                
                # model CP 70% renewable development pathway
                impt_zone.get_ZoneMCPPathway(self, objZone)
                
            for objZone in objMarket.lsZoneOffs:
                
                # copy process assumption, set up renewable development limit, capacity factor
                impt_zone.get_ZoneProcessAssump_offs(self, objZone)
                
                # import existing processe
                impt_zone.get_ZoneExistingProcess_offs(self, objZone)
                
                # model CP 70% renewable development pathway
                impt_zone.get_ZoneMCPPathway(self, objZone)
                    
        return

