#
# General Electricity sector Decarbonization Model (GEDM)
# Copyright (C) 2020 Cheng-Ta Chu.
# Licensed under the MIT License (see LICENSE file).
#
# Module note:
# Simple functions for exporting table in CSV format
#

from os import path
from numpy import savetxt


def TableOutputToCSV(tableOutput, sFileName):
    """ export table in CSV file """
    
    # create file
    if not path.exists(sFileName):
        open(sFileName, 'w').close() 

    # save content
    savetxt( sFileName, tableOutput, fmt='%s', delimiter=',', newline='\n')

    return


def TableOutputToCSV_UTF8(tableOutput, sFileName):
    """ export table in CSV file with UTF-8 encoding """
    
    # create file
    if not path.exists(sFileName):
        open(sFileName, 'w').close() 

    # save content
    savetxt( sFileName, tableOutput, fmt='%s', delimiter=',', newline='\n', encoding='utf-8')

    return

