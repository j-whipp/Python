import host_ipv4

addr = host_ipv4.get_host_ip()

def get_result(addr):
    """Print result from host_ipv4 module"""
    print("IPV4 addr is {}".format(addr))

get_result(addr)