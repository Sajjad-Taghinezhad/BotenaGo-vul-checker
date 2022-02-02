#!/opt/homebrew/bin/python3
from sys import argv
import requests
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

vulns = []
def vulnCheck(ip,headers):
    for hed in headers: 
        if hed == 'WWW-Authenticate' or hed == 'Server':
                if headers[hed]== 'Basic realm="Broadband Router"' or headers[hed] == 'Boa/0.93.15': 
                    print(Fore.MAGENTA+ip)
                    vulns.append(ip)
                      
def fetch(session, ip):
    ip = ip.replace("\n","")
    url = "http://"+ip
    try:
        with session.get(url,timeout=5) as response:
            vulnCheck(ip,response.headers)
    except:
        print(Fore.RED+"Err:"+ip)
                        
def main(ips):           
    with ThreadPoolExecutor(max_workers=int(argv[1])) as executor:
        with requests.Session() as session:
            executor.map(fetch, [session] * len(ips) , ips )
            executor.shutdown(wait=True)
            f = open(argv[3], "w")
            f.write(str(vulns))
            f.close()
if len(argv) < 4: 
    print(Fore.GREEN+"Usage : ./script.py <number of thread> <input IP list file> <output file>"+Fore.RESET)
    exit(0)          
file = open(argv[2], "r")
ips = file.readlines()
file.close()
print(Fore.CYAN+str(len(ips))+Fore.GREEN+" IPs Found")     
main(ips)
          