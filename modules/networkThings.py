import netifaces as ni
import os

from databaseThings import *

if os.name == "nt":
	import winreg as wr

class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class networkThings:

	def __init__(self):
		pass

	def clear(self):
		os.system("cls" if os.name == "nt" else "clear")

	def chooseIface(self):
		ifaces2 = ni.interfaces()
		ifaces = []
		for iface in ifaces2:
			device = ni.ifaddresses(iface)
			if ni.AF_INET in device.keys():
				ifaces.append(iface)
		choosed_iface = 0

		while(choosed_iface not in range(1, len(ifaces) + 1)):
			self.clear()
			print(f"{bgcolors.WARNING}INTERFACES{bgcolors.ENDC}".center(os.get_terminal_size()[0]))

			for index, iface in enumerate(ifaces):
				device = ni.ifaddresses(iface)

				if os.name == "nt":
					iface = str(self.ifaceNameFromGuid(iface))
				# print(f"{index+1}.{iface}", end=" ")

				if ni.AF_INET in device.keys():
					print(f"{index+1}.{iface} (CONNECTED -> {bgcolors.FAIL} {device[ni.AF_INET][0]['addr']}) {bgcolors.ENDC}", end="")
				print()
			choosed_iface = int(input("Choose: "))

		ip = ni.ifaddresses(ifaces[choosed_iface - 1])[2][0]["addr"]
		netmask = ni.ifaddresses(ifaces[choosed_iface - 1])[2][0]["netmask"]
		interface = ifaces[choosed_iface - 1]

		databaseThings().setConfig('ip', ip)
		databaseThings().setConfig('netmask', netmask)
		databaseThings().setConfig('interface', interface)

	def ifaceNameFromGuid(self, iface_guid):
		reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
		reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
		iface_name_real = ""
		try:
			reg_subkey = wr.OpenKey(reg_key, iface_guid + r'\Connection')
			iface_name_real = wr.QueryValueEx(reg_subkey, 'Name')[0]
		except FileNotFoundError:
			pass
		
		if iface_name_real:
			return iface_name_real
		else:
			return iface_guid