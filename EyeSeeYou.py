from selenium import webdriver
from depot.manager import DepotManager
from argparse import ArgumentParser
import os
import sys

def path(value):
    # Make path absoloute
    return os.path.abspath(value)

parser = ArgumentParser()
parser.add_argument("--out-dir", dest="out_dir", required=True, type=path,
                        help='Path to export images')
parser.add_argument("--input-file", dest="input_file", required=True, type=path,
                    help='File being outputted by Masscan to use as input file')
parser.add_argument("--headless", dest="headless", action='store_true',
                    help='Run Chrome in headless mode')
parser.add_argument("--timeout", dest="timeout",
                    help='Set timeout in seconds (default is 3 seconds)')

# Print help if no arguments given
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

chrome_options = webdriver.ChromeOptions()

if args.headless:
    chrome_options.headless = True

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options) 
driver.set_window_size(1024, 768) # set the window size that you need 

if args.timeout:
    driver.set_page_load_timeout(int(args.timeout))
else:
    driver.set_page_load_timeout(3)

targets = []

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
                        driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_http.png'))
                        targets.append(ip + ":" + port)
                    except:
                        print("[!] Something went wrong")
                        targets.append(ip + ":" + port)
            
                    print("Fetching " + "https://" + ip + ":" + port)
                    try:
                        driver.get('https://' + ip + ":" + port)
                        driver.save_screenshot(os.path.join(args.out_dir, str(ip) + ':' + str(port) + '_https.png'))
                        targets.append(ip + ":" + port)
                    except:
                        print("[!] Something went wrong")
                        targets.append(ip + ":" + port)
            elif "exit" in line:
                print("[+] Recevied exit from Masscan. Stopping...")
                sys.exit()