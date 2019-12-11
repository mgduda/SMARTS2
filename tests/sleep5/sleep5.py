import os
import time

class sleep5:
    test_name = "Sleep 5"
    test_description = "Sleep for 5 seconds"
    nCPUs = 1
    dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(5) 
        result.result = "PASSED"
        return 0
        
