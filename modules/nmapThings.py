import nmap

from databaseThings import *

class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class nmapThings:
	def __init__(self):
		self.db = databaseThings()

	def discoverHosts(self):
		getDiscoveredHosts = self.db.getDiscoveredHosts()
		ip = self.db.getConfig("ip")
		netmask = self.db.getConfig("netmask")
		discoveredHosts = []
		discoveredHostsTemp = []
		for row in getDiscoveredHosts:
			discoveredHosts.append(row[0])

		if(netmask == "255.255.255.0"):
			cidr = "24"
		elif(netmask == "255.255.0.0"):
			cidr = "16"
		elif(netmask == "255.0.0.0"):
			cidr = "8"
		elif(netmask == "0.0.0.0"):
			cidr = "4"

		ip_range = ip + "/" + cidr

		nm = nmap.PortScanner()
		##-sn no port, -n no DNS, T4 make it a little faster :)
		nm.scan(hosts=ip_range, arguments='-sn -n -T4')

		for host in nm.all_hosts():
			if host not in discoveredHosts:
				if "mac" in nm[host]["addresses"].keys():
					mac = nm[host]["addresses"]["mac"]
				else:
					## That's us :/
					mac = "FF:FF:FF:FF:FF:FF"
				discoveredHostsTemp.append((host, mac))
		self.db.addHosts(discoveredHostsTemp)

	def scanHost(self, ip, port_range='20-443'):
		nm = nmap.PortScanner()
		print(f"Scanning IP address: {bgcolors.WARNING} {ip} {bgcolors.ENDC}")
		
		nm.scan(hosts=ip, ports=port_range, arguments="-sC -sV -T4 -O -sT")

		host = []

		if ip in nm.all_hosts():
			for proto in nm[ip].all_protocols():
				ports = nm[ip][proto].keys()
				sorted(ports)
				for port in ports:
					product = nm[ip][proto][port]['product']
					version = nm[ip][proto][port]['version']
					name = nm[ip][proto][port]['name']
					extrainfo = nm[ip][proto][port]['extrainfo']

					host.append((ip, port, name, product, extrainfo, version))
			self.db.addScan(host)
			print("Scan completed")
		else:
			print("can not reach host")