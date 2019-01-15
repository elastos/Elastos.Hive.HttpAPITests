HTTP.API Testing Framework 
======================================

# Structure

* [DIR] config
    * [doc] ipfs.conf (A configuration file for ipfs cluster informations)

* [DIR] function
    * [doc] ela_log.py (Program for log functions.)
    * [doc] func.py (Program for public functions.)
    
* [DIR] testCases (Program for each test case.)
    * [doc]...
    * [doc]...
    * [doc]...
    * [doc]...
 
* [DIR] result (Contains log and report directory for each running.)
    * [DIR]...
    * [DIR]...
    * [DIR]...
    * [DIR]...
 
* [DIR] testFiles (Config files for test cases and program.)
    * [doc] data.conf (Test data for each test case.)
    
* [doc] http_api.py (Framework start program)
* [doc] read_conf.py (Function program for read config information)
* [doc] run_case_list.txt (Text file for config which test cases should run.)

# Method

* Setup python 2/3 environment on OS.
* pip install html-testrunner
 (If you can not import HTMTTestRunner, can download HTMLTestRunner.py then put into directory such as python27/lib)
* pip install requests
* pip install requests-toolbelt
* If you run this framework on windows OS, you should setup "curl" command. Download curl from https://curl.haxx.se/windows/
* Config run_case_list.txt if the line start with "#", framework will not run the cases.
* Run command : python http_api.py
* Check result/<data_directory>