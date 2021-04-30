# EyeSeeYou #

Same concept as [Eyewitness](https://github.com/FortyNorthSecurity/EyeWitness) but with less features and minimal dependencies.

Designed to be used in conjuction with a running masscan.

## Installation ##

Install with

    pip install -r requirements.txt

## Usage ##

Run masscan to enumerate a subnet for common web ports (send output to output.txt file):
    
    masscan 10.0.0.0/8 -p80,443,8080 > output.txt

For a full list of common web ports use the included masscan config file

    masscan 10.0.0.0/8 -c all_web_ports.config > output.txt

At the same time run EyeSeeYou.py to grab screenshots.

The below will output screenshot images to the "test_dir" directory for each discovered port:

    EyeSeeYou.py -o test_dir -i output.txt

Optional arguments are --timeout (default 3 seconds) and --headless (run without opening Chrome) 

    EyeSeeYou.py -o test_dir -i output.txt --timeout 5 --headless

You can also provide a file containing a list of IPs or hosts on each line and provide this as an input file to avoid using masscan (ports must be provided)

    EyeSeeYou.py -o test_dir -i hosts.txt --no-masscan 80,443,8080

Use of a SOCKS4 proxy is also supported (default value is 127.0.0.1:1080) but can be overridden by providing an argument 

    EyeSeeYou.py -o test_dir -i output.txt --proxy 

    EyeSeeYou.py -o test_dir -i output.txt --proxy 192.168.1.1:8080
