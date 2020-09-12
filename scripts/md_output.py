#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to construct tables of summarized information
#

from numpy import zeros

import expt_file


def outputAllMarketResults(instance, objMarket, directory):
    ''' construct tables for all output information '''
    
    lsCountryList = list()
    for objZone in objMarket.lsZone:
        if objZone.sCountry not in lsCountryList:
            lsCountryList.append(objZone.sCountry )
            
    dicCountrySummary_CN_IT = {}
            
    ###---------------------------------------------------------------------
    ### zonal process generation (by country)
    ###---------------------------------------------------------------------
    
    for sCountry in lsCountryList:
    
        CountryGen_Coal = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_CoalCCS = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Gas = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_GasCCS = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Oil = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Nuke = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Biomass = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_BECCS = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Hydro = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_Wind = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_WindOff = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_PV = zeros(len(instance.iAllYearSteps_YS))
        CountryGen_REother = zeros(len(instance.iAllYearSteps_YS))
        
        output = []
        
        # header
        header = ["Zone code","Zone ID", "Technology", "Item"]   
        for iYS in instance.iAllYearSteps_YS:
            header.append( str(iYS) )
        output.append(header)
        
        ### land zone balance (MWh -> GWh)
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
    
                for objProcAssum in objZone.lsProcessAssump:
            
                    if objProcAssum.sOperationMode == "Dispatch":
                        
                        sProc = objZone.sZoneID + "/" + objProcAssum.sProcessName
                        
                        # Gross power output
                        out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, "Gross Output (GWh)"]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (sProc, iYS) in objMarket.dicProcDispPwOutGrs_TCD_YS:
                                out_row.append( format( objMarket.dicProcDispPwOutGrs_TCD_YS[sProc, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)

                        # Net power output
                        out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, "Net Output (GWh)"]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (sProc, iYS) in objMarket.dicProcDispPwOutNet_TCD_YS:
                                fValue = objMarket.dicProcDispPwOutNet_TCD_YS[sProc, iYS] / 1000
                                out_row.append( format( fValue, ".0f") )
                                
                                if objProcAssum.sProcessName in ["COA_SUB", "COA_SC", "COA_USC", "COA_IGCC"]:
                                    CountryGen_Coal[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["COA_SC_CCS", "COA_OXY_CCS", "COA_IGCC_CCS"]:
                                    CountryGen_CoalCCS[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["GAS_OCGT", "GAS_CCGT"]:
                                    CountryGen_Gas[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["GAS_CC_CCS"]:
                                    CountryGen_GasCCS[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["OIL_ST"]:
                                    CountryGen_Oil[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["NUK_LWR"]:
                                    CountryGen_Nuke[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["BIO_ST"]:
                                    CountryGen_Biomass[ind_YS] += fValue
                                elif objProcAssum.sProcessName in ["BIGCC_CCS"]:
                                    CountryGen_BECCS[ind_YS] += fValue
                                
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
                        
                    elif objProcAssum.sOperationMode == "Storage":
                        
                        sProc = objZone.sZoneID + "/" + objProcAssum.sProcessName
                        
                        # storage input
                        out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, "Storage Input (GWh)"]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (sProc, iYS) in objMarket.dicProcDispPwOutGrs_TCD_YS:
                                out_row.append( format( objMarket.dicProcStorPwIn_TCS_YS[sProc, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)

                        # storage output
                        out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, "Storage Output (GWh)"]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (sProc, iYS) in objMarket.dicProcDispPwOutNet_TCD_YS:
                                out_row.append( format( objMarket.dicProcStorPwOut_TCS_YS[sProc, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
                            
                    elif objProcAssum.sProcessName in ["HYD_LG","HYD_SM"]:
                        
                        sProc = objZone.sZoneID + "/" + objProcAssum.sProcessName
                        
                        # hydropower output
                        out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, "Hydropower Output (GWh)"]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (sProc, iYS) in objMarket.dicProcHydrPwOut_TCH_YS:
                                fValue = objMarket.dicProcHydrPwOut_TCH_YS[sProc, iYS] / 1000
                                out_row.append( format( fValue, ".0f") )
                                CountryGen_Hydro[ind_YS] += fValue
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
                        
                ### non-dispatchable renewable outputs

                # All
                out_row = [objZone.sZone, objZone.sZoneID, "All non-hydro renewables", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenAll_ZNL_YS:
                        out_row.append( format( objMarket.dicRenewGenAll_ZNL_YS[objZone.sZone, iYS] / 1000, ".0f") )
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                    
                # Wind
                out_row = [objZone.sZone, objZone.sZoneID, "Wind", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenWind_ZNL_YS:
                        fValue = objMarket.dicRenewGenWind_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryGen_Wind[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # PV
                out_row = [objZone.sZone, objZone.sZoneID, "PV", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenPV_ZNL_YS:
                        fValue = objMarket.dicRenewGenPV_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryGen_PV[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # CSP
                out_row = [objZone.sZone, objZone.sZoneID, "CSP", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenCSP_ZNL_YS:
                        fValue = objMarket.dicRenewGenCSP_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryGen_REother[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # Other
                out_row = [objZone.sZone, objZone.sZoneID, "Other Renewalbes", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenOTR_ZNL_YS:
                        fValue = objMarket.dicRenewGenOTR_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryGen_REother[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                    
        ### offshore zone balance (MWh -> GWh)
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:
    
                # Wind
                out_row = [objZone.sZone, objZone.sZoneID, "All Renewables", "Output (GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicRenewGenAllOff_ZNF_YS:
                        fValue = objMarket.dicRenewGenAllOff_ZNF_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryGen_WindOff[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
    
        ### transmission
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
    
                for objTS in objMarket.lsTrans:
                    
                    if objTS.sFrom == objZone.sZoneID:    
                        out_row = [objZone.sZone, objZone.sZoneID, "Transmission to " + objTS.sTo, "(GWh)"]
                        for iYS in instance.iAllYearSteps_YS:
                            if (objTS.sTransID, iYS) in objMarket.dicTransLDZIn_TRL_YS:
                                out_row.append( format( objMarket.dicTransLDZIn_TRL_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
    
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:
    
                for objTS in objMarket.lsTrans_off:
                    
                    if objTS.sFrom == objZone.sZoneID:    
                        out_row = [objZone.sZone, objZone.sZoneID, "Transmission to " + objTS.sTo, "(GWh)"]
                        for iYS in instance.iAllYearSteps_YS:
                            if (objTS.sTransID, iYS) in objMarket.dicTransOFZIn_TRF_YS:
                                out_row.append( format( objMarket.dicTransOFZIn_TRF_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
    
        # append value to summary dictionary 
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Coal"] = CountryGen_Coal
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_CoalCCS"] = CountryGen_CoalCCS
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Gas"] = CountryGen_Gas
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_GasCCS"] = CountryGen_GasCCS
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Oil"] = CountryGen_Oil
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Nuke"] = CountryGen_Nuke
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Biomass"] = CountryGen_Biomass
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_BECCS"] = CountryGen_BECCS
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Hydro"] = CountryGen_Hydro
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_Wind"] = CountryGen_Wind
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_WindOff"] = CountryGen_WindOff
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_PV"] = CountryGen_PV
        dicCountrySummary_CN_IT[ sCountry, "CountryGen_REother"] = CountryGen_REother
    
        # save file
        filePath = directory + "/0_" + sCountry + "_ProcessGeneration.csv"
        expt_file.TableOutputToCSV(output, filePath)
    
    ###----------------------------------------------------------------------
    ### zonal balance (by country)
    ###----------------------------------------------------------------------
    
    for sCountry in lsCountryList:
    
        CountryDemand = zeros(len(instance.iAllYearSteps_YS))
        CountrySupply = zeros(len(instance.iAllYearSteps_YS))
        CountrySpill = zeros(len(instance.iAllYearSteps_YS))
        CountryImport = zeros(len(instance.iAllYearSteps_YS))
        CountryExport = zeros(len(instance.iAllYearSteps_YS))
        
        output = []
        
        # header
        header = ["Zone code","Zone ID", "Flow"]   
        for iYS in instance.iAllYearSteps_YS:
            header.append( str(iYS) )
        output.append(header)
        
        ### land zone balance (MWh -> GWh)
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
                                 
                # Demand
                out_row = [objZone.sZone, objZone.sZoneID, "Demand(GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicDemand_ZNL_YS:
                        fValue = objMarket.dicDemand_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryDemand[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # Supply
                out_row = [objZone.sZone, objZone.sZoneID, "Supply(GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicSupplyZone_ZNL_YS:
                        fValue = objMarket.dicSupplyZone_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountrySupply[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # Spill
                out_row = [objZone.sZone, objZone.sZoneID, "Spill(GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicSpillZone_ZNL_YS:
                        fValue = objMarket.dicSpillZone_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountrySpill[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)

                ####### import ----------------------
                # from other land zones
                for objTS in objMarket.lsTrans:
                    if objTS.sTo == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Import from: " + objTS.sFrom]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransLDZOut_TRL_YS:
                                out_row.append( format( objMarket.dicTransLDZOut_TRL_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
                        
                    # import from other country
                    if objTS.sTo == objZone.sZoneID and objTS.sFrom[0:3] != sCountry:
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransLDZOut_TRL_YS:
                                CountryImport[ind_YS] += objMarket.dicTransLDZOut_TRL_YS[objTS.sTransID, iYS] / 1000
                            
                # from offshore zones
                for objTS in objMarket.lsTrans_off:
                    if objTS.sTo == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Import from: " + objTS.sFrom]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransOFZOut_TRF_YS:
                                out_row.append( format( objMarket.dicTransOFZOut_TRF_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)

                ####### export ------------------------
                for objTS in objMarket.lsTrans:
                    if objTS.sFrom == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Export to: " + objTS.sTo]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransLDZIn_TRL_YS:
                                out_row.append( format( objMarket.dicTransLDZIn_TRL_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
                        
                    # export to other country
                    if objTS.sFrom == objZone.sZoneID and objTS.sTo[0:3] != sCountry:
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransLDZIn_TRL_YS:
                                CountryExport[ind_YS] += objMarket.dicTransLDZIn_TRL_YS[objTS.sTransID, iYS] / 1000

        ### offshore zone balance (MWh -> GWh)
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:

                # Supply
                out_row = [objZone.sZone, objZone.sZoneID, "Supply(GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicSupplyOffs_ZNF_YS:
                        fValue = objMarket.dicSupplyOffs_ZNF_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountrySupply[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # Spill
                out_row = [objZone.sZone, objZone.sZoneID, "Spill(GWh)"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicSpillOffs_ZNF_YS:
                        fValue = objMarket.dicSpillOffs_ZNF_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountrySpill[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)

                # export
                for objTS in objMarket.lsTrans_off:
                    if objTS.sFrom == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Export to: " + objTS.sTo]
                        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                            if (objTS.sTransID, iYS) in objMarket.dicTransOFZIn_TRF_YS:
                                out_row.append( format( objMarket.dicTransOFZIn_TRF_YS[objTS.sTransID, iYS] / 1000, ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
        
        # append value to summary dictionary 
        dicCountrySummary_CN_IT[ sCountry, "CountryDemand"] = CountryDemand
        dicCountrySummary_CN_IT[ sCountry, "CountrySupply"] = CountrySupply
        dicCountrySummary_CN_IT[ sCountry, "CountrySpill"] = CountrySpill
        dicCountrySummary_CN_IT[ sCountry, "CountryImport"] = CountryImport
        dicCountrySummary_CN_IT[ sCountry, "CountryExport"] = CountryExport
        
        # save file
        filePath = directory + "/0_" + sCountry + "_ZoneBalance.csv"
        expt_file.TableOutputToCSV(output, filePath)
    
    
    ###---------------------------------------------------------------------
    ### zonal process capacity (by country)
    ###---------------------------------------------------------------------
    
    for sCountry in lsCountryList:
    
        CountryCap_Coal = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_CoalCCS = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Gas = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_GasCCS = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Oil = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Nuke =zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Biomass = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_BECCS = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_HPS = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Storage = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Hydro = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_Wind = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_WindOff = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_PV = zeros(len(instance.iAllYearSteps_YS))
        CountryCap_REother = zeros(len(instance.iAllYearSteps_YS))
        
        #[zone code, flow, annual net(GWh), TS]
        output = []
        
        # header
        header = ["Zone code","Zone ID", "ProcessName", "CF_Class"]   
        for iYS in instance.iAllYearSteps_YS:
            header.append( str(iYS) )
        output.append(header)
        
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
            
                for objProcAssum in objZone.lsProcessAssump:
                    out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, objProcAssum.iCFClass]                    
                    for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                        fTotalCap = 0
                        for objProc in objZone.lsProcess:
                            if objProc.iDeCommitTime > iYS and objProc.iCommitTime <= iYS:
                                if objProc.sProcessName == objProcAssum.sProcessName and objProc.iCFClass == objProcAssum.iCFClass:
                                    fTotalCap += objProc.iCapacity
                        out_row.append( format( fTotalCap, ".0f") )
                        
                        # country summary data
                        if objProcAssum.sProcessName in ["COA_SUB", "COA_SC", "COA_USC", "COA_IGCC"]:
                            CountryCap_Coal[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["COA_SC_CCS", "COA_OXY_CCS", "COA_IGCC_CCS"]:
                            CountryCap_CoalCCS[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["GAS_OCGT", "GAS_CCGT"]:
                            CountryCap_Gas[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["GAS_CC_CCS"]:
                            CountryCap_GasCCS[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["OIL_ST"]:
                            CountryCap_Oil[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["NUK_LWR"]:
                            CountryCap_Nuke[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["BIO_ST"]:
                            CountryCap_Biomass[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["BIGCC_CCS"]:
                            CountryCap_BECCS[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["HYD_PS"]:
                            CountryCap_HPS[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["BESS_ST1", "BESS_ST4", "BESS_ST8"]:
                            CountryCap_Storage[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["HYD_LG", "HYD_SM"]:
                            CountryCap_Hydro[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["WND_ON"]:
                            CountryCap_Wind[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["PV_FT", "PV_TK", "PV_Dist"]:
                            CountryCap_PV[ind_YS] += fTotalCap
                        elif objProcAssum.sProcessName in ["CSP_ST6", "CSP_ST9", "GEO_hydro"]:
                            CountryCap_REother[ind_YS] += fTotalCap
   
                    output.append(out_row)
                    
        ### offshore zones
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:
            
                for objProcAssum in objZone.lsProcessAssump:
                    out_row = [objZone.sZone, objZone.sZoneID, objProcAssum.sProcessName, objProcAssum.iCFClass]                    
                    for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                        fTotalCap = 0
                        for objProc in objZone.lsProcess:
                            if objProc.iDeCommitTime > iYS and objProc.iCommitTime <= iYS:
                                if objProc.sProcessName == objProcAssum.sProcessName and objProc.iCFClass == objProcAssum.iCFClass:
                                    fTotalCap += objProc.iCapacity
                        out_row.append( format( fTotalCap, ".0f") )
                        CountryCap_WindOff[ind_YS] += fTotalCap
                    output.append(out_row)
        
        ### transmission (land)
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
        
                for objTS in objMarket.lsTrans:
                    if objTS.sFrom == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Transmission from:" + objTS.sFrom , "To:" + objTS.sTo]
                        for iYS in instance.iAllYearSteps_YS:
                            if iYS in objTS.dicTransAccCap_YS:
                                out_row.append( format( objTS.dicTransAccCap_YS[iYS], ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
        
        ### transmission (offshore)
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:
        
                for objTS in objMarket.lsTrans_off:
                    if objTS.sFrom == objZone.sZoneID:
                        out_row = [objZone.sZone, objZone.sZoneID, "Transmission from:" + objTS.sFrom , "To:" + objTS.sTo]
                        for iYS in instance.iAllYearSteps_YS:
                            if iYS in objTS.dicTransAccCap_YS:
                                out_row.append( format( objTS.dicTransAccCap_YS[iYS], ".0f") )
                            else:
                                out_row.append( "0" )
                        output.append(out_row)
        
        # append value to summary dictionary 
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Coal"] = CountryCap_Coal
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_CoalCCS"] = CountryCap_CoalCCS
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Gas"] = CountryCap_Gas
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_GasCCS"] = CountryCap_GasCCS
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Oil"] = CountryCap_Oil
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Nuke"] = CountryCap_Nuke
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Biomass"] = CountryCap_Biomass
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_BECCS"] = CountryCap_BECCS
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_HPS"] = CountryCap_HPS
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Storage"] = CountryCap_Storage
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Hydro"] = CountryCap_Hydro
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_Wind"] = CountryCap_Wind
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_WindOff"] = CountryCap_WindOff
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_PV"] = CountryCap_PV
        dicCountrySummary_CN_IT[ sCountry, "CountryCap_REother"] = CountryCap_REother
        
        # save file
        filePath = directory + "/0_" + sCountry + "_ZoneCapacity.csv"
        expt_file.TableOutputToCSV(output, filePath)
    

    ###--------------------------------------------------------------------
    ### zone information (by country)
    ###--------------------------------------------------------------------
    
    for sCountry in lsCountryList:
    
        CountryFuelCons_Coal = zeros(len(instance.iAllYearSteps_YS))
        CountryFuelCons_Gas = zeros(len(instance.iAllYearSteps_YS))
        CountryFuelCons_Oil = zeros(len(instance.iAllYearSteps_YS))
        CountryFuelCons_Uranium = zeros(len(instance.iAllYearSteps_YS))
        CountryFuelCons_Biomass = zeros(len(instance.iAllYearSteps_YS))
        CountryNetEmission = zeros(len(instance.iAllYearSteps_YS))
        CountryCO2Seq = zeros(len(instance.iAllYearSteps_YS))
        CountryVarGenCost = zeros(len(instance.iAllYearSteps_YS))
        CountryFixedCost = zeros(len(instance.iAllYearSteps_YS))
        
        output = []
        
        # header
        header = ["Zone code","Zone ID", "Item", "Item"]   
        for iYS in instance.iAllYearSteps_YS:
            header.append( str(iYS) )
        output.append(header)
        
        ### fuel consumption (GJ -> TJ)
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
            
                # coal
                out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (TJ)", "Coal"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicFuelCons_COA_ZNL_YS:
                        fValue = objMarket.dicFuelCons_COA_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryFuelCons_Coal[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # gas
                out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (TJ)", "Gas"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicFuelCons_GAS_ZNL_YS:
                        fValue = objMarket.dicFuelCons_GAS_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryFuelCons_Gas[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # oil
                out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (TJ)", "Oil"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicFuelCons_OIL_ZNL_YS:
                        fValue = objMarket.dicFuelCons_OIL_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryFuelCons_Oil[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # uranium
                out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (TJ)", "Uranium"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicFuelCons_NUK_ZNL_YS:
                        fValue = objMarket.dicFuelCons_NUK_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryFuelCons_Uranium[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # biomass
                out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (TJ)", "Biomass"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicFuelCons_BIO_ZNL_YS:
                        fValue = objMarket.dicFuelCons_BIO_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".0f") )
                        CountryFuelCons_Biomass[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
    
        ### emission 
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
            
                # CO2 emission
                out_row = [objZone.sZone, objZone.sZoneID, "CO2 Emission (K.Tonnes)", "Total"]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicCO2Emission_ZNL_YS:
                        fValue = objMarket.dicCO2Emission_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".1f") )
                        CountryNetEmission[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # CCS caoture
                out_row = [objZone.sZone, objZone.sZoneID, "CO2 Emission (K.Tonnes)", "CCS sequestration"]
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicCCSCapture_ZNL_YS:
                        fValue = objMarket.dicCCSCapture_ZNL_YS[objZone.sZone, iYS] / 1000
                        out_row.append( format( fValue, ".1f") )
                        CountryCO2Seq[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
        
        ### market price
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
            
                # marginal generation cost
                out_row = [objZone.sZone, objZone.sZoneID, "Marginal Gen. Cost (USD/kWh)", ""]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicZoneMarketPrice_ZNL_YS:
                        out_row.append( format( objMarket.dicZoneMarketPrice_ZNL_YS[objZone.sZone, iYS], ".4f") )
                    else:
                        out_row.append( "0" )
                output.append(out_row)        
        
        ### cost
        for ind_zone, objZone in enumerate(objMarket.lsZone):
            if objZone.sZone[0:3] ==  sCountry:
        
                # variable generation cost
                out_row = [objZone.sZone, objZone.sZoneID, "Variable Gen. Cost (M.USD)", ""]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicZoneProcCostVarGen_ZNL_YS:
                        fValue = objMarket.dicZoneProcCostVarGen_ZNL_YS[objZone.sZone, iYS]
                        out_row.append( format( fValue, ".2f") )
                        CountryVarGenCost[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
                
                # fixed cost
                out_row = [objZone.sZone, objZone.sZoneID, "Fixed annual Cost (M.USD)", ""]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicZoneProcCostAnnFixed_ZNL_YS:
                        fValue = objMarket.dicZoneProcCostAnnFixed_ZNL_YS[objZone.sZone, iYS]
                        out_row.append( format( fValue, ".2f") )
                        CountryFixedCost[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
            
        for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            if objZone.sZone[0:3] ==  sCountry:
            
                # fixed cost
                out_row = [objZone.sZone, objZone.sZoneID, "Fixed annual Cost (M.USD)", ""]  
                for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
                    if (objZone.sZone, iYS) in objMarket.dicZoneProcCostAnnFixedOff_ZNF_YS:
                        fValue = objMarket.dicZoneProcCostAnnFixedOff_ZNF_YS[objZone.sZone, iYS]
                        out_row.append( format( fValue, ".2f") )
                        CountryFixedCost[ind_YS] += fValue
                    else:
                        out_row.append( "0" )
                output.append(out_row)
            
        # append value to summary dictionary 
        dicCountrySummary_CN_IT[ sCountry, "FuelCons_Coal"] = CountryFuelCons_Coal
        dicCountrySummary_CN_IT[ sCountry, "FuelCons_Gas"] = CountryFuelCons_Gas
        dicCountrySummary_CN_IT[ sCountry, "FuelCons_Oil"] = CountryFuelCons_Oil
        dicCountrySummary_CN_IT[ sCountry, "FuelCons_Uranium"] = CountryFuelCons_Uranium
        dicCountrySummary_CN_IT[ sCountry, "FuelCons_Biomass"] = CountryFuelCons_Biomass
        
        dicCountrySummary_CN_IT[ sCountry, "Emission_Net"] = CountryNetEmission
        dicCountrySummary_CN_IT[ sCountry, "Emission_Sequ"] = CountryCO2Seq
        
        dicCountrySummary_CN_IT[ sCountry, "Cost_VarGen"] = CountryVarGenCost
        dicCountrySummary_CN_IT[ sCountry, "Cost_AnnFIxed"] = CountryFixedCost
     
        # save file
        filePath = directory + "/0_" + sCountry + "_ZoneInfo.csv"
        expt_file.TableOutputToCSV(output, filePath)


    ###--------------------------------------------------------------------
    ### country summary
    ###--------------------------------------------------------------------

    for sCountry in lsCountryList:

        output = []
            
        # header
        header = ["Item","Unit"]   
        for iYS in instance.iAllYearSteps_YS:
            header.append( str(iYS) )
        output.append(header)
    
    
        # energy balance
        out_row = ["Electricity Demand","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryDemand"][ind_YS], ".0f") )
        output.append(out_row)
    
        out_row = ["Electricity Supply","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountrySupply"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Electricity Spilled","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountrySpill"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Electricity Import","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryImport"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Electricity Export","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryExport"][ind_YS], ".0f") )
        output.append(out_row)
    
        ### renewable generation %
        out_row = ["Renewable Gen. to Demand","%"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            totalREGen = 0
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_Biomass"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_BECCS"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_Hydro"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_Wind"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_WindOff"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_PV"][ind_YS]
            totalREGen += dicCountrySummary_CN_IT[sCountry,"CountryGen_REother"][ind_YS]
            
            #totalSpill = float(dicCountrySummary_CN_IT[sCountry,"CountrySpill"][ind_YS])
            
            totalDemand = float(dicCountrySummary_CN_IT[sCountry,"CountryDemand"][ind_YS])
            
            if totalDemand > 0:
                out_row.append( format( totalREGen/totalDemand*100, ".1f") )
            else:
                out_row.append( "0" )
                
        output.append(out_row)

        ### emission
        out_row = ["CO2 Emission","K.Tonnes"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"Emission_Net"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["CO2 Sequestration","K.Tonnes"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"Emission_Sequ"][ind_YS], ".0f") )
        output.append(out_row)
        
        ### cost
        out_row = ["Annual Variable Cost","M.USD"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"Cost_VarGen"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Annual Fixed Cost","M.USD"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"Cost_AnnFIxed"][ind_YS], ".0f") )    
        output.append(out_row)
    
        ### fuel consumption
        out_row = ["Fuel Consumption Coal","TJ"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"FuelCons_Coal"][ind_YS], ".0f") )
        output.append(out_row)

        out_row = ["Fuel Consumption Gas","TJ"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"FuelCons_Gas"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Fuel Consumption Oil","TJ"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"FuelCons_Oil"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Fuel Consumption Uranium","TJ"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"FuelCons_Uranium"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Fuel Consumption Biomass","TJ"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"FuelCons_Biomass"][ind_YS], ".0f") )
        output.append(out_row)
        
        ### capacity
        out_row = ["Capacity - Coal","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Coal"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Coal CCS","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_CoalCCS"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Gas","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Gas"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Gas CCS","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_GasCCS"][ind_YS], ".0f") )
        output.append(out_row)

        out_row = ["Capacity - Oil","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Oil"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Nuclear","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Nuke"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Biomass","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Biomass"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - BECCS","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_BECCS"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Pump Hydro Storage","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_HPS"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Battery Storage","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Storage"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Hydropower","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Hydro"][ind_YS], ".0f") )
        output.append(out_row)

        out_row = ["Capacity - Wind","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_Wind"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Offshore Wind","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_WindOff"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - PV","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_PV"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Capacity - Other Renewables","MW"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryCap_REother"][ind_YS], ".0f") )
        output.append(out_row)
    
    
        ### Generation
        out_row = ["Generation - Coal","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Coal"][ind_YS], ".0f") )
        output.append(out_row)
    
        out_row = ["Generation - Coal CCS","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_CoalCCS"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Gas","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Gas"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Gas CCS","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_GasCCS"][ind_YS], ".0f") )
        output.append(out_row)
    
        out_row = ["Generation - Oil","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Oil"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Nuclear","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Nuke"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Biomass","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Biomass"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - BECCS","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_BECCS"][ind_YS], ".0f") )
        output.append(out_row)

        out_row = ["Generation - Hydropower","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Hydro"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Wind","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_Wind"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Offshore Wind","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_WindOff"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - PV","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_PV"][ind_YS], ".0f") )
        output.append(out_row)
        
        out_row = ["Generation - Other Renewables","GWh"]   
        for ind_YS, iYS in enumerate(instance.iAllYearSteps_YS):
            out_row.append( format(dicCountrySummary_CN_IT[sCountry,"CountryGen_REother"][ind_YS], ".0f") )
        output.append(out_row)
    
        # save file
        filePath = directory + "/0_" + sCountry + "_Summary.csv"
        expt_file.TableOutputToCSV(output, filePath)
    
    return 

