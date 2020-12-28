import os

from vulnThings import *

class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class showThings:

	def __init__(self):
		self.menuItemsMain = ["Scan a host manually", "Discover LAN", "List discovered hosts", "Extra"]
		self.menuItemsDiscovered = ["Scan Exploits", "Scan Shellcodes", "Show Exploits", "Show Shellcodes"]
		self.menuItemsExtra = ["SSH", "Web", "FTP"]
		pass

	def clear(self):
		os.system("cls" if os.name == "nt" else "clear")

	def banner(self):
		ascii_banner = ""
		ascii_banner += " _____ _ _____ _   _ \n"
		ascii_banner += "|  ___/ |_   _| | | |\n"
		ascii_banner += "| |_  | | | | | |_| |\n"
		ascii_banner += "|  _| | | | | |  _  |\n"
		ascii_banner += "|_|   |_| |_| |_| |_|\n"
		ascii_banner += "                     \n"
		print(ascii_banner)

	def infoAboutHost(self, ip):
		print("*"*os.get_terminal_size()[0])
		print()
		print(f"Machine ip: {ip}")
		print(f"Open ports: {len(databaseThings().getMachine(ip))}")
		print(f"Founded exploits: {len(databaseThings().getExploits(ip))}")
		print(f"Founded shellcodes: {len(databaseThings().getShellcodes(ip))}")
		print()
		print("*"*os.get_terminal_size()[0])

	def info(self):
		print("*"*os.get_terminal_size()[0])
		print()
		print(f"current ip: {databaseThings().getConfig('ip')}")
		print(f"current interface : {databaseThings().getConfig('interface')}")
		print(f"current netmask = {databaseThings().getConfig('netmask')}")
		print()
		print("*"*os.get_terminal_size()[0])

	def menu(self, section):

		if section == "main":
			items = self.menuItemsMain
		elif section == "discovered":
			items = self.menuItemsDiscovered
		elif section == "extra":
			items = self.menuItemsExtra
		else:
			items = ["nothing"]

		for index, item in enumerate(items):
			print(f"{index+1}-){item}")
		return input("choose: ")

	def listing(self, items):
		for index, item in enumerate(items):
			print(f"{index+1}-){item}")
		return input("choose: ")

	def discoveredHosts(self, hosts):
		for index, host in enumerate(hosts):
			ip = host[0]
			mac = host[1]
			isScanned = host[2]
			print(f"{index+1}-){ip}", end=" ")
			if isScanned == "1":
				print("(Scanned already)", end=" ")
			else:
				print("(Not Scanned)", end=" ")

			if mac == "FF:FF:FF:FF:FF:FF":
				print("(That's me :))")
			else:
				print()

	def vulns(self, vulns):
		for index, vuln in enumerate(vulns):
			print(f"{index+1} - {vuln[4]}")