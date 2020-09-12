#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Define market class
#


class Market:
    """ market class  """

    def __init__(self, sMarket):
        self.sMarket = str(sMarket)
        self.lsZone = list()        # list of zone objects
        self.lsZoneOffs = list()    # list of offshore zone objects
        self.lsTrans = list()       # list of zone connection objects
        self.lsTrans_off = list()   # list of offshore zone connection objects
        
        ### assumptions on transmission cost and loss
        self.lsDCLineLoss = []  
        self.lsDCConvLoss = [] 
        self.lsACLineLoss = [] 
        self.lsDCCapex = []
        self.lsDCOpex = []
        self.lsDCCapexConv = []
        self.lsDCOpexConv = []
        self.lsACCapex = []
        self.lsACOpex = []
        self.lsCRF = []
        
        ### variables for the formulation        
        self.setProcBaseDisp_TCD = []
        self.setProcBaseStor_TCS = []
        self.setProcBaseHydr_TCH = []
        self.setTransLDZ_TRL = []
        self.setTransOFZ_TRF = []
        self.setProcBaseAS_TCA1 = []
        self.setProcBaseAS_TCA2 = []
        self.setProcBaseAS_TCA3 = []
        
        self.setProcNewDisp_TCD = []
        self.setProcNewStor_TCS = []
        self.setProcNewHydr_TCH = []
        self.setProcNewRE_TCR = []      # renewable process, exclude hydro, biomass
        self.setProcNewRE_Offs_TCR = [] # renewable process offshore
        
        self.setProcNewAS_TCA1 = []
        self.setProcNewAS_TCA2 = []
        self.setProcNewAS_TCA3 = []

        ### indigenous input
        self.dicCNSEmissionFactor_YS = {}
        self.dicCNSEmissionCap_YS = {}  # Tonne
        
        ### annual overall modelling results (values in energy unit, not power)
        
        self.dicDemand_ZNL_YS = {}
        
        self.dicSupplyZone_ZNL_YS = {}  # MWh
        self.dicSupplyOffs_ZNF_YS = {}
        self.dicSpillZone_ZNL_YS = {}
        self.dicSpillOffs_ZNF_YS = {}
        self.dicTransLDZIn_TRL_YS = {}
        self.dicTransLDZOut_TRL_YS = {}
        self.dicTransOFZIn_TRF_YS = {}
        self.dicTransOFZOut_TRF_YS = {}
        self.dicProcDispPwOutGrs_TCD_YS = {}
        self.dicProcDispPwOutNet_TCD_YS = {}
        self.dicProcStorPwIn_TCS_YS = {}
        self.dicProcStorPwOut_TCS_YS = {}
        self.dicProcHydrPwOut_TCH_YS = {}
                
        self.dicRenewGenAll_ZNL_YS = {}
        self.dicRenewGenWind_ZNL_YS = {}
        self.dicRenewGenPV_ZNL_YS = {}
        self.dicRenewGenCSP_ZNL_YS = {}
        self.dicRenewGenOTR_ZNL_YS = {}
        self.dicRenewGenAllOff_ZNF_YS = {}  # offshore        
        
        self.dicFuelCons_COA_ZNL_YS = {}   # GJ
        self.dicFuelCons_GAS_ZNL_YS = {}   # GJ
        self.dicFuelCons_OIL_ZNL_YS = {}   # GJ
        self.dicFuelCons_NUK_ZNL_YS = {}    # GJ
        self.dicFuelCons_BIO_ZNL_YS = {}   # GJ
        
        self.dicCO2Emission_ZNL_YS = {}    # Tonnes
        self.dicCCSCapture_ZNL_YS = {}     # Tonnes
        
        self.dicZoneMarketPrice_ZNL_YS = {} # USD/kWh
        
        self.dicZoneProcCostVarGen_ZNL_YS = {}      # M.USD
        self.dicZoneProcCostAnnFixed_ZNL_YS = {}    # M.USD
        self.dicZoneProcCostAnnFixedOff_ZNF_YS = {}    # M.USD
        
        self.dicAnnualFixCost_YS = {}
        self.dicAnnualVarCost_YS = {}
        
        return
    



    
