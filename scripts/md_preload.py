#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to initialize model settings
#

from numpy import zeros

import cls_process


#----------------------------------------------------
# update testing case TS assumptions
#----------------------------------------------------

def updateTestTS(instance, objMarket, ind_year):
    ''' update montthly testing cases in CE model '''
    # the most extreme hour in each month
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    ResDemZone8760 = []
    for ind_zone, objZone in enumerate(objMarket.lsZone):
        zoneResDem = []
        for ind_TS in range(0,8760):
            
            ### demand
            demand = objZone.fPowerDemand_8760_YS[ind_TS, ind_year]
            
            ### renewable supply
            fAllGenRe = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch":  # include hydro
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_8760[ind_TS]
                        fAllGenRe = fAllGenRe + objProcess.iCapacity * fProcCF
                
            zoneResDem.append( demand - fAllGenRe )
        ResDemZone8760.append(zoneResDem)

    # generation from offshore
    for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
        zoneResDem = []
        for ind_TS in range(0,8760):
            
            ### renewable supply
            fAllGenRe = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch":
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_8760[ind_TS]
                        fAllGenRe = fAllGenRe + objProcess.iCapacity * fProcCF
                
            zoneResDem.append( - fAllGenRe )
        ResDemZone8760.append(zoneResDem)

    # find the highest res demand in each month
    lsHighResDemTSind = []
    lsMonthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    indHour = 0
    for iMonthDays in lsMonthDays:
        iTSHighResDem = 0
        fHighestResDem = -99999999
        for indTS in range( indHour, indHour + (iMonthDays*24) ):
            
            fTotalResDem = 0
            for ind_zone in range(0,len(ResDemZone8760)):
                fTotalResDem += ResDemZone8760[ind_zone][indTS]
            
            if fTotalResDem > fHighestResDem:
                fHighestResDem = fTotalResDem
                iTSHighResDem = indTS
                
        lsHighResDemTSind.append(iTSHighResDem)
        indHour = indHour + iMonthDays*24
    
    # assign the most extreme cases
    for objZone in objMarket.lsZone:
        objZone.fPowerDemand_CEP_RT = []
        for indTS in lsHighResDemTSind:
            objZone.fPowerDemand_CEP_RT.append( objZone.fPowerDemand_8760_YS[indTS, ind_year] )
        
    for objZone in objMarket.lsZone:
        for objProcAssump in objZone.lsProcessAssump:
            if objProcAssump.sOperationMode == "NonDispatch":
                objProcAssump.fRECF_CEP_RT = []
                for indTS in lsHighResDemTSind:
                    objProcAssump.fRECF_CEP_RT.append( objProcAssump.fRECF_8760[indTS] )
                    
    # apply the same TS index to offshore process
    for objZone in objMarket.lsZoneOffs:
        for objProcAssump in objZone.lsProcessAssump:
            if objProcAssump.sOperationMode == "NonDispatch":
                objProcAssump.fRECF_CEP_RT = []
                for indTS in lsHighResDemTSind:
                    objProcAssump.fRECF_CEP_RT.append( objProcAssump.fRECF_8760[indTS] )
    
    return


#----------------------------------------------------
# initial process sets - existing process
#----------------------------------------------------

def initBaseSets(instance, objMarket, ind_year):
    ''' assemble process sets from *existing* process list '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
        
    ### dispatchable process
    lsZoneDispatchProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcess:
            if objProcess.sOperationMode == "Dispatch":
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneDispatchProcess.append( objZone.sZoneID + "/" + sTech )
        
    objMarket.setProcBaseDisp_TCD = lsZoneDispatchProcess
    
    ### storage process
    lsZoneStorageProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcess:
            if objProcess.sOperationMode == "Storage":
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneStorageProcess.append( objZone.sZoneID + "/" + sTech )
    
    objMarket.setProcBaseStor_TCS = lsZoneStorageProcess
    
    ### hydropower process
    lsZoneHydroProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcess:
            if objProcess.sProcessName in ["HYD_LG","HYD_SM"]:
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneHydroProcess.append( objZone.sZoneID + "/" + sTech )
                            
    objMarket.setProcBaseHydr_TCH = lsZoneHydroProcess
    
    ### terrestrial transmission
    setTrans = list()
    for objTrans in objMarket.lsTrans:
        if iYear < 2030:
            if objTrans.b2015Conn == 1:
                setTrans.append(objTrans.sTransID)
        else:
            setTrans.append(objTrans.sTransID)
    
    objMarket.setTransLDZ_TRL = setTrans
    
    ### offshore transmission
    setTrans = list()
    for objTrans in objMarket.lsTrans_off:
        if iYear < 2030:
            if objTrans.b2015Conn == 1:
                setTrans.append(objTrans.sTransID)
        else:
            setTrans.append(objTrans.sTransID)
    
    objMarket.setTransOFZ_TRF = setTrans
    
    ### process providing first tier AS 
    lsZoneProcessT1 = list()
    lsZoneProcessT2 = list()
    lsZoneProcessT3 = list()
    for objZone in objMarket.lsZone:
        for objProcess in objZone.lsProcess:
            sProcCode = objZone.sZoneID + "/" + objProcess.sProcessName
            
            if objProcess.bAS_T1 == 1:
                if sProcCode not in lsZoneProcessT1:
                    lsZoneProcessT1.append( sProcCode )

            if objProcess.bAS_T2 == 1:
                if sProcCode not in lsZoneProcessT2:
                    lsZoneProcessT2.append( sProcCode )

            if objProcess.bAS_T3 == 1:
                if sProcCode not in lsZoneProcessT3:
                    lsZoneProcessT3.append( sProcCode )
    
    objMarket.setProcBaseAS_TCA1 = lsZoneProcessT1
    objMarket.setProcBaseAS_TCA2 = lsZoneProcessT2
    objMarket.setProcBaseAS_TCA3 = lsZoneProcessT3
    
    return


#-------------------------------------------------------------------
# initial process sets - new candidate process
#-------------------------------------------------------------------
    
def initNewSets(instance, objMarket, ind_year):
    ''' assembled process sets from *candidate* process list, for model CE '''
    
    ### dispatchable process
    lsZoneDispatchProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcessAssump:
            if objProcess.sOperationMode == "Dispatch":
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneDispatchProcess.append( objZone.sZoneID + "/" + sTech )
        
    objMarket.setProcNewDisp_TCD = lsZoneDispatchProcess
    
    ### storage process
    lsZoneStorageProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcessAssump:
            if objProcess.sOperationMode == "Storage":
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneStorageProcess.append( objZone.sZoneID + "/" + sTech )
    
    objMarket.setProcNewStor_TCS = lsZoneStorageProcess
    
    ### hydropower process
    lsZoneHydroProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcessAssump:
            if objProcess.sProcessName in ["HYD_LG","HYD_SM"]:
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName)
                    
        for sTech in lsTech:
            lsZoneHydroProcess.append( objZone.sZoneID + "/" + sTech )
                            
    objMarket.setProcNewHydr_TCH = lsZoneHydroProcess
        
    ### renewable process (exclude hydro, biomass)
    lsZoneRenewProcess = list()
    for objZone in objMarket.lsZone:
        lsTech = []
        for objProcess in objZone.lsProcessAssump:
            if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName + "/" + str(objProcess.iCFClass))
                    
        for sTech in lsTech:
            lsZoneRenewProcess.append( objZone.sZoneID + "/" + sTech )
                            
    objMarket.setProcNewRE_TCR = lsZoneRenewProcess
    
    ### renewable process (exclude hydro, biomass), offshore 
    lsZoneRenewProcess = list()
    for objZone in objMarket.lsZoneOffs:
        lsTech = []
        for objProcess in objZone.lsProcessAssump:
            if objProcess.sOperationMode == "NonDispatch":
                if objProcess.sProcessName not in lsTech:
                    lsTech.append(objProcess.sProcessName + "/" + str(objProcess.iCFClass))
                    
        for sTech in lsTech:
            lsZoneRenewProcess.append( objZone.sZoneID + "/" + sTech )
                            
    objMarket.setProcNewRE_Offs_TCR = lsZoneRenewProcess
    
    ### process providing first tier AS 
    lsZoneProcessT1 = list()
    lsZoneProcessT2 = list()
    lsZoneProcessT3 = list()
    for objZone in objMarket.lsZone:
        for objProcess in objZone.lsProcessAssump:
            sProcCode = objZone.sZoneID + "/" + objProcess.sProcessName
            
            if objProcess.bAS_T1 == 1:
                if sProcCode not in lsZoneProcessT1:
                    lsZoneProcessT1.append( sProcCode )

            if objProcess.bAS_T2 == 1:
                if sProcCode not in lsZoneProcessT2:
                    lsZoneProcessT2.append( sProcCode )

            if objProcess.bAS_T3 == 1:
                if sProcCode not in lsZoneProcessT3:
                    lsZoneProcessT3.append( sProcCode )
    
    objMarket.setProcNewAS_TCA1 = lsZoneProcessT1
    objMarket.setProcNewAS_TCA2 = lsZoneProcessT2
    objMarket.setProcNewAS_TCA3 = lsZoneProcessT3
    
    return


#---------------------------------------------------------------------------------
# variables initialization
#---------------------------------------------------------------------------------

def ED_initVariables(instance, objMarket, ind_year):
    ''' initialize variables in ED model '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    iBaseYear = instance.iAllYearSteps_YS[0]
    
    ##### base year initializtion ------------------------------------
    if ind_year == 0:
        
        # transmission capacity
        for objTrans in objMarket.lsTrans:
            objTrans.dicTransAccCap_YS[iYear] = objTrans.fBaseCap
            objTrans.dicTransNewBuild_YS[iYear] = 0

        for objTrans in objMarket.lsTrans_off:
            objTrans.dicTransAccCap_YS[iYear] = objTrans.fBaseCap
            objTrans.dicTransNewBuild_YS[iYear] = 0
                
    ##### CNS carbon emission limits pathway
    if ind_year == 1 and instance.sPathway == "CNS":
        fBaseYearEmission = 0   # Tonne
        fBaseYearGen = 0        # MWh
        for objZone in objMarket.lsZone:
            fBaseYearEmission += objMarket.dicCO2Emission_ZNL_YS[objZone.sZone, iBaseYear]
            fBaseYearGen += objMarket.dicSupplyZone_ZNL_YS[objZone.sZone, iBaseYear]
        for objZone in objMarket.lsZoneOffs:
            fBaseYearGen += objMarket.dicSupplyOffs_ZNF_YS[objZone.sZone, iBaseYear]
        
        fEmissoinPathway = instance.fEmissoinLimits_YS
        for ind_y, iEPYear in enumerate(instance.iAllYearSteps_YS):
            objMarket.dicCNSEmissionFactor_YS[iEPYear] =  fBaseYearEmission / fBaseYearGen * fEmissoinPathway[ind_y]
        
        for ind_y, iEPYear in enumerate(instance.iAllYearSteps_YS):
            fDemand = 0
            for objZone in objMarket.lsZone:
                fDemand += sum(objZone.fPowerDemand_8760_YS[:,ind_y])
            objMarket.dicCNSEmissionCap_YS[iEPYear] = fDemand * objMarket.dicCNSEmissionFactor_YS[iEPYear]
            
    ##### present year data updates ------------------------------------
    
    # present year temporal output variables initialization (temporal)
    
    ### the following variables in power units (MW)
    objMarket.pDemand_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))
    objMarket.pNonDispGen_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))
    
    objMarket.vSupplyZone_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))
    objMarket.vSupplyOffs_ZNF_TS = zeros((len(objMarket.lsZoneOffs),len(instance.lsTimeSlice)))
    objMarket.vSpillZone_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))
    objMarket.vSpillOffs_ZNF_TS = zeros((len(objMarket.lsZoneOffs),len(instance.lsTimeSlice)))
    objMarket.vTransLDZIn_TRL_TS = zeros((len(objMarket.lsTrans),len(instance.lsTimeSlice)))
    objMarket.vTransLDZOut_TRL_TS = zeros((len(objMarket.lsTrans),len(instance.lsTimeSlice)))
    objMarket.vTransOFZIn_TRF_TS = zeros((len(objMarket.lsTrans_off),len(instance.lsTimeSlice)))
    objMarket.vTransOFZOut_TRF_TS = zeros((len(objMarket.lsTrans_off),len(instance.lsTimeSlice)))
    objMarket.vExProcDispPwOutGrs_TCD_TS = zeros((len(objMarket.setProcBaseDisp_TCD),len(instance.lsTimeSlice)))
    objMarket.vExProcDispPwOutNet_TCD_TS = zeros((len(objMarket.setProcBaseDisp_TCD),len(instance.lsTimeSlice)))
    objMarket.vExProcStorPwIn_TCS_TS = zeros((len(objMarket.setProcBaseStor_TCS),len(instance.lsTimeSlice)))
    objMarket.vExProcStorPwOut_TCS_TS = zeros((len(objMarket.setProcBaseStor_TCS),len(instance.lsTimeSlice)))
    objMarket.vExProcHydrPwOut_TCH_TS = zeros((len(objMarket.setProcBaseHydr_TCH),len(instance.lsTimeSlice)))
    objMarket.vExProcASProv_TCA1_TS = zeros((len(objMarket.setProcBaseAS_TCA1),len(instance.lsTimeSlice)))
    objMarket.vExProcASProv_TCA2_TS = zeros((len(objMarket.setProcBaseAS_TCA2),len(instance.lsTimeSlice)))
    objMarket.vExProcASProv_TCA3_TS = zeros((len(objMarket.setProcBaseAS_TCA3),len(instance.lsTimeSlice)))
    
    ### the following variables in energy units (already account rep. time slices)
    objMarket.vFuelCons_COA_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))    # GJ
    objMarket.vFuelCons_GAS_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))    # GJ
    objMarket.vFuelCons_OIL_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))    # GJ
    objMarket.vFuelCons_NUK_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))    # GJ
    objMarket.vFuelCons_BIO_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))    # GJ
    
    objMarket.vCO2Emission_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))     # Tonnes
    objMarket.vCCSCapture_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice)))      # Tonne    
    objMarket.vZoneMarketPrice_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice))) # USD/kWh
    objMarket.vTotalVarGenCost_ZNL_TS = zeros((len(objMarket.lsZone),len(instance.lsTimeSlice))) # M.USD
    
    objMarket.lsDayVarCost = []
    
    ### update capacity ---------------------------------------------   
    
    ### present available process capacity
    for objZone in objMarket.lsZone:
        for objProcessAssump in objZone.lsProcessAssump:
            
            fTotalCap = 0
            for objProcess in objZone.lsProcess:
                if objProcessAssump.sProcessName == objProcess.sProcessName and objProcessAssump.iCFClass == objProcess.iCFClass:
                    if objProcess.iDeCommitTime > iYear:  
                        
                        fTotalCap += objProcess.iCapacity

            objProcessAssump.dicProcAccCapacity_YS[iYear] = fTotalCap

    # offhosre wind capcity
    for objZone in objMarket.lsZoneOffs:
        for objProcessAssump in objZone.lsProcessAssump:
            
            fTotalCap = 0
            for objProcess in objZone.lsProcess:
                if objProcessAssump.sProcessName == objProcess.sProcessName and objProcessAssump.iCFClass == objProcess.iCFClass:
                    if objProcess.iDeCommitTime > iYear:  
                        
                        fTotalCap += objProcess.iCapacity

            objProcessAssump.dicProcAccCapacity_YS[iYear] = fTotalCap
    
    
    ### non-dispatchable generation ---------------------------------------------       
    
    # terrestrial zones
    NonDisGenAll_ZNL_TS = {}
    NonDisGenWind_ZNL_TS = {}
    NonDisGenPV_ZNL_TS = {}
    NonDisGenCSP_ZNL_TS = {}
    NonDisGenOTR_ZNL_TS = {}

    for ind_Zone, objZone in enumerate(objMarket.lsZone):  
        for objTS in instance.lsTimeSlice:
            sTSIndex = objTS.sTSIndex
            
            fAllGen = 0
            allWindGen = 0
            allPVGen = 0
            allCSPGen = 0
            allOtherGen = 0
            
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        if objProcess.sProcessName[0:3] == "WND":
                            fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                            allWindGen = allWindGen + objProcess.iCapacity * fProcCF
                        elif objProcess.sProcessName[0:2] == "PV":
                            fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                            allPVGen = allPVGen + objProcess.iCapacity * fProcCF
                        elif objProcess.sProcessName[0:3] == "CSP":
                            fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                            allCSPGen = allCSPGen + objProcess.iCapacity * fProcCF
                        else:
                            fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                            allOtherGen = allOtherGen + objProcess.iCapacity * fProcCF
            
            fAllGen = allWindGen + allPVGen + allCSPGen + allOtherGen
                
            NonDisGenAll_ZNL_TS[objZone.sZoneID, sTSIndex] = fAllGen
            NonDisGenWind_ZNL_TS[objZone.sZoneID, sTSIndex] = allWindGen
            NonDisGenPV_ZNL_TS[objZone.sZoneID, sTSIndex] = allPVGen
            NonDisGenCSP_ZNL_TS[objZone.sZoneID, sTSIndex] = allCSPGen
            NonDisGenOTR_ZNL_TS[objZone.sZoneID, sTSIndex] = allOtherGen
            
    objMarket.NonDisGenAll_ZNL_TS = NonDisGenAll_ZNL_TS
    objMarket.NonDisGenWind_ZNL_TS = NonDisGenWind_ZNL_TS
    objMarket.NonDisGenPV_ZNL_TS = NonDisGenPV_ZNL_TS
    objMarket.NonDisGenCSP_ZNL_TS = NonDisGenCSP_ZNL_TS
    objMarket.NonDisGenOTR_ZNL_TS = NonDisGenOTR_ZNL_TS
        
    # offshore zones
    NonDisGenAll_ZNF_TS = {}

    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):  
        for objTS in instance.lsTimeSlice:
            sTSIndex = objTS.sTSIndex          
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
            
            NonDisGenAll_ZNF_TS[objZone.sZoneID, sTSIndex] = fAllGen
            
    objMarket.NonDisGenAll_ZNF_TS = NonDisGenAll_ZNF_TS
    
    ### calculate residual demand ---------------------------------------------      
    # generation from hydro
    NonDisGenHYD_ZNL_TS = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):  
        for objTS in instance.lsTimeSlice:
            sTSIndex = objTS.sTSIndex
            
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_TS[int(sTSIndex)-1]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
             
            NonDisGenHYD_ZNL_TS[objZone.sZoneID, sTSIndex] = fAllGen
            
    objMarket.NonDisGenHYD_ZNL_TS = NonDisGenHYD_ZNL_TS
    
    # residual demand
    ResDemand_TS = {}
    for objTS in instance.lsTimeSlice:
        sTSIndex = objTS.sTSIndex
        
        demand = 0
        ReGen = 0
        for ind_Zone, objZone in enumerate(objMarket.lsZone):  
            demand += objZone.fPowerDemand_TS_YS[int(sTSIndex)-1, ind_year]
            ReGen += NonDisGenAll_ZNL_TS[objZone.sZoneID, sTSIndex]
            ReGen += NonDisGenHYD_ZNL_TS[objZone.sZoneID, sTSIndex]
        for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):  
            ReGen += NonDisGenAll_ZNF_TS[objZone.sZoneID, sTSIndex]

        if demand - ReGen > 0:
            ResDemand_TS[sTSIndex] = demand - ReGen
        else:
            ResDemand_TS[sTSIndex] = 1
    objMarket.ResDemand_TS = ResDemand_TS
    
    return 


def CE_initVariables(instance, objMarket, ind_year):
    ''' initialize variables in CE model '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
        
    ### non-dispatchable generation - existing process -------------------       
    # terrestrial zones
    NonDisGenAll_ZNL_TS = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):  
        for objTS in instance.lsTimeSlice_CEP:
            sTSIndex = objTS.sTSIndex
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_CEP[int(sTSIndex)-1]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
            NonDisGenAll_ZNL_TS[objZone.sZoneID, sTSIndex] = fAllGen  
    objMarket.NonDisGenAll_ZNL_TS = NonDisGenAll_ZNL_TS
        
    # offshore zones
    NonDisGenAll_ZNF_TS = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):  
        for objTS in instance.lsTimeSlice_CEP:
            sTSIndex = objTS.sTSIndex          
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_CEP[int(sTSIndex)-1]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
            NonDisGenAll_ZNF_TS[objZone.sZoneID, sTSIndex] = fAllGen
    objMarket.NonDisGenAll_ZNF_TS = NonDisGenAll_ZNF_TS
    
    ### non-dispatchable generation - existing process - testing case -----       
    # terrestrial zones
    NonDisGenAllTest_ZNL_TS = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZone):  
        for iTS in range(0,12):
            sTSIndex = str(iTS)
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_CEP_RT[int(sTSIndex)]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
            NonDisGenAllTest_ZNL_TS[objZone.sZoneID, sTSIndex] = fAllGen  
    objMarket.NonDisGenAllTest_ZNL_TS = NonDisGenAllTest_ZNL_TS
        
    # offshore zones
    NonDisGenAllTest_ZNF_TS = {}
    for ind_Zone, objZone in enumerate(objMarket.lsZoneOffs):  
        for iTS in range(0,12):
            sTSIndex = str(iTS)          
            fAllGen = 0
            for objProcess in objZone.lsProcess:
                if objProcess.iDeCommitTime > iYear:
                    if objProcess.sOperationMode == "NonDispatch" and objProcess.sProcessName not in ["HYD_LG","HYD_SM"]:
                        fProcCF = objZone.lsProcessAssump[objProcess.iZoneProcAssumIndex].fRECF_CEP_RT[int(sTSIndex)]
                        fAllGen = fAllGen + objProcess.iCapacity * fProcCF
            NonDisGenAllTest_ZNF_TS[objZone.sZoneID, sTSIndex] = fAllGen
    objMarket.NonDisGenAllTest_ZNF_TS = NonDisGenAllTest_ZNF_TS
    
    ### available biomass ------------------------
    BiomassSupply_CN = {}
    lsCountryList = list()
    for objZone in objMarket.lsZone:
        if objZone.sCountry not in lsCountryList:
            lsCountryList.append(objZone.sCountry )
            BiomassSupply_CN[objZone.sCountry] = instance.lsCountry[objZone.iCountryIndex].fBiomassLimit_YS[ind_year]
    objMarket.dicBiomassSupply_CN = BiomassSupply_CN
    
    return 

 
def CE_initRenInstallLimits(instance, objMarket, ind_year):
    ''' initialize renewable installation limits '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    lsCountryList = list()
    for objZone in objMarket.lsZone:
        if objZone.sCountry not in lsCountryList:
            lsCountryList.append(objZone.sCountry )
    
    # data items map to IRENA data
    lsRenewable = [ "WND_ON", "WND_OFF", "PV", "CSP", "HYD", "GEO_hydro", "BIO_ST" ]
    
    for objCountry in instance.lsCountry:
        if objCountry.sCountry in lsCountryList:
            for sReProc in lsRenewable:
                
                # check minimum capacity setting, set -1 if no value
                bMinSetting = True
                if (sReProc, str(iYear)) not in objCountry.dicRenMinInstall:
                    objCountry.dicRenewMinCapAdd[sReProc] = -1
                    bMinSetting = False
                    
                # check maximum capacity setting, set -1 if no value
                bMaxSetting = True
                if (sReProc, str(iYear)) not in objCountry.dicRenMaxInstall:                    
                    objCountry.dicRenewMaxCapAdd[sReProc] = -1
                    bMaxSetting = False
            
                # check limits
                if bMinSetting or bMaxSetting:
                    
                    lsZone = objMarket.lsZone
                    if sReProc == "WND_OFF":
                        lsZone = objMarket.lsZoneOffs
                    
                    minInstall = 0
                    if bMinSetting == True:
                        minInstall = objCountry.dicRenMinInstall[sReProc, str(iYear)]
                        
                    maxInstall = 0
                    if bMaxSetting == True:
                        maxInstall = objCountry.dicRenMaxInstall[sReProc, str(iYear)]
            
                    # existing capacity at the period
                    fExistCap = 0
                    for objZone in lsZone:            
                        if objZone.sCountry == objCountry.sCountry:
                            for objProc in objZone.lsProcess:
                                if objProc.sProcessName[0:len(sReProc)] == sReProc and objProc.sProcessName != "HYD_PS":
                                    if objProc.iDeCommitTime > iYear:
                                        fExistCap += objProc.iCapacity
                                        
                    # max capacity of the process
                    fMaxAvailCap = 0
                    for objZone in lsZone:            
                        if objZone.sCountry == objCountry.sCountry:
                            for objProc in objZone.lsProcessAssump:
                                if objProc.sProcessName[0:len(sReProc)] == sReProc and objProc.sProcessName != "HYD_PS":
                                    fMaxAvailCap += objProc.fREDevLimit  
            
                    if minInstall > 0:
                        if minInstall > fExistCap and minInstall < fMaxAvailCap:
                            fAddition = minInstall - fExistCap
                            objCountry.dicRenewMinCapAdd[sReProc] = fAddition
                        else:
                            objCountry.dicRenewMinCapAdd[sReProc] = 0
                            
                    if maxInstall > 0:
                        if sReProc == "BIO_ST": 
                            # biomass has no limit on capacity potential
                            objCountry.dicRenewMaxCapAdd[sReProc] = -1
                        else:
                            if maxInstall > fExistCap and maxInstall < fMaxAvailCap:
                                fAddition = maxInstall - fExistCap
                                objCountry.dicRenewMaxCapAdd[sReProc] = fAddition
                            elif maxInstall > fMaxAvailCap:
                                fAddition = fMaxAvailCap - fExistCap
                                objCountry.dicRenewMaxCapAdd[sReProc] = fAddition
                            else:
                                objCountry.dicRenewMaxCapAdd[sReProc] = 0
                            
    return 


#---------------------------------------------------------------------------------
# capacity addition from CE results
#---------------------------------------------------------------------------------
    
def updateNewBuildCapacity(instance, objMarket, model, ind_year):
    ''' update capacity addition results from CE model '''
    ###### new install capacity (MW) #####

    iYear = instance.iAllYearSteps_YS[ind_year]

    # dispatchable process
    for sProc in model.setProcNewDisp_TCD:
        if model.vNewProcDispCap_TCD[sProc].value > 0:
            fNewCap = model.vNewProcDispCap_TCD[sProc].value
            if fNewCap < 100:
                fNewCap = 100
            sProcZoneID = sProc.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for ind_objProcAss, objProcess in enumerate(objZone.lsProcessAssump):
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProc:
                            _AddNewInstallation(objZone, objProcess, fNewCap, ind_objProcAss, 0, iYear, ind_year)
                            break
                    break
    
    # storage process
    for sProc in model.setProcNewStor_TCS:
        if model.vNewProcStorCap_TCS[sProc].value > 0:
            fNewCap = model.vNewProcStorCap_TCS[sProc].value
            if fNewCap < 50:
                fNewCap = 50
            sProcZoneID = sProc.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for ind_objProcAss, objProcess in enumerate(objZone.lsProcessAssump):
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProc:
                            _AddNewInstallation(objZone, objProcess, fNewCap, ind_objProcAss, 0, iYear, ind_year)
                            break
                    break
    
    # hydro process
    for sProc in model.setProcNewHydr_TCH:
        if model.vNewProcHydrCap_TCH[sProc].value > 0:
            fNewCap = model.vNewProcHydrCap_TCH[sProc].value
            if fNewCap < 50:
                fNewCap = 50
            sProcZoneID = sProc.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for ind_objProcAss, objProcess in enumerate(objZone.lsProcessAssump):
                        if objZone.sZoneID + "/" + objProcess.sProcessName == sProc:
                            _AddNewInstallation(objZone, objProcess, fNewCap, ind_objProcAss, 0, iYear, ind_year)
                            break
                    break
    
    # renewables process
    for sProc in model.setProcNewRE_TCR:
        if model.vNewProcRenewCap_TCR[sProc].value > 0:
            fNewCap = model.vNewProcRenewCap_TCR[sProc].value
            if fNewCap < 50:
                fNewCap = 50
            sProcZoneID = sProc.split("/")[0]
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sProcZoneID:
                    for ind_objProcAss, objProcess in enumerate(objZone.lsProcessAssump):
                        if objZone.sZoneID + "/" + objProcess.sProcessName + "/" + str(objProcess.iCFClass) == sProc:
                            _AddNewInstallation(objZone, objProcess, fNewCap, ind_objProcAss, objProcess.iCFClass, iYear, ind_year)
                            break
                    break

    # offshore renewables process
    for sProc in model.setProcNewRE_Offs_TCR:
        if model.vNewProcRenewCapOffs_TCR[sProc].value > 0:
            fNewCap = model.vNewProcRenewCapOffs_TCR[sProc].value
            if fNewCap < 50:
                fNewCap = 50
            sProcZoneID = sProc.split("/")[0]
            for objZone in objMarket.lsZoneOffs:
                if objZone.sZoneID == sProcZoneID:
                    for ind_objProcAss, objProcess in enumerate(objZone.lsProcessAssump):
                        if objZone.sZoneID + "/" + objProcess.sProcessName + "/" + str(objProcess.iCFClass) == sProc:
                            _AddNewInstallation(objZone, objProcess, fNewCap, ind_objProcAss, objProcess.iCFClass, iYear, ind_year)
                            break
                    break

    ##### upgrade transmission capacity (MW) ------------------------- 
    # transmission capacity
    for sTrans in model.setTransLDZ_TRL:
        for objTrans in objMarket.lsTrans:
            if sTrans == objTrans.sTransID:
                objTrans.dicTransAccCap_YS[iYear] = model.pExTransLDZCap_TRL[sTrans] + model.vNewProcTransCap_TRL[sTrans].value
                objTrans.dicTransNewBuild_YS[iYear] = model.vNewProcTransCap_TRL[sTrans].value
                break

    for sTrans in model.setTransOFZ_TRF:
        for objTrans in objMarket.lsTrans_off:
            if sTrans == objTrans.sTransID:
                objTrans.dicTransAccCap_YS[iYear] = model.pExTransOFZCap_TRF[sTrans] + model.vNewProcTransOffCap_TRF[sTrans].value
                objTrans.dicTransNewBuild_YS[iYear] = model.vNewProcTransOffCap_TRF[sTrans].value
                break

    return 


def _AddNewInstallation(objZone, objProcessAssump, fNewCap, ind_objProcAss, iCFClass, iYear, ind_year):
    ''' add a new process object into the zone '''
    
    iCommitTime = iYear
    sProcessID = objProcessAssump.sProcessName + "_" + str(iCommitTime)

    # new process                        
    objExistProcess = cls_process.ZoneProcess(sProcessName=objProcessAssump.sProcessName, sProcessID=sProcessID)
    objExistProcess.iZoneProcAssumIndex = ind_objProcAss
    objExistProcess.sProcessType = objProcessAssump.sProcessType
    objExistProcess.sFuel = objProcessAssump.sFuel
    objExistProcess.sOperationMode = objProcessAssump.sOperationMode
    objExistProcess.bCCS = objProcessAssump.bCCS
    objExistProcess.bAS_T1 = objProcessAssump.bAS_T1
    objExistProcess.bAS_T2 = objProcessAssump.bAS_T2
    objExistProcess.bAS_T3 = objProcessAssump.bAS_T3
    
    # tech assumption
    objExistProcess.iCapacity = fNewCap
    objExistProcess.fGrossEff = objProcessAssump.fGrossEff_YS[ind_year]
    objExistProcess.fMinLoad = objProcessAssump.fMinLoad_YS[ind_year]
    objExistProcess.fRampRate = objProcessAssump.fRampRate_YS[ind_year]
    objExistProcess.fEquAvailFactor = objProcessAssump.fEquAvailFactor_YS[ind_year]
    objExistProcess.fAuxiliaryCon = objProcessAssump.fAuxiliaryCon_YS[ind_year]
    objExistProcess.fCaptureRate = objProcessAssump.fCaptureRate_YS[ind_year]
    objExistProcess.fDuration = objProcessAssump.fDuration_YS[ind_year]
                            
    objExistProcess.iCFClass = iCFClass
    
    ### commit and decommit time (if the decommit time is before 2015, then change to 2020)
    objExistProcess.iCommitTime = iCommitTime
    objExistProcess.iDeCommitTime = int(iCommitTime + objProcessAssump.fLifetime)
    
    ### cost assumptions
    fCapacity = objExistProcess.iCapacity                                          # MW
    fCapitalCost = objProcessAssump.fCAPEX_YS[ind_year] * fCapacity * 1000         # USD/KW * MW * 1000 = USD
    fYearOMCost = objProcessAssump.fOPEX_YS[ind_year] * fCapacity * 1000           # USD/KW * MW * 1000 = USD
    fDiscountRate = objProcessAssump.fDiscount
    iPlantLife = objProcessAssump.fLifetime
    # fCapitalRecoveyFactor = (D*(1+D)^L) / ( ((1+D)^L)-1 )
    fCapitalRecoveyFactor =  ( fDiscountRate * ((1+fDiscountRate)**iPlantLife)) / ( ((1+fDiscountRate)**iPlantLife) - 1 )
    objExistProcess.fAnnualCapex = fCapitalCost * fCapitalRecoveyFactor / 1000000                # MillionUSD / year
    objExistProcess.fAnnualFixedCost = objExistProcess.fAnnualCapex + (fYearOMCost / 1000000)    # MillionUSD / year
    objExistProcess.fvarOMCost = objProcessAssump.fVarOPEX_YS[ind_year]            # USD/KWh
    
    ### capability for providing ancillary service
    objExistProcess.fASMax_T1 = objExistProcess.iCapacity * objExistProcess.fRampRate / 100 \
        * objExistProcess.bAS_T1 * 0.5  # 30 second ramp capacity
        
    objExistProcess.fASMax_T2 = objExistProcess.iCapacity * objExistProcess.fRampRate / 100 \
        * objExistProcess.bAS_T2 * 10  # 10 min ramp capacity
    if objExistProcess.fASMax_T2 > objExistProcess.iCapacity:
        objExistProcess.fASMax_T2 = objExistProcess.iCapacity
        
    objExistProcess.fASMax_T3 = objExistProcess.iCapacity * objExistProcess.fRampRate / 100 \
        * objExistProcess.bAS_T3 * 30  # 30 min ramp capacity
    if objExistProcess.fASMax_T3 > objExistProcess.iCapacity:
        objExistProcess.fASMax_T3 = objExistProcess.iCapacity
                
    objZone.lsProcess.append(objExistProcess)
                                         
    return

