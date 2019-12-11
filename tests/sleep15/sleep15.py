import os
import time

class sleep15:
    test_name = "Sleep 15"
    test_description = "Sleep for 15 seconds"
    nCPUs = 1
    dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(15) 
        result.result = "PASSED"
        return 0
        
