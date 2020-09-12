#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to initialize instance settings
#


#----------------------------------------------------
# sets
#----------------------------------------------------

def getCountryIndList(objMarket):
    """ get country index list in the market """
        
    lsCountryList = list()
    for objZone in objMarket.lsZone:
        if objZone.iCountryIndex not in lsCountryList:
            lsCountryList.append(objZone.iCountryIndex )
        
    return lsCountryList


def getCountryCodeList(objMarket):
    """ get country code list in the market """
        
    lsCountryList = list()
    for objZone in objMarket.lsZone:
        if objZone.sCountry not in lsCountryList:
            lsCountryList.append(objZone.sCountry )
        
    return lsCountryList


#----------------------------------------------------
# Fixed Parameters
#----------------------------------------------------

def getZonesInCountry(objMarket, model):
    '''  get TS representing hours in a year '''
    
    dData = {}
    for sCountry in model.setCountryCode_CN:
        sZoneList = ""
        for objZone in objMarket.lsZone:
            if objZone.sCountry == sCountry:
                sZoneList = sZoneList + objZone.sZoneID + ";"
        dData[sCountry] = sZoneList
        
    return dData

##### time slice #####   
def getTSRepHourYear(instance, model):
    '''  get TS representing hours in a year '''
    dData = {}
    for objTS in instance.lsTimeSlice:
        dData[objTS.sTSIndex] = objTS.iRepHoursInYear        
    return dData


def getTSRepHourDay(instance, model):
    '''  get TS representing hours in a day '''
    dData = {}
    for objTS in instance.lsTimeSlice:
        dData[objTS.sTSIndex] = objTS.iRepHoursInDay    
    return dData

def getTSRepHourYear_CE(instance, model):
    '''  get TS representing hours in a year, for CE model '''
    dData = {}
    for objTS in instance.lsTimeSlice_CEP:
        dData[objTS.sTSIndex] = objTS.iRepHoursInYear        
    return dData


def getTSRepHourDay_CE(instance, model):
    '''  get TS representing hours in a day, for CE model '''
    dData = {}
    for objTS in instance.lsTimeSlice_CEP:
        dData[objTS.sTSIndex] = objTS.iRepHoursInDay    
    return dData


def getTSIndInDay(instance, model):
    '''  get the set of index of the TS in a day '''
    
    dData = {}
    for sDay_DY in model.setDay_DY:
        TSIndlist = ""
        for objTS in instance.lsTimeSlice:
            if (objTS.sMonth + objTS.sDay) == sDay_DY:
                TSIndlist = TSIndlist + objTS.sTSIndex + ";"
                
        TSIndlist = TSIndlist[0:-1]  # remove the last ";"
        
        dData[sDay_DY] = TSIndlist
        
    return dData


def getTSIndInDay_CE(instance, model):
    '''  get the set of index of the TS in a day, for CE model '''
    
    dData = {}
    for sDay_DY in model.setDay_DY:
        TSIndlist = ""
        for objTS in instance.lsTimeSlice_CEP:
            if (objTS.sMonth + objTS.sDay) == sDay_DY:
                TSIndlist = TSIndlist + objTS.sTSIndex + ";"
                
        TSIndlist = TSIndlist[0:-1]  # remove the last ";"
        
        dData[sDay_DY] = TSIndlist
        
    return dData


def getTSRepHourYear_Day(model, objDayTS):
    '''  get the TS representing hours in a year '''
    
    dData = {}
    for objTS in objDayTS.lsDiurnalTS:
        dData[objTS.sTSIndex] = objTS.iRepHoursInYear
        
    return dData


def getTSRepHourDay_Day(model, objDayTS):
    '''  get the TS representing hours in a day '''
    
    dData = {}
    for objTS in objDayTS.lsDiurnalTS:
        dData[objTS.sTSIndex] = objTS.iRepHoursInDay
        
    return dData


#----------------------------------------------------
# Transmission Parameters
#----------------------------------------------------  
    
def getTransCapacity(model, objMarket, iYear):
    ''' get transmission capacity of terrestrial links '''
    
    dData = {}
    for sTrans in model.setTransLDZ_TRL:
        for objTrans in objMarket.lsTrans:
            if objTrans.sTransID == sTrans:
                if iYear in objTrans.dicTransAccCap_YS:
                    dData[sTrans] = objTrans.dicTransAccCap_YS[iYear]
                else:
                    dData[sTrans] = 0
                break
    return dData


def getTransCapacityOffs(model, objMarket, iYear):
    ''' get transmission capacity of offhsore links '''
    
    dData = {}
    for sTrans in model.setTransOFZ_TRF:
        for objTrans in objMarket.lsTrans_off:
            if objTrans.sTransID == sTrans:
                if iYear in objTrans.dicTransAccCap_YS:
                    dData[sTrans] = objTrans.dicTransAccCap_YS[iYear]
                else:
                    dData[sTrans] = 0
                break
    return dData


def getTransLoss(model, objMarket, ind_year):
    ''' get transmission loss of terrestrial links '''
    
    dData = {}
    for sTrans in model.setTransLDZ_TRL:
        for objTrans in objMarket.lsTrans:
            if objTrans.sTransID == sTrans:
                if objTrans.fDistance > 600:  
                    # HVDC 600km as break point
                    dData[sTrans] = (objTrans.fDistance / 1000 * objMarket.lsDCLineLoss[ind_year] / 100) \
                        + (objMarket.lsDCConvLoss[ind_year] / 100)
                else:
                    # line loss of HVAC lines
                    dData[sTrans] = objTrans.fDistance / 1000 * objMarket.lsACLineLoss[ind_year] / 100
                break
    return dData


def getTransLossOffs(model, objMarket, ind_year):
    ''' get transmission loss of offshore links '''
    
    dData = {}
    for sTrans in model.setTransOFZ_TRF:
        for objTrans in objMarket.lsTrans_off:
            if objTrans.sTransID == sTrans:
                # assume all HCAV
                dData[sTrans] = (objTrans.fDistance / 1000 * objMarket.lsDCLineLoss[ind_year] / 100) \
                        + (objMarket.lsDCConvLoss[ind_year] / 100)
                break
    return dData


def getTransCost(model, objMarket, ind_year):
    ''' get transmission cost of terrestrial links '''
    
    ##### cost assumptions #####
    HVAC_CAPEX = objMarket.lsACCapex[ind_year]                  # USD per kW km
    HVAC_OPEX = objMarket.lsACOpex[ind_year]                    # USD per kW km
    HVDC_CAPEX = objMarket.lsDCCapex[ind_year]                  # USD per kW km
    HVDC_OPEX = objMarket.lsDCOpex[ind_year]                    # USD per kW km
    HVDC_CAPEX_converter = objMarket.lsDCCapexConv[ind_year]    # USD per kW
    HVDC_OPEX_converter = objMarket.lsDCOpexConv[ind_year]      # USD per kW
    CRF = objMarket.lsCRF[ind_year] / 100  # lifetime 50 years, discount rate 5%
    
    dData = {}
    for sTrans in model.setTransLDZ_TRL:
        for objTrans in objMarket.lsTrans:
            if objTrans.sTransID == sTrans:
                distance = objTrans.fDistance
                if distance > 0:
                    CostPerMW = 0
                    if distance > 600:  # HVDC   600km as break point
                        # annual cost per MW
                        CostPerMW = distance * (HVDC_CAPEX*CRF + HVDC_OPEX) * 1000
                        # converter cost per MW
                        CostPerMW = CostPerMW + ( (HVDC_CAPEX_converter*CRF + HVDC_OPEX_converter) * 1000 )
                        # change unit from USD per MW to M.USD per MW
                        CostPerMW = CostPerMW / 1000000
                        
                    else:   # HVAC
                        # annual cost per MW
                        CostPerMW = distance * (HVAC_CAPEX*CRF + HVAC_OPEX) * 1000
                        # change unit from USD per MW to M.USD per MW
                        CostPerMW = CostPerMW / 1000000
                        
                    dData[sTrans] = CostPerMW
                else:
                    dData[sTrans] = 9999
                break
    return dData


def getTransCostOffs(model, objMarket, ind_year):
    ''' get transmission cost of offshore links '''
    
    ##### cost assumptions #####
    HVDC_CAPEX = objMarket.lsDCCapex[ind_year]                  # USD per kW km
    HVDC_OPEX = objMarket.lsDCOpex[ind_year]                    # USD per kW km
    HVDC_CAPEX_converter = objMarket.lsDCCapexConv[ind_year]    # USD per kW
    HVDC_OPEX_converter = objMarket.lsDCOpexConv[ind_year]      # USD per kW
    CRF = objMarket.lsCRF[ind_year] / 100  # lifetime 50 years, discount rate 5%
    
    dData = {}
    for sTrans in model.setTransOFZ_TRF:
        for objTrans in objMarket.lsTrans_off:
            if objTrans.sTransID == sTrans:
                distance = objTrans.fDistance
                if distance > 0:
                    CostPerMW = 0
                    # annual cost per MW
                    CostPerMW = distance * (HVDC_CAPEX*CRF + HVDC_OPEX) * 1000
                    # converter cost per MW
                    CostPerMW = CostPerMW + ( (HVDC_CAPEX_converter*CRF + HVDC_OPEX_converter) * 1000 )
                    # change unit from USD per MW to M.USD per MW
                    CostPerMW = CostPerMW / 1000000 
                    dData[sTrans] = CostPerMW
                else:
                    dData[sTrans] = 9999
                break
    return dData

