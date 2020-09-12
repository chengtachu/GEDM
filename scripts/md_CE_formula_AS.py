#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to construct ancillary services constraints in CE model
#

import pyomo.environ as pe


##### ---- ancillary services zonal ------------------------------------ #####

def constZonalAncillaryService_Zone(model, objMarket):
    ''' ancillary services constraints '''
    
    # all T1 AS capacity in a land zone
    def ruleLDZASReqT1(model, sZone, sTimeSlice) :
        
        vZoneAS = 0       
        for sProc in model.setProcBaseAS_TCA1:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA1_TS[sProc,sTimeSlice]
        for sProc in model.setProcNewAS_TCA1:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProv_TCA1_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT1_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT1_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                            model.setTimeSlice_TS, rule = ruleLDZASReqT1))
    
    # all T2 AS capacity in a land zone
    def ruleLDZASReqT2(model, sZone, sTimeSlice) :
        
        vZoneAS = 0
        for sProc in model.setProcBaseAS_TCA2:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA2_TS[sProc,sTimeSlice]
        for sProc in model.setProcNewAS_TCA2:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProv_TCA2_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT2_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT2_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                            model.setTimeSlice_TS, rule = ruleLDZASReqT2))
    
    # all T3 AS capacity in a land zone
    def ruleLDZASReqT3(model, sZone, sTimeSlice) :
        
        vZoneAS = 0
        for sProc in model.setProcBaseAS_TCA3:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProv_TCA3_TS[sProc,sTimeSlice]  
        for sProc in model.setProcNewAS_TCA3:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProv_TCA3_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT3_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT3_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                            model.setTimeSlice_TS, rule = ruleLDZASReqT3))
    
    return


##### ---- ancillary services zonal (Testing TS) ---------------------- #####

def constZonalAS_Zone_RT(model, objMarket):
    ''' ancillary services constraints in testing TS '''
    
    # all T1 AS capacity in a land zone
    def ruleLDZASReqT1(model, sZone, sTimeSlice) :
        
        vZoneAS = 0       
        for sProc in model.setProcBaseAS_TCA1:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProvTest_TCA1_TS[sProc,sTimeSlice]
        for sProc in model.setProcNewAS_TCA1:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProvTest_TCA1_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT1Test_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT1Test_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                                    model.setTSRT_TS, rule = ruleLDZASReqT1))
    
    # all T2 AS capacity in a land zone
    def ruleLDZASReqT2(model, sZone, sTimeSlice) :
        
        vZoneAS = 0
        for sProc in model.setProcBaseAS_TCA2:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProvTest_TCA2_TS[sProc,sTimeSlice] 
        for sProc in model.setProcNewAS_TCA2:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProvTest_TCA2_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT2Test_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT2Test_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                                    model.setTSRT_TS, rule = ruleLDZASReqT2))
    
    # all T3 AS capacity in a land zone
    def ruleLDZASReqT3(model, sZone, sTimeSlice) :
        
        vZoneAS = 0
        for sProc in model.setProcBaseAS_TCA3:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vExProcASProvTest_TCA3_TS[sProc,sTimeSlice]
        for sProc in model.setProcNewAS_TCA3:
            sProcZone = str(sProc).split("/")[0]
            if sProcZone == sZone:
                vZoneAS = vZoneAS + model.vNewProcASProvTest_TCA3_TS[sProc,sTimeSlice]
        
        return vZoneAS == model.pASReqT3Test_ZNL_TS[sZone, sTimeSlice] 
    
    setattr(model, "conLDZASReqT3Test_ZNL_TS", pe.Constraint(model.setLDZone_ZNL, \
                                    model.setTSRT_TS, rule = ruleLDZASReqT3))
    
    return


##### ---- ancillary services existing units --------------------------- #####

def constZonalAncillaryService_Ex(model, objMarket):
    ''' ancillary services constraints on existing processes '''
    
    ### upper bound limited by ramping capacility
    iUnitAvail = 0.9
    def ruleProcASProvT1(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA1_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA1[sProc] * iUnitAvail
    setattr(model, "conProcASProv_TCA1_TS", pe.Constraint(model.setProcBaseAS_TCA1, \
                        model.setTimeSlice_TS, rule = ruleProcASProvT1))
    
    def ruleProcASProvT2(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA2_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA2[sProc] * iUnitAvail
    setattr(model, "conProcASProv_TCA2_TS", pe.Constraint(model.setProcBaseAS_TCA2, \
                        model.setTimeSlice_TS, rule = ruleProcASProvT2))
    
    def ruleProcASProvT3(model, sProc, sTimeSlice) :
        return model.vExProcASProv_TCA3_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA3[sProc] * iUnitAvail
    setattr(model, "conProcASProv_TCA3_TS", pe.Constraint(model.setProcBaseAS_TCA3, \
                        model.setTimeSlice_TS, rule = ruleProcASProvT3))

    ### ---------- dispatchable units ------------------------
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

    setattr(model, "conProcDispAllCapOut_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                        model.setTimeSlice_TS, rule = ruleProcDispAllCapOut))

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

    setattr(model, "conProcDispMinLDforAS_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD, \
                        model.setTimeSlice_TS, rule = ruleProcDispMinLDforAS))


    # dispatchable units - ensure spinning state for T1 AS
    def ruleProcDispMinLDforAST1(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = model.vExProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
                    
        return vProcCap <= model.vExProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] * 0.5

    setattr(model, "conProcDispMinLDforAST1_TCD_TS", pe.Constraint(model.setProcBaseDisp_TCD,
                        model.setTimeSlice_TS, rule = ruleProcDispMinLDforAST1))


    ### ---------- storage units ------------------------
    # storage unit - overall provision bounded by derated capacity
    def ruleProcStorAllCapOut(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] 
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]

    setattr(model, "conProcStorAllCapOut_TCD_TS", pe.Constraint(model.setProcBaseStor_TCS, \
                        model.setTimeSlice_TS, rule = ruleProcStorAllCapOut))

    # storage unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by 50% of derated capacity, considering its operation
    def ruleProcStorASOutLimit(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= (model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] * 0.5)

    setattr(model, "conProcStorASOutLimit_TCD_TS", pe.Constraint(model.setProcBaseStor_TCS, \
                        model.setTimeSlice_TS, rule = ruleProcStorASOutLimit))


    ### ---------- hydropower ------------------------
    # hydropower limit - overall provision bounded by derated capacity
    def ruleProcHydrAllCapOut(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.pExProcHydrCap_TCH[sProcHydro] * model.pExProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrAllCapOut_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleProcHydrAllCapOut))

    # hydropower unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by instantaneous output (same volume)
    def ruleProcHydrASOutLimit(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        if model.pNewProcHydrCF_TCH_TS[sProcHydro, sTimeSlice] < 0.1:
            return vProcCap == 0
        else:
            return vProcCap <= model.vExProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice] \
                * model.pExProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrASOutLimit_TCH_TS", pe.Constraint(model.setProcBaseHydr_TCH, \
                        model.setTimeSlice_TS, rule = ruleProcHydrASOutLimit))

    return


##### ---- ancillary services existing units (Testing TS) ------------- #####

def constZonalAS_Ex_RT(model, objMarket):
    ''' ancillary services constraints on existing processes in testing TS '''
    
    ### upper bound limited by ramping capacility
    iUnitAvail = 0.9
    def ruleProcASProvT1(model, sProc, sTimeSlice) :
        return model.vExProcASProvTest_TCA1_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA1[sProc] * iUnitAvail
    setattr(model, "conProcASProvTest_TCA1_TS", \
            pe.Constraint(model.setProcBaseAS_TCA1, model.setTSRT_TS, rule = ruleProcASProvT1))
    
    def ruleProcASProvT2(model, sProc, sTimeSlice) :
        return model.vExProcASProvTest_TCA2_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA2[sProc] * iUnitAvail
    setattr(model, "conProcASProvTest_TCA2_TS", \
            pe.Constraint(model.setProcBaseAS_TCA2, model.setTSRT_TS, rule = ruleProcASProvT2))
    
    def ruleProcASProvT3(model, sProc, sTimeSlice) :
        return model.vExProcASProvTest_TCA3_TS[sProc, sTimeSlice] \
            <= model.pExProcMaxAS_TCA3[sProc] * iUnitAvail
    setattr(model, "conProcASProvTest_TCA3_TS", \
            pe.Constraint(model.setProcBaseAS_TCA3, model.setTSRT_TS, rule = ruleProcASProvT3))

    ### ---------- dispatchable units ------------------------
    # dispatchable units - overall provision bounded by derated capacity
    def ruleProcDispAllCapOut(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcBaseAS_TCA3:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA3_TS[sProcDisp, sTimeSlice]
            
        return vProcCap <= model.pExProcDispCap_TCD[sProcDisp] * model.pExProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispAllCapOutTest_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTSRT_TS, rule = ruleProcDispAllCapOut))

    # dispatchable units - ensure spinning state (skip for OGCT and Oil)
    def ruleProcDispMinLDforAS(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcBaseAS_TCA3:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA3_TS[sProcDisp, sTimeSlice]
            
        # if the process is fast start up gas or oil units, can be non-spinning reserve
        if "GAS_OCGT" in sProcDisp or "OIL_ST" in sProcDisp:
            return pe.Constraint.Skip
        else:
            # ensure spinning state, and assume the min load is around 33%
            return vProcCap <= model.vExProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] * 2

    setattr(model, "conProcDispMinLDforASTest_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTSRT_TS, rule = ruleProcDispMinLDforAS))


    # dispatchable units - ensure spinning state for T1 AS
    def ruleProcDispMinLDforAST1(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcBaseAS_TCA1:
            vProcCap = model.vExProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
                    
        return vProcCap <= model.vExProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] * 0.5

    setattr(model, "conProcDispMinLDforAST1Test_TCD_TS", \
            pe.Constraint(model.setProcBaseDisp_TCD, model.setTSRT_TS, rule = ruleProcDispMinLDforAST1))


    ### ---------- storage units ------------------------
    # storage unit - overall provision bounded by derated capacity
    def ruleProcStorAllCapOut(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcStorPwOutTest_TCS_TS[sProcStor, sTimeSlice] 
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor]

    setattr(model, "conProcStorAllCapOutTest_TCD_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTSRT_TS, rule = ruleProcStorAllCapOut))

    # storage unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by 50% of derated capacity, considering its operation
    def ruleProcStorASOutLimit(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        if sProcStor in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= (model.pExProcStorCap_TCS[sProcStor] * model.pExProcStorEAF_TCS[sProcStor] * 0.5)

    setattr(model, "conProcStorASOutLimitTest_TCD_TS", \
            pe.Constraint(model.setProcBaseStor_TCS, model.setTSRT_TS, rule = ruleProcStorASOutLimit))


    ### ---------- hydropower ------------------------
    # hydropower limit - overall provision bounded by derated capacity
    def ruleProcHydrAllCapOut(model, sProcHydro, sTimeSlice) :
        
        vProcCap = 0  
        vProcCap = vProcCap + model.vExProcHydrPwOutTest_TCH_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.pExProcHydrCap_TCH[sProcHydro] * model.pExProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrAllCapOutTest_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTSRT_TS, rule = ruleProcHydrAllCapOut))

    # hydropower unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by instantaneous output (same volume)
    def ruleProcHydrASOutLimit(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        if sProcHydro in model.setProcBaseAS_TCA1:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcBaseAS_TCA2:
            vProcCap = vProcCap + model.vExProcASProvTest_TCA2_TS[sProcHydro, sTimeSlice]

        if model.pNewProcHydrCFTest_TCH_TS[sProcHydro, sTimeSlice] < 0.1:
            return vProcCap == 0
        else:
            return vProcCap <= model.vExProcHydrPwOutTest_TCH_TS[sProcHydro, sTimeSlice] * model.pExProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrASOutLimitTest_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTSRT_TS, rule = ruleProcHydrASOutLimit))

    return


##### ---- ancillary services from new units -------------------------- #####
    
def constZonalAncillaryService_New(model, objMarket):
    ''' ancillary services constraints on new processes '''
    
    ### upper bound limited by ramp rate * capacity
    def ruleProcASProvT1New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProv_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProv_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS[sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProv_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNew_TCA1_TS", \
            pe.Constraint(model.setProcNewAS_TCA1, model.setTimeSlice_TS, rule = ruleProcASProvT1New))
    
    
    def ruleProcASProvT2New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProv_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProv_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS[sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProv_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNew_TCA2_TS", \
            pe.Constraint(model.setProcNewAS_TCA2, model.setTimeSlice_TS, rule = ruleProcASProvT2New))
    
    
    def ruleProcASProvT3New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProv_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProv_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS[sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProv_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNew_TCA3_TS", \
            pe.Constraint(model.setProcNewAS_TCA3, model.setTimeSlice_TS, rule = ruleProcASProvT3New))


    ### ---------- dispatchable units ------------------------
    # dispatchable units - overall provision bounded by derated capacity
    def ruleProcDispAllCapOut(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcNewAS_TCA3:
            vProcCap = vProcCap + model.vNewProcASProv_TCA3_TS[sProcDisp, sTimeSlice]
            
        return vProcCap <= model.vNewProcDispCap_TCD[sProcDisp] * model.pNewProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispAllCapOutNew_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispAllCapOut))

    # dispatchable units - ensure spinning state (skip for OGCT and Oil)
    def ruleProcDispMinLDforAS(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcNewAS_TCA3:
            vProcCap = vProcCap + model.vNewProcASProv_TCA3_TS[sProcDisp, sTimeSlice]
            
        # if the process is fast start up gas or oil units, can be non-spinning reserve
        if "GAS_OCGT" in sProcDisp or "OIL_ST" in sProcDisp:
            return pe.Constraint.Skip
        else:
            # ensure spinning state, and assume the min load is around 33%
            return vProcCap <= model.vNewProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] * 2

    setattr(model, "conProcDispMinLDforASNew_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispMinLDforAS))


    # dispatchable units - ensure spinning state for T1 AS
    def ruleProcDispMinLDforAST1(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = model.vNewProcASProv_TCA1_TS[sProcDisp, sTimeSlice]
                    
        return vProcCap <= model.vNewProcDispPwOutGrs_TCD_TS[sProcDisp, sTimeSlice] * 0.5

    setattr(model, "conProcDispMinLDforAST1New_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTimeSlice_TS, rule = ruleProcDispMinLDforAST1))


    ### ---------- storage units ------------------------
    # storage unit - overall provision bounded by derated capacity
    def ruleProcStorAllCapOut(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcStorPwOut_TCS_TS[sProcStor, sTimeSlice] 
        if sProcStor in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor]

    setattr(model, "conProcStorAllCapOutNew_TCD_TS", \
            pe.Constraint(model.setProcNewStor_TCS, model.setTimeSlice_TS, rule = ruleProcStorAllCapOut))

    # storage unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by 50% of derated capacity, considering its operation
    def ruleProcStorASOutLimit(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        if sProcStor in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= (model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor] * 0.5)

    setattr(model, "conProcStorASOutLimitNew_TCD_TS", \
            pe.Constraint(model.setProcNewStor_TCS, model.setTimeSlice_TS, rule = ruleProcStorASOutLimit))


    ### ---------- hydropower ------------------------
    # hydropower limit - overall provision bounded by derated capacity
    def ruleProcHydrAllCapOut(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.vNewProcHydrCap_TCH[sProcHydro] * model.pNewProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrAllCapOutNew_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleProcHydrAllCapOut))

    # hydropower unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by instantaneous output (same volume)
    def ruleProcHydrASOutLimit(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        if sProcHydro in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProv_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProv_TCA2_TS[sProcHydro, sTimeSlice]

        if model.pNewProcHydrCF_TCH_TS[sProcHydro, sTimeSlice] < 0.1:
            return vProcCap == 0
        else:
            return vProcCap <= model.vNewProcHydrPwOut_TCH_TS[sProcHydro, sTimeSlice] \
                * model.pNewProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrASOutLimitNew_TCH_TS", \
            pe.Constraint(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, rule = ruleProcHydrASOutLimit))

    return


##### ---- ancillary services new units (Testing TS) ---------------- #####
    
def constZonalAS_New_RT(model, objMarket):
    ''' ancillary services constraints on new processes in testing TS'''
    
    ### upper bound limited by ramp rate * capacity
    def ruleProcASProvT1New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProvTest_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProvTest_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS[sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProvTest_TCA1_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA1[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNewTest_TCA1_TS", \
            pe.Constraint(model.setProcNewAS_TCA1, model.setTSRT_TS, rule = ruleProcASProvT1New))
    
    
    def ruleProcASProvT2New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProvTest_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProvTest_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS[sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProvTest_TCA2_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA2[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNewTest_TCA2_TS", \
            pe.Constraint(model.setProcNewAS_TCA2, model.setTSRT_TS, rule = ruleProcASProvT2New))
    
    
    def ruleProcASProvT3New(model, sProc, sTimeSlice) :
        
        if sProc in model.setProcNewDisp_TCD:
            return model.vNewProcASProvTest_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcDispCap_TCD[sProc] * model.pNewProcDispEAF_TCD[sProc]
        elif sProc in model.setProcNewStor_TCS:
            return model.vNewProcASProvTest_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcStorCap_TCS[sProc] * model.pNewProcStorEAF_TCS [sProc]
        elif sProc in model.setProcNewHydr_TCH:
            return model.vNewProcASProvTest_TCA3_TS[sProc, sTimeSlice] \
                <= model.pNewProcMaxAS_TCA3[sProc] * model.vNewProcHydrCap_TCH[sProc] * model.pNewProcHydrEAF_TCH[sProc]
        else:
            return pe.Constraint.Skip
        
    setattr(model, "conProcASProvNewTest_TCA3_TS", \
            pe.Constraint(model.setProcNewAS_TCA3, model.setTSRT_TS, rule = ruleProcASProvT3New))


    ### ---------- dispatchable units ------------------------
    # dispatchable units - overall provision bounded by derated capacity
    def ruleProcDispAllCapOut(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcNewAS_TCA3:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA3_TS[sProcDisp, sTimeSlice]
            
        return vProcCap <= model.vNewProcDispCap_TCD[sProcDisp] * model.pNewProcDispEAF_TCD[sProcDisp]

    setattr(model, "conProcDispAllCapOutNewTest_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTSRT_TS, rule = ruleProcDispAllCapOut))

    # dispatchable units - ensure spinning state (skip for OGCT and Oil)
    def ruleProcDispMinLDforAS(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
        
        if sProcDisp in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcDisp, sTimeSlice]
            
        if sProcDisp in model.setProcNewAS_TCA3:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA3_TS[sProcDisp, sTimeSlice]
            
        # if the process is fast start up gas or oil units, can be non-spinning reserve
        if "GAS_OCGT" in sProcDisp or "OIL_ST" in sProcDisp:
            return pe.Constraint.Skip
        else:
            # ensure spinning state, and assume the min load is around 33%
            return vProcCap <= model.vNewProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] * 2

    setattr(model, "conProcDispMinLDforASNewTest_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTSRT_TS, rule = ruleProcDispMinLDforAS))


    # dispatchable units - ensure spinning state for T1 AS
    def ruleProcDispMinLDforAST1(model, sProcDisp, sTimeSlice) :

        vProcCap = 0  
        
        if sProcDisp in model.setProcNewAS_TCA1:
            vProcCap = model.vNewProcASProvTest_TCA1_TS[sProcDisp, sTimeSlice]
                    
        return vProcCap <= model.vNewProcDispPwOutGrsTest_TCD_TS[sProcDisp, sTimeSlice] * 0.5

    setattr(model, "conProcDispMinLDforAST1NewTest_TCD_TS", \
            pe.Constraint(model.setProcNewDisp_TCD, model.setTSRT_TS, rule = ruleProcDispMinLDforAST1))


    ### ---------- storage units ------------------------
    # storage unit - overall provision bounded by derated capacity
    def ruleProcStorAllCapOut(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcStorPwOutTest_TCS_TS[sProcStor, sTimeSlice] 
        if sProcStor in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor]

    setattr(model, "conProcStorAllCapOutNewTest_TCD_TS", \
            pe.Constraint(model.setProcNewStor_TCS, model.setTSRT_TS, rule = ruleProcStorAllCapOut))

    # storage unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by 50% of derated capacity, considering its operation
    def ruleProcStorASOutLimit(model, sProcStor, sTimeSlice) :

        vProcCap = 0  
        if sProcStor in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcStor, sTimeSlice]
        if sProcStor in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcStor, sTimeSlice]

        return vProcCap <= (model.vNewProcStorCap_TCS[sProcStor] * model.pNewProcStorEAF_TCS[sProcStor] * 0.5)

    setattr(model, "conProcStorASOutLimitNewTest_TCD_TS", \
            pe.Constraint(model.setProcNewStor_TCS, model.setTSRT_TS, rule = ruleProcStorASOutLimit))


    ### ---------- hydropower ------------------------
    # hydropower limit - overall provision bounded by derated capacity
    def ruleProcHydrAllCapOut(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        vProcCap = vProcCap + model.vNewProcHydrPwOutTest_TCH_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcHydro, sTimeSlice]

        return vProcCap <= model.vNewProcHydrCap_TCH[sProcHydro] * model.pNewProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrAllCapOutNewTest_TCH_TS", \
            pe.Constraint(model.setProcNewHydr_TCH, model.setTSRT_TS, rule = ruleProcHydrAllCapOut))

    # hydropower unit - instantaneous provision bounded by instantaneous output
    # overall provision bounded by instantaneous output (same volume)
    def ruleProcHydrASOutLimit(model, sProcHydro, sTimeSlice) :

        vProcCap = 0  
        if sProcHydro in model.setProcNewAS_TCA1:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA1_TS[sProcHydro, sTimeSlice]
        if sProcHydro in model.setProcNewAS_TCA2:
            vProcCap = vProcCap + model.vNewProcASProvTest_TCA2_TS[sProcHydro, sTimeSlice]
            
        if model.pNewProcHydrCFTest_TCH_TS[sProcHydro, sTimeSlice] < 0.1:
            return vProcCap == 0
        else:
            return vProcCap <= model.vNewProcHydrPwOutTest_TCH_TS[sProcHydro, sTimeSlice] \
                * model.pNewProcHydrEAF_TCH[sProcHydro]

    setattr(model, "conProcHydrASOutLimitNewTest_TCH_TS", \
            pe.Constraint(model.setProcNewHydr_TCH, model.setTSRT_TS, rule = ruleProcHydrASOutLimit))

    return

