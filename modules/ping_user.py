import socket
import time
import select
import struct
import sys

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def checksum(data):
    """Calculate ICMP checksum"""
    sum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            w = (data[i] << 8) + data[i + 1]
        else:
            w = data[i] << 8
        sum += w
    
    sum = (sum >> 16) + (sum & 0xFFFF)
    sum = ~sum & 0xFFFF
    return sum

def create_icmp_packet(seq):
    """Create an ICMP echo request packet"""
    icmp_type = 8  # Echo request
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = 12345
    icmp_seq = seq
    
    # Pack header without checksum
    header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    data = b'Hello, World!'  # Payload
    packet = header + data
    
    # Calculate and pack checksum
    icmp_checksum = checksum(packet)
    header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    packet = header + data
    
    return packet

def ping_host(target, timeout=2, count=4):
    """Ping a host using raw sockets"""
    try:
        # Resolve hostname to IP
        ip_address = socket.gethostbyname(target)
        print(f"{Colors.GREEN}Pinging {target} [{ip_address}]{Colors.RESET}")
        
        # Create raw socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError:
            print(f"{Colors.RED}Error: Root/Administrator privileges required for raw sockets{Colors.RESET}")
            print(f"{Colors.RED}Please run as administrator on Windows or with sudo on Linux/Mac{Colors.RESET}")
            return False
        
        sock.settimeout(timeout)
        
        received = 0
        lost = 0
        
        for seq in range(count):
            packet = create_icmp_packet(seq)
            start_time = time.time()
            
            try:
                # Send packet
                sock.sendto(packet, (ip_address, 0))
                
                # Wait for response
                response, addr = sock.recvfrom(1024)
                end_time = time.time()
                
                # Calculate response time
                response_time = (end_time - start_time) * 1000
                
                print(f"{Colors.GREEN}Reply from {addr[0]}: time={response_time:.2f}ms{Colors.RESET}")
                received += 1
                
            except socket.timeout:
                print(f"{Colors.RED}Request timed out for sequence {seq + 1}{Colors.RESET}")
                lost += 1
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.RESET}")
                lost += 1
            
            time.sleep(0.5)  # Small delay between pings
        
        sock.close()
        
        # Summary
        print(f"\n{Colors.GREEN}--- {target} ping statistics ---{Colors.RESET}")
        print(f"Packets: Sent = {count}, Received = {received}, Lost = {lost} ({lost * 100 // count}% loss)")
        
        return lost == 0
        
    except socket.gaierror:
        print(f"{Colors.RED}Error: Could not resolve hostname '{target}'{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        return False

def main():
    print("=" * 50)
    print("         HOST PING TOOL")
    print("=" * 50)
    print( f"{Colors.RED} Made by Quantumroot09 {Colors.RESET}")
    print("=" * 50)
    
    while True:
        target = input(f"\n{Colors.GREEN}ping:{Colors.RESET} ").strip()
        
        if not target:
            print(f"{Colors.RED}Please enter a valid domain or IP address{Colors.RESET}")
            continue
            
        if target.lower() in ['exit', 'quit', 'q']:
            print(f"{Colors.GREEN}Goodbye!{Colors.RESET}")
            break
        
        print()
        ping_host(target)
        print("-" * 50)

def run():
    main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}Goodbye!{Colors.RESET}")
        sys.exit(0)


