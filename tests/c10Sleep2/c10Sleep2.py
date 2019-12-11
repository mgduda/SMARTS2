import os
import time

class c10Sleep2:
    test_name = "10 CPUS Sleep 2"
    test_description = "Sleep for 2 seconds and request 10 cpus"
    nCPUs = 10
    dependencies = None

    def run(self, env, result, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(2) 
        result.result = "PASSED"
        return self.status
        
