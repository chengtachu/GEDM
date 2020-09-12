#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions for import settings at country level
#

from copy import deepcopy
from numpy import genfromtxt, vstack

import cls_misc


def get_CountryTechCostAssump(instance):
    ''' import technical and cost assumptions at country level '''
    # technology assumptions at country level
    # object inherit from base processes
            
    # copy the default instance setting
    for country in instance.lsCountry:
        country.lsProcessAssump = deepcopy(instance.lsProcessDefObjs)
    
    ### import technical assumptions
    
    techno_economic = []    
    file_process = "../Input/3_process/02_Tech_coal.csv"
    techno_economic = genfromtxt(file_process, dtype = str, skip_header=0, delimiter=',')
    
    file_process = "../Input/3_process/02_Tech_gas.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                    dtype = str, skip_header=1, delimiter=',')) )
    
    file_process = "../Input/3_process/02_Tech_other.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                    dtype = str, skip_header=1, delimiter=',')) )
    
    file_process = "../Input/3_process/02_Tech_renewable.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                    dtype = str, skip_header=1, delimiter=',')) )

    # year step period in the original setting
    iOriginYear_OYS = techno_economic[0, 4:]

    for country in instance.lsCountry:
        for process in country.lsProcessAssump:
            sProcessName = process.sProcessName
            sRegionGroup = country.sTechCostGroup
            
            bProcessFlag = False
            for assumption in techno_economic:
                if sProcessName == assumption[0]: 
                    bProcessFlag = True
                    
                    if sRegionGroup == assumption[1]:
                        
                        if assumption[2] == "UnitCapacity":
                            process.iUnitCapacity = assumption[4]
                        
                        elif assumption[2] == "Gross_Eff":
                            process.fGrossEff_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "MinLoad":
                            process.fMinLoad_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                        
                        elif assumption[2] == "RampRate":
                            process.fRampRate_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "EquAvailFactor":
                            process.fEquAvailFactor_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "AuxiliaryCon":
                            process.fAuxiliaryCon_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "CaptureRate": 
                            process.fCaptureRate_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "Duration":
                            process.fDuration_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                        
                else:
                    if bProcessFlag == True:
                        break
                        
    ### import cost assumptions
    
    techno_economic = []
    file_process = "../Input/3_process/03_Cost_coal.csv"
    techno_economic = genfromtxt(file_process, dtype = str, skip_header=1, delimiter=',')
    
    file_process = "../Input/3_process/03_Cost_gas.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                dtype = str, skip_header=1, delimiter=',')) )
    
    file_process = "../Input/3_process/03_Cost_other.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                dtype = str, skip_header=1, delimiter=',')) )
    
    file_process = "../Input/3_process/03_Cost_renewable.csv"
    techno_economic = vstack( (techno_economic, genfromtxt(file_process, \
                                dtype = str, skip_header=1, delimiter=',')) )
                
    for country in instance.lsCountry:
        for process in country.lsProcessAssump:
            sProcessName = process.sProcessName
            sRegionGroup = country.sTechCostGroup
            
            bProcessFlag = False
            for assumption in techno_economic:
                if sProcessName == assumption[0]: 
                    bProcessFlag = True
                    
                    if sRegionGroup == assumption[1]:
                                            
                        if assumption[2] == "CAPEX":
                            process.fCAPEX_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "OPEX":
                            process.fOPEX_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "varOPEX":
                            process.fVarOPEX_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                            assumption[4:], instance.iAllYearSteps_YS)
                            
                        elif assumption[2] == "Lifetime":
                            process.fLifetime = float(assumption[4])

                else:
                    if bProcessFlag == True:
                        break

        # annualized fix cost per MW (# M.USD / yr.MW)
        for process in country.lsProcessAssump:
            for iYS in range( 0, len(instance.iAllYearSteps_YS)):
            
                ### cost assumptions
                fCapacity = 1                                 # MW
                fCapitalCost = process.fCAPEX_YS[iYS] * fCapacity * 1000 # USD/KW * MW * 1000 = USD
                fYearOMCost = process.fOPEX_YS[iYS] * fCapacity * 1000  # USD/KW * MW * 1000 = USD
                fDiscountRate = process.fDiscount
                iPlantLife = process.fLifetime
                # fCapitalRecoveyFactor = (D*(1+D)^L) / ( ((1+D)^L)-1 )
                fCapitalRecoveyFactor =  ( fDiscountRate * ((1+fDiscountRate)**iPlantLife)) \
                    / ( ((1+fDiscountRate)**iPlantLife) - 1 )
                process.fAnnualCapex[iYS] = fCapitalCost * fCapitalRecoveyFactor / 1000000  # M.USD/year
                process.fAnnualFixedCost[iYS] = process.fAnnualCapex[iYS] \
                    + (fYearOMCost / 1000000)  # M.USD/year
    
    return


def get_CountryCommodityAssump(instance):
    ''' import commodity assumptions '''
    # import commodity assumption at country level 
    # commodity assumptions are all applied at country level
    
    file_commodity = "../Input/2_commodity/03_CommodityCost.csv"
    comm_assump = genfromtxt(file_commodity, dtype = str, skip_header=0, delimiter=',')
    
    file_commodity = "../Input/2_commodity/02_CostGroup.csv"
    comm_group = genfromtxt(file_commodity, dtype = str, skip_header=1, delimiter=',')
        
    # year step period in the original setting
    iOriginYear_OYS = comm_assump[0, 3:]
            
    for country in instance.lsCountry:
        
        # look up cost group
        CG_oil = "NPS"
        CG_gas = "NPS_EU"
        CG_coal = "NPS_EU"
        CG_uranium = "NPS"
        CG_biomass = "NPS_EU"
        for row in comm_group:
            if row[1] == country.sCountry:
                CG_oil = row[2]
                CG_gas = row[3]
                CG_coal = row[4]
                CG_uranium = row[5]
                CG_biomass = row[6]
                break
        
        country.lsCommodity = deepcopy(instance.lsCommodity)
        
        for commodity in country.lsCommodity:
            
            Category = commodity.sCategory            
            CostGroup = ""
            if Category == "oil":
                CostGroup = CG_oil
            elif Category == "gas":
                CostGroup = CG_gas
            elif Category == "coal":
                CostGroup = CG_coal
            elif Category == "uranium":
                CostGroup = CG_uranium
            elif Category == "biomass":
                CostGroup = CG_biomass
            
            for assumption in comm_assump:
                if Category == assumption[0] and CostGroup == assumption[1]:
                    commodity.fFuelPrice_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        assumption[3:], instance.iAllYearSteps_YS)

    return


def get_CountryPolicyAndTechAssump(instance):
    ''' import country policy and target assumptions '''
            
    ### carbon cost
    file_data = "../Input/4_policy/02_CarbonCost.csv"
    carbon_cost = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    # year step period in the original setting
    iOriginYear_OYS = carbon_cost[0, 2:]
            
    for country in instance.lsCountry:
        for row_cost in carbon_cost:
            if row_cost[0] == country.sCarbonCostGroup:
                country.fCarbonCost_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        row_cost[2:], instance.iAllYearSteps_YS)
                break
        
    ### ancillary service requirement
    file_data = "../Input/4_policy/03_AncillaryService.csv"
    AS_requirement = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
       
    # year period steps in the original setting
    iOriginYear_OYS = AS_requirement[0, 4:]
            
    for country in instance.lsCountry:
        for row_AS in AS_requirement:
            if row_AS[0] == country.sAncillaryGroup and row_AS[1] == "Primary":
                country.fASFirst_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        row_AS[4:], instance.iAllYearSteps_YS)
                country.fASFirst_YS = [ cell/100 for cell in country.fASFirst_YS ] 
                
            elif row_AS[0] == country.sAncillaryGroup and row_AS[1] == "Secondary":
                country.fASSecond_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        row_AS[4:], instance.iAllYearSteps_YS)
                country.fASSecond_YS = [ cell/100 for cell in country.fASSecond_YS ] 
                
            elif row_AS[0] == country.sAncillaryGroup and row_AS[1] == "Tertiary":
                country.fASThird_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        row_AS[4:], instance.iAllYearSteps_YS)
                country.fASThird_YS = [ cell/100 for cell in country.fASThird_YS ] 

    ### dispatchable process new build limit at specific period (CCS, Nuke)
    file_data = "../Input/4_policy/04_FixedNewBuild_dispatch.csv"
    PolicyDevLimit = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    # year step period in the original setting
    iOriginYear_OYS = PolicyDevLimit[0, 3:]
    
    for country in instance.lsCountry:
        for process in country.lsProcessAssump:
            for row in PolicyDevLimit:
                if row[1] == country.sCountry and row[2] == process.sProcessName:
                    
                    for iYear in instance.iAllYearSteps_YS:
                        for indCol, sValue in enumerate(PolicyDevLimit[0]):
                            if indCol >= 3 and row[indCol] != "":
                                if iYear == int(sValue):
                                    # restriction only applied when it matches the year step period 
                                    process.dicProcDispFixedNewBuild[str(iYear)] = float(row[indCol])
                                    break
                                elif iYear < int(sValue):
                                    # if the year step does not match, set 0
                                    process.dicProcDispFixedNewBuild[str(iYear)] = 0
                                    break
                    break
        
    '''
    ### renewable target      
    file_data = "../Input/4_policy/01_RE_Target.csv"
    RETarget = genfromtxt(file_data, dtype = str, skip_header=1, delimiter=',')
    for country in instance.lsCountry:
        for row in RETarget:
            if row[0] == country.sCountry:
                country.lsRenewableTarget = row[1:]
    '''
            
    return



def get_CountryBaseYearData(instance):
    ''' import country base year data assumptions '''
    # only "own use in industry" and "system loss" are used now        
    
    file_data = "../Input/5_calibration/01_BaseYear_Generation.csv"
    Base_Data = genfromtxt(file_data, dtype = str, skip_header=1, delimiter=',')
    
    for country in instance.lsCountry:
        
        # generation by type
        gen_coal = -1
        gen_gas = -1
        gen_oil = -1
        gen_nuke = -1
        gen_bio = -1
        
        # conversion eff by type
        eff_coal = -1
        eff_gas = -1
        eff_oil = -1
        eff_bio = -1
        
        # flow
        flow_total_gen = -1
        flow_import = -1
        flow_export = -1
        flow_ownuse = -1
        flow_ownindustry = -1
        flow_loss = -1        
        
        for row in Base_Data:
            if row[0] == country.sCountry:
                gen_coal = float(row[2]) 
                gen_gas = float(row[3]) 
                gen_oil = float(row[4]) 
                gen_nuke = float(row[5]) 
                gen_bio = float(row[6]) 
                # conversion eff by type
                eff_coal = float(row[7])
                eff_gas = float(row[8])
                eff_oil = float(row[9])
                eff_bio = float(row[11])
                # flow
                flow_total_gen = float(row[12])
                flow_import = float(row[17])
                flow_export = - float(row[18])  # turn into positive value
                flow_ownuse = float(row[20]) / flow_total_gen
                flow_ownindustry = float(row[22]) / flow_total_gen
                flow_loss = float(row[23]) / flow_total_gen
                break
                 
        country.dicBaseYearData["gen_coal"] = gen_coal
        country.dicBaseYearData["gen_gas"] = gen_gas
        country.dicBaseYearData["gen_oil"] = gen_oil
        country.dicBaseYearData["gen_nuke"] = gen_nuke
        country.dicBaseYearData["gen_bio"] = gen_bio
        country.dicBaseYearData["eff_coal"] = eff_coal
        country.dicBaseYearData["eff_gas"] = eff_gas
        country.dicBaseYearData["eff_oil"] = eff_oil
        country.dicBaseYearData["eff_bio"] = eff_bio
        country.dicBaseYearData["flow_total_gen"] = flow_total_gen
        country.dicBaseYearData["flow_import"] = flow_import
        country.dicBaseYearData["flow_export"] = flow_export
        country.dicBaseYearData["flow_ownuse"] = flow_ownuse
        country.dicBaseYearData["flow_ownindustry"] = flow_ownindustry
        country.dicBaseYearData["flow_loss"] = flow_loss
            
    return


def get_CountryRenInstallLimit(instance):
    ''' import settings on renewable installation limits '''

    ### limits applied on if the setting year matches the time period 
    # minimum installation capacity
    file_cdata = "../Input/8_VRE/01_RE_Min_Install.csv"
    zone_ReMin = genfromtxt(file_cdata, dtype = str, skip_header=0, delimiter=',')
    header = zone_ReMin[0]
    for objCountry in instance.lsCountry:
        for row_Data in zone_ReMin:
            if row_Data[0] == objCountry.sCountry:
                tech_type = row_Data[1]
                for ind_col, tech_cap in enumerate(row_Data):
                    if ind_col > 1:
                        if (tech_cap != "") and ( int(header[ind_col]) in instance.iAllYearSteps_YS):
                            objCountry.dicRenMinInstall[tech_type,header[ind_col]] = float(tech_cap)
          
    # maximum installation capacity    
    file_cdata = "../Input/8_VRE/02_RE_Max_Install.csv"
    zone_ReMax = genfromtxt(file_cdata, dtype = str, skip_header=0, delimiter=',')
    header = zone_ReMax[0]
    for objCountry in instance.lsCountry:
        for row_Data in zone_ReMax:
            if row_Data[0] == objCountry.sCountry:
                tech_type = row_Data[1]
                for ind_col, tech_cap in enumerate(row_Data):
                    if ind_col > 1:
                        if (tech_cap != "") and ( int(header[ind_col]) in instance.iAllYearSteps_YS):
                            objCountry.dicRenMaxInstall[tech_type,header[ind_col]] = float(tech_cap)        
            
    return


def get_CountryHydroCapLimit(instance):
    ''' import hydropower maximum capacity limits '''
    
    file_cdata = "../Input/8_VRE/03_RE_Hydro_Max_Cap.csv"
    country_HydroCap = genfromtxt(file_cdata, dtype = str, skip_header=0, delimiter=',')

    for objCountry in instance.lsCountry:
        
        for row_country in country_HydroCap:
            if row_country[0] == objCountry.sCountry:
                if row_country[2] != "":
                    objCountry.fTotalHydroCapLimit = float(row_country[2])
                else:
                    objCountry.fTotalHydroCapLimit = 0
                break                 
    return


def get_CountryBiomassLimit(instance):
    ''' import the projection of available biomass for power production '''
    
    file_cdata = "../Input/8_VRE/04_RE_Biomass_Max_Pot.csv"
    country_Data = genfromtxt(file_cdata, dtype = str, skip_header=0, delimiter=',')

    # year step period in the original setting
    iOriginYear_OYS = country_Data[0, 1:]
    
    for objCountry in instance.lsCountry:
        for row_country in country_Data:
            if row_country[0] == objCountry.sCountry:
                objCountry.fBiomassLimit_YS = ConvertAssumpYS(iOriginYear_OYS, \
                                        row_country[1:], instance.iAllYearSteps_YS)
                break
    return


def get_MarketTransmission(instance, objMarket):
    ''' import transmission link configurations in a market'''
    # create link objects
    
    ### terrestrial zones
    file_conn = "../Input/6_transmission/01_Zone_conn_base.csv"
    zone_conn = genfromtxt(file_conn, dtype = str, skip_header=1, delimiter=',')

    for ind_row, zone_ter in enumerate(zone_conn):

        for zone in objMarket.lsZone:

            if zone.sZone == zone_ter[4] or zone.sZone == zone_ter[5]:
                FromID = ""
                ToID = ""
                # get zoneID
                for objZone in objMarket.lsZone:
                    if zone_ter[4] == objZone.sZone:
                        FromID = objZone.sZoneID
                        break
                for objZone in objMarket.lsZone:
                    if zone_ter[5] == objZone.sZone:
                        ToID = objZone.sZoneID
                        break
                
                # could connect to a zone which is not in the market
                if ToID == "":
                    ToID = "ET" + str(ind_row)
                if FromID == "":
                    FromID = "ET" + str(ind_row)
                
                # check existing object
                bDupicate = False
                for objTrans in objMarket.lsTrans:
                    if objTrans.sFrom == FromID and objTrans.sTo == ToID:
                        bDupicate == True
                        break
                        
                if bDupicate == False:
                    fDist = float(zone_ter[8])
                    fBaseCap = float(zone_ter[9])
                    # if the base year connection exist, set a minimal 100MW NTC
                    # the value will be updated
                    if zone_ter[6] == "1":
                        fBaseCap = max( fBaseCap, 100 )
                    objTrans = cls_misc.Transmission( From=FromID, To=ToID, \
                        Dist=fDist, Conn2015=zone_ter[6], BaseCap=fBaseCap )
                    objMarket.lsTrans.append(objTrans)
                
                break
            
    ### offshore zones
    file_conn = "../Input/6_transmission/02_Zone_conn_base_offshore.csv"
    zone_conn = genfromtxt(file_conn, dtype = str, skip_header=1, delimiter=',')

    for zone in objMarket.lsZoneOffs:
        
        bProcessFlag = False
        for zone_off in zone_conn:

            if zone_off[2] == zone.sZone:
                bProcessFlag = True
                FromID = ""
                ToID = ""
                # get zoneID
                for objZone in objMarket.lsZoneOffs:
                    if zone_off[2] == objZone.sZone:
                        FromID = objZone.sZoneID
                        break
                for objZone in objMarket.lsZone:
                    if zone_off[3] == objZone.sZone:
                        ToID = objZone.sZoneID
                        break
                
                fDist = float(zone_off[5])
                fBaseCap = float(zone_off[6])
                objTrans = cls_misc.Transmission( From=FromID, To=ToID, \
                    Dist=fDist, Conn2015=zone_off[4], BaseCap=fBaseCap )  
                objMarket.lsTrans_off.append(objTrans)
            else:
                if bProcessFlag == True:
                    break
                
    return


def get_TransTechEcoAssump(instance, objMarket):
    ''' import general techno-economic assumptions of transmission '''

    file_commodity = "../Input/3_process/04_Transmission.csv"
    comm_assump = genfromtxt(file_commodity, dtype = str, skip_header=0, delimiter=',')
    
    # year step period in the original setting
    iOriginYear_OYS = comm_assump[0, 3:]

    for ind_row, data_row in enumerate(comm_assump):
        
        if data_row[0] == "DC_Line_Loss":
            objMarket.lsDCLineLoss = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
            
        elif data_row[0] == "DC_Conv_Loss":
            objMarket.lsDCConvLoss = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "AC_Line_Loss":
            objMarket.lsACLineLoss = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "DC_CAPEX":
            objMarket.lsDCCapex = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "DC_OPEX":
            objMarket.lsDCOpex = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "DC_CAPEX_conv":
            objMarket.lsDCCapexConv = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "DC_OPEX_conv":
            objMarket.lsDCOpexConv = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "AC_CAPEX":
            objMarket.lsACCapex = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "AC_OPEX":
            objMarket.lsACOpex = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)
                
        elif data_row[0] == "CRF":
            objMarket.lsCRF = ConvertAssumpYS(iOriginYear_OYS, \
                                    data_row[3:], instance.iAllYearSteps_YS)

    return


def ConvertAssumpYS(sOriginYear_OYS, sAssumption_OYS, iAllYearSteps_YS):
    ''' convert the data in setting files into defined periods steps '''
    # the year step setting in the CSV files may not match the time period setting
    # using intepolation

    iAssumptions_YS = []
    
    for iYear in iAllYearSteps_YS:
        for ind_OriYear, sOriYear in enumerate(sOriginYear_OYS):
            if iYear <= int(sOriYear):
                iAssumptions_YS.append( float(sAssumption_OYS[ind_OriYear]) )
                break
            elif ind_OriYear == (len(sOriginYear_OYS) - 1):
                # last element in the original assumption list
                iAssumptions_YS.append( float(sAssumption_OYS[ind_OriYear]) )
                break
            elif iYear < int(sOriginYear_OYS[ind_OriYear+1]):
                # intepolate for the value
                iInterval = abs(int(sOriginYear_OYS[ind_OriYear + 1]) \
                                - int(sOriginYear_OYS[ind_OriYear]))
                iInterval_1 = int(sOriginYear_OYS[ind_OriYear+1]) - iYear                
                iInterval_2 = iYear - int(sOriginYear_OYS[ind_OriYear])                        
                fIntpValue = ( float(sAssumption_OYS[ind_OriYear])*iInterval_1 \
                              + float(sAssumption_OYS[ind_OriYear+1])*iInterval_2 ) / iInterval
                iAssumptions_YS.append(fIntpValue)
                break

    return iAssumptions_YS

