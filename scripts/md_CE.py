#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Main function of constructing CE model
#

import pyomo.environ as pe

import md_init_ins
import md_init_zone
import md_CE_formula
import md_CE_formula_AS
import md_CE_output
import md_preload


#------------------------------------------------------------------------------------------
# model capacity expansion
#------------------------------------------------------------------------------------------
    
def model_CE(instance, objMarket, ind_year):
    ''' main functino of the capacity expansion model '''

    # create pyomo model
    model = pe.ConcreteModel()

    # convert sets in the model
    _convertSets_CE(model, instance, objMarket)
    _convertSets_RT(model, instance, objMarket)
    
    # convert parameters in the model
    _convertParameters_CE(model, instance, objMarket, ind_year)
    _convertParameters_RT(model, instance, objMarket, ind_year)

    # define model main variables
    _mainVariables_CE(model, instance, objMarket)
    _mainVariables_RT(model, instance, objMarket)
    
    # constraints and objective function
    _formulation_CE(model, instance, objMarket, ind_year)

    ### solve the LP problem  
    if instance.sSolver == "gams":
        opt = pe.SolverFactory(instance.sSolver, solver_io='direct')
        
        # set pyomo options
        for sDicKey in instance.dicPyomoOption:
            opt.options[sDicKey] = instance.dicPyomoOption[sDicKey]
        
        # set solver options
        lsSolverOption  = []
        for sDicKey in instance.dicSolverOption:
            lsSolverOption.append( sDicKey + " = " + instance.dicSolverOption[sDicKey] + ";" ) 
        opt.options['add_options'] = lsSolverOption
    
    else:
        opt = pe.SolverFactory(instance.sSolver)
   
    results = opt.solve(model)
    #results.write()
    
    # model results
    sModelStatus = _modelResult_CE(model, results, instance, objMarket, ind_year)
    
    # update variables (add new capacity to process list)
    md_preload.updateNewBuildCapacity(instance, objMarket, model, ind_year)

    return sModelStatus


def _convertSets_CE(model, instance, objMarket):
    ''' create CE model sets '''
    
    # all time slice for CE modelling
    model.setTimeSlice_TS = pe.Set(initialize = [ objTS.sTSIndex for objTS in instance.lsTimeSlice_CEP ], ordered=True)
    # days
    model.setDay_DY = pe.Set(initialize = [ objDayTS.MonthDay for objDayTS in instance.lsDayTimeSlice_CEP ], ordered=True)

    # countries code in the market
    model.setCountryCode_CN = pe.Set(initialize = md_init_ins.getCountryCodeList(objMarket), ordered=True)
    # general dispatchalbe processes (for fixed new build constraints)
    model.setDispatchableProc = pe.Set(initialize = [ objProcDef.sProcessName for objProcDef in instance.lsProcessDefObjs \
                                                     if objProcDef.sOperationMode == "Dispatch" ], ordered=True)
    # general renewable processes
    model.setRenewableType = pe.Set(initialize = [ "WND_ON", "WND_OFF", "PV", "CSP", "HYD", "GEO_hydro", "BIO_ST" ], ordered=True)
    
    # all non-dispatchable processes (for model CP 2040 scenario)
    model.setMCPRenewProc = pe.Set(initialize = [ objProcDef.sProcessName for objProcDef in instance.lsProcessDefObjs \
                                                     if objProcDef.sOperationMode == "NonDispatch" ], ordered=True)
    
    # land zones in the market
    model.setLDZone_ZNL = pe.Set(initialize = [ objZone.sZoneID for objZone in objMarket.lsZone ], ordered=True)
    # offshore zones in the market
    model.setOFZone_ZNF = pe.Set(initialize = [ objZone.sZoneID for objZone in objMarket.lsZoneOffs ], ordered=True)
    
    # main commodity
    model.setComMain_CM = pe.Set(initialize = [ objComm.sCommodityName for objComm in instance.lsCommodity ], ordered=True)
        
    ##### all process of the same type merged
    # existing dispatchable process
    model.setProcBaseDisp_TCD = pe.Set(initialize = objMarket.setProcBaseDisp_TCD, ordered=True)    
    # existing storage process (pump hydro storage)
    model.setProcBaseStor_TCS = pe.Set(initialize = objMarket.setProcBaseStor_TCS, ordered=True)
    # existing hydropower process
    model.setProcBaseHydr_TCH = pe.Set(initialize = objMarket.setProcBaseHydr_TCH, ordered=True)  
    
    # existing process providing AS (all existing process merged for base year)
    model.setProcBaseAS_TCA1 = pe.Set(initialize = objMarket.setProcBaseAS_TCA1, ordered=True)  
    model.setProcBaseAS_TCA2 = pe.Set(initialize = objMarket.setProcBaseAS_TCA2, ordered=True)  
    model.setProcBaseAS_TCA3 = pe.Set(initialize = objMarket.setProcBaseAS_TCA3, ordered=True)  
    
    ##### new candidate process #####
    # new dispatchable process
    model.setProcNewDisp_TCD = pe.Set(initialize = objMarket.setProcNewDisp_TCD, ordered=True)    
    # new storage process (pump hydro storage)
    model.setProcNewStor_TCS = pe.Set(initialize = objMarket.setProcNewStor_TCS, ordered=True)
    # new hydropower process
    model.setProcNewHydr_TCH = pe.Set(initialize = objMarket.setProcNewHydr_TCH, ordered=True)  
    # new renewable process
    model.setProcNewRE_TCR = pe.Set(initialize = objMarket.setProcNewRE_TCR, ordered=True)
    # new renewable process - offshore
    model.setProcNewRE_Offs_TCR = pe.Set(initialize = objMarket.setProcNewRE_Offs_TCR, ordered=True) 
    
    # new process providing AS (all existing process merged for base year)
    model.setProcNewAS_TCA1 = pe.Set(initialize = objMarket.setProcNewAS_TCA1, ordered=True)  
    model.setProcNewAS_TCA2 = pe.Set(initialize = objMarket.setProcNewAS_TCA2, ordered=True)  
    model.setProcNewAS_TCA3 = pe.Set(initialize = objMarket.setProcNewAS_TCA3, ordered=True) 
    
    # transmissions between terrestrial zones
    model.setTransLDZ_TRL = pe.Set(initialize = objMarket.setTransLDZ_TRL, ordered=True)  
    # transmissions from offshore zones to terrestrial zones
    model.setTransOFZ_TRF = pe.Set(initialize = objMarket.setTransOFZ_TRF, ordered=True)  
    
    return


def _convertSets_RT(model, instance, objMarket):
    ''' create additional set on testing times slices in ED model '''
    
    # time slice for reliatiliby test cases (0-11)
    model.setTSRT_TS = pe.Set(initialize = [ str(iTS) for iTS in range(0,12) ], ordered=True)
    
    return


def _convertParameters_CE(model, instance, objMarket, ind_year):
    ''' create CE model parameters '''

    iYear = instance.iAllYearSteps_YS[ind_year]
    
    #----------------------------------------------------
    # Fixed Parameters

    # list of zones in a country
    model.pZonesInCountry_CN = pe.Param(model.setCountryCode_CN, \
            initialize = md_init_ins.getZonesInCountry(objMarket, model), within=pe.Any)
    
    # timeslice representing hours in a year
    model.pTSRepHourYear_TS = pe.Param(model.setTimeSlice_TS, \
            initialize = md_init_ins.getTSRepHourYear_CE(instance, model))
    # timeslice representing hours in a day
    model.pTSRepHourDay_TS = pe.Param(model.setTimeSlice_TS, \
            initialize = md_init_ins.getTSRepHourDay_CE(instance, model))
    # TSID in day 
    model.pTSIndInDay_DY = pe.Param(model.setDay_DY, \
            initialize = md_init_ins.getTSIndInDay_CE(instance, model), within=pe.Any)

    # demand profile
    model.pDemand_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.get_DemandProfile(model, objMarket, ind_year))
        
    # zonal non-dispatchable renewable output, only existing process (all renewables exclude hydropower)
    model.pNonDispGen_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getNonDispGen_ZNL_Day(model, objMarket, iYear))
    model.pNonDispGen_ZNF_TS = pe.Param(model.setOFZone_ZNF, model.setTimeSlice_TS, \
            initialize = md_init_zone.getNonDispGen_ZNF_Day(model, objMarket, iYear))
    
    # zonal AS requirements
    model.pASReqT1_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq(model, instance, objMarket, "T1", ind_year))
    model.pASReqT2_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq(model, instance, objMarket, "T2", ind_year))
    model.pASReqT3_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq(model, instance, objMarket, "T3", ind_year))

    # country biomass supply
    model.pBiomassSupply_CN = pe.Param(model.setCountryCode_CN, \
            initialize = objMarket.dicBiomassSupply_CN)

    #----------------------------------------------------
    # Technology Dependent Parameters - existing process
    
    # dispatchable process capacity
    model.pExProcDispCap_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "Cap", iYear))
    # dispatchable process capacity
    model.pExProcDispOUS_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "OUS", iYear))
    # dispatchable process conversion efficiency of dispatchable technologies
    model.pExProcDispEff_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "Eff", iYear))
    # dispatchable process equivalent available factor
    model.pExProcDispEAF_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "EAF", iYear))
    # dispatchable process minimal load
    model.pExProcDispMinLD_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "MLD", iYear))
    # dispatchable CCS capture rate
    model.pExProcDispCCSCapRate_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "CCS", iYear))
    # dispatchable process variable O&M cost
    model.pExProcVarOMCost_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "varOM", iYear))
    # dispatchable variable generation cost (USD/kWh)
    model.pExProcDispVGC_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcVarGenCost(instance, objMarket, model, ind_year))
    # base year annual average CF
    model.pExProcBaseGenCF_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamBaseCF_Year(objMarket, model))
    
    # storage process capacity
    model.pExProcStorCap_TCS = pe.Param(model.setProcBaseStor_TCS, \
            initialize = md_init_zone.getProcParamStor(objMarket, model, "Cap", iYear))
    # storage process efficiency
    model.pExProcStorEff_TCS = pe.Param(model.setProcBaseStor_TCS, \
            initialize = md_init_zone.getProcParamStor(objMarket, model, "Eff", iYear))
    # storage process duration
    model.pExProcStorDur_TCS = pe.Param(model.setProcBaseStor_TCS, \
            initialize = md_init_zone.getProcParamStor(objMarket, model, "Dur", iYear))
    # storage process equivalent available factor
    model.pExProcStorEAF_TCS = pe.Param(model.setProcBaseStor_TCS, \
            initialize = md_init_zone.getProcParamStor(objMarket, model, "EAF", iYear))
    
    # hydropower capacity
    model.pExProcHydrCap_TCH = pe.Param(model.setProcBaseHydr_TCH, \
            initialize = md_init_zone.getProcParamHydro(objMarket, model, "Cap", iYear))
    # hydropower equivalent available factor
    model.pExProcHydrEAF_TCH = pe.Param(model.setProcBaseHydr_TCH, \
            initialize = md_init_zone.getProcParamHydro(objMarket, model, "EAF", iYear))
    # hydropower default power output (MW, condisers EAF)
    model.pExProcHydrGen_TCH_TS = pe.Param(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, \
            initialize = md_init_zone.getProcHydroGen_CE(model, instance, objMarket, iYear))
    
    # existing renewable generation are all aggregated 
    
    # max ramping capability (derated capability) (MW)
    model.pExProcMaxAS_TCA1 = pe.Param(model.setProcBaseAS_TCA1, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T1", iYear))
    model.pExProcMaxAS_TCA2 = pe.Param(model.setProcBaseAS_TCA2, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T2", iYear))
    model.pExProcMaxAS_TCA3 = pe.Param(model.setProcBaseAS_TCA3, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T3", iYear))

    #----------------------------------------------------
    # Technology Dependent Parameters - new candidate process
    
    # dispatchable process capacity
    model.pNewProcDispOUS_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "OUS", ind_year))
    # dispatchable process conversion efficiency of dispatchable technologies
    model.pNewProcDispEff_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "Eff", ind_year))
    # dispatchable process equivalent available factor
    model.pNewProcDispEAF_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "EAF", ind_year))
    # dispatchable process minimal load
    model.pNewProcDispMinLD_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "MLD", ind_year))
    # dispatchable CCS capture rate
    model.pNewProcDispCCSCapRate_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "CCS", ind_year))
    # dispatchable process variable O&M cost
    model.pNewProcVarOMCost_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp_New(objMarket, model, "varOM", ind_year))
    # dispatchable fixed annual cost (M.USD / yr.MW)
    model.pNewProcFixAnnCost_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcFixAnnCost_New(objMarket, model, model.setProcNewDisp_TCD, ind_year))
    # dispatchable variable generation cost (USD/kWh)
    model.pNewProcDispVGC_TCD = pe.Param(model.setProcNewDisp_TCD, \
            initialize = md_init_zone.getProcVarGenCost_New(instance, objMarket, model, ind_year))
    
    # storage process efficiency
    model.pNewProcStorEff_TCS = pe.Param(model.setProcNewStor_TCS, \
            initialize = md_init_zone.getProcParamStor_New(objMarket, model, "Eff", ind_year))
    # storage process duration
    model.pNewProcStorDur_TCS = pe.Param(model.setProcNewStor_TCS, \
            initialize = md_init_zone.getProcParamStor_New(objMarket, model, "Dur", ind_year))
    # storage process equivalent available factor
    model.pNewProcStorEAF_TCS = pe.Param(model.setProcNewStor_TCS, \
            initialize = md_init_zone.getProcParamStor_New(objMarket, model, "EAF", ind_year))
    # hydropower available new build capacity (MW)
    model.pNewProcStorCapLim_TCS = pe.Param(model.setProcNewStor_TCS, \
            initialize = md_init_zone.getProcStorCapLim_New(objMarket, model, iYear))
    # fixed annual cost (M.USD / yr.MW)
    model.pNewProcFixAnnCost_TCS = pe.Param(model.setProcNewStor_TCS, \
            initialize = md_init_zone.getProcFixAnnCost_New(objMarket, model, model.setProcNewStor_TCS, ind_year))
    
    # hydropower equivalent available factor
    model.pNewProcHydrEAF_TCH = pe.Param(model.setProcNewHydr_TCH, \
            initialize = md_init_zone.getProcParamHydro_New(objMarket, model, "EAF", ind_year))
    # hydropower default CF
    model.pNewProcHydrCF_TCH_TS = pe.Param(model.setProcNewHydr_TCH, model.setTimeSlice_TS, \
            initialize = md_init_zone.getProcHydroCF_CE(model, instance, objMarket))    
    # hydropower available new build capacity (MW)
    model.pNewProcHydrCapLim_TCH = pe.Param(model.setProcNewHydr_TCH, \
            initialize = md_init_zone.getProcHydrCapLim_New(objMarket, model, iYear))
    # hydropower fixed annual cost (M.USD / yr.MW)
    model.pNewProcFixAnnCost_TCH = pe.Param(model.setProcNewHydr_TCH, \
            initialize = md_init_zone.getProcFixAnnCost_New(objMarket, model, model.setProcNewHydr_TCH, ind_year))

    # renewable default CF
    model.pNewProcRenDefCF_TCR_TS = pe.Param(model.setProcNewRE_TCR, model.setTimeSlice_TS, \
            initialize = md_init_zone.getProcRenDefCF_New(objMarket, model, iYear))
    # renewable available new build capacity (MW)
    model.pNewProcRenCapLim_TCR = pe.Param(model.setProcNewRE_TCR, \
            initialize = md_init_zone.getProcRenCapLim_New(objMarket, model, iYear))
    # renewable fixed annual cost (M.USD / yr.MW)  
    model.pNewProcFixAnnCost_TCR = pe.Param(model.setProcNewRE_TCR, \
            initialize = md_init_zone.getProcFixAnnCostRE_New(objMarket, model, ind_year))
    
    ##### offshore renewable
    # renewable default CF
    model.pNewProcRenDefCF_Offs_TCR = pe.Param(model.setProcNewRE_Offs_TCR, model.setTimeSlice_TS, \
            initialize = md_init_zone.getProcRenDefCF_Offs_New(objMarket, model, iYear))
    # renewable available new build capacity (MW)
    model.pNewProcRenCapLim_Offs_TCR = pe.Param(model.setProcNewRE_Offs_TCR, \
            initialize = md_init_zone.getProcRenCapLim_Offs_New(objMarket, model, iYear))
    # renewable fixed annual cost (M.USD / yr.MW)  
    model.pNewProcFixAnnCost_Offs_TCR = pe.Param(model.setProcNewRE_Offs_TCR, \
            initialize = md_init_zone.getProcFixAnnCostRE_Offs_New(objMarket, model, ind_year))
    
    # max ramping capability (derated capability) (% to total capacity)
    model.pNewProcMaxAS_TCA1 = pe.Param(model.setProcNewAS_TCA1, \
            initialize = md_init_zone.getProcASMax_New(objMarket, model, "T1", ind_year))
    model.pNewProcMaxAS_TCA2 = pe.Param(model.setProcNewAS_TCA2, \
            initialize = md_init_zone.getProcASMax_New(objMarket, model, "T2", ind_year))
    model.pNewProcMaxAS_TCA3 = pe.Param(model.setProcNewAS_TCA3, \
            initialize = md_init_zone.getProcASMax_New(objMarket, model, "T3", ind_year))
    
    #----------------------------------------------------
    # Transmission Dependent Parameters
    
    # transmission capacity
    model.pExTransLDZCap_TRL = pe.Param(model.setTransLDZ_TRL, \
            initialize = md_init_ins.getTransCapacity(model, objMarket, instance.iAllYearSteps_YS[ind_year-1]))
    model.pExTransOFZCap_TRF = pe.Param(model.setTransOFZ_TRF, \
            initialize = md_init_ins.getTransCapacityOffs(model, objMarket, instance.iAllYearSteps_YS[ind_year-1]))
    
    # trans-zone line loss (0-1)
    model.pTransLDZLoss_TRL = pe.Param(model.setTransLDZ_TRL, \
            initialize = md_init_ins.getTransLoss(model, objMarket, ind_year))
    # offshore to land line loss (0-1)
    model.pTransOFZLoss_TRF = pe.Param(model.setTransOFZ_TRF, \
            initialize = md_init_ins.getTransLossOffs(model, objMarket, ind_year))
    
    # terrestrial transmission cost per MW (M.USD)
    model.pTransLDZCost_TRL = pe.Param(model.setTransLDZ_TRL, \
            initialize = md_init_ins.getTransCost(model, objMarket, ind_year))
    # offshore transmission cost per MW (M.USD)
    model.pTransOFZCost_TRF = pe.Param(model.setTransOFZ_TRF, \
            initialize = md_init_ins.getTransCostOffs(model, objMarket, ind_year))
    
    return


def _convertParameters_RT(model, instance, objMarket, ind_year):
    ''' create CE model parameters for reliability test '''

    iYear = instance.iAllYearSteps_YS[ind_year]
    
    # demand profile of testing case
    model.pDemandTest_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTSRT_TS, \
            initialize = md_init_zone.get_DemandProfile_RT(model, objMarket))
    
    # zonal non-dispatchable renewable output, only existing process (all renewables exclude hydropower)
    model.pNonDispGenTest_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTSRT_TS, \
            initialize = md_init_zone.getNonDispGen_ZNL_RT(model, objMarket))
    model.pNonDispGenOffTest_ZNF_TS = pe.Param(model.setOFZone_ZNF, model.setTSRT_TS, \
            initialize = md_init_zone.getNonDispGenOff_ZNF_RT(model, objMarket))

    # zonal AS requirements
    model.pASReqT1Test_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTSRT_TS, \
            initialize = md_init_zone.getASReq_RT(model, instance, objMarket, "T1", ind_year))
    model.pASReqT2Test_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTSRT_TS, \
            initialize = md_init_zone.getASReq_RT(model, instance, objMarket, "T2", ind_year))
    model.pASReqT3Test_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTSRT_TS, \
            initialize = md_init_zone.getASReq_RT(model, instance, objMarket, "T3", ind_year))

    # hydropower default CF
    model.pNewProcHydrCFTest_TCH_TS = pe.Param(model.setProcNewHydr_TCH, model.setTSRT_TS, \
            initialize = md_init_zone.getProcHydroCFTest_CE(model, instance, objMarket)) 
    # renewable default CF
    model.pNewProcRenDefCFTest_TCR = pe.Param(model.setProcNewRE_TCR, model.setTSRT_TS, \
            initialize = md_init_zone.getProcRenDefCFTest_New(objMarket, model, iYear))
    # renewable default CF
    model.pNewProcRenDefCFTest_Offs_TCR = pe.Param(model.setProcNewRE_Offs_TCR, model.setTSRT_TS, \
            initialize = md_init_zone.getProcRenDefCFTest_Offs_New(objMarket, model, iYear))
    
    return



def _mainVariables_CE(model, instance, objMarket):
    ''' create CE model variables '''
    ### base CE time slice
    
    # zonal supply
    model.vSupplyZone_ZNL_TS = pe.Var(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vSupplyOffs_ZNF_TS = pe.Var(model.setOFZone_ZNF, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # spilled energy
    model.vSpillZone_ZNL_TS = pe.Var(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vSpillOffs_ZNF_TS = pe.Var(model.setOFZone_ZNF, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # transmission (MW)
    model.vTransLDZIn_TRL_TS = pe.Var(model.setTransLDZ_TRL, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransLDZOut_TRL_TS = pe.Var(model.setTransLDZ_TRL, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransOFZIn_TRF_TS = pe.Var(model.setTransOFZ_TRF, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransOFZOut_TRF_TS = pe.Var(model.setTransOFZ_TRF, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    ### generation from aggregated existing units (MW)
    
    # power output (MW)
    model.vExProcDispPwOutGrs_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcDispPwOutNet_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # storage input/output (MW)
    model.vExProcStorPwIn_TCS_TS = pe.Var(model.setProcBaseStor_TCS, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcStorPwOut_TCS_TS = pe.Var(model.setProcBaseStor_TCS, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # hydropower output (MW)
    model.vExProcHydrPwOut_TCH_TS = pe.Var(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # capacity reserve for ancillary service (MW)
    model.vExProcASProv_TCA1_TS = pe.Var(model.setProcBaseAS_TCA1, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcASProv_TCA2_TS = pe.Var(model.setProcBaseAS_TCA2, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcASProv_TCA3_TS = pe.Var(model.setProcBaseAS_TCA3, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    ### new candidate units ### --------------------
    
    # new install capacity (MW)
    model.vNewProcDispCap_TCD = pe.Var(model.setProcNewDisp_TCD, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcStorCap_TCS = pe.Var(model.setProcNewStor_TCS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcHydrCap_TCH = pe.Var(model.setProcNewHydr_TCH, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcRenewCap_TCR = pe.Var(model.setProcNewRE_TCR, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcRenewCapOffs_TCR = pe.Var(model.setProcNewRE_Offs_TCR, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # power output (MW)
    model.vNewProcDispPwOutGrs_TCD_TS = pe.Var(model.setProcNewDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcDispPwOutNet_TCD_TS = pe.Var(model.setProcNewDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # storage input/output (MW)
    model.vNewProcStorPwIn_TCS_TS = pe.Var(model.setProcNewStor_TCS, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcStorPwOut_TCS_TS = pe.Var(model.setProcNewStor_TCS, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # hydropower output (MW)
    model.vNewProcHydrPwOut_TCH_TS = pe.Var(model.setProcNewHydr_TCH, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # renewable output (MW)
    model.vNewProcRenewPwOut_TCR_TS = pe.Var(model.setProcNewRE_TCR, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcRenewPwOutOffs_TCR_TS = pe.Var(model.setProcNewRE_Offs_TCR, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # capacity reserve for ancillary service (MW)
    model.vNewProcASProv_TCA1_TS = pe.Var(model.setProcNewAS_TCA1, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcASProv_TCA2_TS = pe.Var(model.setProcNewAS_TCA2, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcASProv_TCA3_TS = pe.Var(model.setProcNewAS_TCA3, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # transmission
    model.vNewProcTransCap_TRL = pe.Var(model.setTransLDZ_TRL, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcTransOffCap_TRF = pe.Var(model.setTransOFZ_TRF, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    return


def _mainVariables_RT(model, instance, objMarket):
    ''' create CE model variables for reliability test '''
    ###   testing case time slice

    # zonal supply
    model.vSupplyZoneTest_ZNL_TS = pe.Var(model.setLDZone_ZNL, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vSupplyOffsTest_ZNF_TS = pe.Var(model.setOFZone_ZNF, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # spilled energy
    model.vSpillZoneTest_ZNL_TS = pe.Var(model.setLDZone_ZNL, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vSpillOffsTest_ZNF_TS = pe.Var(model.setOFZone_ZNF, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # transmission (MW)
    model.vTransLDZInTest_TRL_TS = pe.Var(model.setTransLDZ_TRL, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransLDZOutTest_TRL_TS = pe.Var(model.setTransLDZ_TRL, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransOFZInTest_TRF_TS = pe.Var(model.setTransOFZ_TRF, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vTransOFZOutTest_TRF_TS = pe.Var(model.setTransOFZ_TRF, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    ### generation from aggregated existing units (MW)
    
    # power output (MW)
    model.vExProcDispPwOutGrsTest_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcDispPwOutNetTest_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # storage output (MW)
    model.vExProcStorPwOutTest_TCS_TS = pe.Var(model.setProcBaseStor_TCS, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # hydropower output (MW)
    model.vExProcHydrPwOutTest_TCH_TS = pe.Var(model.setProcBaseHydr_TCH, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # capacity reserve for ancillary service (MW)
    model.vExProcASProvTest_TCA1_TS = pe.Var(model.setProcBaseAS_TCA1, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcASProvTest_TCA2_TS = pe.Var(model.setProcBaseAS_TCA2, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcASProvTest_TCA3_TS = pe.Var(model.setProcBaseAS_TCA3, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    ### new candidate units ### --------------------
    
    # power output (MW)
    model.vNewProcDispPwOutGrsTest_TCD_TS = pe.Var(model.setProcNewDisp_TCD, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcDispPwOutNetTest_TCD_TS = pe.Var(model.setProcNewDisp_TCD, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # storage output (MW)
    model.vNewProcStorPwOutTest_TCS_TS = pe.Var(model.setProcNewStor_TCS, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # hydropower output (MW)
    model.vNewProcHydrPwOutTest_TCH_TS = pe.Var(model.setProcNewHydr_TCH, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    # renewable output (MW)
    model.vNewProcRenewPwOutTest_TCR_TS = pe.Var(model.setProcNewRE_TCR, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcRenewPwOutOffsTest_TCR_TS = pe.Var(model.setProcNewRE_Offs_TCR, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # capacity reserve for ancillary service (MW)
    model.vNewProcASProvTest_TCA1_TS = pe.Var(model.setProcNewAS_TCA1, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcASProvTest_TCA2_TS = pe.Var(model.setProcNewAS_TCA2, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vNewProcASProvTest_TCA3_TS = pe.Var(model.setProcNewAS_TCA3, model.setTSRT_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))

    return


def _formulation_CE(model, instance, objMarket, ind_year):
    ''' create CE model constraints and objective function '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    # unit dispatch constraints
    md_CE_formula.constUnitGen_Exist(model, objMarket)
    md_CE_formula.constUnitGen_New(model, objMarket)
    
    # storage operation constraints
    md_CE_formula.constStorageOpr_Exist(model, objMarket)
    md_CE_formula.constStorageOpr_New(model, objMarket)
    
    # hydropower dispatch
    md_CE_formula.constHydropowerOpr_Exist(model, objMarket)
    md_CE_formula.constHydropowerOpr_New(model, objMarket)
    
    # renewables
    md_CE_formula.constRenewGen_New(model, objMarket)
    
    # power balance constraints
    md_CE_formula.constPowerBalance(model, objMarket)
    
    # transmission constraints
    md_CE_formula.constTransOpr(model, objMarket)
    
    # ancillary service
    md_CE_formula_AS.constZonalAncillaryService_Zone(model, objMarket)
    md_CE_formula_AS.constZonalAncillaryService_Ex(model, objMarket)
    md_CE_formula_AS.constZonalAncillaryService_New(model, objMarket)

    # minimal genetation of dispatchable units, percentage of base year CF (except for biomass)
    if ind_year < len( instance.iMinExistUnitCF ):
        md_CE_formula.constMinBaseUnitGen(model, objMarket, instance.iMinExistUnitCF[ind_year])

    # max biomass supply limit
    md_CE_formula.constMaxBiomassSupply(model, objMarket)

    # fixed new installation of dispatchable units (CCS, Nuclear)
    md_CE_formula.constFixedNewBuildDisp(instance, model, iYear)
    
    # renewable minimum installation
    if ind_year >= 1 and instance.sPathway != "MCP":
        md_CE_formula.constRenewAddMax(model, instance, objMarket)
        md_CE_formula.constRenewAddMin(model, instance, objMarket)
    
    # hydropwoer capacity limit (applied after 2020)
    if ind_year >= 1:
        md_CE_formula.constHydroCapLimit(model, instance)

    # Model CP 70% renewable pathway (skip hydropower limit)
    if ind_year > 1 and instance.sPathway == "MCP":
        md_CE_formula.constMCP70RenewPathway(model, objMarket, ind_year, iYear)

    # carbon neutral scenario
    if ind_year > 1 and instance.sPathway == "CNS":
        md_CE_formula.constCNSEmissionCap(instance, model, objMarket, ind_year, iYear)
        
    # new renewable growth 25% of all demand per period (include hydro and biomass)
    if ind_year > 1:
        md_CE_formula.constNewRenewLimit(model, instance, objMarket, ind_year)

    # minimal biomass capacity (exclude BECCS)
    if ind_year > 1:
        md_CE_formula.constBioMassCapFloor(model, instance, objMarket)
    
    #### Testing TS cases --------------------
    # unit dispatch constraints    
    md_CE_formula.constUnitGen_Exist_RT(model, objMarket)
    md_CE_formula.constUnitGen_New_RT(model, objMarket)
    
    # storage operation constraints
    md_CE_formula.constStorageOpr_Exist_RT(model, objMarket)
    md_CE_formula.constStorageOpr_New_RT(model, objMarket)
    
    # hydropower dispatch
    md_CE_formula.constHydropowerOpr_Exist_RT(model, objMarket)
    md_CE_formula.constHydropowerOpr_New_RT(model, objMarket)

    # renewables
    md_CE_formula.constRenewGen_New_RT(model, objMarket)
    
    # power balance constraints
    md_CE_formula.constPowerBalance_RT(model, objMarket)
    
    # transmission constraints
    md_CE_formula.constTransOpr_RT(model, objMarket)
    
    # ancillary service
    md_CE_formula_AS.constZonalAS_Zone_RT(model, objMarket)
    md_CE_formula_AS.constZonalAS_Ex_RT(model, objMarket)
    md_CE_formula_AS.constZonalAS_New_RT(model, objMarket)

    ##### objective function
    def TotalSystemCost(model) :
        
        ##### variable cost
        # minimize variable generation cost of existing process
        VarGenCost_Ex = 0
        for TechDisp in model.setProcBaseDisp_TCD:
            for sTS in model.setTimeSlice_TS:
                VarGenCost_Ex += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                    * model.pTSRepHourYear_TS[sTS] * model.pExProcDispVGC_TCD[TechDisp]  # MWh * USD/kWh
        
        VarGenCost_Ex = VarGenCost_Ex / 1000   # M.USD
        
        # import from outside the market
        ImportCost = 0
        for TransLine in model.setTransLDZ_TRL:
            if TransLine[0:2] == "ET":
                for sTS in model.setTimeSlice_TS:
                    ImportCost += (model.vTransLDZIn_TRL_TS[TransLine,sTS] \
                                   * model.pTSRepHourYear_TS[sTS] * instance.iImportPrice / 1000)  # M.USD

        # energy spill
        Spill = 0
        for sZone in model.setLDZone_ZNL:
            for sTS in model.setTimeSlice_TS:
                # energy spill 0.01 USD per kwh
                Spill += (model.vSpillZone_ZNL_TS[sZone,sTS] * model.pTSRepHourYear_TS[sTS] \
                          * instance.iSpillCost / 1000)  # M.USD

        ##### cost of new installation
        
        # variable cost of new installation units        
        VarGenCost_New = 0
        for TechDisp in model.setProcNewDisp_TCD:
            for sTS in model.setTimeSlice_TS:
                VarGenCost_New += model.vNewProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                    * model.pTSRepHourYear_TS[sTS] * model.pNewProcDispVGC_TCD[TechDisp]  # MWh * USD/kWh
        
        VarGenCost_New = VarGenCost_New / 1000   # M.USD        
        
        # dispatchable
        NewCap_Disp = 0
        for sProc in model.setProcNewDisp_TCD:
            NewCap_Disp = NewCap_Disp + (model.vNewProcDispCap_TCD[sProc] \
                                         * model.pNewProcFixAnnCost_TCD[sProc])
        
        # storage 
        NewCap_Stor = 0
        for sProc in model.setProcNewStor_TCS:
            NewCap_Stor = NewCap_Stor + (model.vNewProcStorCap_TCS[sProc] \
                                         * model.pNewProcFixAnnCost_TCS[sProc])
            
        # hydropower
        NewCap_Hydro = 0
        for sProc in model.setProcNewHydr_TCH:
            NewCap_Hydro = NewCap_Hydro + (model.vNewProcHydrCap_TCH[sProc] \
                                           * model.pNewProcFixAnnCost_TCH[sProc])
            
        # renewable
        NewCap_Renew = 0
        for sProc in model.setProcNewRE_TCR:
            NewCap_Renew = NewCap_Renew + (model.vNewProcRenewCap_TCR[sProc] \
                                           * model.pNewProcFixAnnCost_TCR[sProc])
            
        # offshore renewable
        NewCap_RenewOff = 0
        for sProc in model.setProcNewRE_Offs_TCR:
            NewCap_RenewOff = NewCap_RenewOff + (model.vNewProcRenewCapOffs_TCR[sProc] \
                                            * model.pNewProcFixAnnCost_Offs_TCR[sProc])
            
        # terrestrial transmission
        NewCap_Trans = 0
        for sProc in model.setTransLDZ_TRL:
            NewCap_Trans = NewCap_Trans + (model.vNewProcTransCap_TRL[sProc] \
                                           * model.pTransLDZCost_TRL[sProc])
            
        # offshore transmission
        NewCap_TransOff = 0
        for sProc in model.setTransOFZ_TRF:
            NewCap_TransOff = NewCap_TransOff + (model.vNewProcTransOffCap_TRF[sProc] \
                                                 * model.pTransOFZCost_TRF[sProc])
        
        return VarGenCost_Ex + ImportCost + Spill + VarGenCost_New + \
                + NewCap_Disp + NewCap_Stor + NewCap_Hydro + NewCap_Renew \
                + NewCap_RenewOff + NewCap_Trans + NewCap_TransOff

    # M.USD
    model.obj = pe.Objective( rule = TotalSystemCost, sense = pe.minimize )

    return


def _modelResult_CE(model, results, instance, objMarket, ind_year):
    ''' export CE model results '''

    iYear = instance.iAllYearSteps_YS[ind_year]    
    sModelStatus = ""    
    model.solutions.load_from(results) 

    if results.solver.termination_condition == pe.TerminationCondition.optimal or \
        results.solver.termination_condition == pe.TerminationCondition.feasible or \
        results.solver.termination_condition == pe.TerminationCondition.globallyOptimal :
        sModelStatus = "feasible"
        #print("global optimal")
    elif results.solver.termination_condition == pe.TerminationCondition.locallyOptimal or \
        results.solver.termination_condition == pe.TerminationCondition.maxIterations :
        sModelStatus = "feasible"
        #print("local optimal")
    else:
        sModelStatus = "infeasible or solver error"
        #print(" **** other condistions terminate **** ")
    
    #print( "obj value = ", float(pe.value(model.obj)) )
    
    ### update CE model output    
    if sModelStatus == "feasible":       
        directory = "../Output/" + objMarket.sMarket               
        md_CE_output.CE_output_processGen(model, instance, objMarket, directory, iYear)
        md_CE_output.CE_output_zoneBalance(model, instance, objMarket, directory, iYear)

    return sModelStatus

