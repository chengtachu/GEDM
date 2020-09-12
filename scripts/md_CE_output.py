#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Functions to convert CE model result and export to files
#

import expt_file


def CE_output_processGen(model, instance, objMarket, filePath, iYear):
    ''' compile a table of process output information and export to file '''
    
    #[zone ID, technology, capacity, TS]
    output = []
    
    # header
    header = ["Zone Code", "ZoneID", "Technology", "Item", "Installed Capacity(MW)"]   
    for objTS in instance.lsTimeSlice_CEP:
        header.append( "M" + objTS.sMonth + "H" + objTS.sHour )
    output.append(header)
    
    ##### get dispatchable process output  -- existing process
    for sTech in model.setProcBaseDisp_TCD:
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
        out_row.append( format(float(model.pExProcDispCap_TCD[sTech]), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vExProcDispPwOutGrs_TCD_TS[sTech,objTS.sTSIndex].value), ".2f") )
        output.append(out_row)
        
        # Net power output
        out_row = [sZoneCode, TechString[0], TechString[1], "Net Output"]
        # capacity
        out_row.append( format(float(model.pExProcDispCap_TCD[sTech]), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vExProcDispPwOutNet_TCD_TS[sTech,objTS.sTSIndex].value), ".2f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T3
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T3", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA3:
                out_row.append( format(float(model.vExProcASProv_TCA3_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
    ##### get dispatchable process output -- new process
    for sTech in model.setProcNewDisp_TCD:        
        if float(model.vNewProcDispCap_TCD[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
    
            # Gross power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Gross Output"]
            # capacity
            out_row.append( format(float(model.vNewProcDispCap_TCD[sTech].value), ".1f") )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcDispPwOutGrs_TCD_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
            
            # Net power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Net Output"]
            # capacity
            out_row.append( " " )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcDispPwOutNet_TCD_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
            
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T3
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T3", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA3:
                    out_row.append( format(float(model.vNewProcASProv_TCA3_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
    ##### get storage process output  -- existing process
    for sTech in model.setProcBaseStor_TCS:
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
        out_row.append( format(float(model.pExProcStorCap_TCS[sTech]), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(-float(model.vExProcStorPwIn_TCS_TS[sTech,objTS.sTSIndex].value), ".2f") )
        output.append(out_row)

        # output
        out_row = [sZoneCode, TechString[0], TechString[1], "Output"]
        # capacity
        out_row.append( format(float(model.pExProcStorCap_TCS[sTech]), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vExProcStorPwOut_TCS_TS[sTech,objTS.sTSIndex].value), ".2f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
          
           
    ##### get storage process output  -- new process
    for sTech in model.setProcNewStor_TCS:
        if float(model.vNewProcStorCap_TCS[sTech].value) > 0:
            
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
            
            # input
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Input"]
            # capacity
            out_row.append( format(float(model.vNewProcStorCap_TCS[sTech].value), ".1f") )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(-float(model.vNewProcStorPwIn_TCS_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
    
            # output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Output"]
            # capacity
            out_row.append( " " )
            
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcStorPwOut_TCS_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
            
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row) 
              
    ##### get hydropower process output  -- existing process
    for sTech in model.setProcBaseHydr_TCH:
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
        out_row.append( format(float(model.pExProcHydrCap_TCH[sTech]), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vExProcHydrPwOut_TCH_TS[sTech,objTS.sTSIndex].value), ".2f") )
        output.append(out_row)
    
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for objTS in instance.lsTimeSlice_CEP:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
    
    ##### get hydropower process output  -- new process
    for sTech in model.setProcNewHydr_TCH:
        if float(model.vNewProcHydrCap_TCH[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcHydrCap_TCH[sTech].value), ".1f") )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcHydrPwOut_TCH_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
        
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProv_TCA1_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for objTS in instance.lsTimeSlice_CEP:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProv_TCA2_TS[sTech,objTS.sTSIndex].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
      
    ##### get non-dispatchable process output  -- existing process
    for sZone in model.setLDZone_ZNL:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # onshore
        out_row = [sZoneCode, sZone, "Exist Non-disp output", ""]
        capacity = 0  
        out_row.append( format(float(capacity), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.pNonDispGen_ZNL_TS[sZone,objTS.sTSIndex]), ".2f") )
        output.append(out_row)

    for sZone in model.setOFZone_ZNF:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        # offshore
        out_row = [sZoneCode, sZone, "Exist Non-disp output", ""]
        capacity = 0       
        out_row.append( format(float(capacity), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.pNonDispGen_ZNF_TS[sZone,objTS.sTSIndex]), ".2f") )
        output.append(out_row)
    
    ##### get renewable process output  -- new process  
    for sTech in model.setProcNewRE_TCR:
        if float(model.vNewProcRenewCap_TCR[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1] + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcRenewCap_TCR[sTech].value), ".1f") )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcRenewPwOut_TCR_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
    
    for sTech in model.setProcNewRE_Offs_TCR:
        if float(model.vNewProcRenewCapOffs_TCR[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1] + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcRenewCapOffs_TCR[sTech].value), ".1f") )
            # TS output
            for objTS in instance.lsTimeSlice_CEP:
                out_row.append( format(float(model.vNewProcRenewPwOutOffs_TCR_TS[sTech,objTS.sTSIndex].value), ".2f") )
            output.append(out_row)
    
    ##### get cross-zone trans
    for sTrans in model.setTransLDZ_TRL:
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]
        
        # capacity
        capacity = float(model.pExTransLDZCap_TRL[sTrans])
        NewCapacity = float(model.vNewProcTransCap_TRL[sTrans].value)
        out_row.append( format(float(capacity), ".1f") + "/" + format(float(NewCapacity), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vTransLDZIn_TRL_TS[sTrans,objTS.sTSIndex].value), ".2f") )
            
        output.append(out_row)
    
    ##### get offshore-zone trans
    for sTrans in model.setTransOFZ_TRF:
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]   
        
        # capacity
        capacity = str(float(model.pExTransOFZCap_TRF[sTrans]))    
        NewCapacity = float(model.vNewProcTransOffCap_TRF[sTrans].value)
        out_row.append( format(float(capacity), ".1f") + "/" + format(float(NewCapacity), ".1f") )
        # TS output
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(float(model.vTransOFZOut_TRF_TS[sTrans,objTS.sTSIndex].value), ".2f") )
            
        output.append(out_row)    
    
    
    # save file
    filePath = filePath + "/" + str(iYear) + "_CE_ProcessOutput.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


def CE_output_zoneBalance(model, instance, objMarket, filePath, iYear):
    ''' compile a table of zone balance information and export to file '''
    
    #[zone code, flow, annual net(GWh), TS]
    output = []
    
    # header
    header = ["Zone code","Zone ID", "Flow", "Annual Total(GWh)"]   
    for objTS in instance.lsTimeSlice_CEP:
        header.append( "M" + objTS.sMonth + "H" + objTS.sHour )
    output.append(header)
        
    ### land zone balance
    for sZone in model.setLDZone_ZNL:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # demand
        out_row = [sZoneCode, sZone, "Demand(GWh)"]
        total = 0
        for objTS in instance.lsTimeSlice_CEP:
            total = total + (model.pDemand_ZNL_TS[sZone,objTS.sTSIndex] * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(model.pDemand_ZNL_TS[sZone,objTS.sTSIndex] * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # residual demand
        out_row = [sZoneCode, sZone, "Residual Demand(GWh)"]
        total = 0
        out_row.append(total)
        for objTS in instance.lsTimeSlice_CEP:
            demand = float(model.pDemand_ZNL_TS[sZone,objTS.sTSIndex])
            NonDispGen = float(model.pNonDispGen_ZNL_TS[sZone,objTS.sTSIndex])
            out_row.append( format( (demand-NonDispGen) * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # supply
        out_row = [sZoneCode, sZone, "Zone Supply(GWh)"]
        total = 0
        for objTS in instance.lsTimeSlice_CEP:
            total = total + (model.vSupplyZone_ZNL_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(model.vSupplyZone_ZNL_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # spill
        out_row = [sZoneCode, sZone, "Spilled Energy(GWh)"]
        total = 0
        for objTS in instance.lsTimeSlice_CEP:
            total = total + (model.vSpillZone_ZNL_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(model.vSpillZone_ZNL_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        ### import
        # from other land zones
        for sTrans in model.setTransLDZ_TRL:
            TransString = sTrans.split("/")
            if TransString[1] == sZone:
                out_row = [sZoneCode, sZone, "Import from: " + TransString[0]]
                total = 0
                for objTS in instance.lsTimeSlice_CEP:
                    total = total + (model.vTransLDZOut_TRL_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for objTS in instance.lsTimeSlice_CEP:
                    out_row.append( format(model.vTransLDZOut_TRL_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
        
        # from offshore zones
        for sTrans in model.setTransOFZ_TRF:
            TransString = sTrans.split("/")
            if TransString[1] == sZone:
                out_row = [sZoneCode, sZone, "Import from: " + TransString[0]]
                total = 0
                for objTS in instance.lsTimeSlice_CEP:
                    total = total + (model.vTransOFZOut_TRF_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for objTS in instance.lsTimeSlice_CEP:
                    out_row.append( format(model.vTransOFZOut_TRF_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
        
        ### export
        for sTrans in model.setTransLDZ_TRL:
            TransString = sTrans.split("/")
            if TransString[0] == sZone:
                out_row = [sZoneCode, sZone, "Export to: " + TransString[1]]
                total = 0
                for objTS in instance.lsTimeSlice_CEP:
                    total = total + (model.vTransLDZIn_TRL_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for objTS in instance.lsTimeSlice_CEP:
                    out_row.append( format(model.vTransLDZIn_TRL_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
    
    ### offshore zone balance
    for sZone in model.setOFZone_ZNF:

        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # supply
        out_row = [sZoneCode, sZone, "Zone Supply(GWh)"]
        total = 0
        for objTS in instance.lsTimeSlice_CEP:
            total = total + (model.vSupplyOffs_ZNF_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(model.vSupplyOffs_ZNF_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # spill
        out_row = [sZoneCode, sZone, "Curtailment(GWh)"]
        total = 0
        for objTS in instance.lsTimeSlice_CEP:
            total = total + (model.vSpillOffs_ZNF_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
        out_row.append(str(total))
        for objTS in instance.lsTimeSlice_CEP:
            out_row.append( format(model.vSpillOffs_ZNF_TS[sZone,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
        output.append(out_row)
        
        # export
        for sTrans in model.setTransOFZ_TRF:
            TransString = sTrans.split("/")
            if TransString[0] == sZone:
                out_row = [sZoneCode, sZone, "Export to: " + TransString[1]]
                total = 0
                for objTS in instance.lsTimeSlice_CEP:
                    total = total + (model.vTransOFZIn_TRF_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000)
                out_row.append(str(total))
                for objTS in instance.lsTimeSlice_CEP:
                    out_row.append( format(model.vTransOFZIn_TRF_TS[sTrans,objTS.sTSIndex].value * objTS.iRepHoursInYear / 1000, ".3f") )
                output.append(out_row)
    
    # save file
    filePath = filePath + "/" + str(iYear) + "_CE_ZoneBalance.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


### -----------------------------------------------------------------------
### total cost (use this function to output files when needed)
### -----------------------------------------------------------------------

'''
def CE_output_TotalCost(model, instance, objMarket, filePath, iYear):
    
    #[zone code, flow, annual net(GWh), TS]
    output = []
    
    # header
    header = ["Zone ID", "Flow", "Capacity (MW)", "Gen (MWh)", "VGC (USD/kWh)", "Annual Fixed Cost (M.USD)", "Annual Var. Cost (M.USD)"]   
    output.append(header)
        
    ##### existing process
    # minimize variable generation cost of existing process
    for TechDisp in model.setProcBaseDisp_TCD:
        capacity = format(float(model.pExProcDispCap_TCD[TechDisp]), ".1f")
        VarGenCost_Ex = 0
        Gen_Ex = 0
        for sTS in model.setTimeSlice_TS:
            VarGenCost_Ex += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS].value \
                * model.pTSRepHourYear_TS[sTS] * model.pExProcDispVGC_TCD[TechDisp]  # MWh * USD/kWh
            Gen_Ex += model.vExProcDispPwOutGrs_TCD_TS[TechDisp, sTS].value * model.pTSRepHourYear_TS[sTS]
        VarGenCost_Ex = VarGenCost_Ex / 1000   # M.USD
        
        out_row = [TechDisp.split("/")[0], TechDisp.split("/")[1], capacity, Gen_Ex, model.pExProcDispVGC_TCD[TechDisp], "0", VarGenCost_Ex]
        output.append(out_row)
    
    # import from outside the market    
    for TransLine in model.setTransLDZ_TRL:
        ImportCost = 0
        Import = 0
        if TransLine[0:2] == "ET":
            for sTS in model.setTimeSlice_TS:
                ImportCost += (model.vTransLDZIn_TRL_TS[TransLine,sTS].value \
                               * model.pTSRepHourYear_TS[sTS] * instance.iImportPrice / 1000)  # M.USD
                Import += model.vTransLDZIn_TRL_TS[TransLine,sTS].value * model.pTSRepHourYear_TS[sTS]
                
        out_row = ["Import", TransLine, "", Import, "0.2", "0", ImportCost]
        output.append(out_row)

    # energy spill
    for sZone in model.setLDZone_ZNL:
        Spill = 0
        SpillGen = 0
        for sTS in model.setTimeSlice_TS:
            Spill += (model.vSpillZone_ZNL_TS[sZone,sTS].value * model.pTSRepHourYear_TS[sTS] \
                      * instance.iSpillCost / 1000)  # M.USD
            SpillGen += model.vSpillZone_ZNL_TS[sZone,sTS].value * model.pTSRepHourYear_TS[sTS]
            
        out_row = [sZone, "Spill", "", SpillGen, "0.01", "0", Spill]
        output.append(out_row)


    ##### cost of new installation
    # dispatchable
    for sProc in model.setProcNewDisp_TCD:
        if float(model.vNewProcDispCap_TCD[sProc].value) > 0:
            capacity = format(float(model.vNewProcDispCap_TCD[sProc].value), ".1f")
            NewCap_Disp = (model.vNewProcDispCap_TCD[sProc].value * model.pNewProcFixAnnCost_TCD[sProc])
            VarGenCost_New = 0
            Gen_New = 0
            for sTS in model.setTimeSlice_TS:
                VarGenCost_New += model.vNewProcDispPwOutGrs_TCD_TS[sProc, sTS].value \
                    * model.pTSRepHourYear_TS[sTS] * model.pNewProcDispVGC_TCD[sProc]  # MWh * USD/kWh
                Gen_New += model.vNewProcDispPwOutGrs_TCD_TS[sProc, sTS].value * model.pTSRepHourYear_TS[sTS]
            VarGenCost_New = VarGenCost_New / 1000   # M.USD  
            
            out_row = [sProc.split("/")[0], "New" + sProc.split("/")[1], capacity, Gen_New, \
                       format(model.pNewProcDispVGC_TCD[sProc], '.4f'), NewCap_Disp, VarGenCost_New]
            output.append(out_row)
    
    # storage 
    for sProc in model.setProcNewStor_TCS:
        if float(model.vNewProcStorCap_TCS[sProc].value) > 0:
            capacity = format(float(model.vNewProcStorCap_TCS[sProc].value), ".1f")
            NewCap_Stor = (model.vNewProcStorCap_TCS[sProc].value * model.pNewProcFixAnnCost_TCS[sProc])
            out_row = [sProc.split("/")[0], "New" + sProc.split("/")[1], capacity, "0", "0", NewCap_Stor, "0"]
            output.append(out_row)
        
    # hydropower
    for sProc in model.setProcNewHydr_TCH:
        if float(model.vNewProcHydrCap_TCH[sProc].value) > 0:
            capacity = format(float(model.vNewProcHydrCap_TCH[sProc].value), ".1f")
            NewCap_Hydro = (model.vNewProcHydrCap_TCH[sProc].value * model.pNewProcFixAnnCost_TCH[sProc])
            out_row = [sProc.split("/")[0], "New" + sProc.split("/")[1], capacity, "0", "0", NewCap_Hydro, "0"]
            output.append(out_row)
        
    # renewable
    for sProc in model.setProcNewRE_TCR:
        if float(model.vNewProcRenewCap_TCR[sProc].value) > 0:
            capacity = format(float(model.vNewProcRenewCap_TCR[sProc].value), ".1f")
            NewCap_Renew = + (model.vNewProcRenewCap_TCR[sProc].value * model.pNewProcFixAnnCost_TCR[sProc])
            out_row = [sProc.split("/")[0], "New" + sProc.split("/")[1]+sProc.split("/")[2], capacity, "0", "0", NewCap_Renew, "0"]
            output.append(out_row)
        
    # offshore renewable
    for sProc in model.setProcNewRE_Offs_TCR:
        if float(model.vNewProcRenewCapOffs_TCR[sProc].value) > 0:
            capacity = format(float(model.vNewProcRenewCapOffs_TCR[sProc].value), ".1f")
            NewCap_RenewOff = + (model.vNewProcRenewCapOffs_TCR[sProc].value * model.pNewProcFixAnnCost_Offs_TCR[sProc])
            out_row = [sProc.split("/")[0], "New" + sProc.split("/")[1]+sProc.split("/")[2], capacity, "0", "0", NewCap_RenewOff, "0"]
            output.append(out_row)
        
    # terrestrial transmission
    for sProc in model.setTransLDZ_TRL:
        if float(model.vNewProcTransCap_TRL[sProc].value) > 0:
            capacity = format(float(model.vNewProcTransCap_TRL[sProc].value), ".1f")
            NewCap_Trans = (model.vNewProcTransCap_TRL[sProc].value * model.pTransLDZCost_TRL[sProc])
            out_row = ["Land Trans", "New" + sProc, capacity, "0", "0", NewCap_Trans, "0"]
            output.append(out_row)
        
    # offshore transmission
    for sProc in model.setTransOFZ_TRF:
        if float(model.vNewProcTransOffCap_TRF[sProc].value) > 0:
            capacity = format(float(model.vNewProcTransOffCap_TRF[sProc].value), ".1f")
            NewCap_TransOff = (model.vNewProcTransOffCap_TRF[sProc].value * model.pTransOFZCost_TRF[sProc])
            out_row = ["Land Trans", "New" + sProc, capacity, "0", "0", NewCap_TransOff, "0"]
            output.append(out_row)
    
    # save file
    filePath = filePath + "/" + str(iYear) + "_CE_ProcessCost.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return
'''

### -----------------------------------------------------------------------
### reliability test (use this function to output files when needed)
### -----------------------------------------------------------------------

'''
def CE_output_processGen_RT(model, instance, objMarket, filePath, iYear):
    
    #[zone ID, technology, capacity, TS]
    output = []
    
    # header
    header = ["Zone Code", "ZoneID", "Technology", "Item", "Installed Capacity(MW)"]   
    for sTS in model.setTSRT_TS:
        header.append( "M" + str( int(sTS)+1) )
    output.append(header)
    
    ##### get dispatchable process output  -- existing process
    for sTech in model.setProcBaseDisp_TCD:
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
        out_row.append( format(float(model.pExProcDispCap_TCD[sTech]), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vExProcDispPwOutGrsTest_TCD_TS[sTech,sTS].value), ".2f") )
        output.append(out_row)
        
        # Net power output
        out_row = [sZoneCode, TechString[0], TechString[1], "Net Output"]
        # capacity
        out_row.append( format(float(model.pExProcDispCap_TCD[sTech]), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vExProcDispPwOutNetTest_TCD_TS[sTech,sTS].value), ".2f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T3
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T3", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA3:
                out_row.append( format(float(model.vExProcASProvTest_TCA3_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
    ##### get dispatchable process output -- new process
    for sTech in model.setProcNewDisp_TCD:        
        if float(model.vNewProcDispCap_TCD[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
    
            # Gross power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Gross Output"]
            # capacity
            out_row.append( format(float(model.vNewProcDispCap_TCD[sTech].value), ".1f") )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcDispPwOutGrsTest_TCD_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
            
            # Net power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Net Output"]
            # capacity
            out_row.append( " " )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcDispPwOutNetTest_TCD_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
            
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T3
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T3", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA3:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA3_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
        
    ##### get storage process output  -- existing process
    for sTech in model.setProcBaseStor_TCS:
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
        out_row.append( format(float(model.pExProcStorCap_TCS[sTech]), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( "" )
        output.append(out_row)
        
        # output
        out_row = [sZoneCode, TechString[0], TechString[1], "Output"]
        # capacity
        out_row.append( format(float(model.pExProcStorCap_TCS[sTech]), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vExProcStorPwOutTest_TCS_TS[sTech,sTS].value), ".2f") )
        output.append(out_row)
        
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
          
           
    ##### get storage process output  -- new process
    for sTech in model.setProcNewStor_TCS:
        if float(model.vNewProcStorCap_TCS[sTech].value) > 0:
            
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # input
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Input"]
            # capacity
            out_row.append( format(float(model.vNewProcStorCap_TCS[sTech].value), ".1f") )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( "" )
            output.append(out_row)
                
            # output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Output"]
            # capacity
            out_row.append( " " )
            
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcStorPwOutTest_TCS_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
            
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row) 
            
        
    ##### get hydropower process output  -- existing process
    for sTech in model.setProcBaseHydr_TCH:
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
        out_row.append( format(float(model.pExProcHydrCap_TCH[sTech]), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vExProcHydrPwOutTest_TCH_TS[sTech,sTS].value), ".2f") )
        output.append(out_row)
    
        # AS T1
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T1", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA1:
                out_row.append( format(float(model.vExProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
        
        # AS T2
        out_row = [sZoneCode, TechString[0], TechString[1], "AS T2", ""]
        for sTS in model.setTSRT_TS:
            if sTech in model.setProcBaseAS_TCA2:
                out_row.append( format(float(model.vExProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
            else:
                out_row.append( str("0") )
        output.append(out_row)
    
    
    ##### get hydropower process output  -- new process
    for sTech in model.setProcNewHydr_TCH:
        if float(model.vNewProcHydrCap_TCH[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcHydrCap_TCH[sTech].value), ".1f") )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcHydrPwOutTest_TCH_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
        
            # AS T1
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T1", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA1:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA1_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
            
            # AS T2
            out_row = [sZoneCode, TechString[0], "New " + TechString[1], "AS T2", ""]
            for sTS in model.setTSRT_TS:
                if sTech in model.setProcNewAS_TCA2:
                    out_row.append( format(float(model.vNewProcASProvTest_TCA2_TS[sTech,sTS].value), ".2f") )
                else:
                    out_row.append( str("0") )
            output.append(out_row)
    
    
    ##### get non-dispatchable process output  -- existing process
    for sZone in model.setLDZone_ZNL:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # onshore
        out_row = [sZoneCode, sZone, "Exist Non-disp output", ""]
        capacity = 0  
        out_row.append( format(float(capacity), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.pNonDispGenTest_ZNL_TS[sZone,sTS]), ".2f") )
        output.append(out_row)

    for sZone in model.setOFZone_ZNF:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        # offshore
        out_row = [sZoneCode, sZone, "Exist Non-disp output", ""]
        capacity = 0       
        out_row.append( format(float(capacity), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.pNonDispGenOffTest_ZNF_TS[sZone,sTS]), ".2f") )
        output.append(out_row)
    
    
    ##### get renewable process output  -- new process  
    for sTech in model.setProcNewRE_TCR:
        if float(model.vNewProcRenewCap_TCR[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1] + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcRenewCap_TCR[sTech].value), ".1f") )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcRenewPwOutTest_TCR_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
    
    for sTech in model.setProcNewRE_Offs_TCR:
        if float(model.vNewProcRenewCapOffs_TCR[sTech].value) > 0:
        
            TechString = sTech.split("/")
            # get zone code
            sZoneCode = ""
            for objZone in objMarket.lsZone:
                if TechString[0] == objZone.sZoneID:
                    sZoneCode = objZone.sZone
                    break
                
            # power output
            out_row = [sZoneCode, TechString[0], "New " + TechString[1] + TechString[1], "Net output"]
            # capacity
            out_row.append( format(float(model.vNewProcRenewCapOffs_TCR[sTech].value), ".1f") )
            # TS output
            for sTS in model.setTSRT_TS:
                out_row.append( format(float(model.vNewProcRenewPwOutOffsTest_TCR_TS[sTech,sTS].value), ".2f") )
            output.append(out_row)
    
        
    ##### get cross-zone trans
    for sTrans in model.setTransLDZ_TRL:
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]
        
        # capacity
        capacity = float(model.pExTransLDZCap_TRL[sTrans])
        NewCapacity = float(model.vNewProcTransCap_TRL[sTrans].value)
        out_row.append( format(float(capacity), ".1f") + "/" + format(float(NewCapacity), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vTransLDZInTest_TRL_TS[sTrans,sTS].value), ".2f") )
            
        output.append(out_row)
    
    ##### get offshore-zone trans
    for sTrans in model.setTransOFZ_TRF:
        TransString = sTrans.split("/")
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if TransString[0] == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
        
        out_row = [sZoneCode, TransString[0], TransString[1], "Transmission"]   
        
        # capacity
        capacity = str(float(model.pExTransOFZCap_TRF[sTrans]))    
        NewCapacity = float(model.vNewProcTransOffCap_TRF[sTrans].value)
        out_row.append( format(float(capacity), ".1f") + "/" + format(float(NewCapacity), ".1f") )
        # TS output
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vTransOFZOutTest_TRF_TS[sTrans,sTS].value), ".2f") )
            
        output.append(out_row)    
    
    # save file
    filePath = filePath + "/" + str(iYear) + "_CE_ProcessOutput_RT.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return


def CE_output_zoneBalance_RT(model, instance, objMarket, filePath, iYear):
    
    #[zone code, flow, annual net(GWh), TS]
    output = []
    
    # header
    header = ["Zone code","Zone ID", "Flow", "Annual Total(GWh)"]   
    for sTS in model.setTSRT_TS:
        header.append( "M" + str( int(sTS)+1) )
    output.append(header)
        
    ### land zone balance
    for sZone in model.setLDZone_ZNL:
        
        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZone:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # demand
        out_row = [sZoneCode, sZone, "Demand(MW)"]
        total = str(float( sum( model.pDemandTest_ZNL_TS[sZone,:] ) * 730 / 1000) )
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.pDemandTest_ZNL_TS[sZone,sTS]), ".2f") )
        output.append(out_row)
        
        # residual demand
        out_row = [sZoneCode, sZone, "Residual Demand(MW)"]
        total = 0
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            demand = float(model.pDemandTest_ZNL_TS[sZone,sTS])
            NonDispGen = float(model.pNonDispGenTest_ZNL_TS[sZone,sTS])
            out_row.append( format(demand-NonDispGen, ".2f") )
        output.append(out_row)
        
        # supply
        out_row = [sZoneCode, sZone, "Zone Supply(MW)"]
        total = str(float( sum( model.vSupplyZoneTest_ZNL_TS[sZone,:].value ) * 730 / 1000) )
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vSupplyZoneTest_ZNL_TS[sZone,sTS].value), ".2f") )
        output.append(out_row)
        
        # spill
        out_row = [sZoneCode, sZone, "Spilled Energy(MW)"]
        total = str(float( sum( model.vSpillZoneTest_ZNL_TS[sZone,:].value ) * 730 / 1000) )
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vSpillZoneTest_ZNL_TS[sZone,sTS].value), ".2f") )
        output.append(out_row)
        
        ### import
        # from other land zones
        for sTrans in model.setTransLDZ_TRL:
            TransString = sTrans.split("/")
            if TransString[1] == sZone:
                out_row = [sZoneCode, sZone, "Import from: " + TransString[0]]
                total = str(float( sum( model.vTransLDZOutTest_TRL_TS[sTrans,:].value ) * 730 / 1000) )
                out_row.append(total)
                for sTS in model.setTSRT_TS:
                    out_row.append( format(float(model.vTransLDZOutTest_TRL_TS[sTrans,sTS].value), ".2f") )
                output.append(out_row)
        
        # from offshore zones
        for sTrans in model.setTransOFZ_TRF:
            TransString = sTrans.split("/")
            if TransString[1] == sZone:
                out_row = [sZoneCode, sZone, "Import from: " + TransString[0]]
                total = str(float( sum( model.vTransOFZOutTest_TRF_TS[sTrans,:].value ) * 730 / 1000) )
                out_row.append(total)
                for sTS in model.setTSRT_TS:
                    out_row.append( format(float(model.vTransOFZOutTest_TRF_TS[sTrans,sTS].value), ".2f") )
                output.append(out_row)
        
        ### export
        for sTrans in model.setTransLDZ_TRL:
            TransString = sTrans.split("/")
            if TransString[0] == sZone:
                out_row = [sZoneCode, sZone, "Export to: " + TransString[1]]
                total = str(float( sum( model.vTransLDZInTest_TRL_TS[sTrans,:].value ) * 730 / 1000) )
                out_row.append(total)
                for sTS in model.setTSRT_TS:
                    out_row.append( format(float(model.vTransLDZInTest_TRL_TS[sTrans,sTS].value), ".2f") )
                output.append(out_row)
    
    ### offshore zone balance
    for sZone in model.setOFZone_ZNF:

        # get zone code
        sZoneCode = ""
        for objZone in objMarket.lsZoneOffs:
            if sZone == objZone.sZoneID:
                sZoneCode = objZone.sZone
                break
            
        # supply
        out_row = [sZoneCode, sZone, "Zone Supply(MW)"]
        total = str(float( sum( model.vSupplyOffsTest_ZNF_TS[sZone,:].value ) * 730 / 1000) )
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vSupplyOffsTest_ZNF_TS[sZone,sTS].value), ".2f") )
        output.append(out_row)
        
        # spill
        out_row = [sZoneCode, sZone, "Curtailment(MW)"]
        total = str(float( sum( model.vSpillOffsTest_ZNF_TS[sZone,:].value ) * 730 / 1000) )
        out_row.append(total)
        for sTS in model.setTSRT_TS:
            out_row.append( format(float(model.vSpillOffsTest_ZNF_TS[sZone,sTS].value), ".2f") )
        output.append(out_row)
        
        # export
        for sTrans in model.setTransOFZ_TRF:
            TransString = sTrans.split("/")
            if TransString[0] == sZone:
                out_row = [sZoneCode, sZone, "Export to: " + TransString[1]]
                total = str(float( sum( model.vTransOFZInTest_TRF_TS[sTrans,:].value ) * 730 / 1000) )
                out_row.append(total)
                for sTS in model.setTSRT_TS:
                    out_row.append( format(float(model.vTransOFZInTest_TRF_TS[sTrans,sTS].value), ".2f") )
                output.append(out_row)
    
    # save file
    filePath = filePath + "/" + str(iYear) + "_CE_ZoneBalance_RT.csv"
    expt_file.TableOutputToCSV(output, filePath)
    
    return
'''


