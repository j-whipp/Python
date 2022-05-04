#Purpose: Obtain host's default route(primary NIC) ipv4 address using only stdlibs. Can be accomplished easier with imported libraries
#Sockets are characterized by their domain, type, and transport protocol
#AF_INET = (host,port)..read as bound by host and port.
import socket

#The general idea is to construct an ipv4 address socket, establish a connection to an unreachable destination over UDP, and then grab the ipv4_address addr from the connection parameters.
def get_host_ip():
    """Returns host's default route ipv4_address address."""
    #create a AF_INET(ipv4_address addr family) socket utilizing UDP transport(DGRAM short for datagram), and lastly `0` enforces default protocol subroutines(can be omitted).
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    try:
        #Now attempt to establish a connection utilizing the constructed socket, be sure to use an unreachable destination as to not burden with the LAN/WAN.
        udp_sock.connect(('192.254.254.69',1))
        ipv4_address = udp_sock.getsockname()[0]
    #Throw an exception if loopback addr is returned.
    except Exception:
        ipv4_address = '127.0.0.1'
    finally:
        udp_sock.close()
    return ipv4_address

#make it so if the python module(file) can be called as a script
if __name__ == "__main__":
    import sys
    print(get_host_ip())