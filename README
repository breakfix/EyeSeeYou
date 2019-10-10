# EyeSeeYou #

Simple web server enumeration tool.

Same concept as [Eyewitness](https://github.com/FortyNorthSecurity/EyeWitness) but with less features and minimal dependencies.

Designed to be used in conjuction with a running masscan.

## Usage ##

Run masscan to enumerate a subnet for common web ports (send output to output.txt file):
    
    masscan 10.0.0.0/8 -p80,443,8080

At the same time run EyeSeeYou.py to grab screenshots.

The below will output screenshot images to the "test_dir" directory for each discovered port:

    EyeSeeYou.py --out-dir test_dir --input-file output.txt

Optional arguments are --timeout (default 3 seconds) and --headless (run without opening Chrome) 

    EyeSeeYou.py --out-dir test_dir --input-file output.txt --timeout 5 --headless
