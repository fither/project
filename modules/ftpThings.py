from ftplib import FTP

###### make it faster
# list files
# check for write permission
## add upload/download file/s option

class ftpThings:
	def __init__(self):
		pass

	def checkAnonymousLogin(self, host):
		try:
			ftp = FTP(host)
			ftp.login()
			ftp.quit()
			return True
		except:
			return False

	def login(self, host, username, password):
		try:
			ftp = FTP(host)
			ftp.login(username, password)
			ftp.quit()
			print(f"username: {username}, password: {password} worked")
			# if worked, username & password creds are true
		except:
			# creds are wrong
			print(f"username: {username}, password: {password} not worked")
			pass

	def bruteForce(self, host, username, wordlist):
		try:
			for word in wordlist:
				word = word.strip()
				self.login(host, username, word)
		except Exception as e:
			print(e)
			# pass

	def listFiles(self, host, username='', password=''):
		ftp = FTP(host)

		if username and password:
			ftp.login(username, password)

		else:
			ftp.login()

		files = ftp.nlst(ftp.pwd())
		if files:
			for file in files:
				if int(len(ftp.nlst(ftp.pwd() + file)) > 0):
					print(f"file found -> {file}")
				else:
					print(f"folder found -> {file}")

				print(f"object {file} len -> {len(ftp.nlst(ftp.pwd() + file))}")
		else:
			print("no file found")
def main():
	isAnonymousAllowed = False

	host = "localhost"

	wordlist = ["sifre", "parola", "password", "pwd1234", "12356", "123456789", "ftptest123"]


	print(f"Checking for anonymous login on {host}")

	isAnonymousAllowed = ftpThings().checkAnonymousLogin(host)

	if isAnonymousAllowed:
		print("anonymous login is allowed")

		print("looking for files")

		ftpThings().listFiles(host)

	else:
		print("anonymous login is not allowed")

		print("testing ftptest user")

		ftpThings().listFiles(host, "ftptest", "ftptest123")



	# ftpThings().ftpBruteForce("localhost", "ftptest", wordlist)

if __name__ == "__main__":
	main()