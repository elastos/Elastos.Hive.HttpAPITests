HTTP.API Testing Framework 
======================================
# Overview
    This framework for ipfs-cluster http api testing. 
    Use this framework, you can config a file which will make the framework runs the specified testcase suite. 
    After each running, you can find log file and report html in "result" folder, the report will show the pass, fail or error cases.
    
# Framework Layout

* :DIR: `config`
    * :doc: `ipfs.conf` (A configuration file for ipfs cluster information)

* :DIR: `function`
    * :doc: `ela_log.py` (Program for log functions.)
    * :doc: `func.py` (Program for public functions.)
    
* :DIR: `testCases` (Program for each test case.)

* :DIR: `result` (Contains log and report directory for each running.)
 
* :DIR: `testFiles` (Config files for test cases and program.)
    * :doc: `data.conf` (Test data for each test case.)
    
* :doc: `http_api.py` (Framework start program)
* :doc: `read_conf.py` (Function program for read config information)
* :doc: `run_case_list.txt` (Text file for config which test cases should run.)

# Deployment Method

* Setup python environment. For example: setup python27-64bit on windows 7 system.
* Setup pip tools. https://pypi.org/project/pip/ 
* Use pip tool setup some libraries.
    ```shell
    $ pip install html-testrunner
    ```
	
    ```shell
    $ pip install requests
    ```
	
    ```shell
    $ pip install html-testrunner
    ```
	
    ```shell
    $ pip install requests-toolbelt
    ```
* If you can not import HTMTTestRunner, can download HTMLTestRunner.py then put into directory such as python27/lib
* If you run this framework on windows OS, you should setup "curl" command. Download curl from https://curl.haxx.se/windows/
* Config run_case_list.txt if the line start with "#", framework will not run the cases.

# How to config
* Modify `run_case_list.txt`. Write all files name in it. The files name from directory `testCase`. If you don't want to some cases. Make the line start with "#".
* Modify `config\ipfs.conf`. The file contains ipfs-cluster information.
* Modify `testFiles\data.conf`. The file contains testing data for each api. 

# Start testing and check result

* Run command.
    ```shell
    $ python http_api.py
    ```
* Check result in the directory "result".
  Each run the framework will generate a new folder named <time> in "result".
