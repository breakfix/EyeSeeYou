from selenium import webdriver
from argparse import ArgumentParser
import time
import os
import sys

print("""\
    ______          _____       __  __           
   / ____/_  _____ / ___/___  __\ \/ /___  __  __
  / __/ / / / / _ \\__ \/ _ \/ _ \  / __ \/ / / /
 / /___/ /_/ /  __/__/ /  __/  __/ / /_/ / /_/ / 
/_____/\__, /\___/____/\___/\___/_/\____/\__,_/  
      /____/                                  
              v0.2 Matt Johnson @breakfix  
 """)

def path(value):
    # Make path absoloute
    return os.path.abspath(value)

parser = ArgumentParser()
parser.add_argument("-o", dest="out_dir", required=True, type=path,
                        help='Path to export images')
parser.add_argument("-i", dest="input_file", required=True, type=path,
                    help='File being outputted by Masscan to use as input file')
parser.add_argument("--headless", dest="headless", action='store_true',
                    help='Run Chrome in headless mode')
parser.add_argument("--no-masscan", dest="format",
                    help='Read targets from input file instead of running masscan (requires you specify ports to use as argument e.g. --no-masscan 80,443,8080)')
parser.add_argument("--timeout", dest="timeout", default=3,
                    help='Set timeout in seconds (default is 3 seconds)')
parser.add_argument("--proxy", dest="proxy",
                    help='Optionally use a socks4 proxy (specify host and port e.g. --proxy 192.168.1.1:8080')

# Print help if no arguments given
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')

if args.headless:
    chrome_options.headless = True

if args.proxy:
    chrome_options.add_argument("--proxy-server=socks4://" + args.proxy)

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options) 
driver.set_window_size(1024, 768) # set the window size that you need 
driver.set_page_load_timeout(int(args.timeout))

targets = []

if args.format:
    with open(args.input_file, "r") as infile:
        ports = args.format.split(',')
        for line in infile:
            for port in ports:
                target = line.rstrip('\r\n') + ":" + port
                ip = line.rstrip('\r\n')
                if target not in targets:
                    print("Fetching " + "http://" + ip + ":" + port)
                    try:
                        driver.get('http://' + ip + ":" + port)
                        time.sleep(1) # wait for page to fully load
                        driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_http.png'))
                        targets.append(ip + ":" + port)
                    except:
                        print("[!] Something went wrong")
                        targets.append(ip + ":" + port)                
                    print("Fetching " + "https://" + ip + ":" + port)
                    try:
                        driver.get('https://' + ip + ":" + port)
                        time.sleep(1)
                        driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_https.png'))
                        targets.append(ip + ":" + port)
                    except:
                        print("[!] Something went wrong")
                        targets.append(ip + ":" + port)
else:
    while True:
        with open(args.input_file, "r") as infile:
            for line in infile:
                if "Discovered" in line:
                    entry = line.split()
                    port = entry[3].replace("/tcp", "")
                    ip = entry[5]
                    target = ip + ":" + port
                    if target not in targets:
                        print("Fetching " + "http://" + ip + ":" + port)
                        try:
                            driver.get('http://' + ip + ":" + port)
                            time.sleep(1)
                            driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_http.png'))
                            targets.append(ip + ":" + port)
                        except:
                            print("[!] Something went wrong")
                            targets.append(ip + ":" + port)
                
                        print("Fetching " + "https://" + ip + ":" + port)
                        try:
                            driver.get('https://' + ip + ":" + port)
                            time.sleep(1)
                            driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_https.png'))
                            targets.append(ip + ":" + port)
                        except:
                            print("[!] Something went wrong")
                            targets.append(ip + ":" + port)
                elif "exit" in line:
                    print("[+] Recevied exit from Masscan. Stopping...")
                    sys.exit()
