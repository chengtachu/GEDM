#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Define commodity, time slice and transmission  classes
#


#------------ commodity -------------
class Commodity:
    """ Commodity class """

    def __init__(self, **kwargs):
        self.sCommodityName = str( kwargs["CommodityName"] )
        self.sCategory = str( kwargs["Category"] )
        self.fHeatRate = float(kwargs["HeatRate"])
        self.fEmissionFactor_CO2 = float(kwargs["EmissionFactor_CO2"])  # M.Tonne/PJ = Tonn/GJ
        self.fFuelPrice_YS = list()     # USD/GJ
        return
    

#------------ time slice -------------
class TimeSlice:
    """ time slice class """

    def __init__(self, **kwargs):
        self.sTSIndex = str(kwargs["TSIndex"])
        self.sMonth = str(kwargs["Month"])
        self.sDay = str(kwargs["Day"])
        self.sHour = str(kwargs["Hour"])
        self.iDayIndex = int(kwargs["DayIndex"])
        self.iRepDayInYear = int(kwargs["RepDayInYear"])
        self.iRepHoursInDay = int(kwargs["RepHoursInDay"])
        self.iRepHoursInYear = int(kwargs["RepHoursInYear"])
        return


class DayTimeSlice:
    """ TS day class """

    def __init__(self, **kwargs):
        self.MonthDay = str(kwargs["MonthDay"])
        self.iDayIndex = int(kwargs["iDayIndex"])
        self.lsDiurnalTS = list()  # list of DiurnalTimeSlice objects
        return


class DiurnalTimeSlice:
    """ diurnal time slice class """

    def __init__(self, **kwargs):
        self.sTSIndex = kwargs["sTSIndex"]
        self.iTimeSliceIndex = kwargs["iTimeSliceIndex"]
        self.iRepHoursInYear = kwargs["iRepHoursInYear"]
        self.iRepHoursInDay = kwargs["iRepHoursInDay"]
        self.fValue = 0
        return


#------------ transmission -------------
class Transmission:
    """ transmission class, links between zones  """

    def __init__(self, **kwargs):

        self.sTransID = str( kwargs["From"] ) + "/" + str( kwargs["To"] )
        self.sFrom = str( kwargs["From"] )  # source zone
        self.sTo = str( kwargs["To"] )      # destination zone
        self.fDistance = float( kwargs["Dist"] )    # KM, distance of the link
        self.b2015Conn = int( kwargs["Conn2015"] )  # connection status in base year
        self.fBaseCap = float( kwargs["BaseCap"] )  # base year capacity

        self.dicTransNewBuild_YS = {}       # MW, new capacity by period
        self.dicTransAccCap_YS = {}         # MW, total capacity by period
        
        return

