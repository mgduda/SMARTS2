import os
import time

"""
Simple test that will be used to test dependencies. This test will always pass; however, it should
never be ran as sleep5Err *will always* fail; therefore, it should not be scheduled. 
"""

class sleep2DepErr:
    test_name = "Sleep 2 Dep on Sleep5Err"
    test_description = "Sleep for 2 seconds but dependent on sleep5Err"
    nCPUs = 1
    dependencies = ['sleep5Err']

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(2) 
        result.result = "PASSED"
        result.msg = "Sleep2DepErr successfully completed (But it shouldn't have been ran)"
        return 0
        
