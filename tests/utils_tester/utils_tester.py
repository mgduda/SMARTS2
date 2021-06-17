import os
from shutil import copyfile

from smarts.testManager import Test
from smarts.utils import fortran
from smarts.utils import mpas
from smarts.utils import netcdf


class utils_tester(Test):
    test_name = "SMARTS Utility Tester"
    test_description = "Basic tests of the utility functions"
    ncpus = 1

    def edit_namelist(self, namelist, start_time, run_time, do_restart):
        replacements = { 'config_start_time' : start_time,
                         'config_run_duration' : run_time,
                         'config_do_restart' : do_restart}

        fortran.namelist_editor(namelist, replacements)

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        result.result = "PASSED"
        result.msg = "Configuration was correct!"

        namelist = os.path.join(test_dir, 'utils_tester', 'namelist.atmosphere')

        copyfile(namelist, './namelist.atmosphere')
        print("utils_tester: testing utils.fortran.edit_namelist() ...")
        self.edit_namelist('./namelist.atmosphere',
                           "'00:00:00'",
                           "'42_42:42:42'", 
                           "true")


        #
        # testing edit_stream
        #
        print("utils_tester: testing utils.mpas.edit_stream ...")

        replacements = {}
        replacements['restart'] = {'output_interval' : '5_00:00:00'}
        replacements['output'] = {'output_interval' : 'never!', 'filename_template' : "daig-ijlij"}

        stream = os.path.join(test_dir, 'utils_tester', 'streams.atmosphere')
        copyfile(stream, './stream.atmosphere')
        mpas.edit_stream(stream, replacements)

        print("utils_tester: testing check_log ...")
        out_log = os.path.join(test_dir, 'utils_tester', 'log.atmosphere.0000.out')
        crit_log = os.path.join(test_dir, 'utils_tester', 'log.atmosphere.0000.out.crit')

        copyfile(out_log, './log.atmosphere.0000.out')
        copyfile(crit_log, './log.atmosphere.0000.out.crit')

        _, warnings, errors, crits = mpas.check_log(out_log)

        print("utils_tester: testing log.atmosphere.0000.out ...")
        if len(warnings) != 3 or len(errors) != 0 or len(crits) != 0:
            result.result = "FAILED"
            result.msg = "mpas.check_log of {0} was not correct!".format(out_log)
            return
        
        print('utils_tester:', 'Warnings:', len(warnings),
                               'Errors:', len(errors),
                               'Criticals:', len(crits))

        _, warnings, errors, crits = mpas.check_log(crit_log)
        if len(warnings) != 6 or len(errors) != 0 or len(crits) != 1:
            result.result = "FAILED"
            result.msg = "mpas.check_log of {0} was not correct!".format(crit_log)
            return

        print('utils_tester:', 'Warnings:', len(warnings),
                               'Errors:', len(errors),
                               'Criticals:', len(crits))

        #
        # Compare NetCDF files
        #
        netcdf1 = os.path.join(test_dir, 'utils_tester', 'grid.nc')
        netcdfcp = os.path.join(test_dir, 'utils_tester', 'grid.nc')
        compare = netcdf.compare(netcdf1, netcdfcp)
        print(compare)
        for var in compare.keys():
            if compare[var][1] != 0.0 or compare[var][2] != 0.0:
                result.result = "FAILED"
                result.msg = "The netCDF variables has differences"
                return

        result.result = "PASSED"
        result.msg = "SMARTS Utils are all good!"

        return 0
