import os
import time

class sleep10:
    test_name = "Sleep 10"
    test_description = "Sleep for 10 seconds"
    nCPUs = 1
    dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(10) 
        result.result = "PASSED"
        return 0
        
