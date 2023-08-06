# Optum Testbed CLI


CLI for optum testbed is via the otbctl command, which accepts a variety of subcommands such as context, setup, get mocks. 
A full list of all of the supported is given below and working towards add more as we mature through the testbed framework


## Installation 

Clone this repo and run the below commands to enable CLI on your machine

    vlolla@LAMU0QKPX1XVK6D optum-testbed-cli %      

    ./install.sh 

command in the root directory of repo would help to generate binary for the CLI.

    vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % ./install.sh
    Defaulting to user installation because normal site-packages is not writeable
    Obtaining file:///Users/vlolla/git/optum-testbed-cli
    Preparing metadata (setup.py) ... done
    Installing collected packages: optum-testbed-cli
    Attempting uninstall: optum-testbed-cli
        Found existing installation: optum-testbed-cli 0.1.0
        Uninstalling optum-testbed-cli-0.1.0:
        Successfully uninstalled optum-testbed-cli-0.1.0
    Running setup.py develop for optum-testbed-cli
    Successfully installed optum-testbed-cli-0.1.0

Add python bin directory into the path for the CLI to work or you can specify the location to get this installed. 

Please add /Users/$HOME/Library/Python/3.8/bin to PATH.
-rwxr-xr-x  1 vlolla  staff  1000 May 30 17:42 otbctl


    vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % otbctl -h
    usage: otbctl [-h] {setcontext,getcontext,get,setup} ...

    positional arguments:
    {setcontext,getcontext,get,setup}

    optional arguments:
    -h, --help            show this help message and exit

Python modules required:  
 `pip install` ... `tabulate`, `mysql`, `requests`, `import-metadata`

## Set and Get Context 

CLI needs context to point to specific Test Bed server it can be localhost, Azure or any end point. Default is localhost.


### Get context
    vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % otbctl getcontext current
    otbctl context set to ->  http://localhost

### Set context

    vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % otbctl setcontext -s testbed.optum.com
    otbctl context set to ->  testbed.optum.com

Once context is setup rest of the commands goes agaist the context of the test bed server. Please refer the repo https://github.optum.com/OCS-Transformation-Optimization/optum-testbed-framework on testbed framework server deployment.


## Get Mocks

otbctl get commands get list of all the mock avaiable on a given context server

        vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % otbctl get  
        Get Mocks
        200 OK
        MockID          Path            Method          Creation
        swRCz2r7g        /tokens         GET     2022-05-30T20:13:44.631344967Z
        hKwf9trng        /token          GET     2022-05-30T18:41:51.982901055Z


-g <<mockid>> arguments  provide more details of a given mockid

        vlolla@LAMU0QKPX1XVK6D optum-testbed-cli % otbctl get -g swRCz2r7g
        Get Mocks
        Response: 200 OK
        [
            {
                "request": {
                    "path": {
                        "matcher": "ShouldEqual",
                        "value": "/tokens"
                    },
                    "method": {
                        "matcher": "ShouldEqual",
                        "value": "GET"
                    }
                },
                "response": {
                    "status": 200,
                    "delay": {}
                },
                "context": {},
                "state": {
                    "id": "swRCz2r7g",
                    "times_count": 0,
                    "locked": false,
                    "creation_date": "2022-05-30T20:13:44.631344967Z"
                }
            }
        ]