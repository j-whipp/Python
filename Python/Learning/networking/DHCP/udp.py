#DORA
#Discovery Offer Request Ack
#A DHCP client can only receive OFFER,ACK,NACK
#refer to RFC 2132 subsection 4.4 for client behavior/states

#using scapy we can build the DHCPDISCOVERY packet, must build upon each layer combining them with `/`
#Using Wikipedia or the official RFCs as reference we construct the packets
import random
from scapy.all import Ether,IP,UDP,BOOTP,DHCP,conf,srp1,Ether
conf.checkIPaddr = False

#Build the Discover packet
discover_packet = (
    Ether(dst="ff:ff:ff:ff:ff:ff", src=Ether().src, type=0x0800) / #0x0800 denotes EtherType, this case IPv4 encapsulation
    IP(src="0.0.0.0", dst="255.255.255.255") /
    UDP(sport=68, dport=67) /
    BOOTP(
        chaddr= Ether().src,
        xid=random.randint(1, 2**32-1),
    ) /
    DHCP(options=[("message-type", "discover"), "end"])
)

#srp1() sends and receives the first answer(packet) at layer 2 only, in this case the answer will be the DHCPOFFER
received_offer = srp1(discover_packet, iface=conf.iface, verbose=False)

if received_offer[BOOTP].xid != discover_packet[BOOTP].xid:
    print('xid mismatch! any arriving DHCPACKS must be dropped')

#construct the request using some info received in the DHCPOFFER
request_packet = (
    Ether(dst="ff:ff:ff:ff:ff:ff", src=Ether().src, type=0x0800) / #0x0800 denotes EtherType, this case IPv4 encapsulation
    IP(src="0.0.0.0", dst="255.255.255.255") /
    UDP(sport=68, dport=67) /
    BOOTP(
        ciaddr = received_offer[BOOTP].yiaddr,
        siaddr = received_offer[DHCP].options[1][1],
        chaddr= Ether().src,
        xid=random.randint(1, 2**32-1),
    ) /
    DHCP(options=[("message-type", "request"), "end"])
)

server_ack_or_nack = srp1(request_packet, iface=conf.iface, verbose=False)

if server_ack_or_nack[DHCP].options[0][1] == 6:
    ack_type = 'NACK'
    print("Received DHCPNACK meaning our request was not acknowledged..likely misconfiguration of the request")

if server_ack_or_nack[DHCP].options[0][1] == 5:
    ack_type = 'ACK'
    print("Received DHCPACK meaning our request was acknowledged..yay")

print('----------------------------------')
print('Putting it all together we have sent a {} packet, then received an offer, used that offer to craft a {}, and received back {}. We can now begin interface configuration using details obtained in the DORA exchange'.format(discover_packet[DHCP].options[0][1],request_packet[DHCP].options[0][1]
,ack_type))
