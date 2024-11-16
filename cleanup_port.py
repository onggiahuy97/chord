import os
import subprocess

def kill_ports(start_port, end_port):
    for port in range(start_port, end_port + 1):
        try:
            # Get the process ID (PID) of the process using the port
            result = subprocess.run(
                ["lsof", "-i", f":{port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if any process is running on the port
            if result.stdout:
                lines = result.stdout.splitlines()
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        # Kill the process by PID
                        os.kill(int(pid), 9)
                        print(f"Killed process {pid} on port {port}")
        except Exception as e:
            print(f"Error handling port {port}: {e}")

# Kill all processes on ports between 5000 and 5010
kill_ports(5000, 5010)
