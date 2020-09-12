#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions for import settings at zone level
#

from copy import deepcopy
from numpy import genfromtxt, zeros, roll

import cls_process
import impt_country


def get_DemandProfile(instance, objZone):
    ''' import zonal demand profile at default 288 TS for ED model '''
    
    sZone = objZone.sZone

    ### default TS
    objZone.fPowerDemand_TS_YS = zeros((288,len(instance.iAllYearSteps_YS)))
    file_dem = "../Input/7_demand/Zone_288/" + sZone + ".csv"
    zone_dem = genfromtxt(file_dem, dtype = float, skip_header=0, delimiter=',')

    # year step period in the original setting
    iOriginYear_OYS = zone_dem[0, :]
    
    # convert into defined year step period
    zone_dem_288_YS = zeros((288,len(instance.iAllYearSteps_YS)))
    for ind_TS in range(0, 288):
        dem_YS = impt_country.ConvertAssumpYS(iOriginYear_OYS, zone_dem[ind_TS+1,:], \
                                              instance.iAllYearSteps_YS)
        for ind_YS in range(0, len(instance.iAllYearSteps_YS)):
            zone_dem_288_YS[ind_TS, ind_YS] = dem_YS[ind_YS]

    ### convert to GMT time ###  (
    # be areful about shift demand time, originally start from 1am local time
    Time_Zone = objZone.iTimeZone
    for iYS in range(0, len(instance.iAllYearSteps_YS)):
        original288 = zone_dem_288_YS[:,iYS]
        DM_array = []
        for iMonth in range(0,12):
            dayCF = original288[iMonth*24 : (iMonth+1)*24]
            # shift the time from 1-24 to 0-23
            dayCF = roll(dayCF,1)
            # shift time zone
            dayCF = roll(dayCF,-Time_Zone)
                
            DM_array.extend(dayCF)
        
        for TS in range(0,288):
            objZone.fPowerDemand_TS_YS[TS,iYS] = DM_array[TS]

    # adjust end use and transmission and distribution losses
    fOwnindustry = instance.lsCountry[objZone.iCountryIndex].dicBaseYearData["flow_ownindustry"]
    fFlowLoss = instance.lsCountry[objZone.iCountryIndex].dicBaseYearData["flow_loss"]
    if fFlowLoss > 0.1:
        fFlowLoss = 0.1
    if fOwnindustry > 0:
        objZone.fPowerDemand_TS_YS = objZone.fPowerDemand_TS_YS * (1 + fOwnindustry)
    if fFlowLoss > 0:
        objZone.fPowerDemand_TS_YS = objZone.fPowerDemand_TS_YS * (1 + fFlowLoss)
            
    return


def get_DemandProfile_CEP(instance, objZone):
    ''' estimate the zonal demand profile at user defiled TS for CE model '''
    # converted from 8760 hourly data
    
    objZone.fPowerDemand_CEP_YS = zeros((len(instance.lsTimeSlice_CEP), \
                                         len(instance.iAllYearSteps_YS)))
        
    iCETS = len(instance.lsTimeSlice_CEP)
    for YS in range(0, len(instance.iAllYearSteps_YS)):
        objZone.fPowerDemand_CEP_YS[0:iCETS, YS] = convertTS_8760_to_CEP(instance, \
                                                    objZone.fPowerDemand_8760_YS[:, YS])

    return


def convertTS_8760_to_CEP(instance, lsTS8760):
    ''' convert 8760 profile into definded TS for CE model '''
    # note that all profiles have been shifted into GMT time
    
    fNewData_CEP = zeros(len(instance.lsTimeSlice_CEP))
    iTimeValue = zeros((8760,4))
    lsMonthDay = [31,28,31,30,31,30,31,31,30,31,30,31]
    iTimeIndex = 0
    for ind_Month, iMonthDays in enumerate(lsMonthDay):
        for ind_Day in range(0,iMonthDays):
            for ind_Hour in range(0,24):
                iTimeValue[iTimeIndex,0] = ind_Month + 1
                iTimeValue[iTimeIndex,1] = ind_Day + 1
                iTimeValue[iTimeIndex,2] = ind_Hour
                iTimeValue[iTimeIndex,3] = lsTS8760[iTimeIndex]
                iTimeIndex = iTimeIndex + 1
                           
    lsTS_Value = zeros(len(instance.lsTimeSlice_CEP))
    lsTS_Count = zeros(len(instance.lsTimeSlice_CEP))

    for indHour in range(0,8760):
        sMonth = "[" + str(int(iTimeValue[indHour,0])) + "]"
        sHour = "[" + str(int(iTimeValue[indHour,2])) + "]"
        for ind_TS, objTS in enumerate(instance.lsTimeSlice_CEP):
            # check if month and hour match
            if sMonth in objTS.sMonth and sHour in objTS.sHour:
                lsTS_Value[ind_TS] = lsTS_Value[ind_TS] + iTimeValue[indHour,3]
                lsTS_Count[ind_TS] = lsTS_Count[ind_TS] + 1
                break
 
    for ind_TS, objTS in enumerate(instance.lsTimeSlice_CEP):
        fNewData_CEP[ind_TS] = lsTS_Value[ind_TS] / lsTS_Count[ind_TS]

    return fNewData_CEP


def get_DemandProfile_8760(instance, objZone):
    ''' import zonal demand profile of 8760 hours '''
    
    sZone = objZone.sZone
    
    ### 8760 TS
    objZone.fPowerDemand_8760_YS = zeros((8760, len(instance.iAllYearSteps_YS)))
    file_dem = "../Input/7_demand/Zone_8760/" + sZone + ".csv"
    zone_dem = genfromtxt(file_dem, dtype = float, skip_header=0, delimiter=',')

    # year step period in the original setting
    iOriginYear_OYS = zone_dem[0, 1:]
    
    # convert into defined year step period
    zone_dem_8760_YS = zeros((8760,len(instance.iAllYearSteps_YS)))
    for ind_TS in range(0, 8760):
        dem_YS = impt_country.ConvertAssumpYS(iOriginYear_OYS, \
                                zone_dem[ind_TS+1,1:], instance.iAllYearSteps_YS)
        for ind_YS in range(0, len(instance.iAllYearSteps_YS)):
            zone_dem_8760_YS[ind_TS, ind_YS] = dem_YS[ind_YS]

    ### convert to GMT time ###  
    # be careful about shift demand time, originally start from 1am local time
    Time_Zone = objZone.iTimeZone
    for iYS in range(0, len(instance.iAllYearSteps_YS)):
        
        original8760 = zone_dem_8760_YS[:,iYS]
        DM_array = []
        for iDay in range(0,365):
            dayCF = original8760[iDay*24 : (iDay+1)*24]
            # shift the time from 1-24 to 0-23
            dayCF = roll(dayCF,1)
            # shift time zone
            dayCF = roll(dayCF,-Time_Zone)
            
            DM_array.extend(dayCF)
            
        for TS in range(0,8760):
            objZone.fPowerDemand_8760_YS[TS,iYS] = DM_array[TS]
                
    # adjust end use and transmission and distribution losses
    fOwnindustry = instance.lsCountry[objZone.iCountryIndex].dicBaseYearData["flow_ownindustry"]
    fFlowLoss = instance.lsCountry[objZone.iCountryIndex].dicBaseYearData["flow_loss"]
    if fFlowLoss > 0.1:
        fFlowLoss = 0.1
        
    if fOwnindustry > 0:
        objZone.fPowerDemand_8760_YS = objZone.fPowerDemand_8760_YS * (1 + fOwnindustry)
    if fFlowLoss > 0:
        objZone.fPowerDemand_8760_YS = objZone.fPowerDemand_8760_YS * (1 + fFlowLoss)   
        
    return


def get_ZoneProcessAssump(instance, objZone):
    ''' import zonal process assumptions '''
    # inherit most assumptions from country, split renewalbe objects by class, load renewable CF
    # for renewables, only import available options
    
    sZone = objZone.sZone
    sCountry = instance.lsCountry[objZone.iCountryIndex].sCountry
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/8_VRE/DevLimit/" + sCountry + ".csv"
    zone_re = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    # find row index to GEDM capacity limits
    iRowIndex = 3
    for indRow, sValue in enumerate(zone_re):
        if sValue[0] == "Cap_GEDM":
            iRowIndex = indRow
    
    # import renewable CF by class in the zone, TS 288
    file_data = "../Input/8_VRE/CF288/" + sCountry + ".csv"
    zone_reTS288 = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    # import renewable CF by class in the zone, TS 8760 (2017)
    file_data = "../Input/8_VRE/CF8760/" + sCountry + ".csv"
    zone_reTS8760 = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    iCETS = len(instance.lsTimeSlice_CEP)
    
    lsProcess = []
    for objProcess in instance.lsCountry[objZone.iCountryIndex].lsProcessAssump:   
        # copy the process objects if they are not renewable (and not hydro pump storage)
        if objProcess.sProcessType not in ["renewable","storage"]:
            lsProcess.append( deepcopy(objProcess) )
            
        elif objProcess.sProcessType == "storage" and objProcess.sProcessName != "HYD_PS":
            # storage but not pump hydro storage
            lsProcess.append( deepcopy(objProcess) )
            
        elif objProcess.sProcessName in ["BIO_ST", "BIGCC_CCS"]:
            # biomass plants, no limit on capacity
            lsProcess.append( deepcopy(objProcess) )
            
        else:
            # add renewables split by class
            for data_col in range(0,len(zone_re[0])):
                if zone_re[0,data_col] == sZone:  # offshore technology will not appear here
                    sProcessName = zone_re[1,data_col]
                    
                    if objProcess.sProcessName == sProcessName:
                        CF_class = str(zone_re[2,data_col])
                        if CF_class == "":
                            CF_class = 0
                        else:
                            CF_class = int(zone_re[2,data_col])
                        
                        # only import the process with non-zero capacity potential
                        fAvailableCap = float(zone_re[iRowIndex, data_col])
                        if fAvailableCap > 0:
                        
                            new_process = deepcopy(objProcess)
                            # capacity limit
                            new_process.iCFClass = CF_class
                            new_process.fREDevLimit = fAvailableCap
                            # CF TS
                            new_process.fRECF_TS = [ float(TS) for TS in zone_reTS288[3:, data_col] ]
                            # CF 8760
                            new_process.fRECF_8760 = [ float(TS) for TS in zone_reTS8760[3:, data_col] ]
                            # CF for CEP
                            new_process.fRECF_CEP[0:iCETS] = convertTS_8760_to_CEP(instance, new_process.fRECF_8760)
                            
                            lsProcess.append( new_process )
            
    objZone.lsProcessAssump = lsProcess
    
    return


def get_ZoneProcessDispBaseCF(instance, objZone):
    ''' get base year CF assumption for non-renewable process '''
    
    sZone = objZone.sZone
    sCountry = instance.lsCountry[objZone.iCountryIndex].sCountry
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/5_calibration/Zone_BaseYear_CF/" + sCountry + ".csv"
    zone_BaseCF = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    for proc_CF in zone_BaseCF:
        if proc_CF[0] == sZone:
            
            for objProcAssump in objZone.lsProcessAssump:
                if objProcAssump.sProcessName == proc_CF[1]:
                    objProcAssump.fBaseDispCF_288 = [ float(sCF) for sCF in proc_CF[3:] ]
                    break
    return


def get_ZonePVLandLimit(instance, objZone):
    ''' import zonal limit on available land area for solar technolgies '''
    
    sZone = objZone.sZone
    sCountry = instance.lsCountry[objZone.iCountryIndex].sCountry
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/8_VRE/SolarAreaLimit/" + sCountry + ".csv"
    zone_re = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    for row_zone in zone_re:
        if row_zone[0] == sZone:
            objZone.fPVLandLimit = float(row_zone[1])
            break
        
    return


def get_ZoneMCP70Pathway(instance, objZone):
    ''' import optimal renewable mix of 70% penetration for MCP scenario '''
    
    sZone = objZone.sZone
    sCountry = objZone.sCountry
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/4_policy/RE_MCP70/" + sCountry + ".csv"
    zone_re = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    # year step period in the original setting
    iOriginYear_OYS = zone_re[0, 2:]
    
    for row_zone in zone_re:
        if row_zone[0] == sZone:            
            sProcessName = row_zone[1]
            iMCP70_YS = impt_country.ConvertAssumpYS(iOriginYear_OYS, \
                                    row_zone[2:], instance.iAllYearSteps_YS)
            for ind_Year, iYear in enumerate(instance.iAllYearSteps_YS):
                objZone.dicMCP70RenewPathway_RE_YS[sProcessName, \
                                    str(iYear)] = float(iMCP70_YS[ind_Year])
                
    return


def get_ZoneProcessAssump_offs(instance, objZone):
    ''' import zonal process assumptions of offshore technologies '''
    # inherit most assumptions from country, split renewalbe objects by class, load renewable CF
    
    sZone = objZone.sZone
    sCountry = instance.lsCountry[objZone.iCountryIndex].sCountry
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/8_VRE/DevLimit/" + sCountry + ".csv"
    zone_re = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    # find row index to GEDM capacity limits
    iRowIndex = 3
    for indRow, sValue in enumerate(zone_re):
        if sValue[0] == "Cap_GEDM":
            iRowIndex = indRow
    
    # import renewable CF by class in the zone, TS 288
    file_data = "../Input/8_VRE/CF288/" + sCountry + ".csv"
    zone_reTS288 = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    # import renewable CF by class in the zone, TS 8760
    file_data = "../Input/8_VRE/CF8760/" + sCountry + ".csv"
    zone_reTS8760 = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
    
    iCETS = len(instance.lsTimeSlice_CEP)
    
    lsProcess = []
    for objProcess in instance.lsCountry[objZone.iCountryIndex].lsProcessAssump:   
        if objProcess.sProcessName in ["WND_OFF_SH","WND_OFF_IN","WND_OFF_DE"]:
            # add the renewables split by class
            for data_col in range(0,len(zone_re[0])):
                if zone_re[0,data_col] == sZone:
                    sProcessName = zone_re[1,data_col]
                    
                    if objProcess.sProcessName == sProcessName:
                        CF_class = str(zone_re[2,data_col])
                        if CF_class == "":
                            CF_class = 0
                        else:
                            CF_class = int(zone_re[2,data_col])
                            
                        # only import the process with non-zero capacity potential
                        fAvailableCap = float(zone_re[iRowIndex, data_col])
                        if fAvailableCap > 0:
                            
                            new_process = deepcopy(objProcess)
                        
                            # capacity limit
                            new_process.iCFClass = CF_class
                            new_process.fREDevLimit = fAvailableCap
                            # CF TS
                            new_process.fRECF_TS = \
                                [ float(TS) for TS in zone_reTS288[3:, data_col] ]
                            # CF 8760
                            new_process.fRECF_8760 = \
                                [ float(TS) for TS in zone_reTS8760[3:, data_col] ]
                            # CF for CEP
                            new_process.fRECF_CEP[0:iCETS] = \
                                convertTS_8760_to_CEP(instance, new_process.fRECF_8760)
                            
                            lsProcess.append( new_process )
            
    objZone.lsProcessAssump = lsProcess
    
    return


def get_ZoneExistingProcess(instance, objZone):
    ''' import existing processe/plants in the zone '''
    
    sZone = objZone.sZone
    
    file_data = "../Input/5_calibration/Zone_Exist_Process/" + sZone + ".csv"
    zone_proc = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    for row_proc in zone_proc[1:]:
        sProcessName = row_proc[0]
        
        for ind_objProcAss, objProcessAssump in enumerate(objZone.lsProcessAssump):
            if sProcessName == objProcessAssump.sProcessName:
                
                for ind_year, col_year_cap in enumerate(row_proc[1:]):
                    if float(col_year_cap) > 0:
                        
                        iCommitTime = round(float(zone_proc[0,ind_year+1]))
                        sProcessID = sProcessName + "_" + str(iCommitTime)

                        # new process                        
                        objExistProcess = cls_process.ZoneProcess( \
                                    sProcessName=sProcessName, sProcessID=sProcessID)
                        objExistProcess.iZoneProcAssumIndex = ind_objProcAss
                        objExistProcess.sProcessType = objProcessAssump.sProcessType
                        objExistProcess.sFuel = objProcessAssump.sFuel
                        objExistProcess.sOperationMode = objProcessAssump.sOperationMode
                        objExistProcess.bCCS = objProcessAssump.bCCS
                        objExistProcess.bAS_T1 = objProcessAssump.bAS_T1
                        objExistProcess.bAS_T2 = objProcessAssump.bAS_T2
                        objExistProcess.bAS_T3 = objProcessAssump.bAS_T3
                        
                        # tech assumption
                        objExistProcess.iCapacity = float(col_year_cap)
                        # assuming a small efficiency decade on older units
                        objExistProcess.fGrossEff = \
                            objProcessAssump.fGrossEff_YS[0] * ( 1- (2015-iCommitTime)*0.001 )
                        objExistProcess.fMinLoad = objProcessAssump.fMinLoad_YS[0]
                        objExistProcess.fRampRate = objProcessAssump.fRampRate_YS[0]
                        objExistProcess.fEquAvailFactor = objProcessAssump.fEquAvailFactor_YS[0]
                        objExistProcess.fAuxiliaryCon = objProcessAssump.fAuxiliaryCon_YS[0]
                        objExistProcess.fCaptureRate = objProcessAssump.fCaptureRate_YS[0]
                        objExistProcess.fDuration = objProcessAssump.fDuration_YS[0]
                                                
                        ### commit and decommit time 
                        # if the decommit time is before 2015, then change to 2020
                        objExistProcess.iCommitTime = iCommitTime
                        iDeCommitTime = iCommitTime + objProcessAssump.fLifetime
                        if iDeCommitTime <= 2015:
                            iDeCommitTime = 2020
                        objExistProcess.iDeCommitTime = iDeCommitTime
                        
                        ### cost assumptions
                        fCapacity = objExistProcess.iCapacity        # MW
                        fCapitalCost = objProcessAssump.fCAPEX_YS[0] * fCapacity * 1000  # USD/KW * MW * 1000 = USD
                        fYearOMCost = objProcessAssump.fOPEX_YS[0] * fCapacity * 1000  # USD/KW * MW * 1000 = USD
                        fDiscountRate = objProcessAssump.fDiscount
                        iPlantLife = objProcessAssump.fLifetime
                        # fCapitalRecoveyFactor = (D*(1+D)^L) / ( ((1+D)^L)-1 )
                        fCapitalRecoveyFactor =  ( fDiscountRate * ((1+fDiscountRate)**iPlantLife)) \
                            / ( ((1+fDiscountRate)**iPlantLife) - 1 )
                        objExistProcess.fAnnualCapex = fCapitalCost \
                            * fCapitalRecoveyFactor / 1000000    # M.USD / year
                        objExistProcess.fAnnualFixedCost = objExistProcess.fAnnualCapex \
                            + (fYearOMCost / 1000000)    # M.USD / year
                        objExistProcess.fvarOMCost = objProcessAssump.fVarOPEX_YS[0]   # USD/KWh
                        
                        ### capability for providing ancillary service
                        objExistProcess.fASMax_T1 = objExistProcess.iCapacity \
                            * objExistProcess.fRampRate / 100 \
                            * objExistProcess.bAS_T1 * 0.5  # 30 second ramp capacity
                            
                        objExistProcess.fASMax_T2 = objExistProcess.iCapacity \
                            * objExistProcess.fRampRate / 100 \
                            * objExistProcess.bAS_T2 * 10  # 10 min ramp capacity
                        if objExistProcess.fASMax_T2 > objExistProcess.iCapacity:
                            objExistProcess.fASMax_T2 = objExistProcess.iCapacity
                            
                        objExistProcess.fASMax_T3 = objExistProcess.iCapacity \
                            * objExistProcess.fRampRate / 100 \
                            * objExistProcess.bAS_T3 * 30  # 30 min ramp capacity
                        if objExistProcess.fASMax_T3 > objExistProcess.iCapacity:
                            objExistProcess.fASMax_T3 = objExistProcess.iCapacity

                        ### for renewables, assign CF class to the higest CF tranche 
                        # but need to check the available capacity
                        if sProcessName in ["WND_ON","PV_FT","PV_TK","CSP_ST6","CSP_ST9"]:
                            
                            bAssign = False
                            iLastProcessInd = 0
                            for ind_obj, objProAssump_temp in reversed(list(enumerate(objZone.lsProcessAssump))):
                                if sProcessName == objProAssump_temp.sProcessName:
                                    iLastProcessInd = ind_obj
                                    if (objProAssump_temp.fREDevLimit - objProAssump_temp.fREExistCap) >= objExistProcess.iCapacity:
                                        objExistProcess.iCFClass = objProAssump_temp.iCFClass
                                        objProAssump_temp.fREExistCap = \
                                            objProAssump_temp.fREExistCap + objExistProcess.iCapacity
                                        objExistProcess.iZoneProcAssumIndex = iLastProcessInd
                                        bAssign = True
                                        break
                                    
                            # assign to the lowest CF tranche if it cannot fit in higher tranches
                            if bAssign == False:
                                objExistProcess.iCFClass = objZone.lsProcessAssump[iLastProcessInd].iCFClass
                                objZone.lsProcessAssump[iLastProcessInd].fREExistCap = objExistProcess.iCapacity
                                objExistProcess.iZoneProcAssumIndex = iLastProcessInd
                                    
                        objZone.lsProcess.append(objExistProcess)
                        
                break

    return


def get_ZoneExistingProcess_offs(instance, objZone):
    ''' import existing processe/plants in the offshore zone '''
    
    sZone = objZone.sZone
    
    # import renewable capacity limit by class in the zone
    file_data = "../Input/5_calibration/Zone_Exist_Process_offshore/" + sZone + ".csv"
    zone_proc = genfromtxt(file_data, dtype = str, skip_header=0, delimiter=',')
            
    for row_proc in zone_proc[1:]:
        sProcessName = row_proc[0]
        
        for ind_objProcAss, objProcessAssump in enumerate(objZone.lsProcessAssump):
            if sProcessName == objProcessAssump.sProcessName:
                
                for ind_year, col_year_cap in enumerate(row_proc[1:]):
                    if float(col_year_cap) > 0:
                        
                        iCommitTime = round(float(zone_proc[0,ind_year+1]))
                        sProcessID = sProcessName + "_" + str(iCommitTime)

                        # new process                        
                        objExistProcess = \
                            cls_process.ZoneProcess(sProcessName=sProcessName, sProcessID=sProcessID)
                        objExistProcess.iZoneProcAssumIndex = ind_objProcAss
                        objExistProcess.sProcessType = objProcessAssump.sProcessType
                        objExistProcess.sFuel = objProcessAssump.sFuel
                        objExistProcess.sOperationMode = objProcessAssump.sOperationMode
                        objExistProcess.bCCS = objProcessAssump.bCCS
                        
                        # tech assumption
                        objExistProcess.iCapacity = float(col_year_cap)
                        objExistProcess.fEquAvailFactor = objProcessAssump.fEquAvailFactor_YS[0]
                        objExistProcess.iCommitTime = iCommitTime
                        iDeCommitTime = iCommitTime + objProcessAssump.fLifetime
                        objExistProcess.iDeCommitTime = iDeCommitTime
                        
                        ### cost assumptions
                        fCapacity = objExistProcess.iCapacity    # MW
                        fCapitalCost = objProcessAssump.fCAPEX_YS[0] * fCapacity * 1000  # USD/KW * MW * 1000 = USD
                        fYearOMCost = objProcessAssump.fOPEX_YS[0] * fCapacity * 1000  # USD/KW * MW * 1000 = USD
                        fDiscountRate = objProcessAssump.fDiscount
                        iPlantLife = objProcessAssump.fLifetime
                        # fCapitalRecoveyFactor = (D*(1+D)^L) / ( ((1+D)^L)-1 )
                        fCapitalRecoveyFactor =  ( fDiscountRate * ((1+fDiscountRate)**iPlantLife)) \
                            / ( ((1+fDiscountRate)**iPlantLife) - 1 )
                        objExistProcess.fAnnualCapex = fCapitalCost \
                            * fCapitalRecoveyFactor / 1000000                # MillionUSD / year
                        objExistProcess.fAnnualFixedCost = objExistProcess.fAnnualCapex \
                            + (fYearOMCost / 1000000)    # MillionUSD / year
                        objExistProcess.fvarOMCost = objProcessAssump.fVarOPEX_YS[0]            # USD/KWh
                        
                        ### for renewables, assign CF class to the higest CF tranche, but check the available capacity
                        bAssign = False
                        iLastProcessInd = 0
                        for ind_obj, objProAssump_temp in reversed(list(enumerate(objZone.lsProcessAssump))):
                            if sProcessName == objProAssump_temp.sProcessName:
                                iLastProcessInd = ind_obj
                                if (objProAssump_temp.fREDevLimit - objProAssump_temp.fREExistCap) >= objExistProcess.iCapacity:
                                    objExistProcess.iCFClass = objProAssump_temp.iCFClass
                                    objProAssump_temp.fREExistCap = \
                                        objProAssump_temp.fREExistCap + objExistProcess.iCapacity
                                    objExistProcess.iZoneProcAssumIndex = iLastProcessInd
                                    bAssign = True
                                    break
                                
                        # assign to the lowest CF tranche if it cannot fit in higher tranches
                        if bAssign == False:
                            objExistProcess.iCFClass = objZone.lsProcessAssump[iLastProcessInd].iCFClass
                            objZone.lsProcessAssump[iLastProcessInd].fREExistCap = objExistProcess.iCapacity
                            objExistProcess.iZoneProcAssumIndex = iLastProcessInd
                                    
                        objZone.lsProcess.append(objExistProcess)
                        
                break

    return


