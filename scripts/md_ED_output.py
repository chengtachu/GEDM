#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to convert ED model result and export to files
#

import expt_file


def updateDayDispatchResults(model, instance, objMarket, objDay):
    ''' extract daily ED model result '''
    
    for objDiurnalTS in objDay.lsDiurnalTS:
        sTSIndex = str(objDiurnalTS.sTSIndex)
        iTSIndex = objDiurnalTS.iTimeSliceIndex

        ### zonal variables
        for ind_ZN, sZone in enumerate(model.setLDZone_ZNL):
            objMarket.vSupplyZone_ZNL_TS[ind_ZN,iTSIndex] \
                = float(model.vSupplyZone_ZNL_TS[sZone,sTSIndex].value)
            objMarket.vSpillZone_ZNL_TS[ind_ZN,iTSIndex] \
                = float(model.vSpillZone_ZNL_TS[sZone,sTSIndex].value)
            
        for ind_ZN, sZone in enumerate(model.setOFZone_ZNF):
            objMarket.vSupplyOffs_ZNF_TS[ind_ZN,iTSIndex] \
                = float(model.vSupplyOffs_ZNF_TS[sZone,sTSIndex].value)
            objMarket.vSpillOffs_ZNF_TS[ind_ZN,iTSIndex] \
                = float(model.vSpillOffs_ZNF_TS[sZone,sTSIndex].value)

        ### transmission variables
        for ind_TR, sTrans in enumerate(model.setTransLDZ_TRL):
            objMarket.vTransLDZIn_TRL_TS[ind_TR,iTSIndex] \
                = float(model.vTransLDZIn_TRL_TS[sTrans,sTSIndex].value)
            objMarket.vTransLDZOut_TRL_TS[ind_TR,iTSIndex] \
                = float(model.vTransLDZOut_TRL_TS[sTrans,sTSIndex].value)
    
        for ind_TR, sTrans in enumerate(model.setTransOFZ_TRF):
            objMarket.vTransOFZIn_TRF_TS[ind_TR,iTSIndex] \
                = float(model.vTransOFZIn_TRF_TS[sTrans,sTSIndex].value)
            objMarket.vTransOFZOut_TRF_TS[ind_TR,iTSIndex] \
                = float(model.vTransOFZOut_TRF_TS[sTrans,sTSIndex].value)
    
        ### process variables
        for ind_proc, sProc in enumerate(model.setProcBaseDisp_TCD):
            objMarket.vExProcDispPwOutGrs_TCD_TS[ind_proc,iTSIndex] \
                = float(model.vExProcDispPwOutGrs_TCD_TS[sProc,sTSIndex].value)
            objMarket.vExProcDispPwOutNet_TCD_TS[ind_proc,iTSIndex] \
                = float(model.vExProcDispPwOutNet_TCD_TS[sProc,sTSIndex].value)

        for ind_proc, sProc in enumerate(model.setProcBaseStor_TCS):
            objMarket.vExProcStorPwIn_TCS_TS[ind_proc,iTSIndex] \
                = float(model.vExProcStorPwIn_TCS_TS[sProc,sTSIndex].value)
            objMarket.vExProcStorPwOut_TCS_TS[ind_proc,iTSIndex] \
                = float(model.vExProcStorPwOut_TCS_TS[sProc,sTSIndex].value)

        for ind_proc, sProc in enumerate(model.setProcBaseHydr_TCH):
            objMarket.vExProcHydrPwOut_TCH_TS[ind_proc,iTSIndex] \
                = float(model.vExProcHydrPwOut_TCH_TS[sProc,sTSIndex].value)

        ### ancillary services
        for ind_AS, sAS in enumerate(model.setProcBaseAS_TCA1):
            objMarket.vExProcASProv_TCA1_TS[ind_AS,iTSIndex] \
                = float(model.vExProcASProv_TCA1_TS[sAS, sTSIndex].value)
            
        for ind_AS, sAS in enumerate(model.setProcBaseAS_TCA2):
            objMarket.vExProcASProv_TCA2_TS[ind_AS,iTSIndex] \
                = float(model.vExProcASProv_TCA2_TS[sAS, sTSIndex].value)
            
        for ind_AS, sAS in enumerate(model.setProcBaseAS_TCA3):
            objMarket.vExProcASProv_TCA3_TS[ind_AS,iTSIndex] \
                = float(model.vExProcASProv_TCA3_TS[sAS, sTSIndex].value)


    #####  exogenous output  -----------------------------------
    
    ### variable cost of dispatchable process
    
    for ind_ZN, objZone in enumerate(objMarket.lsZone):
        for objDiurnalTS in objDay.lsDiurnalTS:
            sTSIndex = str(objDiurnalTS.sTSIndex)
            iTSIndex = objDiurnalTS.iTimeSliceIndex        
        
            VarGenCost_Ex = 0
            for ind_proc, sProc in enumerate(model.setProcBaseDisp_TCD):
                if objZone.sZoneID == sProc.split("/")[0]:
                
                    VarGenCost_Ex += model.vExProcDispPwOutGrs_TCD_TS[sProc, sTSIndex].value \
                        * model.pTSRepHourYear_TS[sTSIndex] * model.pExProcDispVGC_TCD[sProc]  # MWh * USD/kWh
                    
            VarGenCost_Ex = VarGenCost_Ex / 1000   # M.USD
            objMarket.vTotalVarGenCost_ZNL_TS[ind_ZN, iTSIndex] = VarGenCost_Ex
    
    ### fuel consumption & CO2 emission
    
    for objDiurnalTS in objDay.lsDiurnalTS:
        sTSIndex = str(objDiurnalTS.sTSIndex)
        iTSIndex = objDiurnalTS.iTimeSliceIndex

        for ind_ZN, objZone in enumerate(objMarket.lsZone):
            for ind_proc, sProc in enumerate(model.setProcBaseDisp_TCD):
                if objZone.sZoneID == sProc.split("/")[0]:
                
                    # get the fuel type of the process
                    for objProcAssump in objZone.lsProcessAssump:
                        if objProcAssump.sProcessName == sProc.split("/")[1]:
                            
                            convertEff = float(model.pExProcDispEff_TCD[sProc])
                            
                            CCSCaptureRate = float(model.pExProcDispCCSCapRate_TCD[sProc])
                            
                            # MWh * rep-hour / efficiency * 3.6 --> (GJ)
                            fConsump = model.vExProcDispPwOutGrs_TCD_TS[sProc,sTSIndex].value \
                                * objDiurnalTS.iRepHoursInYear / convertEff * 3.6
                            
                            if objProcAssump.sFuel == "coal":  # emission factor 0.0946 tonnes/GJ
                                objMarket.vFuelCons_COA_ZNL_TS[ind_ZN,iTSIndex] += fConsump
                                objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0946 * (1-CCSCaptureRate)
                                objMarket.vCCSCapture_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0946 * CCSCaptureRate
                                
                            elif objProcAssump.sFuel == "gas":
                                objMarket.vFuelCons_GAS_ZNL_TS[ind_ZN,iTSIndex] += fConsump
                                objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0561 * (1-CCSCaptureRate)
                                objMarket.vCCSCapture_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0561 * CCSCaptureRate
                                
                            elif objProcAssump.sFuel == "oil":
                                objMarket.vFuelCons_OIL_ZNL_TS[ind_ZN,iTSIndex] += fConsump
                                objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0733
                                
                            elif objProcAssump.sFuel == "uranium":
                                objMarket.vFuelCons_NUK_ZNL_TS[ind_ZN,iTSIndex] += fConsump
                                objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0001
                                
                            elif objProcAssump.sFuel == "biomass":
                                objMarket.vFuelCons_BIO_ZNL_TS[ind_ZN,iTSIndex] += fConsump
                                objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.0001
                                if CCSCaptureRate > 0:
                                    objMarket.vCO2Emission_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.112 * CCSCaptureRate * -1
                                    objMarket.vCCSCapture_ZNL_TS[ind_ZN,iTSIndex] += fConsump * 0.112 * CCSCaptureRate
    
                            break
    
    ### algorithm to calculate zonal market price ----------------------------------------
    for objDiurnalTS in objDay.lsDiurnalTS:
        sTSIndex = str(objDiurnalTS.sTSIndex)
        iTSIndex = objDiurnalTS.iTimeSliceIndex
        
        lsZoneVarGenCost = []
        for ind_ZN, objZone in enumerate(objMarket.lsZone):

            # find the process with highest variable generation cost
            highestCost = 0
            for ind_proc, sProc in enumerate(model.setProcBaseDisp_TCD):
                if objZone.sZoneID == sProc.split("/")[0] and "BIO_" not in sProc:
                    if float(model.vExProcDispPwOutGrs_TCD_TS[sProc, sTSIndex].value) > 0:
                        if model.pExProcDispVGC_TCD[sProc] > highestCost:
                            highestCost = model.pExProcDispVGC_TCD[sProc]
            
            lsZoneVarGenCost.append( [objZone.sZoneID, highestCost] )
            
        # sort variable generation cost by zone
        lsZoneVarGenCost = sorted(lsZoneVarGenCost, key=lambda lsZoneVarGenCost: lsZoneVarGenCost[1], reverse=True)
            
        for indexZone in lsZoneVarGenCost:
            fZonePrice = indexZone[1]
            sZoneID = indexZone[0]
        
            for ind_TR, sTrans in enumerate(model.setTransLDZ_TRL): 
                
                # export from this zone
                if sTrans.split("/")[0] == sZoneID:
                    
                    # transmission in operation
                    if model.vTransLDZIn_TRL_TS[sTrans,sTSIndex].value > 0.01:
                        
                        sToZone = sTrans.split("/")[1]
                        fDesZonePrice = 0
                        fDesZoneInd = 0
                        for ind_zone, lsZone in enumerate(lsZoneVarGenCost):
                            if sToZone == lsZone[0]:
                                fDesZonePrice = lsZone[1]
                                fDesZoneInd = ind_zone
                                break
                        
                        fLineLoss = model.pTransLDZLoss_TRL[sTrans]
                        
                        if fZonePrice / (1-fLineLoss) > fDesZonePrice:
                            lsZoneVarGenCost[fDesZoneInd][1] = fZonePrice / (1-fLineLoss)
        
                    
        for ind_ZN, objZone in enumerate(objMarket.lsZone):
            for objZoneCost in lsZoneVarGenCost:
                if objZoneCost[0] == objZone.sZoneID:
                    objMarket.vZoneMarketPrice_ZNL_TS[ind_ZN, iTSIndex] = objZoneCost[1]
                    break

    return 


def ED_output_TotalCost(instance, objMarket, ind_year, filePath):
    ''' calculate total fixed and variable cost of the system '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    ##### fixed cost  (M.USD / yr)
    totalFixCost = 0
    for objZone in objMarket.lsZone:
        for objProcess in objZone.lsProcess:
            if objProcess.iDeCommitTime > iYear:  
                totalFixCost = totalFixCost + objProcess.fAnnualFixedCost
    objMarket.dicAnnualFixCost_YS[iYear] = totalFixCost
    
    ##### variable cost  (M.USD / yr)
    totalVarCost = sum( objMarket.lsDayVarCost )
    objMarket.dicAnnualVarCost_YS[iYear] = totalVarCost
    
    return
    

def ED_output_processGen(instance, objMarket, ind_year, filePath):
    ''' compile a table of process output information and export to file '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    #[zone ID, technology, capacity, TS]
    output = []
    
    # header
    header = ["Zone Code", "ZoneID", "Technology", "Item", "Installed Capacity(MW)"]   
    for objTS in instance.lsTimeSlice:
        header.append( "M" + objTS.sMonth + "H" + objTS.sHour )
    output.append(header)
    
    ##### get dispatchable tech output
    for ind_Tech, sTech in enumerate(objMarket.setProcBaseDisp_TCD):
        TechString = sTech.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TechString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break

        # Gross power output
        out_row = [sZoneCode, TechString[0], TechString[1], "Gross Output"]
        # capacity
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName == TechString[1]:
                out_row.append( format(objProcessAssump.dicProcAccCapacity_YS[iYear], ".1f") )
                break
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vExProcDispPwOutGrs_TCD_TS[ind_Tech, ind_TS], ".1f") )
        output.append(out_row)
        
        # Net power output
        out_row = [sZoneCode, TechString[0], TechString[1], "Net Output"]
        # capacity
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName == TechString[1]:
                out_row.append( format(objProcessAssump.dicProcAccCapacity_YS[iYear], ".1f") )
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vExProcDispPwOutNet_TCD_TS[ind_Tech, ind_TS], ".1f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA1):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA1_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA2):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA2_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
        
        # AS T3
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T3", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA3):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA3_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
    
    
    ##### get storage tech output
    for ind_Tech, sTech in enumerate(objMarket.setProcBaseStor_TCS):
        TechString = sTech.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TechString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        # input
        out_row = [sZoneCode, TechString[0], TechString[1], "Input"]
        # capacity
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName == TechString[1]:
                out_row.append( format(objProcessAssump.dicProcAccCapacity_YS[iYear], ".1f") )
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(-objMarket.vExProcStorPwIn_TCS_TS[ind_Tech, ind_TS], ".1f") )
        output.append(out_row)

        # output
        out_row = [sZoneCode, TechString[0], TechString[1], "Output"]
        # capacity
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName == TechString[1]:
                out_row.append( format(objProcessAssump.dicProcAccCapacity_YS[iYear], ".1f") )
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vExProcStorPwOut_TCS_TS[ind_Tech, ind_TS], ".1f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA1):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA1_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA2):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA2_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
    
    
    ##### hydro output
    for ind_Tech, sTech in enumerate(objMarket.setProcBaseHydr_TCH):
        TechString = sTech.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TechString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # power output
        out_row = [sZoneCode, TechString[0], TechString[1], "Net output"]
        # capacity
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName == TechString[1]:
                out_row.append( format(objProcessAssump.dicProcAccCapacity_YS[iYear], ".1f") )
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vExProcHydrPwOut_TCH_TS[ind_Tech, ind_TS], ".1f") )
        output.append(out_row)
    
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA1):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA1_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fASProv = 0
            for ind_AS, sAS in enumerate(objMarket.setProcBaseAS_TCA2):
                if sAS == sTech:
                    fASProv = objMarket.vExProcASProv_TCA2_TS[ind_AS, ind_TS]
                    break
            out_row.append( format( fASProv, ".1f" ) )
        output.append(out_row)
    
    
    ##### get non-dispatchable renewable generations
    for objZone in objMarket.lsZone:
        
        ### onshore all
        out_row = [objZone.sZone, objZone.sZoneID, "Non-dispatchable output", "All"]
        fCapacity = 0
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sOperationMode == "NonDispatch" and objProcessAssump.sProcessName not in ["HYD_LG","HYD_SM"]:
                fCapacity = fCapacity + objProcessAssump.dicProcAccCapacity_YS[iYear]
        out_row.append( format(fCapacity, ".1f") )
        
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(float(objMarket.NonDisGenAll_ZNL_TS[objZone.sZoneID, objTS.sTSIndex]), ".1f") )

        output.append(out_row)
        
        ### onshore wind
        out_row = [objZone.sZone, objZone.sZoneID, "Non-dispatchable output", "Wind"]
        fCapacity = 0
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName[0:3] == "WND":
                fCapacity = fCapacity + objProcessAssump.dicProcAccCapacity_YS[iYear]
        out_row.append( format(fCapacity, ".1f") )
        
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(float(objMarket.NonDisGenWind_ZNL_TS[objZone.sZoneID, objTS.sTSIndex]), ".1f") )

        output.append(out_row)

        ### onshore PV
        out_row = [objZone.sZone, objZone.sZoneID, "Non-dispatchable output", "PV"]
        fCapacity = 0
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName[0:3] == "PV_":
                fCapacity = fCapacity + objProcessAssump.dicProcAccCapacity_YS[iYear]
        out_row.append( format(fCapacity, ".1f") )
        
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(float(objMarket.NonDisGenPV_ZNL_TS[objZone.sZoneID, objTS.sTSIndex]), ".1f") )

        output.append(out_row)
        
        ### onshore CSP
        out_row = [objZone.sZone, objZone.sZoneID, "Non-dispatchable output", "CSP"]
        fCapacity = 0
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName[0:3] == "CSP":
                fCapacity = fCapacity + objProcessAssump.dicProcAccCapacity_YS[iYear]
        out_row.append( format(fCapacity, ".1f") )
        
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(float(objMarket.NonDisGenCSP_ZNL_TS[objZone.sZoneID, objTS.sTSIndex]), ".1f") )

        output.append(out_row)
        

    for objZone in objMarket.lsZoneOffs:
                
        # offshore wind
        out_row = [objZone.sZone, objZone.sZoneID, "Non-dispatchable output", "offshore"]
        fCapacity = 0
        for objProcessAssump in objZone.lsProcessAssump:
            if objProcessAssump.sProcessName[0:3] == "WND":
                fCapacity = fCapacity + objProcessAssump.dicProcAccCapacity_YS[iYear]
        out_row.append( format(fCapacity, ".1f") )
        
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(float(objMarket.NonDisGenAll_ZNF_TS[objZone.sZoneID, objTS.sTSIndex]), ".1f") )

        output.append(out_row)
    
    
    ##### get cross-zone trans
    for ind_trans, sTrans in enumerate(objMarket.setTransLDZ_TRL):
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]
        
        # capacity
        for objTrans in objMarket.lsTrans:
            if objTrans.sTransID == sTrans:
                out_row.append( format(objTrans.dicTransAccCap_YS[iYear], ".1f") )
                
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vTransLDZIn_TRL_TS[ind_trans, ind_TS], ".1f") )
            
        output.append(out_row)
    
    ##### get offshore-zone trans
    for ind_trans, sTrans in enumerate(objMarket.setTransOFZ_TRF):
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]   
        
        # capacity
        for objTrans in objMarket.lsTrans_off:
            if objTrans.sTransID == sTrans:
                out_row.append( format(objTrans.dicTransAccCap_YS[iYear], ".1f") )
                
        # TS output
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vTransOFZOut_TRF_TS[ind_trans, ind_TS], ".1f") )
            
        output.append(out_row)
    
    
    # save file
    filePath = filePath + "/" + str(iYear) +"_ED_ProcessOutput.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


def ED_output_zoneBalance(instance, objMarket, ind_year, filePath):
    ''' compile a table of zone balance information and export to file '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    output = []
    
    # header
    header = ["Zone code","Zone ID", "Flow", "Annual Total(GWh)"]   
    for objTS in instance.lsTimeSlice:
        header.append( "M" + objTS.sMonth + "H" + objTS.sHour )
    output.append(header)
    
    ### land zone balance
    for ind_zone, objZone in enumerate(objMarket.lsZone):
            
        # demand
        out_row = [objZone.sZone, objZone.sZoneID, "Demand(GWh)"]
        total = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            total = total + (objZone.fPowerDemand_TS_YS[ind_TS, ind_year] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objZone.fPowerDemand_TS_YS[ind_TS, ind_year] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # supply
        out_row = [objZone.sZone, objZone.sZoneID, "Zone Supply(GWh)"]
        total = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            total = total + (objMarket.vSupplyZone_ZNL_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vSupplyZone_ZNL_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
                
        # spill
        out_row = [objZone.sZone, objZone.sZoneID, "Spilled Energy(GWh)"]
        total = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            total = total + (objMarket.vSpillZone_ZNL_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vSpillZone_ZNL_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)

        ### import
        # from other land zones
        for ind_trans, sTrans in enumerate(objMarket.setTransLDZ_TRL):
            TransString = sTrans.split("/")
            if TransString[1] == objZone.sZoneID:
                out_row = [objZone.sZone, objZone.sZoneID, "Import from: " + TransString[0]]
                total = 0
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    total = total + (objMarket.vTransLDZOut_TRL_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    out_row.append( format(objMarket.vTransLDZOut_TRL_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
        
        # from offshore zones
        for ind_trans, sTrans in enumerate(objMarket.setTransOFZ_TRF):
            TransString = sTrans.split("/")
            if TransString[1] == objZone.sZoneID:
                out_row = [objZone.sZone, objZone.sZoneID, "Import from: " + TransString[0]]
                total = 0
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    total = total + (objMarket.vTransOFZOut_TRF_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    out_row.append( format(objMarket.vTransOFZOut_TRF_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
        
        ### export
        for ind_trans, sTrans in enumerate(objMarket.setTransLDZ_TRL):
            TransString = sTrans.split("/")
            if TransString[0] == objZone.sZoneID:
                out_row = [objZone.sZone, objZone.sZoneID, "Export to: " + TransString[1]]
                total = 0
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    total = total + (objMarket.vTransLDZIn_TRL_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    out_row.append( format(objMarket.vTransLDZIn_TRL_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
    
    ### offshore zone balance
    for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
            
        # supply
        out_row = [objZone.sZone, objZone.sZoneID, "Zone Supply(GWh)"]
        total = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            total = total + (objMarket.vSupplyOffs_ZNF_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vSupplyOffs_ZNF_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # spill
        out_row = [objZone.sZone, objZone.sZoneID, "Curtailment(GWh)"]
        total = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            total = total + (objMarket.vSpillOffs_ZNF_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format(objMarket.vSpillOffs_ZNF_TS[ind_zone, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # export
        for ind_trans, sTrans in enumerate(objMarket.setTransOFZ_TRF):
            TransString = sTrans.split("/")
            if TransString[0] == objZone.sZoneID:
                out_row = [objZone.sZone, objZone.sZoneID, "Export to: " + TransString[1]]
                total = 0
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    total = total + (objMarket.vTransOFZIn_TRF_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for ind_TS, objTS in enumerate(instance.lsTimeSlice):
                    out_row.append( format(objMarket.vTransOFZIn_TRF_TS[ind_trans, ind_TS] * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
    
    # save file
    filePath = filePath + "/" + str(iYear) +"_ED_ZoneBalance.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


def ED_output_zoneInfo(instance, objMarket, ind_year, filePath):
    ''' compile a table of zone information and export to file '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    #[zone code, flow, annual net(GWh), TS]
    output = []
    
    # header
    header = ["Zone code","Zone ID", "Item", "Item"]   
    for objTS in instance.lsTimeSlice:
        header.append( "M" + objTS.sMonth + "H" + objTS.sHour )
    output.append(header)
    
    ### fuel consumption
    for ind_zone, objZone in enumerate(objMarket.lsZone):
        
        # coal
        out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (GJ)", "Coal"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vFuelCons_COA_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
        
        # gas
        out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (GJ)", "Gas"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vFuelCons_GAS_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
        
        # oil
        out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (GJ)", "Oil"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vFuelCons_OIL_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
        
        # uranium
        out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (GJ)", "Uranium"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vFuelCons_NUK_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
        
        # biomass
        out_row = [objZone.sZone, objZone.sZoneID, "Fuel Consumption (GJ)", "Biomass"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vFuelCons_BIO_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)

    ### emission 
    for ind_zone, objZone in enumerate(objMarket.lsZone):
        
        # CO2 emission
        out_row = [objZone.sZone, objZone.sZoneID, "CO2 Emission (Tonnes)", "Total"]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vCO2Emission_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
        
        # CCS caoture
        out_row = [objZone.sZone, objZone.sZoneID, "CO2 Emission (Tonnes)", "CCS sequestration"]
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vCCSCapture_ZNL_TS[ind_zone, ind_TS], ".0f") )
        output.append(out_row)
    
    ### market price
    for ind_zone, objZone in enumerate(objMarket.lsZone):
        
        # marginal generation cost
        out_row = [objZone.sZone, objZone.sZoneID, "Marginal Gen. Cost (USD/kWh)", ""]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vZoneMarketPrice_ZNL_TS[ind_zone, ind_TS], ".4f") )
        output.append(out_row)
    
    ### cost
    for ind_zone, objZone in enumerate(objMarket.lsZone):
    
        # variable generation cost
        out_row = [objZone.sZone, objZone.sZoneID, "Variable Gen. Cost (M.USD)", ""]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            out_row.append( format( objMarket.vTotalVarGenCost_ZNL_TS[ind_zone, ind_TS], ".2f") )
        output.append(out_row)
        
        # fixed cost
        out_row = [objZone.sZone, objZone.sZoneID, "Fixed annual Cost (M.USD)", ""]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            if ind_TS == 0:
                out_row.append( format( objMarket.dicZoneProcCostAnnFixed_ZNL_YS[objZone.sZone, iYear] , ".2f") )
            else:
                out_row.append( "" )
        output.append(out_row)
        
    for ind_zone, objZone in enumerate(objMarket.lsZoneOffs):
        
        # fixed cost
        out_row = [objZone.sZone, objZone.sZoneID, "Fixed annual Cost (M.USD)", ""]  
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            if ind_TS == 0:
                out_row.append( format( objMarket.dicZoneProcCostAnnFixedOff_ZNF_YS[objZone.sZone, iYear] , ".2f") )
            else:
                out_row.append( "" )
        output.append(out_row)
        
    # save file
    filePath = filePath + "/" + str(iYear) +"_ED_ZoneInfo.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


def ED_output_AnnualInfo(instance, objMarket, ind_year):
    ''' keep annual ED model result for building a summary table later '''
    
    iYear = instance.iAllYearSteps_YS[ind_year]
    
    ### zonal supply and demand (MWh)
    for ind_ZN, objZone in enumerate(objMarket.lsZone):
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objZone.fPowerDemand_TS_YS[ind_TS,ind_year] * objTS.iRepHoursInYear
        objMarket.dicDemand_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vSupplyZone_ZNL_TS[ind_ZN,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicSupplyZone_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vSpillZone_ZNL_TS[ind_ZN,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicSpillZone_ZNL_YS[objZone.sZone, iYear] = fTotalValue

    for ind_ZN, objZone in enumerate(objMarket.lsZoneOffs):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vSupplyOffs_ZNF_TS[ind_ZN,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicSupplyOffs_ZNF_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vSpillOffs_ZNF_TS[ind_ZN,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicSpillOffs_ZNF_YS[objZone.sZone, iYear] = fTotalValue

    ### transmission variables (MWh)
    for ind_TR, sTrans in enumerate(objMarket.setTransLDZ_TRL):
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vTransLDZIn_TRL_TS[ind_TR,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicTransLDZIn_TRL_YS[sTrans, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vTransLDZOut_TRL_TS[ind_TR,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicTransLDZOut_TRL_YS[sTrans, iYear] = fTotalValue

    for ind_TR, sTrans in enumerate(objMarket.setTransOFZ_TRF):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vTransOFZIn_TRF_TS[ind_TR,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicTransOFZIn_TRF_YS[sTrans, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vTransOFZOut_TRF_TS[ind_TR,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicTransOFZOut_TRF_YS[sTrans, iYear] = fTotalValue
           
    ### generation by technology (MWh)
    for ind_Proc, sProc in enumerate(objMarket.setProcBaseDisp_TCD):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vExProcDispPwOutGrs_TCD_TS[ind_Proc,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicProcDispPwOutGrs_TCD_YS[sProc, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vExProcDispPwOutNet_TCD_TS[ind_Proc,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicProcDispPwOutNet_TCD_YS[sProc, iYear] = fTotalValue
        
    for ind_Proc, sProc in enumerate(objMarket.setProcBaseStor_TCS):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vExProcStorPwIn_TCS_TS[ind_Proc,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicProcStorPwIn_TCS_YS[sProc, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vExProcStorPwOut_TCS_TS[ind_Proc,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicProcStorPwOut_TCS_YS[sProc, iYear] = fTotalValue
        
    for ind_Proc, sProc in enumerate(objMarket.setProcBaseHydr_TCH):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vExProcHydrPwOut_TCH_TS[ind_Proc,ind_TS] * objTS.iRepHoursInYear
        objMarket.dicProcHydrPwOut_TCH_YS[sProc, iYear] = fTotalValue
        
    ### renewable generation (exclude hydro) (MWh)   
    for ind_ZN, objZone in enumerate(objMarket.lsZone):
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenAll_ZNL_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenAll_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenWind_ZNL_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenWind_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenPV_ZNL_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenPV_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenCSP_ZNL_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenCSP_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenOTR_ZNL_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenOTR_ZNL_YS[objZone.sZone, iYear] = fTotalValue

    for ind_ZN, objZone in enumerate(objMarket.lsZoneOffs):

        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.NonDisGenAll_ZNF_TS[objZone.sZoneID, objTS.sTSIndex] * objTS.iRepHoursInYear
        objMarket.dicRenewGenAllOff_ZNF_YS[objZone.sZone, iYear] = fTotalValue

    ### fuel consumption (GJ)
    for ind_ZN, objZone in enumerate(objMarket.lsZone):
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vFuelCons_COA_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicFuelCons_COA_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vFuelCons_GAS_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicFuelCons_GAS_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vFuelCons_OIL_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicFuelCons_OIL_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vFuelCons_NUK_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicFuelCons_NUK_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vFuelCons_BIO_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicFuelCons_BIO_ZNL_YS[objZone.sZone, iYear] = fTotalValue

    ### other information (emission: tonnes, market price: USD/kWh, variable cost, fixed cost: M.USD)
    for ind_ZN, objZone in enumerate(objMarket.lsZone):
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vCO2Emission_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicCO2Emission_ZNL_YS[objZone.sZone, iYear] = fTotalValue
        
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vCCSCapture_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicCCSCapture_ZNL_YS[objZone.sZone, iYear] = fTotalValue

        fPrice = []
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fPrice.append(objMarket.vZoneMarketPrice_ZNL_TS[ind_ZN,ind_TS])
        objMarket.dicZoneMarketPrice_ZNL_YS[objZone.sZone, iYear] = sum(fPrice) / len(fPrice)

        # annual variable cost (dispatchable process) (already account rep. hours)
        fTotalValue = 0
        for ind_TS, objTS in enumerate(instance.lsTimeSlice):
            fTotalValue += objMarket.vTotalVarGenCost_ZNL_TS[ind_ZN,ind_TS]
        objMarket.dicZoneProcCostVarGen_ZNL_YS[objZone.sZone, iYear] = fTotalValue

        # annual fixed cost (all process)
        fTotalValue = 0
        for objProcess in objZone.lsProcess:
            if objProcess.iDeCommitTime > iYear:
                fTotalValue += objProcess.fAnnualFixedCost
        objMarket.dicZoneProcCostAnnFixed_ZNL_YS[objZone.sZone, iYear] = fTotalValue

    for ind_ZN, objZone in enumerate(objMarket.lsZoneOffs):

        # annual fixed cost (all process)
        fTotalValue = 0
        for objProcess in objZone.lsProcess:
            if objProcess.iDeCommitTime > iYear:
                fTotalValue += objProcess.fAnnualFixedCost
        objMarket.dicZoneProcCostAnnFixedOff_ZNF_YS[objZone.sZone, iYear] = fTotalValue

    return

