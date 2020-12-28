import requests
import os
import time

from databaseThings import *

class gobusterThings:
	def __init__(self):
		self.wordlistUrl = "https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt"

	def findDirs(self, url, port, wordlist):
		print("Scanning dirs/files".center(os.get_terminal_size()[0], "*"))
		dirs = []
		status_codes = [200, 204, 301, 302, 307, 401]
		url = "http://" + url + ":" + port
		try:
			r1 = requests.get(url)
			if r1.ok:
				if os.path.exists(wordlist):
					words = open(wordlist, "r")
					for word in words:
						word = word.strip()
						trying_url = url + "/" + word
						r2 = requests.get(trying_url)
						if r2.status_code in status_codes:
							dirs.append(word)
							print(f"{trying_url.strip()} [{r2.status_code}]")
						else:
							print(" "*int(os.get_terminal_size()[0] - 1), end="\r")
							print(f"{trying_url.strip()}", end="\r")
				else:
					print("wordlist not found")
			else:
				print("website is not reachable")
		except requests.exceptions.ConnectionError as err:
			print(f"can not connect -> {err}")
		return dirs
