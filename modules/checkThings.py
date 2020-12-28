import os
import sys
import time
import subprocess
import ctypes

from databaseThings import *

class checkThings:
	def __init__(self):
		pass

	def OS(self):
		if os.name == "posix":
			return "linux"
		elif os.name == "nt":
			# sys.exit("sorry, it's for linux only (for now :))")
			return "windows"

	def uid(self):
		try:
			if os.getuid() != 0:
				sys.exit("\nOnly root can run this script")
		except AttributeError:
			if ctypes.windll.shell32.IsUserAnAdmin() != 1:
				sys.exit("\nOnly admin can run this script")

	def IP(self, ip):
		splittedIP = ip.split('.')
		if len(splittedIP) == 4:
			if((int(splittedIP[0]) <= 254 and int(splittedIP[0]) >= 0) and 
				(int(splittedIP[1]) <= 254 and int(splittedIP[1]) >= 0) and 
				(int(splittedIP[2]) <= 254 and int(splittedIP[2]) >= 0) and 
				(int(splittedIP[3]) <= 254 and int(splittedIP[3]) >= 0)):
				return True
		return False

	def modules(self):
		print()
		print("Searching for required modules...")

		# moduleList = [["nmap", "python-nmap"], ["sqlite3", "pysqlite3"], ["netifaces", "netifaces"]]

		# for module in moduleList:
		# 	try:
		# 		import module[0]
		# 		print(f"{module[0]} found.")
		# 	except:
		# 		print(f"{module[0]} not found. Installing")
		# 		self.installModule(module[1])

		try:
			import nmap
			print(f"nmap found.")
		except:
			print(f"nmap not found, installing.")
			self.installModule("python-nmap")

		time.sleep(0.5)

		try:
			import sqlite3
			print(f"sqlite3 found.")
		except:
			print(f"sqlite3 not found, installing.")
			self.installModule("pysqlite3")

		time.sleep(0.5)

		try:
			import netifaces
			print(f"netifaces found")
		except:
			print(f"netifaces not found, installing.")
			self.installModule("netifaces")

			# if module[1] not in sys.modules:
			# else:
			time.sleep(0.5)

	def installModule(self, module):
		cmd = sys.executable + " -m pip install " + module
		subprocess.check_call(cmd, shell=True)

		# if hasattr(pip, 'main'):
		# 	pip.main(['install', module])
		# else:
		# 	pip._internal.main(['install', module])

	def findCsvExploits(self):
		print()
		print("Searching for exploits files...")
		time.sleep(0.5)

		csvUrlExploits = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"

		filesPath = str(os.getcwd()) + "/files/csv/"
		possiblePaths = ["/usr/share/exploitdb/", "/opt/exploitdb/", filesPath]

		csvFileExploits = "files_exploits.csv"
		csvPathExploits = ""

		for path in possiblePaths:
			for root, dir, files in os.walk(path):
				if not csvPathExploits and csvFileExploits in files:
					print(f"founded in {root}")
					time.sleep(0.5)
					databaseThings().setConfig('csvPathExploits', root)
					return

		if not csvPathExploits:
			print("exploits file not found, downloading")
			requestExploits = requests.get(csvUrlExploits)
			open(filesPath + csvFileExploits, 'wb').write(requestExploits.content)
			if os.path.exists(filesPath + csvFileExploits):
				print(f"downloaded to {filesPath + csvFileExploits}")
				time.sleep(0.5)
				databaseThings().setConfig('csvPathExploits', filesPath)	
				return

	def findCsvShellcodes(self):
		print()
		print("Searching for shellcodes files...")
		time.sleep(0.5)

		csvUrlShellcodes = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_shellcodes.csv"

		filesPath = str(os.getcwd()) + "/files/csv/"
		possiblePaths = ["/usr/share/exploitdb/", "/opt/exploitdb/", filesPath]

		csvFileShellcodes = "files_shellcodes.csv"
		csvPathShellcodes = ""

		for path in possiblePaths:
			for root, dir, files in os.walk(path):
				if not csvPathShellcodes and csvFileShellcodes in files:
					print(f"founded in {root}")
					time.sleep(0.5)
					databaseThings().setConfig('csvPathShellcodes', root)
					return

		if not csvPathShellcodes:
			print("shellcodes file not found, downloading")
			requestShellcodes = requests.get(csvUrlShellcodes)
			open(filesPath + csvFileShellcodes, 'wb').write(requestShellcodes.content)
			if os.path.exists(filesPath + csvFileShellcodes):
				print(f"downloaded to {filesPath + csvFileShellcodes}")
				time.sleep(0.5)
				databaseThings().setConfig('csvPathShellcodes', filesPath)
				return

	def findWordlists(self):
		print()
		print("Searching for wordlists")
		time.sleep(0.5)

		filesPath = str(os.getcwd()) + "/files/wordlists"
		possiblePaths = ["/usr/share/wordlists/", "/usr/share/dirbuster/wordlists/", filesPath]

		wordlistsFiles = ["rockyou.txt", "common.txt"]
		foundedWordlists = {}

		for path in possiblePaths:
			for root, dir, files in os.walk(path):
				for wordlistFile in wordlistsFiles:
					if wordlistFile in files:
						print(f"founded {wordlistFile} in {root}")
						foundedWordlists[wordlistFile] = root + f"/{wordlistFile}"

		if len(foundedWordlists.items()) > 0:
			for key, value in foundedWordlists.items():
				databaseThings().setWordlist(key, value)
		else:
			print("could not found any wordlist :/")