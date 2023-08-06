# bdvr, an Customized Blackduck_Vulnerability_report

# Use case:

Project stakeholders want to know which files are affected with vulnerabilities after a Blackduck HUB scan.

# Drawbacks:

The current blackduck generates multiple reports. To fulfill above requirement once has to refer 2 different reports to really able to trace the source files affected.

# Features

1. Produces customized report where we can see vulnerability, OSS name, affected source path details all in one report
2. Color coded
   low risk = no color
   medium risk = Yellow
   High risk = Red
3. Omits all other files which has no vulnerabilities.

### Prerequiites:

Go to Your Blackduck Project > Generate 'Create Version detail report' > checkbox Source and Vulnerabilities checked.

## Command to run

```sh

usage: -m [-h] -p P [-o]

options:
  -h, --help  show this help message and exit
  -p P        Blackduck report folder is ex: D:\BD_REPORT\PROJECT_DATETIMESTAMP.zip
  -o          (Optional) To automatically open the file

py bdvr.py -p Blackduck_generated_reports.zip

#To automatically open the file add -o option
py bdvr.py -p Blackduck_generated_reports.zip -o

```

## Issues

Please send your bugs to dineshr93@gmail.com
