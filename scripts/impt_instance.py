#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions for import modelling instance settings
#

from numpy import genfromtxt

import cls_misc
import cls_process
import cls_country
import cls_market
import cls_zone
import impt_country


def get_SolverSettings(instance):
    """ get solver settings """
    
    instance.sSolver = ""
    instance.dicPyomoOption = {}
    instance.dicSolverOption = {}
    
    file_setting = "../Input/1_model_config/01_SolverConfig.csv"
    dt_data = genfromtxt(file_setting, dtype = str, skip_header=0, delimiter=',')
    for sSetting in dt_data:
        if sSetting[0] == "Solver":
            instance.sSolver = sSetting[2]
        elif sSetting[0] == "Pyomo options" and sSetting[3] == "1":
            instance.dicPyomoOption[sSetting[1]] = sSetting[2]
        elif sSetting[0] == "Solver options" and sSetting[3] == "1":
            instance.dicSolverOption[sSetting[1]] = sSetting[2]

    return instance


def get_ReDevScenario():
    """ get model scenario configuration """
    
    file_country = "../Input/1_model_config/02_ModelConfig.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter='#')
    sReDevSetting = "DEF"
    for sSetting in dt_data:
        if sSetting[0] == "ReDevSen":
            sReDevSetting = str(sSetting[1])

    return sReDevSetting


def get_AllYearSteps():
    """ get time period steps configurations  """
    
    file_country = "../Input/1_model_config/03_YearStep.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter=',')
    iYearSteps_YS = []
    for data in dt_data[1:]:
        iYearSteps_YS.append( int(data) )

    return iYearSteps_YS


def get_TimeSlice(sModelMode):
    """ get time-slice settings """
    
    file_country = ""
    if sModelMode == "ED":
        file_country = "../Input/1_model_config/04_TimeSlice_ED.csv"
    elif sModelMode == "CE":
        file_country = "../Input/1_model_config/05_TimeSlice_CE.csv"
        
    dt_data = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')
    
    lsTimeSlice = list()
    for row in dt_data:
        lsTimeSlice.append(cls_misc.TimeSlice(TSIndex=row[0], Month=row[1], Day=row[2], Hour=row[3], \
                                              DayIndex=row[4], RepDayInYear=row[5], RepHoursInDay=row[6], \
                                              RepHoursInYear=row[7]))
    return lsTimeSlice


def set_DayTimeSlice(lsTimeSlice):
    """ structure the time-slice by day """
    
    lsDayTimeSlice = list()
    iDayIndex = 0
    iDaySliceStart = 0
    iDaySliceEnd = 0

    while(iDaySliceStart < len(lsTimeSlice)):
        # find the first time-slice of a day
        sDay = ""
        for iIndex in range(iDaySliceStart, len(lsTimeSlice)):
            if lsTimeSlice[iIndex].iDayIndex == lsTimeSlice[iDaySliceStart].iDayIndex:
                iDaySliceEnd = iIndex
                sDay = lsTimeSlice[iIndex].sMonth + lsTimeSlice[iIndex].sDay
            else:
                break

        lsDayTimeSlice.append(cls_misc.DayTimeSlice( MonthDay = sDay, iDayIndex = iDayIndex ))
        iDayIndex = iDayIndex + 1

        for iIndex in range(iDaySliceStart, iDaySliceEnd+1):
            lsDayTimeSlice[-1].lsDiurnalTS.append(cls_misc.DiurnalTimeSlice( \
                          sTSIndex = lsTimeSlice[iIndex].sTSIndex, \
                          iTimeSliceIndex = iIndex, \
                          iRepHoursInYear = lsTimeSlice[iIndex].iRepHoursInYear, \
                          iRepHoursInDay = lsTimeSlice[iIndex].iRepHoursInDay ))
            
        # to next segement 
        iDaySliceStart = iDaySliceEnd + 1

    return lsDayTimeSlice


def get_CommodityDef():
    """ get commodity definition settings """
    
    file_country = "../Input/2_commodity/01_MainCommodity.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')
    
    lsCommodity = list()
    for row in dt_data:
        lsCommodity.append(cls_misc.Commodity(CommodityName=row[0],Category=row[1],HeatRate=row[2],\
                                              EmissionFactor_CO2=row[3]))
    return lsCommodity


def get_ProcessDef(iAllYearSteps_YS):
    """ get process definition settings """
    
    file_country = "../Input/3_process/01_MainProcess.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')
    
    lsProcessDef = list()
    for row in dt_data:
        lsProcessDef.append(cls_process.ProcessAssump(ProcessName=row[0], ProcessType=row[1], \
            ProcessFullName=row[2], Fuel=row[3], OperationMode=row[4], CCS=row[5], \
            AS_T1=row[6], AS_T2=row[7], AS_T3=row[8], iYS=len(iAllYearSteps_YS)))
    return lsProcessDef


def get_Market(instance):
    """ get market/zone structure and build a list market objects """
    
    lsMarket = list()

    file_country = "../Input/1_model_config/11_MarketStruct.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')
    
    file_zone = "../Input/1_model_config/22_Zone_TimeZone.csv"
    dt_zone = genfromtxt(file_zone, dtype = str, skip_header=1, delimiter=',')
    
    ### get the market structure of aggregated zones
    zone_market = []
    ind_column = 3  # market name
    for row in dt_data:
        if row[ind_column] not in zone_market:
            zone_market.append(str(row[ind_column]))

    # create market object
    for sMarket in zone_market:
        lsMarket.append(cls_market.Market(sMarket))

    ### create zone object      
    for row in dt_data:
        sCountry = str(row[0])
        sZone = str(row[1])
        sZoneType = str(row[2])
        zone_market = str(row[ind_column])

        # get time zone
        iTimeZone = 0
        for row_zone in dt_zone:
            if row_zone[1] == sZone:
                iTimeZone = int(float(row_zone[2]))   # receive as integer
                break

        for ind_market, objMarket in enumerate(lsMarket):
            if zone_market == objMarket.sMarket:
                if sZoneType == "Terrestrial":
                    objMarket.lsZone.append(cls_zone.Zone(sCountry, sZone, ind_market, iTimeZone))
                else:
                    objMarket.lsZoneOffs.append(cls_zone.ZoneOffs(sCountry, sZone, ind_market))
                break
    
    ### assign zoneID
    for objMarket in lsMarket:
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            objZone.sZoneID = objZone.sCountry + "Z" + str(ind_zone)
            
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            objZone.sZoneID = objZone.sCountry + "ZF" + str(ind_zone)
        
    return lsMarket


def get_Country(instance):
    """ get a list of country objects with index to their zones """

    file_country = "../Input/1_model_config/11_MarketStruct.csv"
    dt_Market = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')

    ### create country object
    country = []
    for row in dt_Market:
        if row[0] not in country:
            country.append(str(row[0]))

    lsCountry = list()
    
    file_country = "../Input/1_model_config/21_CountryAssumpGroup.csv"
    dt_country = genfromtxt(file_country, dtype = str, skip_header=1, delimiter=',')    

    # create country object
    for sCountry in country:

        TechCostGroup = ""
        CarbonCostGroup = ""
        AncillaryGroup = ""
        
        for row_country in dt_country:
            if row_country[1] == sCountry:
                # techno-ecomonic assumption group
                TechCostGroup = str(row_country[3])
                # carbon cost gruop
                CarbonCostGroup = str(row_country[4]) 
                # ancillary service group
                AncillaryGroup = str(row_country[5])
                break
        
        lsCountry.append(cls_country.Country(sCountry, TechCostGroup, CarbonCostGroup, AncillaryGroup))
          
    # update country index in zone
    for objMarket in instance.lsMarket:
        # terrestrial zones
        for objZone in objMarket.lsZone:
            for row in dt_Market:
                if row[1] == objZone.sZone:
                    country = row[0]
                    for ind_country, objCountry in enumerate(lsCountry):
                        if objCountry.sCountry == country:
                            objZone.iCountryIndex = ind_country
                            break
                    break
                
        # offshore zones
        for objZone in objMarket.lsZoneOffs:
            for row in dt_Market:
                if row[1] == objZone.sZone:
                    country = row[0]
                    for ind_country, objCountry in enumerate(lsCountry):
                        if objCountry.sCountry == country:
                            objZone.iCountryIndex = ind_country
                            break
                    break

    return lsCountry


def get_MinExistUnitCF():
    """ get setting of minimum CF of existing dispatchable units """
    
    file_country = "../Input/1_model_config/02_ModelConfig.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter='#')
    iMinCF = []
    for sSetting in dt_data:
        if sSetting[0] == "MinExistUnitCF":
            for iCol in range(1,9):
                if sSetting[iCol] != "":
                    iMinCF.append(float(sSetting[iCol]))

    return iMinCF


def get_ImportPrice():
    """ get electricity import price (import from other market) """
    
    file_country = "../Input/1_model_config/02_ModelConfig.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter='#')
    iImportPrice = 0.3
    for sSetting in dt_data:
        if sSetting[0] == "ImportPrice":
            iImportPrice = float(sSetting[1])

    return iImportPrice


def get_EnergySpillCost():
    """ get electricity spill cost """
    
    file_country = "../Input/1_model_config/02_ModelConfig.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter='#')
    iCost = 0.01
    for sSetting in dt_data:
        if sSetting[0] == "EnergySpillCost":
            iCost = float(sSetting[1])

    return iCost


def get_EmissionLimits(instance):
    """ get emission limits for CNS scenario """
    
    file_country = "../Input/4_policy/05_CNS_EmissionLimits.csv"
    dt_data = genfromtxt(file_country, dtype = str, skip_header=0, delimiter=',')
    # year step period in the original setting
    iOriginYear_OYS = dt_data[0, 1:]
    fYearSteps_YS = impt_country.ConvertAssumpYS(iOriginYear_OYS, dt_data[1, 1:], instance.iAllYearSteps_YS)
                
    return fYearSteps_YS

