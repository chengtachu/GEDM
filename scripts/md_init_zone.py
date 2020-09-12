#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to initialize settings in a zone
#

#----------------------------------------------------------------------------
### zonal assumptions for model ED (model iteration on daily basis)
#----------------------------------------------------------------------------

def get_DemandProfile_Day(model, objMarket, ind_year):
    ''' get demand profile of ED model '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objZone.fPowerDemand_TS_YS[int(sTSIndex)-1, ind_year]

    return dData


def getNonDispGen_ZNL_Day(model, objMarket, iYear):
    ''' get aggregated zonal non-dispatchable generation - terrestrial zone '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAll_ZNL_TS[objZone.sZoneID, sTSIndex]

    return dData


def getNonDispGen_ZNF_Day(model, objMarket, iYear):
    '''  get aggregated zonal non-dispatchable generation - offshore zone '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAll_ZNF_TS[objZone.sZoneID, sTSIndex]

    return dData


def getASReq_day(model, instance, objMarket, sAS, ind_year):
    '''  get zonal ancillary service requirement at given TS '''
    
    dData = {}
    for objZone in objMarket.lsZone:
        fASReq = 0
        if sAS == "T1":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASFirst_YS[ind_year]
        elif sAS == "T2":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASSecond_YS[ind_year]
        elif sAS == "T3":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASThird_YS[ind_year]        

        for sTSIndex in model.setTimeSlice_TS:
            # percentage of hourly power demand
            dData[objZone.sZoneID, sTSIndex] = \
                fASReq * objZone.fPowerDemand_TS_YS[int(sTSIndex)-1, ind_year]
        
    return dData


#----------------------------------------------------------------------------
### zonal assumptions for model CE
#----------------------------------------------------------------------------
    
# get demand profile
def get_DemandProfile(model, objMarket, ind_year):
    '''  get demand profile of CE model'''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objZone.fPowerDemand_CEP_YS[int(sTSIndex)-1, ind_year]

    return dData


def getNonDispGen_ZNL(model, objMarket, iYear):
    '''  get aggregated zonal non-dispatchable generation '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAll_ZNL_TS[objZone.sZoneID, sTSIndex]

    return dData


def getNonDispGen_ZNF(model, objMarket, iYear):
    '''  get aggregated zonal non-dispatchable generation offshore zone '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):
        for sTSIndex in model.setTimeSlice_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAll_ZNF_TS[objZone.sZoneID, sTSIndex]

    return dData


def getASReq(model, instance, objMarket, sAS, ind_year):
    '''  get zonal ancillary service requirement at given TS '''
    
    dData = {}
    for objZone in objMarket.lsZone:
        fASReq = 0
        if sAS == "T1":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASFirst_YS[ind_year]
        elif sAS == "T2":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASSecond_YS[ind_year]
        elif sAS == "T3":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASThird_YS[ind_year]        

        for sTSIndex in model.setTimeSlice_TS:
            # percentage of hourly power demand
            dData[objZone.sZoneID, sTSIndex] = \
                fASReq * objZone.fPowerDemand_CEP_YS[int(sTSIndex)-1, ind_year]
        
    return dData


#----------------------------------------------------------------------------
### zonal assumptions for model CE testing cases
#----------------------------------------------------------------------------
    
def get_DemandProfile_RT(model, objMarket):
    '''  get hourly demand of monthly testing cases '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTSRT_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objZone.fPowerDemand_CEP_RT[int(sTSIndex)]

    return dData


def getNonDispGen_ZNL_RT(model, objMarket):
    '''  get aggregated non-dispatchable generation of testing cases '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):
        for sTSIndex in model.setTSRT_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAllTest_ZNL_TS[objZone.sZoneID, sTSIndex]

    return dData


def getNonDispGenOff_ZNF_RT(model, objMarket):
    ''' get aggregated non-dispatchable generation of testing cases - offshore zone '''
    
    dData = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):
        for sTSIndex in model.setTSRT_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                objMarket.NonDisGenAllTest_ZNF_TS[objZone.sZoneID, sTSIndex]

    return dData


def getASReq_RT(model, instance, objMarket, sAS, ind_year):
    '''  get zonal ancillary service requirement at testing cases '''
    
    dData = {}
    for objZone in objMarket.lsZone:
        fASReq = 0
        if sAS == "T1":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASFirst_YS[ind_year]
        elif sAS == "T2":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASSecond_YS[ind_year]
        elif sAS == "T3":
            fASReq = instance.lsCountry[objZone.iCountryIndex].fASThird_YS[ind_year]        

        for sTSIndex in model.setTSRT_TS:
            dData[objZone.sZoneID, sTSIndex] = \
                fASReq * objZone.fPowerDemand_CEP_RT[int(sTSIndex)]
        
    return dData


#--------------------------------------------------------------------------------
# Technology Parameters - dispatchable
#--------------------------------------------------------------------------------    
    
def getProcParamDisp(objMarket, model, sParameter, iYear):
    ''' get aggregated process parameters - existing dispatchable processes '''
    
    dData = {}
    for sProcess in model.setProcBaseDisp_TCD:
        sProcZoneID = sProcess.split("/")[0]
        
        liCap = []
        liParam = []
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
            
                for objProcess in objZone.lsProcess:
                    if objProcess.iDeCommitTime > iYear:  
                        # by default no units will decommit in base year 2015
                    
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                            
                            liCap.append( objProcess.iCapacity )
                            
                            if sParameter == "Cap":
                                liParam.append( objProcess.iCapacity )
                            elif sParameter == "OUS":
                                liParam.append( objProcess.fAuxiliaryCon )
                            elif sParameter == "Eff":
                                liParam.append( objProcess.fGrossEff )
                            elif sParameter == "EAF":
                                liParam.append( objProcess.fEquAvailFactor )
                            elif sParameter == "MLD":
                                liParam.append( objProcess.fMinLoad )
                            elif sParameter == "CCS":
                                liParam.append( objProcess.fCaptureRate )
                            elif sParameter == "varOM":
                                liParam.append( objProcess.fvarOMCost )  
        
        if len(liCap) > 0:
            sumCap = sum(liCap)
            for ind_p, param in enumerate(liCap):
                liCap[ind_p] = liCap[ind_p] / sumCap
            
            if sParameter == "Cap":
                dData[sProcess] = sumCap
            else:
                fParam = 0
                for ind_p, param in enumerate(liParam):
                    fParam += param * liCap[ind_p]
                dData[sProcess] = fParam
        else:
            if sParameter == "Eff":
                # assign a default value, otherwise could cause divid zero bugs
                dData[sProcess] = 0.33
            else:
                dData[sProcess] = 0
                
    return dData


def getProcParamDisp_New(objMarket, model, sParameter, ind_year):
    ''' get aggregated process parameters - dispatchable - new build '''
    
    dData = {}
    for sProcess in model.setProcNewDisp_TCD:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
            
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        if sParameter == "OUS":
                            dData[sProcess] = objProcess.fAuxiliaryCon_YS[ind_year]
                        elif sParameter == "Eff":
                            dData[sProcess] = objProcess.fGrossEff_YS[ind_year]
                        elif sParameter == "EAF":
                            dData[sProcess] = objProcess.fEquAvailFactor_YS[ind_year]
                        elif sParameter == "MLD":
                            dData[sProcess] = objProcess.fMinLoad_YS[ind_year]
                        elif sParameter == "CCS":
                            dData[sProcess] = objProcess.fCaptureRate_YS[ind_year]
                        elif sParameter == "varOM":
                            dData[sProcess] = objProcess.fVarOPEX_YS[ind_year]
                        break

    return dData


def getProcVarGenCost(instance, objMarket, model, ind_year):
    ''' get variable generation cost of existing dispatchable processes '''
    
    dData = {}
    
    for objZone in objMarket.lsZone:
        for sProcess in model.setProcBaseDisp_TCD:
            
            if objZone.sZoneID + "/" in sProcess:
                sProcessCode = sProcess.split("/")[1]
                
                # variable generation cost
                varOMCost = model.pExProcVarOMCost_TCD[sProcess]
                
                # search for fuel type
                sFuel = ""
                for obeProcDef in instance.lsProcessDefObjs:
                    if obeProcDef.sProcessName == sProcessCode:
                        sFuel = obeProcDef.sFuel
                        break
                
                # fuel and carbon cost
                cost_fuel = 0                
                fuel_price = 0
                cost_emission = 0
                carbon_price = instance.lsCountry[objZone.iCountryIndex].fCarbonCost_YS[ind_year]   # USD/tCO2e
                
                for objComm in instance.lsCountry[objZone.iCountryIndex].lsCommodity:     
                    if objComm.sCategory == sFuel:
                        
                        convert_eff = model.pExProcDispEff_TCD[sProcess]
                        CCSCaptureRate = model.pExProcDispCCSCapRate_TCD[sProcess]
                        
                        # ----------- fuel cost --------------
                        fuel_price = objComm.fFuelPrice_YS[ind_year]   # USD/GJ
                        fuel_price = fuel_price / 277.778        # USD/GJ -> USD/kWh
                        cost_fuel = fuel_price / convert_eff
                        
                        # ----------- emission cost ---------------
                        # emission factor (kg/MJ = MTon/PJ)
                        fEmissionFactor = objComm.fEmissionFactor_CO2
                        # fuel consumption per kWh
                        fFuelConsumption = 1 / convert_eff          # kWh
                        fFuelConsumption = fFuelConsumption * 3.6   # kWh -> MJ (per kWh)
                        # carbon cost (USD/Tonne -> USD/kg)
                        carbon_price = carbon_price / 1000
                        # emission cost  (kg/MJ) * (MJ/kWh) * (USD/kg) = USD/kWh
                        cost_emission = fEmissionFactor * fFuelConsumption \
                            * carbon_price * (1-CCSCaptureRate)
                        
                        if sFuel == "biomass":
                            cost_emission = 0
                            if CCSCaptureRate > 0:
                                cost_emission = fEmissionFactor * fFuelConsumption \
                                    * convert_eff * carbon_price * CCSCaptureRate * -1
                        
                        break

                dData[sProcess] = cost_fuel + cost_emission + varOMCost
                
    return dData


def getProcVarGenCost_New(instance, objMarket, model, ind_year):
    ''' get variable generation cost of new build dispatchable processes  '''
    
    dData = {}
    
    for objZone in objMarket.lsZone:
        for sProcess in model.setProcNewDisp_TCD:
            
            if objZone.sZoneID + "/" in sProcess:
                sProcessCode = sProcess.split("/")[1]
                
                # variable generation cost
                varOMCost = model.pNewProcVarOMCost_TCD[sProcess]
                
                # search for fuel type
                sFuel = ""
                for obeProcDef in instance.lsProcessDefObjs:
                    if obeProcDef.sProcessName == sProcessCode:
                        sFuel = obeProcDef.sFuel
                        break
                
                # fuel and carbon cost
                cost_fuel = 0                
                fuel_price = 0
                cost_emission = 0
                carbon_price = instance.lsCountry[objZone.iCountryIndex].fCarbonCost_YS[ind_year]   # USD/tCO2e
                
                for objComm in instance.lsCountry[objZone.iCountryIndex].lsCommodity:     
                    if objComm.sCategory == sFuel:
                        
                        convert_eff = model.pNewProcDispEff_TCD[sProcess]
                        CCSCaptureRate = model.pNewProcDispCCSCapRate_TCD[sProcess]
                        
                        # ----------- fuel cost --------------
                        fuel_price = objComm.fFuelPrice_YS[ind_year]   # USD/GJ
                        fuel_price = fuel_price / 277.778    # USD/GJ -> USD/kWh
                        cost_fuel = fuel_price / convert_eff
                        
                        # ----------- emission cost ---------------
                        # emission factor (kg/MJ = MTon/PJ)
                        fEmissionFactor = objComm.fEmissionFactor_CO2
                        # fuel consumption per kWh
                        fFuelConsumption = 1 / convert_eff          # kWh
                        fFuelConsumption = fFuelConsumption * 3.6   # kWh -> MJ (per kWh)
                        # carbon cost (USD/Tonne -> USD/kg)
                        carbon_price = carbon_price / 1000
                        # emission cost  (kg/MJ) * (MJ/kWh) * (USD/kg) = USD/kWh
                        cost_emission = fEmissionFactor * fFuelConsumption \
                            * carbon_price * (1-CCSCaptureRate)
                        
                        if sFuel == "biomass":
                            cost_emission = 0
                            if CCSCaptureRate > 0:
                                cost_emission = fEmissionFactor * fFuelConsumption \
                                    * convert_eff * carbon_price * CCSCaptureRate * -1
                        
                        break
                
                dData[sProcess] = cost_fuel + cost_emission + varOMCost

    return dData


def getProcParamBaseCF_Month(objMarket, model, objDay):
    ''' get base year CF of dispatchable units generation (by month) '''
    
    iDayIndex = objDay.iDayIndex
    
    dData = {}
    for sProcess in model.setProcBaseDisp_TCD:
        sProcZoneID = sProcess.split("/")[0]
        
        fBaseCF = 0
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
    
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                            if objProcess.fBaseDispCF_288 is not None:
                                fBaseCF = sum(objProcess.fBaseDispCF_288[iDayIndex*24 : (iDayIndex+1)*24]) / 24
                                break

        dData[sProcess] = fBaseCF
        
    return dData


def getProcParamBaseBioGen_Month(objMarket, model, objDay, setCountryCode_CN):
    ''' get base year biomass processes generation (by month) '''
    
    iDayIndex = objDay.iDayIndex
    dData = {}
    
    for sCountry in setCountryCode_CN:
        
        totalGen = 0
        for objZone in objMarket.lsZone:
            if objZone.sCountry == sCountry:
        
                # base year CF
                fBaseCF = 0
                for objProcess in objZone.lsProcessAssump:
                    if objProcess.sProcessName == "BIO_ST":
                        if objProcess.fBaseDispCF_288 is not None:
                            fBaseCF = sum(objProcess.fBaseDispCF_288[ iDayIndex*24 : (iDayIndex+1)*24]) / 24
                            break
                
                # base year generation
                for objProcess in objZone.lsProcess:
                    if objProcess.sProcessName == "BIO_ST":
                        if objProcess.iCommitTime <= 2015:
                            totalGen +=  fBaseCF * objProcess.iCapacity \
                                * objProcess.fEquAvailFactor * 24
    
        dData[sCountry] = totalGen  # MWh
        
    return dData


def getProcParamBaseCF_Year(objMarket, model):
    '''' get base year dispatchable units generation CF (annual average) '''
    
    dData = {}
    for sProcess in model.setProcBaseDisp_TCD:
        sProcZoneID = sProcess.split("/")[0]
        
        fBaseCF = 0
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
    
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                            if objProcess.fBaseDispCF_288 is not None:
                                fBaseCF = sum(objProcess.fBaseDispCF_288[:]) \
                                    / len(objProcess.fBaseDispCF_288[:])
                                break

        dData[sProcess] = fBaseCF
        
    return dData


def getProcFixAnnCost_New(objMarket, model, setProc, ind_year):
    ''' get annualized fix cost of new build process '''
    # in M.USD per MW
    
    dData = {}
    
    for sProcess in setProc:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        dData[sProcess] = objProcess.fAnnualFixedCost[ind_year]
                        break
 
    return dData


#--------------------------------------------------------------------------------
# Technology Parameters - storage
#--------------------------------------------------------------------------------  
    
def getProcParamStor(objMarket, model, sParameter, iYear):
    ''' get aggregated parameters - existing storage processes '''
    
    dData = {}
    for sProcess in model.setProcBaseStor_TCS:
        sProcZoneID = sProcess.split("/")[0]
        
        liCap = []
        liParam = []
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
            
                for objProcess in objZone.lsProcess:
                    if objProcess.iDeCommitTime > iYear:                    
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                            
                            liCap.append( objProcess.iCapacity )
                            
                            if sParameter == "Cap":
                                liParam.append( objProcess.iCapacity )
                            elif sParameter == "Eff":
                                liParam.append( objProcess.fGrossEff )
                            elif sParameter == "EAF":
                                liParam.append( objProcess.fEquAvailFactor )
                            elif sParameter == "Dur":
                                liParam.append( objProcess.fDuration )            
        
        if len(liCap) > 0:
            sumCap = sum(liCap)
            for ind_p, param in enumerate(liCap):
                liCap[ind_p] = liCap[ind_p] / sumCap
            
            if sParameter == "Cap":
                dData[sProcess] = sumCap
            else:
                fParam = 0
                for ind_p, param in enumerate(liParam):
                    fParam += param * liCap[ind_p]
                dData[sProcess] = fParam
        else:
            if sParameter == "Eff":
                # assign a default value, otherwise could cause divid zero bugs
                dData[sProcess] = 0.8
            else:
                dData[sProcess] = 0
                
    return dData


def getProcParamStor_New(objMarket, model, sParameter, ind_year):
    ''' get new build storage process parameters '''
    
    dData = {}
    for sProcess in model.setProcNewStor_TCS:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        if sParameter == "Eff":
                            dData[sProcess] = objProcess.fGrossEff_YS[ind_year]
                        elif sParameter == "EAF":
                            dData[sProcess] = objProcess.fEquAvailFactor_YS[ind_year]
                        elif sParameter == "Dur":
                            dData[sProcess] = objProcess.fDuration_YS[ind_year]     
                        break
    return dData


def getProcStorCapLim_New(objMarket, model, iYear):
    ''' get the new build capacity limit of storage process (pumped hydro storage) '''
    
    dData = {}
    for sProcess in model.setProcNewStor_TCS:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        if objProcess.sProcessName == "HYD_PS":
                            
                            # default limiot
                            fTotalLimit = objProcess.fREDevLimit
                            
                            # existing capacity
                            fTotalExisting = 0
                            for objProcessEx in objZone.lsProcess:
                                if objProcessEx.iDeCommitTime > iYear:                    
                                    if objProcessEx.sProcessName == objProcess.sProcessName:
                                        fTotalExisting = fTotalExisting + objProcessEx.iCapacity
                                        
                            dData[sProcess] = max( 0, fTotalLimit - fTotalExisting)
                            
                        else:
                            dData[sProcess] = 999999
                        break

    return dData


#--------------------------------------------------------------------------------
# Technology Parameters - hydropower
#--------------------------------------------------------------------------------  
    
def getProcParamHydro(objMarket, model, sParameter, iYear):
    ''' get aggregated process parameters - existing hydropower '''     
    
    dData = {}
    for sProcess in model.setProcBaseHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        sProcZoneName = sProcess.split("/")[1]
        
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
    
                fCap_LG = 0
                fCap_SM = 0
                fEAF_LG = 0.9 # assumption on default efficiency
                fEAF_SM = 0.9 # assumption on default efficiency
                for objProcess in objZone.lsProcess:
                    if objProcess.iDeCommitTime > iYear:  
                            
                        if objProcess.sProcessName == "HYD_LG":
                            fCap_LG = fCap_LG + objProcess.iCapacity
                            fEAF_LG = objProcess.fEquAvailFactor
                        if objProcess.sProcessName == "HYD_SM":
                            fCap_SM = fCap_SM + objProcess.iCapacity
                            fEAF_SM = objProcess.fEquAvailFactor
                    
                if sParameter == "Cap":
                    if sProcZoneName == "HYD_LG":
                        dData[sProcess] = fCap_LG
                    elif sProcZoneName == "HYD_SM":
                        dData[sProcess] = fCap_SM
                elif sParameter == "EAF":
                    if sProcZoneName == "HYD_LG":
                        dData[sProcess] = fEAF_LG
                    elif sProcZoneName == "HYD_SM":
                        dData[sProcess] = fEAF_SM

    return dData


def getProcParamHydro_New(objMarket, model, sParameter, ind_year):
    ''' get new build hydropower process parameters '''
    
    dData = {}
    for sProcess in model.setProcNewHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        if sParameter == "Eff":
                            dData[sProcess] = objProcess.fGrossEff_YS[ind_year]
                        elif sParameter == "EAF":
                            dData[sProcess] = objProcess.fEquAvailFactor_YS[ind_year]   
            
                        break
    return dData


def getProcHydroGen(model, instance, objMarket, iYear):
    ''' get default hydopower generation of existing units '''
    
    dData = {}
    for sProcess in model.setProcBaseHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                fCap_LG = 0
                fCap_SM = 0
                fEAF_LG = 0
                fEAF_SM = 0
                iZoneProcAssumIndex_LG = -1
                iZoneProcAssumIndex_SM = -1
                
                for objProcess in objZone.lsProcess:
                    if objProcess.iDeCommitTime > iYear: 
    
                        if objProcess.sProcessName == "HYD_LG":
                            fCap_LG = fCap_LG + objProcess.iCapacity
                            fEAF_LG = objProcess.fEquAvailFactor
                            iZoneProcAssumIndex_LG = objProcess.iZoneProcAssumIndex
                        elif objProcess.sProcessName == "HYD_SM":
                            fCap_SM = fCap_SM + objProcess.iCapacity
                            fEAF_SM = objProcess.fEquAvailFactor
                            iZoneProcAssumIndex_SM = objProcess.iZoneProcAssumIndex
                        
                sProcZoneName = sProcess.split("/")[1]
                    
                if sProcZoneName == "HYD_LG":
                    if fCap_LG > 0:
                        for sTSIndex in model.setTimeSlice_TS:
                            fProcCF = objZone.lsProcessAssump[iZoneProcAssumIndex_LG].fRECF_TS[int(sTSIndex)-1]        
                            # the available factor should not influence output 
                            # the flow is fixed, but bounded by max EAF
                            if fProcCF < fEAF_LG:
                                dData[sProcess, sTSIndex] = fCap_LG * fProcCF
                            else:
                                dData[sProcess, sTSIndex] = fCap_LG * fEAF_LG
                    else:
                        # assign 0 to the dictionary to avoid errors when the units decommited
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = 0
                            
                elif sProcZoneName == "HYD_SM":
                    if fCap_SM > 0:
                        for sTSIndex in model.setTimeSlice_TS:
                            fProcCF = objZone.lsProcessAssump[iZoneProcAssumIndex_SM].fRECF_TS[int(sTSIndex)-1]        
                            dData[sProcess, sTSIndex] = fCap_SM * fProcCF * fEAF_SM
                    else:
                        # assign 0 to the dictionary to avoid errors when the units decommited
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = 0

    return dData


def getProcHydroGen_CE(model, instance, objMarket, iYear):
    ''' get default hydopower generation of existing units '''
    
    dData = {}
    for sProcess in model.setProcBaseHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                fCap_LG = 0
                fCap_SM = 0
                fEAF_LG = 0
                fEAF_SM = 0
                iZoneProcAssumIndex_LG = -1
                iZoneProcAssumIndex_SM = -1
                for objProcess in objZone.lsProcess:
                    if objProcess.iDeCommitTime > iYear: 
    
                        if objProcess.sProcessName == "HYD_LG":
                            fCap_LG = fCap_LG + objProcess.iCapacity
                            fEAF_LG = objProcess.fEquAvailFactor
                            iZoneProcAssumIndex_LG = objProcess.iZoneProcAssumIndex
                        elif objProcess.sProcessName == "HYD_SM":
                            fCap_SM = fCap_SM + objProcess.iCapacity
                            fEAF_SM = objProcess.fEquAvailFactor
                            iZoneProcAssumIndex_SM = objProcess.iZoneProcAssumIndex
                        
                sProcZoneName = sProcess.split("/")[1]
                    
                if sProcZoneName == "HYD_LG":
                    if fCap_LG > 0:
                        for sTSIndex in model.setTimeSlice_TS:
                            fProcCF = objZone.lsProcessAssump[iZoneProcAssumIndex_LG].fRECF_CEP[int(sTSIndex)-1]        
                            # the available factor should not influence output 
                            # the flow is fixed, but bounded by max EAF
                            if fProcCF < fEAF_LG:
                                dData[sProcess, sTSIndex] = fCap_LG * fProcCF
                            else:
                                dData[sProcess, sTSIndex] = fCap_LG * fEAF_LG
                    else:
                        # assign 0 to the dictionary to avoid errors when the units decommited
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = 0
                            
                elif sProcZoneName == "HYD_SM":
                    if fCap_SM > 0:
                        for sTSIndex in model.setTimeSlice_TS:
                            fProcCF = objZone.lsProcessAssump[iZoneProcAssumIndex_SM].fRECF_CEP[int(sTSIndex)-1]        
                            dData[sProcess, sTSIndex] = fCap_SM * fProcCF * fEAF_SM
                    else:
                        # assign 0 to the dictionary to avoid errors when the units decommited
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = 0
        
    return dData


def getProcHydroCF_CE(model, instance, objMarket):
    ''' get default hydopower CF '''
    
    dData = {}
    for sProcess in model.setProcNewHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP[int(sTSIndex)-1] 
                        break      
    return dData


def getProcHydroCFTest_CE(model, instance, objMarket):
    ''' get default hydopower CF for CE model '''
    
    dData = {}
    for sProcess in model.setProcNewHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:
                        
                        for sTSIndex in model.setTSRT_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP_RT[int(sTSIndex)] 
                        break      
    return dData


def getProcHydrCapLim_New(objMarket, model, iYear):
    ''' get the new build capacity limit of hydropower '''
    
    dData = {}
    for sProcess in model.setProcNewHydr_TCH:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName == sProcess:

                        # default limiot
                        fTotalLimit = objProcess.fREDevLimit
                        
                        # existing capacity
                        fTotalExisting = 0
                        for objProcessEx in objZone.lsProcess:
                            if objProcessEx.iDeCommitTime > iYear:                    
                                if objProcessEx.sProcessName == objProcess.sProcessName:
                                    fTotalExisting = fTotalExisting + objProcessEx.iCapacity
                                    
                        dData[sProcess] = max( 0, fTotalLimit - fTotalExisting)
                        break
    return dData


#--------------------------------------------------------------------------------
# Technology Parameters - renewables
#--------------------------------------------------------------------------------  

def getProcRenDefCF_New(objMarket, model, iYear):
    ''' get the defult capacity factors of new renewables '''
    
    dData = {}
    for sProcess in model.setProcNewRE_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP[int(sTSIndex)-1]
                        break
    return dData


def getProcRenDefCF_Offs_New(objMarket, model, iYear):
    ''' get the defult capacity factors of offshore new renewables '''
    
    dData = {}
    for sProcess in model.setProcNewRE_Offs_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZoneOffs:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        for sTSIndex in model.setTimeSlice_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP[int(sTSIndex)-1]
                        break
    return dData


def getProcRenDefCFTest_New(objMarket, model, iYear):
    ''' get the defult capacity factors of renewables in testing hours'''
    
    dData = {}
    for sProcess in model.setProcNewRE_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        for sTSIndex in model.setTSRT_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP_RT[int(sTSIndex)]
                        break
    return dData


def getProcRenDefCFTest_Offs_New(objMarket, model, iYear):
    ''' get the defult capacity factors of offshore renewables in testing hours'''
    
    dData = {}
    for sProcess in model.setProcNewRE_Offs_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZoneOffs:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        for sTSIndex in model.setTSRT_TS:
                            dData[sProcess, sTSIndex] = objProcess.fRECF_CEP_RT[int(sTSIndex)]
                        break
    return dData


def getProcRenCapLim_New(objMarket, model, iYear):
    ''' get the new build capacity limit of renewables '''
    
    dData = {}
    for sProcess in model.setProcNewRE_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        # default limit
                        fTotalLimit = objProcess.fREDevLimit                        
                        # existing capacity
                        fTotalExisting = 0
                        for objProcessEx in objZone.lsProcess:
                            if objProcessEx.iDeCommitTime > iYear:                    
                                if objProcessEx.sProcessName == objProcess.sProcessName \
                                    and objProcessEx.iCFClass == objProcess.iCFClass:
                                    fTotalExisting = fTotalExisting + objProcessEx.iCapacity
                                    
                        dData[sProcess] = max( 0, fTotalLimit - fTotalExisting)
                        break
    return dData


def getProcRenCapLim_Offs_New(objMarket, model, iYear):
    ''' get the new build capacity limit of offshore renewables '''
    
    dData = {}
    for sProcess in model.setProcNewRE_Offs_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZoneOffs:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        # default limiot
                        fTotalLimit = objProcess.fREDevLimit                        
                        # existing capacity
                        fTotalExisting = 0
                        for objProcessEx in objZone.lsProcess:
                            if objProcessEx.iDeCommitTime > iYear:                    
                                if objProcessEx.sProcessName == objProcess.sProcessName \
                                    and objProcessEx.iCFClass == objProcess.iCFClass:
                                    fTotalExisting = fTotalExisting + objProcessEx.iCapacity
                                    
                        dData[sProcess] = max( 0, fTotalLimit - fTotalExisting)
                        break
    return dData


def getProcFixAnnCostRE_New(objMarket, model, ind_year):
    ''' get annualized fix cost of new build process  '''
    # in M.USD per MW
    
    dData = {}
    for sProcess in model.setProcNewRE_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        dData[sProcess] = objProcess.fAnnualFixedCost[ind_year]
                        break
    return dData


def getProcFixAnnCostRE_Offs_New(objMarket, model, ind_year):
    ''' get annualized fix cost of new build offshore process  '''
    # in M.USD per MW
    
    dData = {}
    for sProcess in model.setProcNewRE_Offs_TCR:
        sProcZoneID = sProcess.split("/")[0]
        for objZone in objMarket.lsZoneOffs:
            if objZone.sZoneID == sProcZoneID:
                
                for objProcess in objZone.lsProcessAssump:
                    if objZone.sZoneID + "/" + objProcess.sProcessName \
                        + "/" + str(objProcess.iCFClass) == sProcess:
                        dData[sProcess] = objProcess.fAnnualFixedCost[ind_year]
                        break
    return dData


#--------------------------------------------------------------------------------
# Technology Parameters - ancillary service
#--------------------------------------------------------------------------------  
    
def getProcASMax(objMarket, model, sParameter, iYear):
    ''' get max provision of each existing process '''
    
    dData = {}

    if sParameter == "T1":
        for sProcCode in model.setProcBaseAS_TCA1:
            sProcZoneID = sProcCode.split("/")[0]
            fASMax = 0
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for objProcess in objZone.lsProcess:
                        if objProcess.iDeCommitTime > iYear: 
                            if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                                fASMax += objProcess.fASMax_T1 * objProcess.fEquAvailFactor
            dData[sProcCode] = fASMax
            
    elif sParameter == "T2":
        for sProcCode in model.setProcBaseAS_TCA2:
            sProcZoneID = sProcCode.split("/")[0]            
            fASMax = 0
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for objProcess in objZone.lsProcess:
                        if objProcess.iDeCommitTime > iYear: 
                            if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                                fASMax += objProcess.fASMax_T2 * objProcess.fEquAvailFactor
            dData[sProcCode] = fASMax
            
    elif sParameter == "T3":
        for sProcCode in model.setProcBaseAS_TCA3:
            sProcZoneID = sProcCode.split("/")[0]
            fASMax = 0
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for objProcess in objZone.lsProcess:
                        if objProcess.iDeCommitTime > iYear: 
                            if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                                fASMax += objProcess.fASMax_T3 * objProcess.fEquAvailFactor
            dData[sProcCode] = fASMax
        
    return dData


def getProcASMax_New(objMarket, model, sParameter, ind_year):
    ''' get max provision of each new process '''
    
    dData = {}
    iUnitAvail = 0.9

    if sParameter == "T1":
        for sProcCode in model.setProcNewAS_TCA1:
            sProcZoneID = sProcCode.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    
                    for objProcess in objZone.lsProcessAssump:
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                            # 30 second ramp capacity
                            dData[sProcCode] = min( iUnitAvail, objProcess.fRampRate_YS[ind_year] / 100 * 0.5)
            
    elif sParameter == "T2":
        for sProcCode in model.setProcNewAS_TCA2:
            sProcZoneID = sProcCode.split("/")[0]            
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    
                    for objProcess in objZone.lsProcessAssump:
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                            # 10 min ramp capacity
                            dData[sProcCode] = min( iUnitAvail, objProcess.fRampRate_YS[ind_year] / 100 * 10) 
            
    elif sParameter == "T3":
        for sProcCode in model.setProcNewAS_TCA3:
            sProcZoneID = sProcCode.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    
                    for objProcess in objZone.lsProcessAssump:
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProcCode:
                            # 30 min ramp capacity
                            dData[sProcCode] = min( iUnitAvail, objProcess.fRampRate_YS[ind_year] / 100 * 30) 
        
    return dData

