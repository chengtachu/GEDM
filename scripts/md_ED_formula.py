#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to construct ED model constraints
#

import pyomo.environ as pe


def constUnitGen(model, objMarket):
    ''' dispatchable process generation constraints '''

    ### gross power output
    def ruleProcessPowerOutGross_Disp(model, sProcDisp, sTimeSlice) :

        # consider overall planned/forced outage, equivalent available factor
        return model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            <= model.pExProcDispCap_TCD[sProcDisp] * model.pExProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcessPowerOutGross_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, rule = ruleProcessPowerOutGross_Disp))

    ### net power output
    def ruleProcessPowerOutNet_Disp(model, sProcDisp, sTimeSlice) :

        return model.vExProcDispPwOutNet_TCD_TS[sProcDisp, sTimeSlice] \
            == model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] \
            * (1-model.pExProcDispOUS_TCD[sProcDisp])

    setattr(model, "conProcessPowerOutNet_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, rule = ruleProcessPowerOutNet_Disp))

    return


##### ------------------------------------------------------------------ #####
def constStorageOpr(model, objMarket):
    ''' storage system operation constraints '''
    
    ### max hourly output (MW)
    def ruleStorPowerOutMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation  
        return model.vExProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] \
            <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerOutMax_TCS_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTimeSlice_TS, rule = ruleStorPowerOutMax))    
    
    ### max hourly input (MW)
    def ruleStorPowerInMax(model, sProcStor, sTimeSlice) :  
        
        # only non-dispatchable generation   
        return model.vExProcStorPwIn_TCS_TS[sProcStor, sTimeSlice] \
            <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]
    
    setattr(model, "conStorPowerInMax_TCS_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTimeSlice_TS, rule = ruleStorPowerInMax))   
      
    ### daily total generation constraint (MWh)
    def ruleStorDayGen(model, sProcStor) :  
        
        fCapacity = model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] # MW
        fMaxDayOutput = fCapacity * model.pExProcStorDur_TCS[sProcStor]   # total stored energy, MW -> MWh
        
        fDayOutput = 0
        for sTSIndex in model.setTimeSlice_TS:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vExProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
    
        return fDayOutput <= fMaxDayOutput
    
    setattr(model, "conStorDayGen_TCS_DY", \
            pe.Constraint(model.setProcBaseStor_TCS, rule = ruleStorDayGen))  
    
    ### daily input/output balance constraint
    def ruleStorDayBalance(model, sProcStor) :  
        
        fGrossEffeciency = model.pExProcStorEff_TCS[sProcStor]
        
        fDayOutput = 0
        fDayInput = 0
        for sTSIndex in model.setTimeSlice_TS:
            iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
            fDayOutput += model.vExProcStorPwOut_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
            fDayInput += model.vExProcStorPwIn_TCS_TS[sProcStor, sTSIndex] * iTSRepHour
    
        return fDayInput == (fDayOutput / fGrossEffeciency)
    
    setattr(model, "conStorDayBalance_TCS_DY", \
            pe.Constraint(model.setProcBaseStor_TCS, rule = ruleStorDayBalance))   
    
    return


##### ------------------------------------------------------------------ #####
def constHydropowerOpr(model, objMarket):
    ''' large hydropower operation constraints (partially dispatchable) '''
    
    ### small hydro output
    def ruleHydrPowerOutputSml(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_SM":
            # default generation (EAF already included)
            return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] \
                == model.pExProcHydrGen_TCH_TS[TechHydro, sTimeSlice]
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPowerOutputSml_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleHydrPowerOutputSml))

    ### large hydro generation limit - upper bound
    def ruleHydrPowerOutUpBnd(model, TechHydro, sTimeSlice) :

        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.pExProcHydrCap_TCH[TechHydro]
            fEAF = model.pExProcHydrEAF_TCH[TechHydro]
            return model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice] <=  fCapacity * fEAF
        else:
            return pe.Constraint.Skip

    setattr(model, "conHydrPowerOutUpBnd_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleHydrPowerOutUpBnd))

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

    setattr(model, "conHydrPowerOutLowBnd_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleHydrPowerOutLowBnd))

    ### large hydro generation daily dispatch
    def ruleHydrPowerOutDispatch(model, TechHydro) :

        iDispatchBase = 0.3
        sTech = str(TechHydro).split("/")[1]
        if sTech[0:6] == "HYD_LG":
            fCapacity = model.pExProcHydrCap_TCH[TechHydro] # MW
            if fCapacity > 0:
                defaultGen = float(model.pExProcHydrGen_TCH_TS[TechHydro, model.setTimeSlice_TS[1]])
                if (defaultGen / fCapacity) >= iDispatchBase:
                    
                    # total available dispatchable energy
                    total_dispatchable = 0
                    for sTSIndex in model.setTimeSlice_TS:
                        iTSRepHour = model.pTSRepHourDay_TS[sTSIndex]
                        hourGen = float(model.pExProcHydrGen_TCH_TS[TechHydro, sTSIndex])
                        total_dispatchable = total_dispatchable + (hourGen * iTSRepHour)  # MWh
                        
                    # total generation
                    total_generation = 0
                    for sTSIndex in model.setTimeSlice_TS:
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

    setattr(model, "conHydrPowerOutDispatch_TCH_DY", \
            pe.Constraint(model.setProcBaseHydr_TCH, rule = ruleHydrPowerOutDispatch))

    return


##### ------------------------------------------------------------------ #####
def constPowerBalance(model, objMarket):
    ''' power balance constraints for each zone '''
    
    # --- land zones ------------------------------
    
    ### power supply of land zones
    def ruleLDZProcPowerSupply(model, sZone, sTimeSlice) :
        
        vPowerOutput = 0        
        # dispatchable output
        for TechDisp in model.setProcBaseDisp_TCD:
            if (sZone + "/") in TechDisp:
                vPowerOutput = vPowerOutput + model.vExProcDispPwOutNet_TCD_TS[TechDisp, sTimeSlice]                
        # storage output
        for TechStor in model.setProcBaseStor_TCS:
            if (sZone + "/") in TechStor:
                vPowerOutput = vPowerOutput + model.vExProcStorPwOut_TCS_TS[TechStor, sTimeSlice] \
                    - model.vExProcStorPwIn_TCS_TS[TechStor, sTimeSlice] 
                
        # hydropower output
        for TechHydro in model.setProcBaseHydr_TCH:
            if (sZone + "/") in TechHydro:
                vPowerOutput = vPowerOutput + model.vExProcHydrPwOut_TCH_TS[TechHydro, sTimeSlice]  
                
        # add non-dispatchable generation
        return model.vSupplyZone_ZNL_TS[sZone, sTimeSlice] \
            == vPowerOutput + model.pNonDispGen_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZPowerSupply_ZNL_TS", \
            pe.Constraint(model.setLDZone_ZNL, model.setTimeSlice_TS, rule = ruleLDZProcPowerSupply))
    
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
            + vTransZoneOutput + vTransOffshoreOutput - vTransZoneInput == model.pDemand_ZNL_TS[sZone, sTimeSlice]
        
    setattr(model, "conPowerBalanceZone_ZNL_TS", \
            pe.Constraint(model.setLDZone_ZNL, model.setTimeSlice_TS, rule = rulePowerBalanceLandZone))
    

    # --- offshore zones ------------------------------
    
    ### power supply of offshore zones
    def ruleOFZProcPowerSupply(model, sZone, sTimeSlice) :  
        
        # only non-dispatchable generation    
        return model.vSupplyOffs_ZNF_TS[sZone, sTimeSlice] == model.pNonDispGen_ZNF_TS[sZone, sTimeSlice] 
    
    setattr(model, "conOFZPowerSupply_ZNF_TS", \
            pe.Constraint(model.setOFZone_ZNF, model.setTimeSlice_TS, rule = ruleOFZProcPowerSupply))    
    
    ### all transmission(line) input + spill = total supply
    def ruleTransOFZInput(model, sZone, sTimeSlice) :  
        
        vAllTransOffshoreInput_TS = 0
        for TransLine in model.setTransOFZ_TRF:
            if (sZone + "/") in TransLine:
                vAllTransOffshoreInput_TS = \
                    vAllTransOffshoreInput_TS + model.vTransOFZIn_TRF_TS[TransLine, sTimeSlice]
                
        return model.vSupplyOffs_ZNF_TS[sZone, sTimeSlice] \
            == vAllTransOffshoreInput_TS + model.vSpillOffs_ZNF_TS[sZone, sTimeSlice]
    
    setattr(model, "conOFZBalanceZone_ZNF_TS", \
            pe.Constraint(model.setOFZone_ZNF, model.setTimeSlice_TS, rule = ruleTransOFZInput))   
        
    return


##### ------------------------------------------------------------------ #####
def constTransOpr(model, objMarket):
    ''' transmission constraints '''

    # transmission(line) input limited by capacity
    def ruleTransZoneInputCap(model, TransZone, sTimeSlice) :

        return model.vTransLDZIn_TRL_TS[TransZone, sTimeSlice] <= model.pTransLDZCap_TRL[TransZone]

    setattr(model, "conTransZoneInputCap_TRL_TS", \
            pe.Constraint(model.setTransLDZ_TRL, model.setTimeSlice_TS, rule = ruleTransZoneInputCap))


    # transmission(line) output consider losses
    def ruleTransZoneOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransLDZLoss_TRL[TransZone]
        return model.vTransLDZOut_TRL_TS[TransZone, sTimeSlice] \
            == model.vTransLDZIn_TRL_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransZoneOutput_TRL_TS", \
            pe.Constraint(model.setTransLDZ_TRL, model.setTimeSlice_TS, rule = ruleTransZoneOutput))


    # transmission(line) input offshore limited by capacity
    def ruleTransOffshoreInputCap(model, TransZone, sTimeSlice) :

        return model.vTransOFZIn_TRF_TS[TransZone, sTimeSlice] <= model.pTransOFZCap_TRF[TransZone]

    setattr(model, "conTransOffsInputCap_TRF_TS", \
            pe.Constraint(model.setTransOFZ_TRF, model.setTimeSlice_TS, rule = ruleTransOffshoreInputCap))


    # transmission(line) output offshore consider lossess
    def ruleTransOffshoreOutput(model, TransZone, sTimeSlice) :

        fLineLoss = model.pTransOFZLoss_TRF[TransZone]
        return model.vTransOFZOut_TRF_TS[TransZone, sTimeSlice] \
            == model.vTransOFZIn_TRF_TS[TransZone, sTimeSlice] * (1-fLineLoss)

    setattr(model, "conTransOffsOutput_TRF_TS", \
            pe.Constraint(model.setTransOFZ_TRF, model.setTimeSlice_TS, rule = ruleTransOffshoreOutput))
        
    return


##### ------------------------------------------------------------------ #####
def constZonalAncillaryService(model, objMarket):
    ''' ancillary services constraints '''
    
    ##### zonal AS requirement 
    # all T1 AS capacity in a land zone
    def ruleLDZASReqT1(model, sZone, sTimeSlice) :
        
        vZoneAS = 0        
        for sProc in model.setProcBaseAS_TCA1:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA1_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT1_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT1_ZNL_TS", \
            pe.Constraint(model.setLDZone_ZNL, model.setTimeSlice_TS, rule = ruleLDZASReqT1))
    
    # all T2 AS capacity in a land zone
    def ruleLDZASReqT2(model, sZone, sTimeSlice) :
        
        vZoneAS = 0        
        for sProc in model.setProcBaseAS_TCA2:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA2_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT2_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT2_ZNL_TS", \
            pe.Constraint(model.setLDZone_ZNL, model.setTimeSlice_TS, rule = ruleLDZASReqT2))
    
    # all T3 AS capacity in a land zone
    def ruleLDZASReqT3(model, sZone, sTimeSlice) :
        
        vZoneAS = 0        
        for sProc in model.setProcBaseAS_TCA3:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA3_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT3_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT3_ZNL_TS", \
            pe.Constraint(model.setLDZone_ZNL, model.setTimeSlice_TS, rule = ruleLDZASReqT3))
    
    ##### capacity limit of each process - single type AS
    def ruleProcASProvT1(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA1_TS[sProc, sTimeSlice] <= model.pExProcMaxAS_TCA1[sProc]    
    setattr(model, "conProcASProv_TCA1_TS", \
            pe.Constraint(model.setProcBaseAS_TCA1, model.setTimeSlice_TS, rule = ruleProcASProvT1))
    
    def ruleProcASProvT2(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA2_TS[sProc, sTimeSlice] <= model.pExProcMaxAS_TCA2[sProc] 
    setattr(model, "conProcASProv_TCA2_TS", \
            pe.Constraint(model.setProcBaseAS_TCA2, model.setTimeSlice_TS, rule = ruleProcASProvT2))
    
    def ruleProcASProvT3(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA3_TS[sProc, sTimeSlice] <= model.pExProcMaxAS_TCA3[sProc] 
    setattr(model, "conProcASProv_TCA3_TS", \
            pe.Constraint(model.setProcBaseAS_TCA3, model.setTimeSlice_TS, rule = ruleProcASProvT3))

    ### all provided capacity of a process 
    # dispatchable units - overall provision bounded by derated capacity
    def ruleProcDispAllCapOut(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcBaseAS_TCA3:
            vProcCap = vProcCap + model.vExProcASProv_TCA3_TS[sProcDisp, sTimeSlice]
            
        return vProcCap <= model.pExProcDispCap_TCD[sProcDisp] * model.pExProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispAllCapOut_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispAllCapOut))

    # dispatchable units - ensure spinning state (skip for OGCT and Oil)
    def ruleProcDispMinLDforAS(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcBaseAS_TCA3:
            vProcCap = vProcCap + model.vExProcASProv_TCA3_TS[sProcDisp, sTimeSlice]
            
        # if the process is fast start up gas or oil units, can be non-spinning reserve
        if "GAS_OCGT" in sProcDisp or "OIL_ST" in sProcDisp:
            return pe.Constraint.Skip
        else:
            # ensure spinning state, and assume the min load is around 33%
            return vProcCap <= model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] * 2

    setattr(model, "conProcDispMinLDforAS_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispMinLDforAS))


    # dispatchable units - ensure spinning state for T1 AS
    def ruleProcDispMinLDforAST1(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = model.vExProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
                    
        return vProcCap <= model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] * 0.5

    setattr(model, "conProcDispMinLDforAST1_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispMinLDforAST1))


    # storage unit - overall provision bounded by derated capacity
    def ruleProcStorAllCapOut(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] 
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]

    setattr(model, "conProcStorAllCapOut_TCD_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTimeSlice_TS, rule = ruleProcStorAllCapOut))

    # storage unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by 50% of derated capacity, considering its operation
    def ruleProcStorASOutLimit(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= (model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] * 0.5)

    setattr(model, "conProcStorASOutLimit_TCD_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTimeSlice_TS, rule = ruleProcStorASOutLimit))

    # hydropower limit - overall provision bounded by derated capacity
    def ruleProcHydrAllCapOut(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.pExProcHydrCap_TCH[sProcHydro] * model.pExProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrAllCapOut_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleProcHydrAllCapOut))

    # hydropower unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by instantaneous output (same volume)
    def ruleProcHydrASOutLimit(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.vExProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice]

    setattr(model, "conProcHydrASOutLimit_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleProcHydrASOutLimit))

    return


##### ------------------------------------------------------------------ #####
def constMinBaseUnitGen(model, objMarket, fMinBaseGen):
    ''' constraint on generation from existing dispatchable units '''
    
    def ruleProcBaseDayMinGen_Disp(model, sProcDisp):

        sTech = str(sProcDisp).split("/")[1]
        if sTech not in ["BIO_ST","BIGCC_CCS"]:
        
            BaseCF = model.pExProcBaseGenCF_TCD[sProcDisp]
            if BaseCF == 0:
                return pe.Constraint.Skip
            else:
                BaseCF = BaseCF * fMinBaseGen
                
                # target day generation
                targetGen = 0
                for sTSIndex in model.setTimeSlice_TS:
                    targetGen = targetGen + (model.pExProcDispCap_TCD[sProcDisp] * BaseCF)
                
                # day generettion
                dayGen = 0
                for sTSIndex in model.setTimeSlice_TS:
                    dayGen = dayGen + model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTSIndex]
                
                return dayGen >= targetGen
        
        else:
            return pe.Constraint.Skip

    setattr(model, "conProcBaseDayMinGen_TCD", \
            pe.Constraint(model.setProcBaseDisp_TCD, rule = ruleProcBaseDayMinGen_Disp))

    return


def constMinBaseUnitGen_Bio(model, instance, objMarket):
    ''' constraint on generation from existing BIO_ST units '''
    
    def ruleProcBaseMinGen_Bio(model, sCountry):

        # total base year country generation, release the value by * 0.9
        country_gen = model.pExProcBaseBioGen_CN[sCountry] * 0.9

        bTechAvail = False
        day_gen = 0
        for sProcDisp in model.setProcBaseDisp_TCD:
            if sProcDisp[0:3] == sCountry:
                sTech = str(sProcDisp).split("/")[1]
                if sTech in ["BIO_ST"]:
                    if model.pExProcDispCap_TCD[sProcDisp] > 0:
                        
                        bTechAvail = True                   
                        for sTSIndex in model.setTimeSlice_TS:
                            day_gen = day_gen + model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTSIndex]

        if bTechAvail == True:
            return day_gen >= country_gen
        else:
            return pe.Constraint.Skip

    setattr(model, "conProcBaseMinGenBio_CN", \
            pe.Constraint(model.setCountryCode_CN, rule = ruleProcBaseMinGen_Bio))

    return


##### ----- carbon neutral scenario emission cap -------------------------- #####

def constCNSEmissionCap(instance, model, objMarket, ind_year):                
    ''' constraint on emission limit in CNS scenario '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    iYear_pre = instance.iAllYearSteps_YS[ind_year-1]
    
    # last period can not be 0, otherwise infeasible
    fEmissionCap = objMarket.dicCNSEmissionCap_YS[iYear]
    if fEmissionCap == 0:
        fEmissionCap = objMarket.dicCNSEmissionCap_YS[iYear_pre] * 0.1
    
    annualResDem = sum(objMarket.ResDemand_TS.values())
    emissionCap_year = {}
    for objTS in instance.lsTimeSlice:
        emissionCap_year[objTS.sTSIndex] = \
            objMarket.ResDemand_TS[objTS.sTSIndex] / annualResDem * fEmissionCap
    
    emissionCap_Day = 0  # Tonne
    for sTS in model.setTimeSlice_TS:
        emissionCap_Day += emissionCap_year[sTS]
    
    # loose cap constraint
    if emissionCap_Day < fEmissionCap*0.03:
        emissionCap_Day = fEmissionCap*0.03
    else:
        emissionCap_Day = emissionCap_Day * 1.2
    
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
                * model.pTSRepHourYear_TS[sTS] / model.pExProcDispEff_TCD[TechDisp] * 3600  
                # MW * (TS) / Eff * 3600 = MJ
        
        CCSCaptureRate = model.pExProcDispCCSCapRate_TCD[TechDisp]
        
        if sFuel == "biomass":
            fTotalEmission += 0  # BIO_ST
            if CCSCaptureRate > 0:  # BIGCC_CCS
                fTotalEmission += fEmissionFactor * fTecFuelCons * CCSCaptureRate * -1
        else:
            fTotalEmission += fEmissionFactor * fTecFuelCons * (1-CCSCaptureRate)
                        
    fTotalEmission = fTotalEmission / 1000  # convert to tonne
    
    model.conCNSEmissionCap = pe.Constraint( expr = fTotalEmission <= emissionCap_Day )
    
    return

