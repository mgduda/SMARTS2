import os
import time

""" 
A small, simple test to test if dependencies are working. It won't be ran if sleep5 is not ran AND
sleep5 does not pass (which sleep5 will always pass)
"""

class sleep2Dep:
    test_name = "Sleep 2 Dep on Sleep5"
    test_description = "Sleep for 2 Seconds dependent on sleep5"
    nCPUs = 1
    dependencies = ['sleep5']

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(2) 
        result.result = "PASSED"
        result.msg = "Sleep2Dep successfully completed"
        return 0
        
