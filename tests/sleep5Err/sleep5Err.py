import os
import time

class sleep5Err:
    test_name = "Sleep 5 Error"
    test_description = "Sleep for 5 seconds and 'Fail'"
    nCPUs = 1
    dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(5) 
        result.result = "FAILED"
        return -1
        
