#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to construct CE model constraints
#

import pyomo.environ as pe

##### ---- dispatchable ----------------------------------------------- #####

def constUnitGen_Exist(model, objMarket):
    ''' generation constraints of existing dispatchable process '''

    ### gross power output of existing dispatchable units
    def ruleProcessPowerOutGross_Disp(model, sProcDisp, sTimeSlice) :

        # consider overall planned/forced outage, equivalent available factor
        return model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            <= model.pExProcDispCap_TCD[sProcDisp] * model.pExProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispPwOutGross_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                                model.setTimeSlice_TS, rule = ruleProcessPowerOutGross_Disp))

    ### net power output of existing dispatchable units
    def ruleProcessPowerOutNet_Disp(model, sProcDisp, sTimeSlice) :

        return model.vExProcDispPwOutNet_TCD_TS[sProcDisp, sTimeSlice] \
            == model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            * (1-model.pExProcDispOUS_TCD[sProcDisp])

    setattr(model, "conProcDispPwOutNet_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                                model.setTimeSlice_TS, rule = ruleProcessPowerOutNet_Disp))

    return


def constUnitGen_New(model, objMarket):
    ''' generation constraints of new dispatchable process '''
    
    ### gross power output of new candidate dispatchable units
    def ruleProcessPowerOutGross_Disp(model, sProcDisp, sTimeSlice) :

        # consider overall planned/forced outage, equivalent available factor
        return model.vNewProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            <= model.vNewProcDispCap_TCD[sProcDisp] * model.pNewProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispPwOutGrossNew_TCD_TS", pe.Constraint(model.setProcNewDisp_TCD, \
                                model.setTimeSlice_TS, rule = ruleProcessPowerOutGross_Disp))

    ### net power output of new candidate dispatchable units
    def ruleProcessPowerOutNet_Disp(model, sProcDisp, sTimeSlice) :

        return model.vNewProcDispPwOutNet_TCD_TS[sProcDisp, sTimeSlice] \
            == model.vNewProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            * (1-model.pNewProcDispOUS_TCD[sProcDisp])

    setattr(model, "conProcDispPwOutNetNew_TCD_TS", pe.Constraint(model.setProcNewDisp_TCD, \
                                model.setTimeSlice_TS, rule = ruleProcessPowerOutNet_Disp))

    return


##### ---- dispatchable (testing TS) ----------------------------------------------- #####
    
def constUnitGen_Exist_RT(model, objMarket):
    ''' generation constraints of existing dispatchable process on testing TS '''
    
    ### gross power output of existing dispatchable units
    def ruleProcessPowerOutGross_Disp(model, sProcDisp, sTimeSlice) :

        # consider overall planned/forced outage, equivalent available factor
        return model.vExProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] \
            <= model.pExProcDispCap_TCD[sProcDisp] * model.pExProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispPwOutGrossTest_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                                model.setTSRT_TS, rule = ruleProcessPowerOutGross_Disp))

    ### net power output of existing dispatchable units
    def ruleProcessPowerOutNet_Disp(model, sProcDisp, sTimeSlice) :

        return model.vExProcDispPwOutNetTest_TCD_TS[sProcDisp, sTimeSlice] \
            == model.vExProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] \
            * (1-model.pExProcDispOUS_TCD[sProcDisp])

    setattr(model, "conProcDispPwOutNetTest_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                                model.setTSRT_TS, rule = ruleProcessPowerOutNet_Disp))

    return


def constUnitGen_New_RT(model, objMarket):
    ''' generation constraints of new dispatchable process on testing TS '''
    
    ### gross power output of new candidate dispatchable units
    def ruleProcessPowerOutGross_Disp(model, sProcDisp, sTimeSlice) :

        # consider overall planned/forced outage, equivalent available factor
        return model.vNewProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] \
            <= model.vNewProcDispCap_TCD[sProcDisp] * model.pNewProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispPwOutGrossNewTest_TCD_TS", pe.Constraint(model.setProcNewDisp_TCD, \
                                model.setTSRT_TS, rule = ruleProcessPowerOutGross_Disp))

    ### net power output of new candidate dispatchable units
    def ruleProcessPowerOutNet_Disp(model, sProcDisp, sTimeSlice) :

        return model.vNewProcDispPwOutNetTest_TCD_TS[sProcDisp, sTimeSlice] \
            == model.vNewProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] \
            * (1-model.pNewProcDispOUS_TCD[sProcDisp])

    setattr(model, "conProcDispPwOutNetNewTest_TCD_TS", pe.Constraint(model.setProcNewDisp_TCD, \
                                model.setTSRT_TS, rule = ruleProcessPowerOutNet_Disp))

    return


##### ---- storage --------------------------------------------------- #####
    
def constStorageOpr_Exist(model, objMarket):
    ''' existing storage system operation constraints '''
    
    ### max hourly output of existing units (MW)
    def ruleStorPowerOutMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation  
        return model.vExProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] \
            <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerOutMax_TCS_TS", pe.Constraint(model.setProcBaseStor_TCS, \
                            model.setTimeSlice_TS, rule = ruleStorPowerOutMax))    
    
    ### max hourly input of new units (MW)
    def ruleStorPowerInMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation   
        return model.vExProcStorPwIn_TCS_TS[sProcStor, sTimeSlice] \
            <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerInMax_TCS_TS", pe.Constraint(model.setProcBaseStor_TCS, \
                            model.setTimeSlice_TS, rule = ruleStorPowerInMax))  

    ### daily total generation constraint (MWh)
    def ruleStorDayGen(model, sProcStor, setDay_DY) :  
        
        fCapacity = model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] # MW
        fMaxDayOutput = fCapacity * model.pExProcStorDur_TCS[sProcStor]   # total stored energy, MW -> MWh
        
        fDayOutput = 0
        liTSInDay = model.pTSIndInDay_DY[setDay_DY].split(';')
        for sTSIndex in liTSInDay:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vExProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
    
        return fDayOutput <= fMaxDayOutput
    
    setattr(model, "conStorDayGen_TCS_DY", pe.Constraint(model.setProcBaseStor_TCS, \
                            model.setDay_DY, rule = ruleStorDayGen))  
    
    ### daily input/output balance constraint
    def ruleStorDayBalance(model, sProcStor, setDay_DY) :  
        
        fGrossEffeciency = model.pExProcStorEff_TCS[sProcStor]
        
        fDayOutput = 0
        fDayInput = 0
    
        liTSInDay = model.pTSIndInDay_DY[setDay_DY].split(';')
        for sTSIndex in liTSInDay:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vExProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
            fDayInput += model.vExProcStorPwIn_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
            
        return fDayInput == (fDayOutput / fGrossEffeciency)
    
    setattr(model, "conStorDayBalance_TCS_DY", pe.Constraint(model.setProcBaseStor_TCS, \
                            model.setDay_DY, rule = ruleStorDayBalance))
    
    return


def constStorageOpr_New(model, objMarket):
    ''' new storage system operation constraints '''
    
    ### max hourly output of new units (MW)
    def ruleStorPowerOutMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation  
        return model.vNewProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] \
            <= model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerOutMaxNew_TCS_TS", pe.Constraint(model.setProcNewStor_TCS, \
                            model.setTimeSlice_TS, rule = ruleStorPowerOutMax))    
    
    ### max hourly input of new units (MW)
    def ruleStorPowerInMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation   
        return model.vNewProcStorPwIn_TCS_TS[sProcStor, sTimeSlice] \
            <= model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerInMaxNew_TCS_TS", pe.Constraint(model.setProcNewStor_TCS, \
                            model.setTimeSlice_TS, rule = ruleStorPowerInMax))  

    ### daily total generation constraint (MWh)
    def ruleStorDayGen(model, sProcStor, setDay_DY) :  
        
        fCapacity = model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor] # MW
        fMaxDayOutput = fCapacity * model.pNewProcStorDur_TCS[sProcStor]   # total stored energy, MW -> MWh
        
        fDayOutput = 0
        liTSInDay = model.pTSIndInDay_DY[setDay_DY].split(';')
        for sTSIndex in liTSInDay:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vNewProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
    
        return fDayOutput <= fMaxDayOutput
    
    setattr(model, "conStorDayGenNew_TCS_DY", pe.Constraint(model.setProcNewStor_TCS, \
                                model.setDay_DY, rule = ruleStorDayGen))  
    
    ### daily input/output balance constraint
    def ruleStorDayBalance(model, sProcStor, setDay_DY) :  
        
        fGrossEffeciency = model.pNewProcStorEff_TCS[sProcStor]
        
        fDayOutput = 0
        fDayInput = 0
    
        liTSInDay = model.pTSIndInDay_DY[setDay_DY].split(';')
        for sTSIndex in liTSInDay:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vNewProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
            fDayInput += model.vNewProcStorPwIn_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
            
        return fDayInput == (fDayOutput / fGrossEffeciency)
    
    setattr(model, "conStorDayBalanceNew_TCS_DY", pe.Constraint(model.setProcNewStor_TCS, \
                                model.setDay_DY, rule = ruleStorDayBalance))
    
    ### installation capacity limit (PHS)
    def ruleStorInstLim(model, sProcStor) :  
                    
        sTech = str(sProcStor).split("/")[1]
        if sTech[0:6] == "HYD_PS":
            return model.vNewProcStorCap_TCS[sProcStor] <= model.pNewProcStorCapLim_TCS[sProcStor] 
        else:
            return pe.Constraint.Skip
    
    setattr(model, "conStorInstLimNew_TCS_DY", pe.Constraint(model.setProcNewStor_TCS, rule = ruleStorInstLim))
    
    return


##### ---- storage (Testing TS) ------------------------------------------------------- #####
    
def constStorageOpr_Exist_RT(model, objMarket):
    ''' existing storage system operation constraints on testing TS '''
    
    ### max hourly output of existing units (MW)
    def ruleStorPowerOutMax(model, sProcStor, sTimeSlice) :  
        
        fMinOutput = model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] \
            * model.pNewProcStorDur_TCS[sProcStor] / 12
        
        # only non-dispatchable generation  
        return model.vExProcStorPwOutTest_TCS_TS[sProcStor, sTimeSlice] <= fMinOutput
    
    setattr(model, "conStorPowerOutMaxTest_TCS_TS", pe.Constraint(model.setProcBaseStor_TCS, \
                                model.setTSRT_TS, rule = ruleStorPowerOutMax))    
        
    return


def constStorageOpr_New_RT(model, objMarket):
    ''' new storage system operation constraints on testing TS '''
    
    ### max hourly output of new units (MW)
    def ruleStorPowerOutMax(model, sProcStor, sTimeSlice) :  
        
        fMinOutput = model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor] \
            * model.pNewProcStorDur_TCS[sProcStor] / 12
        
        # only non-dispatchable generation  
        return model.vNewProcStorPwOutTest_TCS_TS[sProcStor, sTimeSlice] <= fMinOutput
    
    setattr(model, "conStorPowerOutMaxNewTest_TCS_TS", pe.Constraint(model.setProcNewStor_TCS, \
                                model.setTSRT_TS, rule = ruleStorPowerOutMax))    
        
    return


##### ---- hydro ------------------------------------------------------- #####
    
def constHydropowerOpr_Exist(model, objMarket):
    ''' existing large hydropower operation constraints '''

    ### small hydro output
    def ruleHydrPowerOutputSml(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_SM":
            # default generation
            return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] \
                == model.pExProcHydrGen_TCH_TS[TechHydro, sTimeSlice]
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutputSml_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutputSml))

    ### large hydro generation limit - upper bound
    def ruleHydrPowerOutUpBnd(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.pExProcHydrCap_TCH[TechHydro]
            fEAF = model.pExProcHydrEAF_TCH[TechHydro]
            return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] <=  fCapacity * fEAF
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutUpBnd_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutUpBnd))

    ### large hydro generation limit - lower bound
    def ruleHydrPowerOutLowBnd(model, TechHydro, sTimeSlice) :

        iDispatchBase = 0.3
        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            ### the lower limit is 30% CF, smaller than this is non-dispatchable (this does not subjected to EAF)
            fCapacity = model.pExProcHydrCap_TCH[TechHydro]
            defaultGen = float(model.pExProcHydrGen_TCH_TS[TechHydro, sTimeSlice])
            if fCapacity > 0:
                if (defaultGen / fCapacity) >= iDispatchBase:
                    return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] >=  fCapacity * iDispatchBase
                else:
                    return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] ==  defaultGen
            else:
                return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] ==  0
            
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutLowBnd_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutLowBnd))

    ### large hydro generation daily dispatch
    def ruleHydrPowerOutDispatch(model, TechHydro, setDay):

        iDispatchBase = 0.3
        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.pExProcHydrCap_TCH[TechHydro] # MW
            if fCapacity > 0:
                liTSInDay = model.pTSIndInDay_DY[setDay].split(';')
                defaultGen = float(model.pExProcHydrGen_TCH_TS[TechHydro, model.setTimeSlice_TS[1]])
                if (defaultGen / fCapacity) >= iDispatchBase:
                    
                    # total dispatchable
                    total_dispatchable = 0
                    for sTSIndex in liTSInDay:
                        iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
                        hourGen = float(model.pExProcHydrGen_TCH_TS[TechHydro, sTSIndex])
                        total_dispatchable = total_dispatchable + (hourGen * iTSRepHour)  # MWh
                    # total generation
                    total_generation = 0
                    for sTSIndex in liTSInDay:
                        iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
                        hourGen = model.vExProcHydrPwOut_TCH_TS[TechHydro, sTSIndex]
                        total_generation = total_generation + ( hourGen * iTSRepHour )
                        
                    return total_generation == total_dispatchable
                        
                else:
                    return pe.Constraint.Skip  # CF is too low, non-dispatchable
            else:
                return pe.Constraint.Skip
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutOpr_TCH_DY", pe.Constraint(model.setProcBaseHydr_TCH, \
                            model.setDay_DY, rule = ruleHydrPowerOutDispatch))

    return 


def constHydropowerOpr_New(model, objMarket):
    ''' new large hydropower operation constraints '''
    
    ### small hydro output
    def ruleHydrPowerOutputSml(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_SM":
            # default generation
            return model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] \
                == model.vNewProcHydrCap_TCH[TechHydro] * \
                model.pNewProcHydrCF_TCH_TS[TechHydro, sTimeSlice] * model.pNewProcHydrEAF_TCH[TechHydro]
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutputSmlNew_TCH_TS", pe.Constraint(model.setProcNewHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutputSml))

    ### large hydro generation limit - upper bound
    def ruleHydrPowerOutUpBnd(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.vNewProcHydrCap_TCH[TechHydro]
            fEAF = model.pNewProcHydrEAF_TCH[TechHydro]
            return model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] <=  fCapacity * fEAF
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutUpBndNew_TCH_TS", pe.Constraint(model.setProcNewHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutUpBnd))

    ### large hydro generation limit - lower bound
    def ruleHydrPowerOutLowBnd(model, TechHydro, sTimeSlice) :

        iDispatchBase = 0.3
        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            ### the lower limit is 30% CF, smaller than this is non-dispatchable (this does not subjected to EAF)
            fCapacity = model.vNewProcHydrCap_TCH[TechHydro]
            defaultGenCF = float(model.pNewProcHydrCF_TCH_TS[TechHydro, sTimeSlice])
            if defaultGenCF >= iDispatchBase:
                return model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] >=  fCapacity * iDispatchBase
            else:
                return model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] ==  fCapacity * defaultGenCF
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutLowBndNew_TCH_TS", pe.Constraint(model.setProcNewHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleHydrPowerOutLowBnd))

    ### large hydro generation daily dispatch
    def ruleHydrPowerOutDispatch(model, TechHydro, setDay):

        iDispatchBase = 0.3
        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.vNewProcHydrCap_TCH[TechHydro] # MW
            
            liTSInDay = model.pTSIndInDay_DY[setDay].split(';')
            defaultGenCF = float(model.pNewProcHydrCF_TCH_TS[TechHydro, liTSInDay[0]])
            if defaultGenCF >= iDispatchBase:
                
                # total dispatchable (MWh)
                total_dispatchable = 0
                for sTSIndex in liTSInDay:
                    iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
                    hourGen = float(model.pNewProcHydrCF_TCH_TS[TechHydro, sTSIndex]) * fCapacity
                    total_dispatchable = total_dispatchable + (hourGen * iTSRepHour)
                    
                # total generation (MWh)
                total_generation = 0
                for sTSIndex in liTSInDay:
                    iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
                    hourGen = model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTSIndex]
                    total_generation = total_generation + ( hourGen * iTSRepHour )
                    
                return total_generation == total_dispatchable
                    
            else:
                return pe.Constraint.Skip  # CF is too low, non-dispatchable
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutOprNew_TCH_DY", pe.Constraint(model.setProcNewHydr_TCH, \
                            model.setDay_DY, rule = ruleHydrPowerOutDispatch))


    ### installation capacity limit
    def ruleHydrInstLim(model, TechHydro) :  
                    
        return model.vNewProcHydrCap_TCH[TechHydro] <= model.pNewProcHydrCapLim_TCH[TechHydro] 

    setattr(model, "conHydrInstLimNew_TCS_DY", pe.Constraint(model.setProcNewHydr_TCH, rule = ruleHydrInstLim))
    
    return 


##### ---- hydro (Testing TS)------------------------------------------------------- #####
    
def constHydropowerOpr_Exist_RT(model, objMarket):
    ''' existing large hydropower operation constraints in testing TS '''
    
    ### small hydro output
    def ruleHydrPowerOutputSml(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_SM":
            # default generation
            return model.vExProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice] \
                == model.pExProcHydrCap_TCH[TechHydro] \
                * model.pNewProcHydrCFTest_TCH_TS[TechHydro, sTimeSlice] \
                * model.pExProcHydrEAF_TCH[TechHydro]
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutputSmlTest_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                            model.setTSRT_TS, rule = ruleHydrPowerOutputSml))

    ### large hydro generation limit - upper bound
    def ruleHydrPowerOutUpBnd(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            
            # default generation
            return model.vExProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice] \
                == model.pExProcHydrCap_TCH[TechHydro] \
                * model.pNewProcHydrCFTest_TCH_TS[TechHydro, sTimeSlice] \
                * model.pExProcHydrEAF_TCH[TechHydro]
            
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutUpBndTest_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                            model.setTSRT_TS, rule = ruleHydrPowerOutUpBnd))

    return 


def constHydropowerOpr_New_RT(model, objMarket):
    ''' new large hydropower operation constraints in testing TS'''
    
    ### small hydro output
    def ruleHydrPowerOutputSml(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_SM":
            # default generation
            return model.vNewProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice] \
                == model.vNewProcHydrCap_TCH[TechHydro] \
                * model.pNewProcHydrCFTest_TCH_TS[TechHydro, sTimeSlice] \
                * model.pNewProcHydrEAF_TCH[TechHydro]
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutputSmlNewTest_TCH_TS", pe.Constraint(model.setProcNewHydr_TCH, \
                            model.setTSRT_TS, rule = ruleHydrPowerOutputSml))

    ### large hydro generation limit - upper bound
    def ruleHydrPowerOutUpBnd(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            
            # default generation
            return model.vNewProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice] \
                == model.vNewProcHydrCap_TCH[TechHydro] \
                * model.pNewProcHydrCFTest_TCH_TS[TechHydro, sTimeSlice] \
                * model.pNewProcHydrEAF_TCH[TechHydro]
                
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPwOutUpBndNewTest_TCH_TS", pe.Constraint(model.setProcNewHydr_TCH, \
                            model.setTSRT_TS, rule = ruleHydrPowerOutUpBnd))

    return 


##### ---- renewable ------------------------------------------------------- #####

def constRenewGen_New(model, objMarket):
    ''' renewable power generation from new processes '''
    
    ### hourly output (MW)
    def ruleRenewPwOutNew(model, sProcRenew, sTimeSlice) :  
        
        return model.vNewProcRenewPwOut_TCR_TS[sProcRenew, sTimeSlice] \
            == model.vNewProcRenewCap_TCR[sProcRenew] \
            * model.pNewProcRenDefCF_TCR_TS[sProcRenew, sTimeSlice]
    
    setattr(model, "conRenewPwOutNew_TCR_TS", pe.Constraint(model.setProcNewRE_TCR, \
                            model.setTimeSlice_TS, rule = ruleRenewPwOutNew))    
    
    ### installation capacity limit
    def ruleRenewInstLim(model, sProcRenew) :  
                    
        return model.vNewProcRenewCap_TCR[sProcRenew] \
            <= model.pNewProcRenCapLim_TCR[sProcRenew] 

    setattr(model, "conRenewInstLimNew_TCR_DY", pe.Constraint(model.setProcNewRE_TCR, rule = ruleRenewInstLim))


    ### hourly output (MW) - offhsore
    def ruleRenewPwOutOffNew(model, sProcRenew, sTimeSlice) :
        
        return model.vNewProcRenewPwOutOffs_TCR_TS[sProcRenew, sTimeSlice] \
            == model.vNewProcRenewCapOffs_TCR[sProcRenew] \
            * model.pNewProcRenDefCF_Offs_TCR[sProcRenew, sTimeSlice]
    
    setattr(model, "conRenewPwOutOffNew_TCR_TS", pe.Constraint(model.setProcNewRE_Offs_TCR, \
                            model.setTimeSlice_TS, rule = ruleRenewPwOutOffNew))    
    
    ### installation capacity limit - offhsore
    def ruleRenewInstLimOff(model, sProcRenew) :  
                    
        return model.vNewProcRenewCapOffs_TCR[sProcRenew] \
            <= model.pNewProcRenCapLim_Offs_TCR[sProcRenew] 

    setattr(model, "conRenewInstLimOffNew_TCR_DY", pe.Constraint(model.setProcNewRE_Offs_TCR, rule = ruleRenewInstLimOff))

    return


##### ---- renewable (Testing TS) ------------------------------------------------------- #####

def constRenewGen_New_RT(model, objMarket):
    ''' renewable power generation from new processes in testing TS '''
    
    ### hourly output (MW)
    def ruleRenewPwOutNew(model, sProcRenew, sTimeSlice) :  
        
        return model.vNewProcRenewPwOutTest_TCR_TS[sProcRenew, sTimeSlice] \
            == model.vNewProcRenewCap_TCR[sProcRenew] \
            * model.pNewProcRenDefCFTest_TCR[sProcRenew, sTimeSlice]
    
    setattr(model, "conRenewPwOutNewTest_TCR_TS", pe.Constraint(model.setProcNewRE_TCR, \
                                model.setTSRT_TS, rule = ruleRenewPwOutNew))    

    ### hourly output (MW) - offhsore
    def ruleRenewPwOutOffNew(model, sProcRenew, sTimeSlice) :
        
        return model.vNewProcRenewPwOutOffsTest_TCR_TS[sProcRenew, sTimeSlice] \
            == model.vNewProcRenewCapOffs_TCR[sProcRenew] \
            * model.pNewProcRenDefCFTest_Offs_TCR[sProcRenew, sTimeSlice]
    
    setattr(model, "conRenewPwOutOffNewTest_TCR_TS", pe.Constraint(model.setProcNewRE_Offs_TCR, \
                                model.setTSRT_TS, rule = ruleRenewPwOutOffNew))    

    return
    

##### ---- power balance -------------------------------------------------- #####

def constPowerBalance(model, objMarket):
    ''' power balance constraints for each zone '''
    
    # --- terrestrial zones ----------------------------------
    
    ### power supply of land zones
    def ruleLDZProcPowerSupply(model, sZone, sTimeSlice) :
        
        ### existing units
        vPowerOutput_Ex = 0        
        # dispatchable output
        for TechDisp in model.setProcBaseDisp_TCD:
            if (sZone + "/") in TechDisp:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcDispPwOutNet_TCD_TS[TechDisp, sTimeSlice]                
        # storage output
        for TechStor in model.setProcBaseStor_TCS:
            if (sZone + "/") in TechStor:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcStorPwOut_TCS_TS[TechStor, sTimeSlice] \
                    - model.vExProcStorPwIn_TCS_TS[TechStor, sTimeSlice] 
        # hydropower output
        for TechHydro in model.setProcBaseHydr_TCH:
            if (sZone + "/") in TechHydro:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice]                  
        # non-dispatchable renewables
        vPowerOutput_Ex = vPowerOutput_Ex + model.pNonDispGen_ZNL_TS[sZone, sTimeSlice]  
                
        ### new units
        vPowerOutput_New = 0
        # dispatchable output
        for TechDisp in model.setProcNewDisp_TCD:
            if (sZone + "/") in TechDisp:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcDispPwOutNet_TCD_TS[TechDisp, sTimeSlice]                
        # storage output
        for TechStor in model.setProcNewStor_TCS:
            if (sZone + "/") in TechStor:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcStorPwOut_TCS_TS[TechStor, sTimeSlice] \
                    - model.vNewProcStorPwIn_TCS_TS[TechStor, sTimeSlice] 
        # hydropower output
        for TechHydro in model.setProcNewHydr_TCH:
            if (sZone + "/") in TechHydro:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice]  
        # non-dispatchable renewables
        for TechRenew in model.setProcNewRE_TCR:
            if (sZone + "/") in TechRenew:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcRenewPwOut_TCR_TS[TechRenew, sTimeSlice]  
        
        return model.vSupplyZone_ZNL_TS[sZone, sTimeSlice] == vPowerOutput_Ex + vPowerOutput_New
    
    setattr(model, "conLDZPowerSupply_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                        model.setTimeSlice_TS, rule = ruleLDZProcPowerSupply))
    
    ### power balance of land zones
    def rulePowerBalanceLandZone(model, sZone, sTimeSlice) :

        # transmission input (into lines, export)
        vTransZoneInput = 0
        for TransLine in model.setTransLDZ_TRL:
            if (sZone + "/") in TransLine:
                vTransZoneInput = vTransZoneInput + model.vTransLDZIn_TRL_TS[TransLine, sTimeSlice]
        
        # transmission output (from transmission lines, import)
        vTransZoneOutput = 0
        for TransLine in model.setTransLDZ_TRL:
            TragetZone = str(TransLine).split("/")[1]
            if sZone == TragetZone:
                vTransZoneOutput = vTransZoneOutput + model.vTransLDZOut_TRL_TS[TransLine, sTimeSlice]
        
        # transmission output from offshore zones (from transmission lines)
        vTransOffshoreOutput = 0
        for TransLine in model.setTransOFZ_TRF:
            TragetZone = str(TransLine).split("/")[1]
            if sZone == TragetZone:
                vTransOffshoreOutput = vTransOffshoreOutput + model.vTransOFZOut_TRF_TS[TransLine, sTimeSlice]
        
        # supply - spill + line output - line input  = demand
        return model.vSupplyZone_ZNL_TS[sZone, sTimeSlice] - model.vSpillZone_ZNL_TS[sZone, sTimeSlice] \
            + vTransZoneOutput + vTransOffshoreOutput - vTransZoneInput \
            == model.pDemand_ZNL_TS[sZone, sTimeSlice]
        
    setattr(model, "conPowerBalanceZone_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                    model.setTimeSlice_TS, rule = rulePowerBalanceLandZone))
    
    # --- offshore zones ------------------------------
    
    ### power supply of offshore zones
    def ruleOFZProcPowerSupply(model, sZone, sTimeSlice) :  
        
        vPowerOutput = 0 
        # existing units
        vPowerOutput = vPowerOutput + model.pNonDispGen_ZNF_TS[sZone, sTimeSlice]  
        # new installation non-dispatchable renewables
        for TechRenew in model.setProcNewRE_Offs_TCR:
            if (sZone + "/") in TechRenew:
                vPowerOutput = vPowerOutput + model.vNewProcRenewPwOutOffs_TCR_TS[TechRenew, sTimeSlice]  
                
        # only non-dispatchable generation    
        return model.vSupplyOffs_ZNF_TS[sZone, sTimeSlice] == vPowerOutput
    
    setattr(model, "conOFZPowerSupply_ZNF_TS", pe.Constraint(model.setOFZone_ZNF, \
                    model.setTimeSlice_TS, rule = ruleOFZProcPowerSupply))    
    
    ### all transmission(line) input + spill = total supply
    def ruleTransOFZInput(model, sZone, sTimeSlice) :  
        
        vAllTransOffshoreInput_TS = 0
        for TransLine in model.setTransOFZ_TRF:
            if (sZone + "/") in TransLine:
                vAllTransOffshoreInput_TS = vAllTransOffshoreInput_TS + model.vTransOFZIn_TRF_TS[TransLine, sTimeSlice]
                
        return model.vSupplyOffs_ZNF_TS[sZone, sTimeSlice] \
            == vAllTransOffshoreInput_TS + model.vSpillOffs_ZNF_TS[sZone, sTimeSlice]
    
    setattr(model, "conOFZBalanceZone_ZNF_TS", pe.Constraint(model.setOFZone_ZNF, \
                    model.setTimeSlice_TS, rule = ruleTransOFZInput))   

    return


##### ---- power balance (Testing TS) -------------------------------------------------- #####

def constPowerBalance_RT(model, objMarket):
    ''' power balance constraints for each zone in testing TS '''
    
    # --- land zones ----------------------------------
    
    ### power supply of land zones
    def ruleLDZProcPowerSupply(model, sZone, sTimeSlice) :
        
        ### existing units
        vPowerOutput_Ex = 0        
        # dispatchable output
        for TechDisp in model.setProcBaseDisp_TCD:
            if (sZone + "/") in TechDisp:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcDispPwOutNetTest_TCD_TS[TechDisp, sTimeSlice]                
        # storage output
        for TechStor in model.setProcBaseStor_TCS:
            if (sZone + "/") in TechStor:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcStorPwOutTest_TCS_TS[TechStor, sTimeSlice] 
        # hydropower output
        for TechHydro in model.setProcBaseHydr_TCH:
            if (sZone + "/") in TechHydro:
                vPowerOutput_Ex = vPowerOutput_Ex + model.vExProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice]                  
        # non-dispatchable renewables
        vPowerOutput_Ex = vPowerOutput_Ex + model.pNonDispGenTest_ZNL_TS[sZone, sTimeSlice]  
                
        ### new units
        vPowerOutput_New = 0
        # dispatchable output
        for TechDisp in model.setProcNewDisp_TCD:
            if (sZone + "/") in TechDisp:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcDispPwOutNetTest_TCD_TS[TechDisp, sTimeSlice]                
        # storage output
        for TechStor in model.setProcNewStor_TCS:
            if (sZone + "/") in TechStor:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcStorPwOutTest_TCS_TS[TechStor, sTimeSlice]
        # hydropower output
        for TechHydro in model.setProcNewHydr_TCH:
            if (sZone + "/") in TechHydro:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcHydrPwOutTest_TCH_TS[TechHydro, sTimeSlice]  
        # non-dispatchable renewables
        for TechRenew in model.setProcNewRE_TCR:
            if (sZone + "/") in TechRenew:
                vPowerOutput_New = vPowerOutput_New + model.vNewProcRenewPwOutTest_TCR_TS[TechRenew, sTimeSlice]  
        
        return model.vSupplyZoneTest_ZNL_TS[sZone, sTimeSlice] == vPowerOutput_Ex + vPowerOutput_New
    
    setattr(model, "conLDZPowerSupplyTest_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                            model.setTSRT_TS, rule = ruleLDZProcPowerSupply))
    
    ### power balance of land zones
    def rulePowerBalanceLandZone(model, sZone, sTimeSlice) :

        # transmission input (into lines, export)
        vTransZoneInput = 0
        for TransLine in model.setTransLDZ_TRL:
            if (sZone + "/") in TransLine:
                vTransZoneInput = vTransZoneInput + model.vTransLDZInTest_TRL_TS[TransLine, sTimeSlice]
        
        # transmission output (from transmission lines, import)
        vTransZoneOutput = 0
        for TransLine in model.setTransLDZ_TRL:
            TragetZone = str(TransLine).split("/")[1]
            if sZone == TragetZone:
                vTransZoneOutput = vTransZoneOutput + model.vTransLDZOutTest_TRL_TS[TransLine, sTimeSlice]
        
        # transmission output from offshore zones (from transmission lines)
        vTransOffshoreOutput = 0
        for TransLine in model.setTransOFZ_TRF:
            TragetZone = str(TransLine).split("/")[1]
            if sZone == TragetZone:
                vTransOffshoreOutput = vTransOffshoreOutput + model.vTransOFZOutTest_TRF_TS[TransLine, sTimeSlice]
        
        # supply - spill + line output - line input  = demand
        return model.vSupplyZoneTest_ZNL_TS[sZone, sTimeSlice] - model.vSpillZoneTest_ZNL_TS[sZone, sTimeSlice] \
            + vTransZoneOutput + vTransOffshoreOutput - vTransZoneInput \
            == model.pDemandTest_ZNL_TS[sZone, sTimeSlice]
        
    setattr(model, "conPowerBalanceZoneTest_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                        model.setTSRT_TS, rule = rulePowerBalanceLandZone))
    
    # --- offshore zones ------------------------------
    
    ### power supply of offshore zones
    def ruleOFZProcPowerSupply(model, sZone, sTimeSlice) :  
        
        vPowerOutput = 0 
        # existing units
        vPowerOutput = vPowerOutput + model.pNonDispGenOffTest_ZNF_TS[sZone, sTimeSlice]  
        # new installation non-dispatchable renewables
        for TechRenew in model.setProcNewRE_Offs_TCR:
            if (sZone + "/") in TechRenew:
                vPowerOutput = vPowerOutput + model.vNewProcRenewPwOutOffsTest_TCR_TS[TechRenew, sTimeSlice]  
                
        # only non-dispatchable generation    
        return model.vSupplyOffsTest_ZNF_TS[sZone, sTimeSlice] == vPowerOutput
    
    setattr(model, "conOFZPowerSupplyTest_ZNF_TS", pe.Constraint(model.setOFZone_ZNF, model.setTSRT_TS, rule = ruleOFZProcPowerSupply))    
    
    ### all transmission(line) input + spill = total supply
    def ruleTransOFZInput(model, sZone, sTimeSlice) :  
        
        vAllTransOffshoreInput_TS = 0
        for TransLine in model.setTransOFZ_TRF:
            if (sZone + "/") in TransLine:
                vAllTransOffshoreInput_TS = vAllTransOffshoreInput_TS + model.vTransOFZInTest_TRF_TS[TransLine, sTimeSlice]
                
        return model.vSupplyOffsTest_ZNF_TS[sZone, sTimeSlice] == vAllTransOffshoreInput_TS + model.vSpillOffsTest_ZNF_TS[sZone, sTimeSlice]
    
    setattr(model, "conOFZBalanceZoneTest_ZNF_TS", pe.Constraint(model.setOFZone_ZNF, model.setTSRT_TS, rule = ruleTransOFZInput))   

    return


##### ---- transmission ------------------------------------------------ #####

def constTransOpr(model, objMarket):
    ''' transmission constraints '''

    # transmission(line) input limited by capacity
    def ruleTransZoneInputCap(model, TransZone, sTimeSlice) :

        return model.vTransLDZIn_TRL_TS[TransZone, sTimeSlice] \
            <= model.pExTransLDZCap_TRL[TransZone] + model.vNewProcTransCap_TRL[TransZone]

    setattr(model, "conTransZoneInputCap_TRL_TS", pe.Constraint(model.setTransLDZ_TRL, \
                        model.setTimeSlice_TS, rule = ruleTransZoneInputCap))


    # transmission(line) output consider losses
    def ruleTransZoneOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransLDZLoss_TRL[TransZone]
        return model.vTransLDZOut_TRL_TS[TransZone, sTimeSlice] \
            == model.vTransLDZIn_TRL_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransZoneOutput_TRL_TS", pe.Constraint(model.setTransLDZ_TRL, \
                        model.setTimeSlice_TS, rule = ruleTransZoneOutput))


    # transmission(line) input offshore limited by capacity
    def ruleTransOffshoreInputCap(model, TransZone, sTimeSlice) :

        return model.vTransOFZIn_TRF_TS[TransZone, sTimeSlice] \
            <= model.pExTransOFZCap_TRF[TransZone] + model.vNewProcTransOffCap_TRF[TransZone]

    setattr(model, "conTransOffsInputCap_TRF_TS", pe.Constraint(model.setTransOFZ_TRF, \
                        model.setTimeSlice_TS, rule = ruleTransOffshoreInputCap))


    # transmission(line) output offshore consider lossess
    def ruleTransOffshoreOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransOFZLoss_TRF[TransZone]
        return model.vTransOFZOut_TRF_TS[TransZone, sTimeSlice] \
            == model.vTransOFZIn_TRF_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransOffsOutput_TRF_TS", pe.Constraint(model.setTransOFZ_TRF, \
                        model.setTimeSlice_TS, rule = ruleTransOffshoreOutput))
        
    return


##### ---- transmission (Testing TS)------------------------------------ #####

def constTransOpr_RT(model, objMarket):
    ''' transmission constraints in testing TS '''

    # transmission(line) input limited by capacity
    def ruleTransZoneInputCap(model, TransZone, sTimeSlice) :

        return model.vTransLDZInTest_TRL_TS[TransZone, sTimeSlice] \
            <= model.pExTransLDZCap_TRL[TransZone] + model.vNewProcTransCap_TRL[TransZone]

    setattr(model, "conTransZoneInputCapTest_TRL_TS", pe.Constraint(model.setTransLDZ_TRL, \
                        model.setTSRT_TS, rule = ruleTransZoneInputCap))


    # transmission(line) output consider losses
    def ruleTransZoneOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransLDZLoss_TRL[TransZone]
        return model.vTransLDZOutTest_TRL_TS[TransZone, sTimeSlice] \
            == model.vTransLDZInTest_TRL_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransZoneOutputTest_TRL_TS", pe.Constraint(model.setTransLDZ_TRL, \
                        model.setTSRT_TS, rule = ruleTransZoneOutput))


    # transmission(line) input offshore limited by capacity
    def ruleTransOffshoreInputCap(model, TransZone, sTimeSlice) :

        return model.vTransOFZInTest_TRF_TS[TransZone, sTimeSlice] \
            <= model.pExTransOFZCap_TRF[TransZone] + model.vNewProcTransOffCap_TRF[TransZone]

    setattr(model, "conTransOffsInputCapTest_TRF_TS", pe.Constraint(model.setTransOFZ_TRF, \
                        model.setTSRT_TS, rule = ruleTransOffshoreInputCap))


    # transmission(line) output offshore consider lossess
    def ruleTransOffshoreOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransOFZLoss_TRF[TransZone]
        return model.vTransOFZOutTest_TRF_TS[TransZone, sTimeSlice] \
            == model.vTransOFZInTest_TRF_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransOffsOutputTest_TRF_TS", pe.Constraint(model.setTransOFZ_TRF, \
                        model.setTSRT_TS, rule = ruleTransOffshoreOutput))
        
    return



##### ----- minimal CF of existing units ------------------------------- #####
def constMinBaseUnitGen(model, objMarket, fMinBaseGen):
    ''' constraints on minimum generation '''
    
    def ruleProcBaseMinGen_Disp(model, sProcDisp):

        BaseCF = model.pExProcBaseGenCF_TCD[sProcDisp]
        
        if BaseCF == 0:
            return pe.Constraint.Skip
        
        elif model.pExProcDispCap_TCD[sProcDisp] == 0:
            return pe.Constraint.Skip
        
        elif sProcDisp.split("/")[1] in ["BIO_ST", "BIGCC_CCS"]:
            return pe.Constraint.Skip
        
        else:
            BaseCF = BaseCF * fMinBaseGen
            
            # target generation
            targetGen = 0
            for sTSIndex in model.setTimeSlice_TS:
                targetGen = targetGen + (model.pExProcDispCap_TCD[sProcDisp] \
                                         * BaseCF) * model.pTSRepHourYear_TS[sTSIndex]
            
            # annual generettion
            dayGen = 0
            for sTSIndex in model.setTimeSlice_TS:
                dayGen = dayGen + model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTSIndex] \
                    * model.pTSRepHourYear_TS[sTSIndex]
            
            return dayGen >= targetGen

    setattr(model, "conProcBaseAnnualMinGen_TCD", \
            pe.Constraint(model.setProcBaseDisp_TCD, rule = ruleProcBaseMinGen_Disp))

    return


##### ----- max biomass supply limit ----------------------------------- #####
def constMaxBiomassSupply(model, objMarket):
    ''' constraints on maximum biomass fuel supply '''
    
    def ruleProcBiomassMaxSupply(model, sCountry):

        fTotalBiomassDemand = 0
        for TechDisp in model.setProcBaseDisp_TCD:
            if TechDisp[0:3] == sCountry:
                sTech = str(TechDisp).split("/")[1]
                if sTech in ["BIO_ST", "BIGCC_CCS"]:
                    for sTS in model.setTimeSlice_TS:
                        fTotalBiomassDemand += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                            * model.pTSRepHourYear_TS[sTS] / model.pExProcDispEff_TCD[TechDisp] * 0.0036  
                            # MW * (TS) / Eff * 0.0036 = TJ
                    
        for TechDisp in model.setProcNewDisp_TCD:
            if TechDisp[0:3] == sCountry:
                sTech = str(TechDisp).split("/")[1]
                if sTech in ["BIO_ST", "BIGCC_CCS"]:
                    for sTS in model.setTimeSlice_TS:
                        fTotalBiomassDemand += model.vNewProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                            * model.pTSRepHourYear_TS[sTS] / model.pNewProcDispEff_TCD[TechDisp] * 0.0036  
                            # MW * (TS) / Eff * 0.0036 = TJ
          
        return fTotalBiomassDemand <= model.pBiomassSupply_CN[sCountry]

    setattr(model, "conProcBiomassMaxSupply_CN", pe.Constraint(model.setCountryCode_CN, rule = ruleProcBiomassMaxSupply))

    return


##### ----- fixed new build of dispathcable units ---------------------- #####

def constFixedNewBuildDisp(instance, model, iYear):
    ''' constraints on addition of dispatchable process '''
    
    def ruleFixedNewBuildDisp(model, sCountry, sProcDisp):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                for objProcCountry in objCountry.lsProcessAssump:
                    if objProcCountry.sProcessName == sProcDisp:
                        
                        if str(iYear) in objProcCountry.dicProcDispFixedNewBuild:
                            
                            TotalDispCap = 0
                            for sProc in model.setProcNewDisp_TCD:
                                if sProc[0:3] == sCountry and sProc.split("/")[1] == sProcDisp:
                                    TotalDispCap += model.vNewProcDispCap_TCD[sProc]
                            return TotalDispCap == objProcCountry.dicProcDispFixedNewBuild[str(iYear)] 
                        else:
                            return pe.Constraint.Skip
                        
        return pe.Constraint.Skip
                        
    setattr(model, "conFixedNewBuildDisp_CN_TCD", pe.Constraint(model.setCountryCode_CN, \
                    model.setDispatchableProc, rule = ruleFixedNewBuildDisp))

    return


##### ----- new renewable -------------------------------------------- #####

def constRenewAddMax(model, instance, objMarket):
    '''  constraints on addition of renewable process '''
    
    def ruleRenewAddMax(model, sCountry, sProcRenew):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                # [ "WND_ON", "WND_OFF", "PV", "CSP", "HYD", "GEO_hydro", "BIO_ST" ]
                if sProcRenew not in objCountry.dicRenewMaxCapAdd:
                    return pe.Constraint.Skip
                else:
                    
                    ### bio mass
                    if sProcRenew in ["BIO_ST"]:
                        
                        if objCountry.dicRenewMaxCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewDisp_TCD:
                                if sProc[0:3] == sCountry and sProc.split("/")[1] == sProcRenew:
                                    totalNewCap += model.vNewProcDispCap_TCD[sProc] 
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap <= objCountry.dicRenewMaxCapAdd[sProcRenew] 
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip
                                        
                    ### hydropower
                    elif sProcRenew in ["HYD"]:
                         
                        if objCountry.dicRenewMaxCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewHydr_TCH:
                                if sProc[0:3] == sCountry:
                                    totalNewCap += model.vNewProcHydrCap_TCH[sProc]
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap <= objCountry.dicRenewMaxCapAdd[sProcRenew] 
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip
                        
                    ### terrestrial renewables
                    elif sProcRenew in ["WND_ON", "PV", "CSP", "GEO_hydro"]:
                        
                        if objCountry.dicRenewMaxCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewRE_TCR:
                                if sProc[0:3] == sCountry:
                                    sProcessName = sProc.split("/")[1]
                                    if sProcessName[0:len(sProcRenew)] == sProcRenew:
                                        totalNewCap += model.vNewProcRenewCap_TCR[sProc]
                                        bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap <= objCountry.dicRenewMaxCapAdd[sProcRenew] 
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip

                    ### offshore renewables
                    elif sProcRenew in ["WND_OFF"]:
                    
                        if objCountry.dicRenewMaxCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewRE_Offs_TCR:
                                if sProc[0:3] == sCountry:
                                    totalNewCap += model.vNewProcRenewCapOffs_TCR[sProc]
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap <= objCountry.dicRenewMaxCapAdd[sProcRenew] 
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip
                    
        return pe.Constraint.Skip
                        
    setattr(model, "conRenewAddMax_CN_TCR", pe.Constraint(model.setCountryCode_CN, model.setRenewableType, rule = ruleRenewAddMax))

    return


def constRenewAddMin(model, instance, objMarket):
    '''  constraints on mimimum addition of renewable process '''
    
    def ruleRenewAddMin(model, sCountry, sProcRenew):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                # [ "WND_ON", "WND_OFF", "PV", "CSP", "HYD", "GEO_hydro", "BIO_ST" ]
                if sProcRenew not in objCountry.dicRenewMinCapAdd:
                    return pe.Constraint.Skip
                else:
                    
                    ### bio mass
                    if sProcRenew in ["BIO_ST"]:
                        
                        if objCountry.dicRenewMinCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewDisp_TCD:
                                if sProc[0:3] == sCountry and sProc.split("/")[1] == sProcRenew:
                                    totalNewCap += model.vNewProcDispCap_TCD[sProc] 
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap >= objCountry.dicRenewMinCapAdd[sProcRenew]
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip
                                        
                    ### hydropower
                    elif sProcRenew in ["HYD"]:
                         
                        if objCountry.dicRenewMinCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewHydr_TCH:
                                if sProc[0:3] == sCountry:
                                    totalNewCap += model.vNewProcHydrCap_TCH[sProc]
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap >= objCountry.dicRenewMinCapAdd[sProcRenew]
                            else:
                                return pe.Constraint.Skip 
                        else:
                            return pe.Constraint.Skip
                        
                    ### terrestrial renewables
                    elif sProcRenew in ["WND_ON", "PV", "CSP", "GEO_hydro"]:
                        
                        if objCountry.dicRenewMinCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewRE_TCR:
                                if sProc[0:3] == sCountry:
                                    sProcessName = sProc.split("/")[1]
                                    if sProcessName[0:len(sProcRenew)] == sProcRenew:
                                        totalNewCap += model.vNewProcRenewCap_TCR[sProc]
                                        bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap >= objCountry.dicRenewMinCapAdd[sProcRenew]
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip

                    ### offshore renewables
                    elif sProcRenew in ["WND_OFF"]:
                    
                        if objCountry.dicRenewMinCapAdd[sProcRenew] >= 0:
                            totalNewCap = 0
                            bProcAvailable = False
                            for sProc in model.setProcNewRE_Offs_TCR:
                                if sProc[0:3] == sCountry:
                                    totalNewCap += model.vNewProcRenewCapOffs_TCR[sProc]
                                    bProcAvailable = True
                            if bProcAvailable == True:
                                return totalNewCap >= objCountry.dicRenewMinCapAdd[sProcRenew]
                            else:
                                return pe.Constraint.Skip
                        else:
                            return pe.Constraint.Skip
                    
        return pe.Constraint.Skip
                        
    setattr(model, "conRenewAddMin_CN_TCR", pe.Constraint(model.setCountryCode_CN, \
                            model.setRenewableType, rule = ruleRenewAddMin))

    return


##### ----- hydro capacity max limit ----------------------------------- #####

def constHydroCapLimit(model, instance):
    '''  constraints on maximum installation of hydropower '''
    
    def ruleHydroCapLimit(model, sCountry):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                fCapLimit = objCountry.fTotalHydroCapLimit

                # existing capacity
                fCapExist = 0
                for sProcess in model.setProcBaseHydr_TCH:
                    if sProcess[0:3] == sCountry:
                        sTech = str(sProcess).split("/")[1]
                        if sTech in ["HYD_LG", "HYD_SM"]:
                            fCapExist += model.pExProcHydrCap_TCH[sProcess]
                    
                # new process
                fCapNew = 0
                bProcAvailable = False
                for sProcess in model.setProcNewHydr_TCH:
                    if sProcess[0:3] == sCountry:
                        sTech = str(sProcess).split("/")[1]
                        if sTech in ["HYD_LG", "HYD_SM"]:
                            fCapNew += model.vNewProcHydrCap_TCH[sProcess]
                            bProcAvailable = True
                    
                if bProcAvailable == True:
                    if fCapExist > fCapLimit:
                        return fCapNew == 0
                    else:
                        return fCapLimit >= fCapExist + fCapNew
                else:
                    return pe.Constraint.Skip
 
        return pe.Constraint.Skip
                        
    setattr(model, "conHydroCapLimit_CN_TCH", pe.Constraint(model.setCountryCode_CN, rule = ruleHydroCapLimit))

    return


##### ----- renewable minimal capacity of MCP 70 results -------------- #####

def constMCP70RenewPathway(model, objMarket, ind_year, iYear):                
    '''  constraints minimal renewable capacity installation in MCP scenario '''
    
    ### land zones
    def ruleMCP70RenewPathway(model, sZoneID, sREProcess):

        bTargetValue = -1
        for objZone in objMarket.lsZone:
            if objZone.sZoneID == sZoneID:
                if (sREProcess, str(iYear)) in objZone.dicMCP70RenewPathway_RE_YS:
                    bTargetValue = objZone.dicMCP70RenewPathway_RE_YS[sREProcess, str(iYear)]
                    break

        if bTargetValue <= 0:
            return pe.Constraint.Skip
        else:
            # existing capacity
            fExistCap = 0
            for objZone in objMarket.lsZone:
                if objZone.sZoneID == sZoneID:
                    for objProce in objZone.lsProcess:
                        if objProce.iDeCommitTime > iYear and objProce.sProcessName == sREProcess:
                            fExistCap += objProce.iCapacity
             
            NewCap = 0
            bNewProcAvail = False
            for sNewProc in model.setProcNewRE_TCR:  # this set exclude all hydropower
                if sNewProc.split("/")[0] == sZoneID and sNewProc.split("/")[1] == sREProcess:
                    NewCap += model.vNewProcRenewCap_TCR[sNewProc]
                    bNewProcAvail = True
                    
            if bNewProcAvail == True:
                # assume all capacity is no less 80% of target
                return NewCap + fExistCap >= bTargetValue * 0.8
            else:
                return pe.Constraint.Skip
                        
    setattr(model, "conMCP70RenewPathway_ZNL_RE", pe.Constraint(model.setLDZone_ZNL, \
                        model.setMCPRenewProc, rule = ruleMCP70RenewPathway))

    ### offshore zones
    def ruleMCP70RenewPathwayOffs(model, sZoneID, sREProcess):

        bTargetValue = -1
        for objZone in objMarket.lsZoneOffs:
            if objZone.sZoneID == sZoneID:
                if (sREProcess, str(iYear)) in objZone.dicMCP70RenewPathway_RE_YS:
                    bTargetValue = objZone.dicMCP70RenewPathway_RE_YS[sREProcess, str(iYear)]
                    break

        if bTargetValue <= 0:
            return pe.Constraint.Skip
        else:
            # existing capacity
            fExistCap = 0
            for objZone in objMarket.lsZoneOffs:
                if objZone.sZoneID == sZoneID:    
                    for objProce in objZone.lsProcess:
                        if objProce.iDeCommitTime > iYear and objProce.sProcessName == sREProcess:
                            fExistCap += objProce.iCapacity

            NewCap = 0
            bNewProcAvail = False
            for sNewProc in model.setProcNewRE_Offs_TCR:
                if sNewProc.split("/")[0] == sZoneID and sNewProc.split("/")[1] == sREProcess:
                    NewCap += model.vNewProcRenewCapOffs_TCR[sNewProc]
                    bNewProcAvail = True
                    
            if bNewProcAvail == True:
                # assume all capacity is no less 80% of target
                return NewCap + fExistCap >= bTargetValue * 0.8
            else:
                return pe.Constraint.Skip

    setattr(model, "conMCP70RenewPathwayOff_ZNF_RE", pe.Constraint(model.setOFZone_ZNF, \
                    model.setMCPRenewProc, rule = ruleMCP70RenewPathwayOffs))

    return


##### ----- carbon neutral scenario emission cap -------------------------- #####

def constCNSEmissionCap(instance, model, objMarket, ind_year, iYear):                
    '''  constraints on annual emissions in CNS scenario '''
    
    fTotalEmission = 0  # kg
    ### existing plant
    for TechDisp in model.setProcBaseDisp_TCD:
        sTech = str(TechDisp).split("/")[1]
        
        # search for fuel type
        sFuel = ""
        for obeProcDef in instance.lsProcessDefObjs:
            if obeProcDef.sProcessName == sTech:
                sFuel = obeProcDef.sFuel
                break
        
        fEmissionFactor = 0  # emission factor (kg/MJ = MTon/PJ)
        for objComm in instance.lsCommodity:     
            if objComm.sCategory == sFuel:
                fEmissionFactor = objComm.fEmissionFactor_CO2
        
        # fuel consumption
        fTecFuelCons = 0
        for sTS in model.setTimeSlice_TS:
            fTecFuelCons += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                * model.pTSRepHourYear_TS[sTS] / model.pExProcDispEff_TCD[TechDisp] * 3600  # MW * (TS) / Eff * 3600 = MJ
        
        CCSCaptureRate = model.pExProcDispCCSCapRate_TCD[TechDisp]
        
        if sFuel == "biomass":
            fTotalEmission += 0  # BIO_ST
            if CCSCaptureRate > 0:  # BIGCC_CCS
                fTotalEmission += fEmissionFactor * fTecFuelCons * CCSCaptureRate * -1
        else:
            fTotalEmission += fEmissionFactor * fTecFuelCons * (1-CCSCaptureRate)
                        
    ### new plants
    for TechDisp in model.setProcNewDisp_TCD:
        sTech = str(TechDisp).split("/")[1]

        # search for fuel type
        sFuel = ""
        for obeProcDef in instance.lsProcessDefObjs:
            if obeProcDef.sProcessName == sTech:
                sFuel = obeProcDef.sFuel
                break
        
        fEmissionFactor = 0  # emission factor (kg/MJ = MTon/PJ)
        for objComm in instance.lsCommodity:     
            if objComm.sCategory == sFuel:
                fEmissionFactor = objComm.fEmissionFactor_CO2
        
        # fuel consumption
        fTecFuelCons = 0
        for sTS in model.setTimeSlice_TS:
            fTecFuelCons += model.vNewProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                * model.pTSRepHourYear_TS[sTS] / model.pNewProcDispEff_TCD[TechDisp] * 3600  # MW * (TS) / Eff * 3600 = MJ
        
        CCSCaptureRate = model.pNewProcDispCCSCapRate_TCD[TechDisp]
        
        if sFuel == "biomass":
            fTotalEmission += 0  # BIO_ST
            if CCSCaptureRate > 0:  # BIGCC_CCS
                fTotalEmission += fEmissionFactor * fTecFuelCons * CCSCaptureRate * -1
        else:
            fTotalEmission += fEmissionFactor * fTecFuelCons * (1-CCSCaptureRate)
    
    fTotalEmission = fTotalEmission / 1000  # convert to tonne
    
    model.conCNSEmissionCap = pe.Constraint( expr = fTotalEmission <= objMarket.dicCNSEmissionCap_YS[iYear] )
    
    return


##### ----- new install renewable growth limit ------------------------------------------ #####

def constNewRenewLimit(model, instance, objMarket, ind_year):
    ''' constraints on the growth of all renewable generation '''
    
    iYear_pre = instance.iAllYearSteps_YS[ind_year-1]
    baseGrowthLimit = 0.25    
    
    # relax this config for 2040 to avoid infeasible
    if ind_year == 5:
        baseGrowthLimit = 0.4
    
    def ruleNewRenewInstallLimit(model, sCountry):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                # annual demand of previous period
                fCountryAnnualDemand_Pre = 0
                for objZone in objMarket.lsZone:
                    if objZone.sCountry == sCountry:
                        fCountryAnnualDemand_Pre += objMarket.dicDemand_ZNL_YS[objZone.sZone,iYear_pre]
                
                # annual demand (MWh)
                fCountryAnnualDemand = 0
                for sZoneID in model.setLDZone_ZNL:
                    if sZoneID[0:3] == sCountry:
                        for sTSIndex in model.setTimeSlice_TS:
                            fCountryAnnualDemand += model.pDemand_ZNL_TS[sZoneID, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                
                adjGrowthLimit = baseGrowthLimit / fCountryAnnualDemand_Pre * fCountryAnnualDemand
                
                # all biomass generation of previous year (MWh)
                fAllBioGenPreviousYS = 0
                for sProcess in model.setProcBaseDisp_TCD:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["BIO_ST","BIGCC_CCS"]:
                        fAllBioGenPreviousYS += objMarket.dicProcDispPwOutNet_TCD_YS[sProcess,iYear_pre]
                        
                # all hydro generation of previous year (MWh)
                fAllHydroGenPreviousYS = 0
                for sProcess in model.setProcBaseHydr_TCH:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["HYD_LG", "HYD_SM"]:
                        fAllHydroGenPreviousYS += objMarket.dicProcHydrPwOut_TCH_YS[sProcess,iYear_pre]
                
                # non-hydro renewable generation of previous year (MWh)
                fAllReGenPreviousYS = 0
                for objZone in objMarket.lsZone:
                    if objZone.sCountry == sCountry:
                        fAllReGenPreviousYS += objMarket.dicRenewGenAll_ZNL_YS[objZone.sZone,iYear_pre]
                        
                # non-hydro renewable generation of previous year offshore (MWh)
                fAllReGenPreviousYS_off = 0
                for objZone in objMarket.lsZoneOffs:
                    if objZone.sCountry == sCountry:
                        fAllReGenPreviousYS_off += objMarket.dicRenewGenAllOff_ZNF_YS[objZone.sZone,iYear_pre]
                
                # total renewable generation limit 
                # assume a 25% increase limit from the last period, including hydro and biomass
                fTotalReGenLimit = fAllBioGenPreviousYS + fAllReGenPreviousYS \
                    + fAllHydroGenPreviousYS + fAllReGenPreviousYS_off \
                    + (fCountryAnnualDemand * adjGrowthLimit)
                
                bProcAvailable = False
                
                # biomass process
                fBioGen = 0
                for sProcess in model.setProcBaseDisp_TCD:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["BIO_ST","BIGCC_CCS"]:
                        for sTSIndex in model.setTimeSlice_TS:
                            fBioGen += model.vExProcDispPwOutNet_TCD_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                fNewBioGen = 0
                for sProcess in model.setProcNewDisp_TCD:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["BIO_ST","BIGCC_CCS"]:
                        bProcAvailable = True
                        for sTSIndex in model.setTimeSlice_TS:
                            fNewBioGen += model.vNewProcDispPwOutNet_TCD_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]

                # hydro process
                fHydroGen = 0
                for sProcess in model.setProcBaseHydr_TCH:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["HYD_LG", "HYD_SM"]:
                        for sTSIndex in model.setTimeSlice_TS:
                            fHydroGen += model.vExProcHydrPwOut_TCH_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                fNewHydroGen = 0
                for sProcess in model.setProcNewHydr_TCH:
                    if sProcess[0:3] == sCountry and sProcess.split("/")[1] in ["HYD_LG", "HYD_SM"]:
                        bProcAvailable = True
                        for sTSIndex in model.setTimeSlice_TS:
                            fNewHydroGen += model.vNewProcHydrPwOut_TCH_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]

                # non-dispatch renewable process (exclude hydrtopower)
                fRenewGen = 0
                for sZoneID in model.setLDZone_ZNL:
                    if sZoneID[0:3] == sCountry:
                        for sTSIndex in model.setTimeSlice_TS:
                            fRenewGen += model.pNonDispGen_ZNL_TS[sZoneID, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                fNewRenewGen = 0
                for sProcess in model.setProcNewRE_TCR:
                    if sProcess[0:3] == sCountry:
                        bProcAvailable = True
                        for sTSIndex in model.setTimeSlice_TS:
                            fNewRenewGen += model.vNewProcRenewPwOut_TCR_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                
                # offshore renewable process
                fOffRenewGen = 0
                for sZoneID in model.setOFZone_ZNF:
                    if sZoneID[0:3] == sCountry:
                        for sTSIndex in model.setTimeSlice_TS:
                            fOffRenewGen += model.pNonDispGen_ZNF_TS[sZoneID, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                fNewOffRenewGen = 0
                for sProcess in model.setProcNewRE_Offs_TCR:
                    if sProcess[0:3] == sCountry:
                        bProcAvailable = True
                        for sTSIndex in model.setTimeSlice_TS:
                            fNewOffRenewGen += model.vNewProcRenewPwOutOffs_TCR_TS[sProcess, sTSIndex] \
                                * model.pTSRepHourYear_TS[sTSIndex]
                
                if bProcAvailable == False:
                    return pe.Constraint.Skip
                else:
                    return (fBioGen+ fNewBioGen + fHydroGen+ fNewHydroGen \
                            + fRenewGen+ fNewRenewGen + fOffRenewGen + fNewOffRenewGen) \
                            <= fTotalReGenLimit
                    
        return pe.Constraint.Skip
                        
    setattr(model, "conNewRenewInstallLimit_CN", \
            pe.Constraint(model.setCountryCode_CN, rule = ruleNewRenewInstallLimit))

    return


##### ----- biomass minimal capacity ------------------------------------------ #####

def constBioMassCapFloor(model, instance, objMarket):
    ''' constraints on minimum capacity of biomass processes  '''
    
    def ruleBiomassCapLimit(model, sCountry):

        for objCountry in instance.lsCountry:
            if objCountry.sCountry == sCountry:
                
                # 2020 capacity
                f2020Capacity = 0
                for objZone in objMarket.lsZone:
                    if objZone.sCountry == sCountry:
                        for objProc in objZone.lsProcess:
                            if objProc.iCommitTime <= 2015:
                                if objProc.sProcessName in ["BIO_ST"]:
                                    f2020Capacity += objProc.iCapacity
                
                # existing capacity
                fCapExist = 0
                for sProcess in model.setProcBaseDisp_TCD:
                    if sProcess[0:3] == sCountry:
                        sTech = str(sProcess).split("/")[1]
                        if sTech in ["BIO_ST"]:
                            fCapExist += model.pExProcDispCap_TCD[sProcess]
                    
                # new process
                fCapNew = 0
                bProcAvailable = False
                for sProcess in model.setProcNewDisp_TCD:
                    if sProcess[0:3] == sCountry:
                        sTech = str(sProcess).split("/")[1]
                        if sTech in ["BIO_ST"]:
                            fCapNew += model.vNewProcDispCap_TCD[sProcess]
                            bProcAvailable = True
                    
                if bProcAvailable == True:
                    return fCapExist + fCapNew >= f2020Capacity
                else:
                    return pe.Constraint.Skip
 
        return pe.Constraint.Skip
                        
    setattr(model, "conBiomassCapLimit_CN_TCD", \
            pe.Constraint(model.setCountryCode_CN, rule = ruleBiomassCapLimit))

    return

