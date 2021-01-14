import sqlite3

class databaseThings:
	def __init__(self):
		self.dbName = "test.db"
		self.discoveredHostsTable = "discoveredHosts"
		self.scannedHostsTable = "scannedHostsDetails"
		self.configTable = "configs"
		self.exploitsTable = "exploits"
		self.shellcodesTable = "shellcodes"
		self.wordlistsTable = "wordlists"
		self.webDirectoriesTable = "webdirectories"
		self.credsTable = "creds"

	def getTables(self):
		self.tables = [
			[self.discoveredHostsTable, ["ip", "mac", "isScanned"]],
			[self.scannedHostsTable, ["ip", "port", "name", "product", "extra_info", "version"]],
			[self.configTable, ["name", "path"]],
			[self.exploitsTable, ["ip", "port", "exploit_name", "path", "desc"]],
			[self.shellcodesTable, ["ip", "port", "shellcode_name", "path", "desc"]],
			[self.wordlistsTable, ["name", "path"]],
			[self.webDirectoriesTable, ["ip", "port", "path"]],
			[self.credsTable, ["ip", "proto", "port", "username", "password"]]
		]

		return self.tables

	def checkTables(self):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		tables = self.getTables()

		for table in tables:
			tableName = table[0]
			tableColumns = table[1]
			
			##OperationalError -> table or column on table not exist :/	
			try:
				c.execute(f"SELECT * FROM {tableName}")
			except sqlite3.OperationalError as err:				
				if "no such column" in str(err):
					c.execute(f"DROP TABLE {tableName}")
				c.execute(f"CREATE TABLE {tableName} ({' text,'.join(tableColumns)} text)")

		conn.commit()
		conn.close()

	def clearTables(self):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		tables = self.getTables()

		for table in tables:
			tableName = table[0]
			c.execute(f"DELETE FROM {tableName}")

		conn.commit()
		conn.close()

	def addHosts(self, hosts):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		for host in hosts:
			ip = host[0]
			mac = host[1]
			c.execute(f"INSERT INTO {self.discoveredHostsTable} VALUES (?,?,?)", (ip, mac, '0'))

		conn.commit()
		conn.close()

	def addScan(self, host):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		ip = host[0][0]
		print(ip)

		## mark as scanned on database
		c.execute(f"UPDATE {self.discoveredHostsTable} SET isScanned='1' WHERE ip='{ip}'")

		for info in host:
			ip = info[0]
			port = info[1]
			name = info[2]
			product = info[3]
			extra_info = info[4]
			version = info[5]

			##check for port existens
			if len(c.execute(f"SELECT ip, port FROM {self.scannedHostsTable} WHERE ip=? AND port=?", (ip, port)).fetchall()) <= 0:
				c.execute(f"INSERT INTO {self.scannedHostsTable} VALUES (?,?,?,?,?,?)", (ip, port, name, product, extra_info, version))

		conn.commit()
		conn.close()

	def getIdFromIP(self, ip):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		for row in c.execute(f"SELECT rowid, ip FROM {self.discoveredHostsTable} WHERE ip=? LIMIT 1", (ip)):
			_id = row['rowid']

		conn.commit()
		conn.close()

		return _id

	def getDiscoveredHosts(self):
		discoveredHosts = []

		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		for row in c.execute(f"SELECT ip, mac, isScanned FROM {self.discoveredHostsTable}"):
			discoveredHosts.append(row)

		conn.commit()
		conn.close()
		return discoveredHosts

	def getScannedHosts(self):
		scannedHosts = []
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()
		for row in c.execute(f"SELECT ip, mac, isScanned FROM {self.discoveredHostsTable}"):
			if row[2] == "1":
				scannedHosts.append(row)
		conn.commit()
		conn.close()
		return scannedHosts

	def setConfig(self, name, path):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()
		if len(c.execute(f"SELECT name, path FROM {self.configTable} WHERE name='{name}'").fetchall()) > 0:
			c.execute(f"UPDATE {self.configTable} SET path='{path}' WHERE name='{name}'")
		else:
			c.execute(f"INSERT INTO {self.configTable} VALUES (?,?)", (name, path))
		conn.commit()
		conn.close()

	def getConfig(self, name):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()
		result = c.execute(f"SELECT name, path FROM {self.configTable} WHERE name='{name}'").fetchone()
		conn.commit()
		conn.close()
		return str(result[1])

	def setWordlist(self, name, path):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()
		if len(c.execute(f"SELECT name, path FROM {self.wordlistsTable} WHERE name='{name}'").fetchall()) > 0:
			c.execute(f"UPDATE {self.wordlistsTable} SET path='{path}' WHERE name='{name}'")
		else:
			c.execute(f"INSERT INTO {self.wordlistsTable} VALUES (?,?)", (name, path))
		conn.commit()
		conn.close()

	def getWordlist(self, name):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()
		result = c.execute(f"SELECT name, path FROM {self.wordlistsTable} WHERE name LIKE '%{name}%'").fetchone()
		conn.commit()
		conn.close()
		return str(result[1])

	def getMachine(self, ip):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		machine = []

		for row in c.execute(f"SELECT ip, port, name, product, extra_info, version FROM {self.scannedHostsTable} WHERE ip='{ip}'"):
			machine.append(row)

		conn.commit()
		conn.close()

		return machine

	def setExploits(self, ip, exploits):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		for exploit in exploits:
			c.execute(f"INSERT INTO {self.exploitsTable} VALUES(?,?,?,?,?)", (ip, exploit[0], exploit[1], exploit[2], exploit[3]))
		conn.commit()
		conn.close()

	def setShellcodes(self, ip, shellcodes):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		for shellcode in shellcodes:
			c.execute(f"INSERT INTO {self.shellcodesTable} VALUES(?,?,?,?,?)", (ip, shellcode[0], shellcode[1], shellcode[2], shellcode[3]))
		conn.commit()
		conn.close()

	def getExploits(self, ip):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		exploits = []

		for row in c.execute(f"SELECT ip, port, exploit_name, path, desc FROM {self.exploitsTable} WHERE ip='{ip}'"):
			exploits.append(row)

		conn.commit()
		conn.close()

		return exploits

	def getShellcodes(self, ip):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		shellcodes = []

		for row in c.execute(f"SELECT ip, port, shellcode_name, path, desc FROM {self.shellcodesTable} WHERE ip='{ip}'"):
			shellcodes.append(row)

		conn.commit()
		conn.close()

		return shellcodes

	def getMachinesThatHas(self, service):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		machines = []

		for row in c.execute(f"SELECT ip, port, name FROM {self.scannedHostsTable} WHERE name LIKE '%{service}%'"):
			machine = {
				"ip": row[0],
				"port": row[1],
				"name": row[2]
			}
			machines.append(machine)
		conn.commit()
		conn.close()

		return machines

	def addDirectories(self, ip, paths):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		dirs = self.getDirectories(ip)

		for path in paths:
			if path not in dirs:
				c.execute(f"INSERT INTO {self.webDirectoriesTable} VALUES(?,?)", (ip, path))

		conn.commit()
		conn.close()

	def getDirectories(self, ip):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		dirs = []

		for row in c.execute(f"SELECT ip, path FROM {self.webDirectoriesTable} WHERE ip='{ip}'"):
			dirs.append(row[1])

		conn.commit()
		conn.close()

		return dirs

	def addCred(self, ip, proto, port, username, password):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		creds = getCreds(ip, proto, port)

		credExist = False

		for cred in creds:
			if username == cred[3] and password == cred[4]:
				credExist = True

		if credExist:
			# already found
			pass
		else:
			c.execute(f"INSERT INTO {self.credsTable} VALUES(?, ?, ?, ?, ?)", (ip, proto, port, username, password))

		conn.commit()
		conn.close()

	def getCreds(self, ip, proto, port):
		conn = sqlite3.connect(self.dbName)
		c = conn.cursor()

		creds = []

		for row in c.execute(f"SELECT ip, proto, port, username, password FROM {self.credsTable} WHERE ip='{ip} and proto='{proto}' and port='{port}'"):
			creds.append(row)

		conn.commit()
		conn.close()

		return creds
