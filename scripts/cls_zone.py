#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Define zone class
#


class Zone:
    """ terrestrial zone class  """

    def __init__(self, sCountry, Zone, ind_market, iTimeZone):
        self.sZone = Zone
        self.sZoneID = ""
        self.sCountry = sCountry
        self.iTimeZone = iTimeZone
        self.iCountryIndex = -1
        self.iMarketIndex = ind_market
        # list of process assumption in this zone
        self.lsProcessAssump = list()   
        # list of exist process in current modelling instance
        self.lsProcess = list()         

        ### assumptions
        # all demand were calibrated and adjusted with base year induestry use and losses
        # all demand were converted to UTC+0 time
        self.fPowerDemand_TS_YS = []    # MW, for dispatch operatoin
        self.fPowerDemand_CEP_YS = []   # MW, for capacity expansion
        self.fPowerDemand_CEP_RT = []   # MW, testing extreme cases in CE, update in each period
        self.fPowerDemand_8760_YS = []  # MW, original annual hourly data
        self.fPVLandLimit = 0           # km2 
        
        # target capacity of renewables in each period in MCP scenario 
        self.dicMCP70RenewPathway_RE_YS = {}       
        
        return


class ZoneOffs:
    """ offshore zone class  """

    def __init__(self, sCountry, Zone, ind_market):
        self.sZone = Zone
        self.sZoneID = ""
        self.sCountry = sCountry
        self.iCountryIndex = -1
        self.iMarketIndex = ind_market
        # list of process assumption in this zone
        self.lsProcessAssump = list()  
        # list of exist process in current modelling
        self.lsProcess = list()         
        
        # target capacity of renewables in each period in MCP scenario 
        self.dicMCP70RenewPathway_RE_YS = {}       
        
        return





