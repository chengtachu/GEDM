#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Define process(technology) class
#

from numpy import zeros


#------------ technology/process -------------
# basic process definition at country level
class ProcessAssump:
    """ process assumption class  """

    # this class for creating objects at both country and zone level
    # country level is used for general assumption initiation
    # zone level inherit the data from country assumptions
    # renewable options is split by CF class
    # the zonal modelling results are kept in this class
    # be aware of the same sProcessName of renewables with different CF class
    
    def __init__(self, **kwargs):
        self.sProcessName = str( kwargs["ProcessName"] )
        self.sProcessType = str( kwargs["ProcessType"] )
        self.sProcessFullName = str( kwargs["ProcessFullName"] )
        self.sFuel = str( kwargs["Fuel"] )
        self.sOperationMode = str( kwargs["OperationMode"] )    # Dispatch, NonDispatch, LimitDispatch, Storage
        self.bCCS = int( kwargs["CCS"] )
        self.bAS_T1 = int( kwargs["AS_T1"] )
        self.bAS_T2 = int( kwargs["AS_T2"] )
        self.bAS_T3 = int( kwargs["AS_T3"] )
        
        # technical assumption (country level)
        self.iUnitCapacity = 0                  # MW
        self.fGrossEff_YS = zeros( int(kwargs["iYS"]) )         # 0-1
        self.fMinLoad_YS = zeros( int(kwargs["iYS"]) )          # 0-1
        self.fRampRate_YS = zeros( int(kwargs["iYS"]) )         # %P/Min
        self.fEquAvailFactor_YS = zeros( int(kwargs["iYS"]) )   # 0-1   # CF already accout for availability for renewables
        self.fAuxiliaryCon_YS = zeros( int(kwargs["iYS"]) )     # 0-1  # own use
        self.fCaptureRate_YS = zeros( int(kwargs["iYS"]) )      # 0-1, for CCS
        self.fDuration_YS = zeros( int(kwargs["iYS"]) )         # hours, for storage
        
        # cost assumption (country level)
        self.fCAPEX_YS = zeros( int(kwargs["iYS"]) )            # USD/kW
        self.fOPEX_YS = zeros( int(kwargs["iYS"]) )             # USD/kW
        self.fVarOPEX_YS = zeros( int(kwargs["iYS"]) )          # USD/kWh
        self.fLifetime = 0             # Year
        self.fVarOM = 0                # USD/kWh
        self.fDiscount = 0.05          # 0-1
        
        self.fAnnualCapex = zeros( int(kwargs["iYS"]) )      # (M.USD / yr.MW)
        self.fAnnualFixedCost = zeros( int(kwargs["iYS"]) )  # (M.USD / yr.MW)
        
        # fixed new build of dispatchable units (country level)
        self.dicProcDispFixedNewBuild = {}    # MW
        
        ### additional parameters (only for on renewable techs, and storage)        
        # renewable zonal capacity and limit by class
        self.iCFClass = 0
        self.fREDevLimit = 0        # MW, overall capacity develoment limit
        self.fREExistCap = 0        # MW, capacity of existing units
        self.fPVLandLimit = 0       # km2, available area for all solar tech
                
        self.fRECF_TS = []          # 0-1, CF for dispatch operatoin
        self.fRECF_CEP = []         # 0-1, CF for capacity expansion
        self.fRECF_CEP_RT = []      # 0-1, Cf for testing extreme cases in CE, update in each period
        self.fRECF_8760 = []        # 0-1, original annual hourly CF data

        self.fBaseDispCF_288 = None # 0-1, original annual hourly CF data

        #### modelling results
        self.dicProcNewBuild_YS = {}       # MW
        self.dicProcAccCapacity_YS = {}    # MW

        return


# technical assumption for the process in a zone
class ZoneProcess():
    """ zonal process class  """

    def __init__(self, **kwargs):
        
        self.sCompany = ""
        self.iZoneProcAssumIndex = 0
        self.sProcessName = str( kwargs["sProcessName"] )
        self.sProcessID = str( kwargs["sProcessID"] )
        self.sProcessType = ""
        self.sFuel = ""
        self.sOperationMode = ""
        self.bCCS = 0
        
        self.iOperatoinStatus_TS_YS = None  # 0:shutsown  1:generating  2:commited
            
        self.iCapacity = 0          # MW
        self.fGrossEff = 0          # 0-1
        self.fMinLoad = 0           # 0-1
        self.fRampRate = 0          # %P/Min
        self.fEquAvailFactor = 0    # 0-1
        self.fAuxiliaryCon = 0      # 0-1  # own use
        self.fCaptureRate = 0       # 0-1
        self.fDuration = 0          # hours
        
        self.iCommitTime = 0        # year
        self.iDeCommitTime = 0      # year
        
        self.iCFClass = 0
                
        ''' ---- derived assumptions ---- '''
        # fDeratedCapacity          (MW)
        # fAnnualCapex              (M.USD / yr)
        # fAnnualFixedCost          (M.USD / yr)
        # fvarOMCost                (USD/kWh)  
                    
        # iCFClass                  CF tranche class for renewables
        
        # fASMax_T1    # MW, max capacity for first tier ancillary service
        # fASMax_T2    # MW, max capacity for second tier ancillary service
        # fASMax_T3    # MW, max capacity for third tier ancillary service

        return
 
    



