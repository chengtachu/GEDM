#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Main function and process flow of the GEDM
#

from os import path, makedirs
from time import strftime, localtime
import pyomo.environ as pe

import md_init_ins
import md_init_zone
import md_preload
import md_ED_formula
import md_ED_output
import md_CE
import md_output

def main_function(instance, objMarket):
    ''' main function of model iteration control '''

    # path of output CSV files
    directory = "../Output/" + objMarket.sMarket   
    if not path.exists(directory):
        makedirs(directory)

    for ind_year, iYear in enumerate(instance.iAllYearSteps_YS):
        
        # construct the sets
        md_preload.initBaseSets(instance, objMarket, ind_year)
        
        # paramters init
        md_preload.ED_initVariables(instance, objMarket, ind_year)    
        
        bFeasible_ED = True
        for objDay in instance.lsDayTimeSlice:
            
            sModelStatus = _model_ED(instance, objMarket, ind_year, objDay)
            
            if sModelStatus == "feasible":
                print(strftime("%H:%M:%S", localtime()) + " " + \
                      objMarket.sMarket + " " + str(iYear) + " Day" \
                          + str(objDay.iDayIndex+1) + " ED optimal solution processed")
            else:
                bFeasible_ED = False
                print(strftime("%H:%M:%S", localtime()) + " " + \
                      objMarket.sMarket + " " + str(iYear) + " Day" \
                          + str(objDay.iDayIndex+1) + " ED problem **** infeasible ****")
                break
            
        if bFeasible_ED == True:
            # annual dispatch result update to dictionary
            md_ED_output.ED_output_AnnualInfo(instance, objMarket, ind_year)            
                
            # output results
            md_ED_output.ED_output_TotalCost(instance, objMarket, ind_year, directory)
            md_ED_output.ED_output_processGen(instance, objMarket, ind_year, directory)
            md_ED_output.ED_output_zoneBalance(instance, objMarket, ind_year, directory)
            md_ED_output.ED_output_zoneInfo(instance, objMarket, ind_year, directory)
    
            # output all annual market results by country (update when finish each YS)
            md_output.outputAllMarketResults(instance, objMarket, directory)            
        else:
            break

        ### capacity expansion for next year step --------------------
        if iYear != instance.iAllYearSteps_YS[-1]:
    
            # update testing case TS
            md_preload.updateTestTS(instance, objMarket, ind_year+1)

            # define sets                
            md_preload.initBaseSets(instance, objMarket, ind_year+1)
            md_preload.initNewSets(instance, objMarket, ind_year+1)
            
            # modelling paramters init
            md_preload.CE_initVariables(instance, objMarket, ind_year+1)
            
            # initialize renewable installation limits
            md_preload.CE_initRenInstallLimits(instance, objMarket, ind_year+1)
            
            sModelStatus = md_CE.model_CE(instance, objMarket, ind_year+1)
            
            if sModelStatus == "feasible":
                print(strftime("%H:%M:%S", localtime()) + " " + \
                      objMarket.sMarket + " " + str(instance.iAllYearSteps_YS[ind_year+1]) \
                          + " CE optimal solution processed")
            else:
                print(strftime("%H:%M:%S", localtime()) + " " + \
                      objMarket.sMarket + " " + str(instance.iAllYearSteps_YS[ind_year+1]) \
                          + " CE problem **** infeasible ****")
                break
    
    return


#--------------------------------------------------------------------
# model economic dispatch
#--------------------------------------------------------------------

def _model_ED(instance, objMarket, ind_year, objDay):
    ''' main functino of the daily economic dispatch model '''

    # create pyomo model object
    model = pe.ConcreteModel()
    
    # convert sets in the model
    _convertSets_ED(model, instance, objMarket, objDay)
    
    # convert parameters in the model
    _convertParameters_ED(model, instance, objMarket, ind_year, objDay)

    # define model main variables
    _mainVariables_ED(model, instance, objMarket)

    # constraints and objective function
    _formulation_ED(model, instance, objMarket, ind_year)

    ### solve the LP problem
    opt = pe.SolverFactory(instance.sSolver, solver_io='direct')
    
    # set pyomo options
    for sDicKey in instance.dicPyomoOption:
        opt.options[sDicKey] = instance.dicPyomoOption[sDicKey]
    
    # set solver options
    lsSolverOption  = []
    for sDicKey in instance.dicSolverOption:
        lsSolverOption.append( sDicKey + " = " + instance.dicSolverOption[sDicKey] + ";" ) 
    opt.options['add_options'] = lsSolverOption
    
    # solving the problem
    results = opt.solve(model)
    #results.write()
    
    # process model results
    sModelStatus = _modelResult_ED(model, results, instance, objMarket, objDay)

    return sModelStatus


def _convertSets_ED(model, instance, objMarket, objDay):
    ''' create ED model sets '''

    # time slice of the day
    model.setTimeSlice_TS = pe.Set( \
            initialize = [ obDiurjTS.sTSIndex for obDiurjTS in objDay.lsDiurnalTS ], ordered=True)

    # countries code in the market
    model.setCountryCode_CN = pe.Set( \
            initialize = md_init_ins.getCountryCodeList(objMarket), ordered=True)
    
    # land zones in the market
    model.setLDZone_ZNL = pe.Set( \
            initialize = [ objZone.sZoneID for objZone in objMarket.lsZone ], ordered=True)
    # offshore zones in the market
    model.setOFZone_ZNF = pe.Set( \
            initialize = [ objZone.sZoneID for objZone in objMarket.lsZoneOffs ], ordered=True)
    
    # main commodity
    model.setComMain_CM = pe.Set( \
            initialize = [ objComm.sCommodityName for objComm in instance.lsCommodity ], ordered=True)
    
    
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
    
    # transmissions between terrestrial zones
    model.setTransLDZ_TRL = pe.Set(initialize = objMarket.setTransLDZ_TRL, ordered=True)  
    # transmissions from offshore zones to terrestrial zones
    model.setTransOFZ_TRF = pe.Set(initialize = objMarket.setTransOFZ_TRF, ordered=True)  
    
    return


def _convertParameters_ED(model, instance, objMarket, ind_year, objDay):
    ''' create ED model parameters '''

    iYear = instance.iAllYearSteps_YS[ind_year]
    
    #----------------------------------------------------
    # Fixed Parameters

    # list of zones in a country
    model.pZonesInCountry_CN = pe.Param(model.setCountryCode_CN, \
            initialize = md_init_ins.getZonesInCountry(objMarket, model), within=pe.Any)
    
    # timeslice representing hours in a year
    model.pTSRepHourYear_TS = pe.Param(model.setTimeSlice_TS, \
            initialize = md_init_ins.getTSRepHourYear_Day(model, objDay))
    # timeslice representing hours in a day
    model.pTSRepHourDay_TS = pe.Param(model.setTimeSlice_TS, \
            initialize = md_init_ins.getTSRepHourDay_Day(model, objDay))

    # demand profile
    model.pDemand_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.get_DemandProfile_Day(model, objMarket, ind_year))
    
    # zonal non-dispatchable renewable output (all renewables exclude hydropower)
    model.pNonDispGen_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getNonDispGen_ZNL_Day(model, objMarket, iYear))
    model.pNonDispGen_ZNF_TS = pe.Param(model.setOFZone_ZNF, model.setTimeSlice_TS, \
            initialize = md_init_zone.getNonDispGen_ZNF_Day(model, objMarket, iYear))
    
    # zonal AS requirements
    model.pASReqT1_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq_day(model, instance, objMarket, "T1", ind_year))
    model.pASReqT2_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq_day(model, instance, objMarket, "T2", ind_year))
    model.pASReqT3_ZNL_TS = pe.Param(model.setLDZone_ZNL, model.setTimeSlice_TS, \
            initialize = md_init_zone.getASReq_day(model, instance, objMarket, "T3", ind_year))

    #----------------------------------------------------
    # Technology Dependent Parameters
    
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
    
    # CCS capture rate
    model.pExProcDispCCSCapRate_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "CCS", iYear))
    
    # dispatchable process variable O&M cost
    model.pExProcVarOMCost_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamDisp(objMarket, model, "varOM", iYear))
    
    # variable generation cost (USD/kWh)
    model.pExProcDispVGC_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcVarGenCost(instance, objMarket, model, ind_year))
    
    # base year month-day CF
    model.pExProcBaseGenCF_TCD = pe.Param(model.setProcBaseDisp_TCD, \
            initialize = md_init_zone.getProcParamBaseCF_Month(objMarket, model, objDay))
    
    # base year biomass generation (MWh)
    model.pExProcBaseBioGen_CN = pe.Param(model.setCountryCode_CN, \
            initialize = md_init_zone.getProcParamBaseBioGen_Month(objMarket, model, objDay, model.setCountryCode_CN))
    
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
    # default power output (MW, considers EAF)
    model.pExProcHydrGen_TCH_TS = pe.Param(model.setProcBaseHydr_TCH, model.setTimeSlice_TS, \
            initialize = md_init_zone.getProcHydroGen(model, instance, objMarket, iYear))
    
    # max ramping capability (derated capability)
    model.pExProcMaxAS_TCA1 = pe.Param(model.setProcBaseAS_TCA1, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T1", iYear))
    model.pExProcMaxAS_TCA2 = pe.Param(model.setProcBaseAS_TCA2, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T2", iYear))
    model.pExProcMaxAS_TCA3 = pe.Param(model.setProcBaseAS_TCA3, \
            initialize = md_init_zone.getProcASMax(objMarket, model, "T3", iYear))
    
    #----------------------------------------------------
    # Transmission Dependent Parameters
    
    # transmission capacity
    model.pTransLDZCap_TRL = pe.Param(model.setTransLDZ_TRL, \
            initialize = md_init_ins.getTransCapacity(model, objMarket, iYear))
    model.pTransOFZCap_TRF = pe.Param(model.setTransOFZ_TRF, \
            initialize = md_init_ins.getTransCapacityOffs(model, objMarket, iYear))
    
    # trans-zone line loss (0-1)
    model.pTransLDZLoss_TRL = pe.Param(model.setTransLDZ_TRL, \
            initialize = md_init_ins.getTransLoss(model, objMarket, ind_year))
    # offshore to land line loss (0-1)
    model.pTransOFZLoss_TRF = pe.Param(model.setTransOFZ_TRF, \
            initialize = md_init_ins.getTransLossOffs(model, objMarket, ind_year))
    
    return


def _mainVariables_ED(model, instance, objMarket):
    ''' create ED model variables '''

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
    
    ### generation from aggregated units (MW)
    
    # power output (MW)
    model.vExProcDispPwOutGrs_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    model.vExProcDispPwOutNet_TCD_TS = pe.Var(model.setProcBaseDisp_TCD, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    
    # storage input (MW)
    model.vExProcStorPwIn_TCS_TS = pe.Var(model.setProcBaseStor_TCS, model.setTimeSlice_TS, \
            domain=pe.NonNegativeReals, initialize=0, bounds=(0.0,None))
    # storage output (MW)
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

    return


def _formulation_ED(model, instance, objMarket, ind_year):
    ''' construct ED model constraints and objective function '''
    
    # unit dispatch constraints
    md_ED_formula.constUnitGen(model, objMarket)
    
    # storage operation constraints
    md_ED_formula.constStorageOpr(model, objMarket)
    
    # hydropower dispatch
    md_ED_formula.constHydropowerOpr(model, objMarket)
    
    # power balance constraints
    md_ED_formula.constPowerBalance(model, objMarket)
    
    # transmission constraints
    md_ED_formula.constTransOpr(model, objMarket)
    
    # ancillary service
    md_ED_formula.constZonalAncillaryService(model, objMarket)
    
    # minimal genetation of dispatchable units, percentage of base year CF (except for biomass)
    if ind_year < len( instance.iMinExistUnitCF ):
        md_ED_formula.constMinBaseUnitGen(model, objMarket, instance.iMinExistUnitCF[ind_year])
        
    # minimal genetation of dispatchable units, biomass (exclude BECCS)
    md_ED_formula.constMinBaseUnitGen_Bio(model, instance, objMarket)
    
    # emission cap for carbon neutral scenario
    if ind_year > 1 and instance.sPathway == "CNS":
        md_ED_formula.constCNSEmissionCap(instance, model, objMarket, ind_year)        
    
    ##### objective function
    def TotalSystemVarCost(model) :
        
        ### minimize variable generation cost
        GenCost = 0
        for TechDisp in model.setProcBaseDisp_TCD:
            for sTS in model.setTimeSlice_TS:
                GenCost += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS] \
                    * model.pTSRepHourYear_TS[sTS] * model.pExProcDispVGC_TCD[TechDisp]  # MWh * USD/kWh
        
        GenCost = GenCost / 1000   # M.USD
        
        ### import from outside the market
        ImportCost = 0
        for TransLine in model.setTransLDZ_TRL:
            if TransLine[0:2] == "ET":
                for sTS in model.setTimeSlice_TS:
                    # import price 0.3 USD per kwh
                    ImportCost += (model.vTransLDZIn_TRL_TS[TransLine,sTS] \
                                   * 30 * instance.iImportPrice / 1000)  # M.USD

        ### energy spill
        Spill = 0
        for sZone in model.setLDZone_ZNL:
            for sTS in model.setTimeSlice_TS:
                # energy spill 0.01 USD per kwh
                Spill += (model.vSpillZone_ZNL_TS[sZone,sTS] * 30 \
                          * instance.iSpillCost / 1000)  # M.USD

        return GenCost + ImportCost + Spill

    model.obj = pe.Objective( rule = TotalSystemVarCost, sense = pe.minimize ) # M.USD
    
    return


def _modelResult_ED(model, results, instance, objMarket, objDay):
    ''' export ED model results '''
    
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
    
    ### update daily ED model results    
    if sModelStatus == "feasible":
        objMarket.lsDayVarCost.append(float(pe.value(model.obj)))
        md_ED_output.updateDayDispatchResults(model, instance, objMarket, objDay)

    return sModelStatus

