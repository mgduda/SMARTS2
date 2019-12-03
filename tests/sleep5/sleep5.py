import os
import time

class sleep5:
    test_name = "Sleep 5"
    test_description = "Sleep for 5 seconds"
    nCPUs = 1
    status = None
    dependencies = None

    def run(self, env, src_dir, test_dir, hpc=None, *args, **kwargs):
        time.sleep(5) 
        self.status = "PASSED"
        return self.status
        
