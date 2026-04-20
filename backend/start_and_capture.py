#!/usr/bin/env python
import subprocess
import sys
import os
import time

def run_command(cmd, description):
    print(f"\n=== {description} ===")
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Give the process some time to run
        time.sleep(3)
        
        stdout, stderr = process.communicate(timeout=5)
        
        if stdout:
            print("=== Standard Output ===")
            print(stdout.strip())
        
        if stderr:
            print("=== Standard Error ===")
            print(stderr.strip())
        
        print(f"Return code: {process.returncode}")
        
        return process.returncode
        
    except subprocess.TimeoutExpired:
        print(f"ERROR: Command timed out")
        try:
            process.kill()
            time.sleep(0.5)
        except:
            pass
        return -1
        
    except Exception as e:
        print(f"ERROR: {e}")
        return -2

if __name__ == "__main__":
    print("Starting backend server startup diagnostic")
    print("=" * 60)
    
    # Test 1: Simple Python execution
    run_command("python extremely_simple.py", "Simple Python execution test")
    
    # Test 2: Debug system check
    run_command("python debug_system.py", "System debug test")
    
    # Test 3: Direct run attempt
    run_command("python direct_run.py 2>&1", "Direct backend start attempt")
    
    print("\n" + "=" * 60)
    print("Diagnostic completed")
