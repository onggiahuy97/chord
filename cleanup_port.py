import socket
import psutil
import time
from typing import List

def is_port_in_use(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def find_process_by_port(port: int) -> List[psutil.Process]:
    """Find all processes using the specified port."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def cleanup_port(port: int) -> None:
    """Kill processes using the specified port."""
    if is_port_in_use(port):
        processes = find_process_by_port(port)
        for proc in processes:
            try:
                print(f"Killing process {proc.pid} ({proc.name()}) using port {port}")
                proc.terminate()  # Try graceful termination first
                proc.wait(timeout=3)  # Wait for the process to terminate
            except psutil.TimeoutExpired:
                print(f"Force killing process {proc.pid}")
                proc.kill()  # Force kill if graceful termination fails
            except psutil.NoSuchProcess:
                pass
        time.sleep(0.1)  # Small delay to ensure port is released

def cleanup_ports(start_port: int = 5000, end_port: int = 5010) -> None:
    """Clean up a range of ports."""
    print(f"Cleaning up ports {start_port}-{end_port}")
    for port in range(start_port, end_port + 1):
        if is_port_in_use(port):
            print(f"\nPort {port} is in use")
            cleanup_port(port)
        else:
            print(f"Port {port} is free")

def check_ports_status(start_port: int = 5000, end_port: int = 5010) -> None:
    """Check and display the status of ports."""
    print("\nCurrent port status:")
    for port in range(start_port, end_port + 1):
        status = "in use" if is_port_in_use(port) else "free"
        print(f"Port {port}: {status}")

if __name__ == "__main__":
    try:
        # Clean up ports
        cleanup_ports()
        
        # Check final status
        check_ports_status()
        
        print("\nPort cleanup completed successfully")
        
    except Exception as e:
        print(f"\nError during cleanup: {e}")