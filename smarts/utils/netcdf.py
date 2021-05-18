import numpy as np
from netCDF4 import Dataset

""" NetCDF Utilities """

def compare(file1, file2, skip=[]):
    """ compare - take the differences between two NetCDF files. Each numerical field will
    be differenced and the minimum and maximum will be placed in a dictionary indexed by the
    variables name. Each dictionary value for a variable will be tuple of three values, the first
    being a string message of any errors, the second will be the minimum and the third will be the
    maximum.

    Arguments:
        file1 - Path to the first file
        file2 - Path to the second file
       
    Keyword Arguments:
        skip - List - default: [] - List of variables to skip
        
    TODO: Update the messages used here. They're a bit silly and could probably be something else.
    Maybe true or false if there are differences or there are not differences?
    """


    f1 = Dataset(file1, 'r')
    f2 = Dataset(file2, 'r')

    varCompare = {}

    for var in f1.variables:
        if var not in f2.variables:
            varCompare[var] = [None, None, None]
            varCompare[var][0] = "{0} was not found in {1}".format(str(var), str(file1))
            varCompare[var][1] = None
            varCompare[var][2] = None

    for var in f2.variables:
        if var not in f1.variables:
            varCompare[var] = [None, None, None]
            varCompare[var][0] = "{0} was not found in {1}".format(str(var), str(file1))
            varCompare[var][1] = None
            varCompare[var][2] = None

    for var in f1.variables:
        if f1.variables[var].dtype not in ('float32', 'float64', 'int32'):
            varCompare[var] = [None, None, None]
            varCompare[var][0] = "{0} is not a numerical field and will not be compared".format(str(var))
            varCompare[var][1] = None
            varCompare[var][2] = None
            continue

        if var in skip:
            varCompare[var] = [None, None, None]
            varCompare[var][0] = "{0} was not compared as we were told to skip it".format(str(var))
            varCompare[var][1] = None
            varCompare[var][2] = None
            continue

        diff = f1.variables[var][:] - f2.variables[var][:]
        varCompare[var] = [None, None, None]
        varCompare[var][0] = "min max diff for var {0} between {1} and {2}".format(str(var), str(file1), str(file2))
        varCompare[var][1] = np.min(diff)
        varCompare[var][2] = np.max(diff)


    return varCompare
