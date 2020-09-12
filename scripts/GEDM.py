#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Main function interface
#

from time import strftime, localtime

import cls_instance
import md_main


if __name__ == '__main__':
        
    # create an instance of a market, and import main configurations
    instance = cls_instance.Instance()
    print(strftime("%H:%M:%S", localtime()) + " instance created")

    # import related inputs at country level
    instance.get_CountryAssumption()
    print(strftime("%H:%M:%S", localtime()) + " region and country assumption imported")

    # import related inputs at market level
    instance.get_MarketSettings()
    print(strftime("%H:%M:%S", localtime()) + " market assumption imported")

    # import related inputs at zone level
    instance.get_ZoneAssumption()
    print(strftime("%H:%M:%S", localtime()) + " market and zone data imported")
    
    # loop for each market instance and run the market instances
    for objMarket in instance.lsMarket:
        md_main.main_function(instance, objMarket)
        
    print(strftime("%H:%M:%S", localtime()) + " all modelling problems processed")

