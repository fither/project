import csv
import time
import os
import requests

from databaseThings import *

class vulnThings:

	def __init__(self):
		self.baseUrl = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/"

	def searchExploits(self, machine):
		csv_path = databaseThings().getConfig("csvPathExploits")
		exploits = []

		filesPathExploits = str(os.getcwd()) + "/files/exploits/"

		for row in machine:
			product = row[3]
			port = row[1]

			if product:
				print(f"searching for {product}")
				infos = product.split(" ")
				with open( csv_path + 'files_exploits.csv', encoding='utf-8') as csv_file:
					csv_reader = csv.reader(csv_file, delimiter=',')
					line_count = 0

					for row in csv_reader:
						if line_count == 0:
							line_count+=1
						else:
							exp_id = row[0]
							exp_file = row[1]
							exp_description = row[2]

							isHave = True
							for word in infos:
								if word.lower() not in exp_description.lower():
									isHave = False

							if isHave:
								exploit = [port, exp_id, exp_file, exp_description]
								exploits.append(exploit)

								nameFileExploit = exp_file.split("/")[-1]
								if os.path.exists(filesPathExploits + nameFileExploit):
									print(f"exploit {nameFileExploit} exist")
								else:
									urlExploit = self.baseUrl + exp_file
									print(f"downloading exploit {nameFileExploit}")
									open(filesPathExploits + nameFileExploit, 'wb').write(requests.get(urlExploit).content)
								time.sleep(0.5)
			else:
				print(f"no info for port: {port}")
		return exploits

	def searchShellcodes(self, machine):
		csv_path = databaseThings().getConfig("csvPathShellcodes")
		shellcodes = []

		filesPathShellcodes = str(os.getcwd()) + "/files/shellcodes/"

		for row in machine:
			product = row[3]
			port = row[1]

			if product:
				print(f"scanning for {product}")
				infos = product.split(" ")

				with open( csv_path + 'files_shellcodes.csv', encoding='utf-8') as csv_file:
					csv_reader = csv.reader(csv_file, delimiter=',')
					line_count = 0

					for row in csv_reader:
						if line_count == 0:
							line_count+=1
						else:
							shl_id = row[0]
							shl_file = row[1]
							shl_description = row[2]

							isHave = True
							for word in infos:
								if word.lower() not in shl_description.lower():
									isHave = False

							if isHave:
								shellcode = [port, shl_id, shl_file, shl_description]
								shellcodes.append(shellcode)

								nameFileShellcode = shl_file.split("/")[-1]
								if os.path.exists(filesPathShellcodes + nameFileShellcode):
									print(f"shellcode {nameFileShellcode} exist")
								else:
									urlShellcode = self.baseUrl + shl_file
									print(f"downloading shellcode {nameFileShellcode}")
									open(filesPathShellcodes + nameFileShellcode, 'wb').write(requests.get(urlShellcode).content)
								time.sleep(0.5)
			else:
				print(f"no info for port: {port}")
		return shellcodes