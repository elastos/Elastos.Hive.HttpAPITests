HTTP.API Testing Framework 
======================================
# Overview
    This framework for ipfs-cluster http api testing. 
    Use this framework, you can config a file which will make the framework runs the specified testcase suite. 
    After each running, you can find log file and report html in "result" folder, the report will show the pass, fail or error cases.
    
# Framework Layout

* `config`(This is a directory.)
    * `ipfs.conf` (A configuration file for ipfs cluster information)

* `function`(This is a directory.)
    * `ela_log.py` (Program file for log functions.)
    * `func.py` (Program file for public functions.)
    
* `testCases` (This is a directory. It contains each test case file.)

* `result` (This is a directory. It contains log and report directory for each running.)
 
* `testFiles` (This is a directory. It contains config files for test cases and program.)
    * `data.conf` (A file contains test data for each test case.)
    
* `http_api.py` (Framework start program file.)
* `read_conf.py` (Function program file for read config information)
* `run_case_list.txt` (Text file for config which test cases should run.)

# Deployment Method

* Setup python2.7 environment on windows 7 system.
    

::
    
    (1) Download "Windows x86-64 MSI installer" from https://www.python.org/downloads/release/python-2713/    
    (2) Double click and install the package and add environment variables(C:\Python27\;C:\Python27\Scripts) into os path.
     
* Some python setup package can integrate "pip" tool. If not you should download and setup pip tools.

::
    
    On windows OS run "cmd" command run `pip` if return "Not internal or external commands or runnable programs" means you don not have the tool.
    
    Method 1: 
        Use `easy_install` command, run `easy_install pip` 
    Method 2: 
        (1) Download "pip-19.0.1.tar.gz" from https://pypi.org/project/pip/#files .
        (2) Decompression the tar.gz.
        (3) Open `cmd` go into the pip directory, then run `python ez_setup`.
    Method 3:
        Downloading https://bootstrap.pypa.io/get-pip.py and running `python get-pip.py`
     
* Use pip tool setup some libraries. 
    
    Command such as : pip install <package-name>
    
    ```shell
    $ pip install html-testrunner
    ```
	
	Should install html-testrunner, requests, toolbelt.

* If you can not import HTMTTestRunner, can download HTMLTestRunner.py (https://pypi.org/project/HTMLTestRunner/) then put into directory such as python27/lib
* If you run this framework on windows OS, you should setup "curl" command. Download curl from https://curl.haxx.se/windows/
* Config run_case_list.txt. If the line start with "#", framework will not run the cases.

# How to config
* Modify `run_case_list.txt`. Write all files name in it. The files name from directory `testCase`. If you don't want to some cases. Make the line start with "#".

 ::
 
    testVersion
    testId
    testPeers
    testPeersPid
    testPins
    testPinsCidSync
    testPinsCidrRecover
    testPinsRecover
    testApiV0UidNew
    testApiV0UidLogin
    testApiV0UidInfo
    testApiV0PinAdd
    testApiV0PinLs
    testApiV0PinRm
    testApiV0FileLs
    testApiV0FileAdd
    testApiV0FileGet
    testApiV0FileCat
    testApiV0FilesCp
    testApiV0FilesFlush
    testApiV0FilesLs
    testApiV0FilesMkdir
    testApiV0FilesMv
    testApiV0FilesRead
    testApiV0FilesRm
    testApiV0FilesStat
    testApiV0FilesWrite
    testApiV0NamePublish

* Modify `config\ipfs.conf`. The file contains ipfs-cluster information. There are three important parameters should be set.
 
 ::
    
    ipfs_master_api_baseurl         =   http://10.10.88.88      # One ipfs-cluster node http-api address baseurl. 
    ipfs_master_api_port	        =   9094                    # The node api port number.
    ipfs_master_api_endpoint_port   =   9095                    # The node api endpoint port.
    
    An example of http-api address: http://10.10.88.88:9094/version
    
    
* Modify `testFiles\data.conf`. The file contains testing data for each api. 

 ::
 
    In this document you can config test data for each http-api. Then each <testcase>.py file will use the testing data to do test. 
    For example:
    
        [API_V0_UID_NEW]                                    # Branch name, use upper letters and "_".  /api/v0/uid/new => API_V0_UID_NEW
        api = /api/v0/uid/new                               # HTTP-API string
        normal_response_body = {"UID":"","PeerID":""}       # Response body.
                                
        other_parameters_cases   =                          # Some api strings for test.
                    XXX=1,
                    verbose=1&xxx=1,
                    xxx=xxx&verbose=0,
                    quiet=1&verbose=1,
                    quiet=1&verbose=0,
                    quiet=0&verbose=0,
                    quiet=0&verbose=xxx,
                    quiet=xxx&verbose=1
            
    You can also config some testing data in [common] branch. 

# Start testing and check result

* Run command.
    ```shell
    $ python http_api.py
    ```
* Check result in the directory "result".
  Each time run the framework will generate a new folder named <time> in "result". It contains two files: output.log and report.html.
  
  ::
        
        You can check the log file for testing detail.
        
        2019-01-28 15:46:58,163 - root - INFO - -------------------------
        2019-01-28 15:46:58,163 - root - INFO - [testApiV0UidLogin.py] TEST CASE: [test_normal_get]
        2019-01-28 15:46:58,163 - root - INFO - -------------------------
        2019-01-28 15:46:58,163 - root - INFO - curl --connect-timeout 10 -m 10 http://10.10.88.88:9095/api/v0/uid/new
        2019-01-28 15:46:58,855 - root - INFO - uid-6024939e-5280-40dc-a507-798ba140672b
        2019-01-28 15:46:58,857 - root - INFO - curl --connect-timeout 10 -m 10 -o /dev/null -s -w %{http_code} "http://10.10.88.88:9095/api/v0/uid/login?uid=uid-6024939e-5280-40dc-a507-798ba140672b"
        2019-01-28 15:46:59,055 - root - INFO - 200
        2019-01-28 15:46:59,069 - root - INFO - -------------------------
