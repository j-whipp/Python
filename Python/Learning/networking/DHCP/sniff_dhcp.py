from scapy.all import conf,sniff
sniff(iface=conf.iface, filter="port 68 and port 67", prn=lambda pkt:"%s: " % (pkt.summary())) #sniffs and prints captures in real-time until canceled