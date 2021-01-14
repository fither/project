#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''

TO DO

--- (?) check for apps ( make dependencies )
--- (+) copy exploit/shellcode file to tmp directory --> download 
--- edit exploit/shellcode
--- (+) seperate e/s options
--- (+) info banner (current class show)
--- (+) add dirbuster/gobuster (web content discovery)
--- add ftp crack
--- add ssh crack
--- (+) seperate functions
--- (+) use sqlite3
--- add MITM 3:)
--- Use socket level programming...
--- (+) Add windows admin check

'''

import sys
import time

sys.path.append('./modules/')

from checkThings import *
from showThings import *

if checkThings().OS() == "linux":
    checkThings().uid()
elif checkThings().OS() == "windows":
    checkThings().uid()

## check needed modules
showThings().clear()
checkThings().modules()
# print("CHECKING REQUIRES".center(os.get_terminal_size()[0], "*"))

from vulnThings import *
from nmapThings import *
from networkThings import *
from databaseThings import *
from gobusterThings import *
from ftpThings import *

def main(): 

    check = checkThings()
    myNmap = nmapThings()
    show = showThings()
    vuln = vulnThings()
    network = networkThings()
    db = databaseThings()
    gb = gobusterThings()
    ftp = ftpThings()

    ## check tables for existens 
    db.checkTables()

    ## clear tables for clear start :)
    clearTables = input("Clear All Tables?(y/n)\nAnswer: ")
    if clearTables == "y" or clearTables == "Y":
        db.clearTables()

    ## check wordlist files
    check.findWordlists()

    ## check exploit/shellcode files
    check.findCsvExploits()
    check.findCsvShellcodes()

    print()
    input("Press enter to continue.")

    try:
        while True:
            show.clear()
            show.banner()
            answer = show.menu("main")

            if(answer == "1"):
                show.clear()
                isIpFormatTrue = False
                while(isIpFormatTrue != True):
                    print("Enter IP Address(example: 192.168.1.15 [default: 127.0.0.1]) [0 to back]")
                    ip = input("IP: ")
                    if not ip:
                        ip = '127.0.0.1'
                    elif ip == "0":
                        break
                    isIpFormatTrue = check.IP(ip)
                if isIpFormatTrue:
                    db.setConfig("ip", ip)
                    myNmap.scanHost(ip)
            elif answer == "2" :
                show.clear()
                network.chooseIface()
                while True:
                    show.clear()
                    show.info()
                    print("Scanning for hosts...")
                    myNmap.discoverHosts()
                    discoveredHosts = db.getDiscoveredHosts()
                    show.discoveredHosts(discoveredHosts)
                    print()	
                    print("Choose a host to scan")
                    print("0 to back, 00 to rescan)")
                    # print("start-end for multiple scan (like 1-5)")
                    choose = input("Host: ")
                    if choose == "0":
                        break
                    elif choose == "00":
                        continue
                    elif int(choose) in range(1, len(discoveredHosts) +1):
                        ip = discoveredHosts[int(choose) - 1][0]
                        show.clear()
                        myNmap.scanHost(ip)
                        break
                    else:
                        print("Please choose from list")
                        time.sleep(0.5)
            elif answer == "3":
                show.clear()
                print("Discovered Hosts".center(os.get_terminal_size()[0], "*"))
                scannedHosts = db.getScannedHosts()
                scannedHosts = [host[0] for host in scannedHosts]
                if len(scannedHosts) > 0:
                    host = int(show.listing(scannedHosts))
                    if host not in range(1, len(scannedHosts) + 1):
                        continue
                    ip = scannedHosts[host - 1]
                    while True:
                        show.clear()
                        show.infoAboutHost(ip)
                        answer = show.menu("discovered")
                        if answer == "0":
                            break
                        elif answer == "1":
                            db.setExploits(ip, vuln.searchExploits(db.getMachine(ip)))
                        elif answer == "2" :
                            db.setShellcodes(ip, vuln.searchShellcodes(db.getMachine(ip)))
                        elif answer == "3":
                            show.vulns(db.getExploits(ip))
                            input("Press enter to continue")
                        elif answer == "4":
                            show.vulns(db.getShellcodes(ip))
                            input("Press enter to continue")
                        else:
                            print("You choose wrong")
                            time.sleep(0.5)
                    time.sleep(0.5)
                else:
                    print("Not scanned any host yet")
                    time.sleep(0.5)
            elif answer == "4":
                while True:
                    show.clear()
                    print("EXTRA".center(os.get_terminal_size()[0], "*"))
                    answer = show.menu("extra")
                    if answer == "0":
                        break
                    elif answer == "1":
                        # ssh
                        pass
                    elif answer == "2":
                        # http
                        machines = db.getMachinesThatHas("http")
                        if len(machines) > 0:
                            for index, machine in enumerate(machines):
                                print(f"{index+1}-) {machine['ip']} - {machine['port']} - {machine['name']}")
                            answer = input("Choose: ")
                            if answer == "0":
                                break
                            elif int(answer) in range(1, len(machines) + 1):
                                ip = machines[int(answer)-1]['ip']
                                port = machines[int(answer)-1]['port']
                                try:
                                    dirs = gb.findDirs(ip, port, db.getWordlist("common"))
                                    if len(dirs) > 0:
                                        db.addDirectories(ip, dirs)
                                    else:
                                        print("no directory found")
                                        input()
                                    time.sleep(0.5)
                                except:
                                    pass
                            else:
                                pass
                        else:
                            print("No host found that has webserver")
                            time.sleep(0.5)
                    elif answer == "3":
                        # ftp
                        machines = db.getMachinesThatHas("ftp")
                        if len(machines) > 0:
                            for index, machine in enumerate(machines):
                                print(f"{index+1}-) {machine['ip']} - {machine['port']} - {machine['name']}")
                            answer = input("Choose: ")
                            if answer == "0":
                                break
                            elif int(answer) in range(1, len(machines) + 1):
                                ip = machines[int(answer)-1]['ip']
                                port = machines[int(answer)-1]['port']
                                name = machines[int(answer)-1]['name']

                                print(f"Checking for anonymous login on {ip}")

                                if ftp.checkAnonymousLogin(ip, port):
                                    print(f"Anonymous login is allowed")
                                    db.addCred(ip, proto, port, "", "")
                                else:
                                    print(f"Anonymous login is not allowed")
                                    username = input("please enter username for bruteforcing: ")

                                    if username:
                                        result = ftp.bruteForce(ip, port, username, db.getWordlist('rockyou.txt'))
                                        if result:
                                            username = result[0]
                                            password = result[1]

                                            db.addCred(ip, name, port, username, password)
                                            ftp.listFiles(host=ip, port=port, username=username, password=password)
                                            time.sleep(0.5)
                                            break
                                        else:
                                            print(f"creds could not found :/")
                                            time.sleep(0.5)
                                            break
                                    else:
                                        time.sleep(0.5)
                                        break
                        else:
                            print("No host found that has ftp")
                            time.sleep(1)
                            break
                    else:
                        pass
            else:
                print("Please choose from list")
                time.sleep(0.5)

    except ValueError:
    	print("\nYou entered wrong")
    except KeyboardInterrupt:
    	print("\n(ctrl + c detected)\nExiting")
    except nmap.nmap.PortScannerError as err:
        print(f"\nNmap Error :/ -> {err}")
    # except Exception as e:
    # 	print("\n"+str(e))

if __name__ == "__main__":
	main()