import sys, os, re, requests, json, yaml, validators
from tabulate import tabulate
from .log_management import log_management
from .otbctl_main  import otbcli
from .otbctl_mock import mockapi
from .yaml_validate import validate_config
from .github_service import github_service

errorDualLogger = log_management.get_error_dual_logger()
infoDualLogger = log_management.get_info_dual_logger()
infoFileLogger = log_management.get_info_file_logger()

class testbed():
    context = otbcli.getContext('otbctl-context')

    def allMocks():
        try:
            server_url = testbed.context +"/mocks"
        except TypeError:
            errorDualLogger.error("Context must be set first. usage: otbctl setcontext")
            exit()
        try:
            response = requests.get(server_url)
        except:
            errorDualLogger.error("Error: failed to connect to server.")
            exit()
        if response.status_code == 400:
            errorDualLogger.error(f'400 response from server {response.url}')
            sys.exit
        elif response.status_code == 200:
            responsedata = response.json() 
            if(responsedata == 0):
                infoDualLogger.info("No Mocks are registered")
            else:
                return response.json()

    def getMocks():
        mocks_table = []
        if len(testbed.allMocks()) == 0:
            infoDualLogger.info("No mocks found on server.")
            infoDualLogger.info("Usage: 'otbctl -h' for help.")
        else:
            for mock in testbed.allMocks():
                mock_row = []
                state = mock['state']['id']
                path = mock['request']['path']['value']
                creation = mock['state']['creation_date']
                method = mock['request']['method']['value']
                locked = mock['state']['locked']
                mock_row.extend([state, path, method, locked, creation])
                mocks_table.append(mock_row)
            infoDualLogger.info(tabulate(mocks_table, headers=["\nMockID", "\nPath", "\nMethod", "\nLocked?", "\nCreation"]))

    def getMockbyID(id):
        server_url = testbed.context +"/mocks?id="+id
        method='GET'

        response = requests.get(server_url)

        if response.status_code == 400:
            errorDualLogger.error(f'Response: 400 Not Found {response.url}')
            sys.exit
        elif response.status_code == 200:  
            infoDualLogger.info('Response: 200 OK') 
            responsedata = response.json()
            if (responsedata == 0):
                infoDualLogger.info("No Mocks are registered")
            else:
                infoDualLogger.info(f'{json.dumps(response.json(), indent=4)}')
        return response.json()

    def addMock(config_yamls):
        try:
            server_url = testbed.context +"/mocks"

        except TypeError:
            errorDualLogger.error("Context must be set first. usage: otbctl setcontext")
            exit()
        if config_yamls[0][0] == '.': # 1st character of 1st item in arguments list
            # this if prevents 'otbctl add -f . foo bar' or 'otbctl add -f ....'
            if len(config_yamls[0]) > 1 or len(config_yamls) > 1: 
                infoDualLogger.info("Usage: 'otbctl add -f' plus file name(s), or 'otbctl add -f .' for all mocks in current directory.")
                exit()
            else:
                config_yamls = [] # remove '.', add files.
                for filename in os.listdir():
                    config_yamls.append(filename)
        for file in config_yamls:
            if validators.url(file) == True: # checks if arg from user is a URL.
                file = github_service.addMockFromGitHub(file)

            config = validate_config(file)
            method = 'POST'
            # getdatafromapi='{"access_token":"d6ac8cff-3807-364c-97c5-7b3f312cb054","scope":"am_application_scope default","token_type":"Bearer","expires_in":464}"'

            with open(config) as f:
                cfg = yaml.safe_load(f)

            workflows_type = type(cfg['workflows'])
            if workflows_type == dict:
                getdatafromapi = mockapi.mockit(config) 
                infoFileLogger.info(f"Received data from Configured end point {getdatafromapi}")
                payload = class_instance.buildPayload(getdatafromapi, config)
                headers = {'Content-Type': 'application/json'}
                try:
                    response = requests.request(method, server_url, headers=headers, data=payload)
                except UnicodeEncodeError:
                    errorDualLogger.error(f"Error: part of response body from {getdatafromapi} was invalid.")
                infoFileLogger.info(response.text)

            elif workflows_type == list:
                flows_ct = len(cfg['workflows'])
                flow_index = 0 # tells program which flow in YAML to execute on.

                while flow_index < flows_ct: # iterates through multiple flows
                    getdatafromapi = mockapi.mockit(config, flow_index)
                    infoFileLogger.info(f"Received data from Configured end point {getdatafromapi}")
                    payload = class_instance.buildPayload(getdatafromapi, config, flow_index)
                                    
                    headers = {'Content-Type': 'application/json'}
                    try:
                        response = requests.request(method, server_url, headers=headers, data=payload)
                    except UnicodeEncodeError:
                        errorDualLogger.error(f"Error: part of response body from {getdatafromapi} was invalid.")
                        exit()
                    infoFileLogger.info(response.text)                
                    flow_index += 1

    def buildPayload(self, payload, config_yaml, flow_index = None):
        replacedString = payload.replace('\\"','\\\\"')
        replacedString = replacedString.replace('"','\\"')
        replaceadditional = replacedString.replace('\\\\"','\\\\"')
        querylist = {}
        headerlist = {}

        with open(config_yaml) as f:
            cfg = yaml.safe_load(f)
        if flow_index == None:
            status = cfg['workflows']['flow']['testbed']['request']['status']
            converted_num = f'{status}'
            
            if(cfg['workflows']['flow']['testbed']['request']['params'] is not None):
                for x in cfg['workflows']['flow']['testbed']['request']['params']:
                    querylist.update(x)
            queryParams = str(querylist)
            replacedquery = queryParams.replace('\'','"')

            if(cfg['workflows']['flow']['testbed']['request']['headers'] is not None):
                for y in cfg['workflows']['flow']['testbed']['request']['headers']:
                    headerlist.update(y)
            replacedHeaders = str(headerlist).replace('\'','"')
            requestBody = cfg['workflows']['flow']['testbed']['request']['body']
            if(requestBody is not None and (type(requestBody)!=str)):
                replacedBody = cfg['workflows']['flow']['testbed']['request']['body']['value'].replace('"','\\"')
                replacedNewLine= replacedBody.replace('\n','\\n')
            elif(requestBody is not None):
                replacedBody = requestBody.replace('"','\\"')
                replacedNewLine = replacedBody.replace('\n','\\n')
            
            if(cfg['workflows']['flow']['testbed']['request']['method'] =='POST'):
                jsonString = '[{"request": { "method": "' + cfg['workflows']['flow']['testbed']['request']['method']+'","path": "'+cfg['workflows']['flow']['testbed']['request']['path']+'","body":"'+ replacedNewLine+'"},"response": { "status": '+converted_num +',"headers":' + replacedHeaders+',"body": "' +replaceadditional+ '"}}]'
            else:
                jsonString = '[{"request": { "method": "' + cfg['workflows']['flow']['testbed']['request']['method']+'","path": "'+cfg['workflows']['flow']['testbed']['request']['path']+'","query_params":'+replacedquery+'},"response": { "status": '+converted_num +',"headers":' + replacedHeaders+',"body": "' +replaceadditional+ '"}}]'
        
        else:
            status = cfg['workflows'][flow_index]['flow']['testbed']['request']['status']
            converted_num = f'{status}'
            
            if(cfg['workflows'][flow_index]['flow']['testbed']['request']['params'] is not None):
                for x in cfg['workflows'][flow_index]['flow']['testbed']['request']['params']:
                    querylist.update(x)
            queryParams = str(querylist)
            replacedquery = queryParams.replace('\'','"')

            if(cfg['workflows'][flow_index]['flow']['testbed']['request']['headers'] is not None):
                for y in cfg['workflows'][flow_index]['flow']['testbed']['request']['headers']:
                    headerlist.update(y)
                    
            replacedHeaders = str(headerlist).replace('\'','"')
            requestBody = cfg['workflows'][flow_index]['flow']['testbed']['request']['body']

            if(requestBody is not None and (type(requestBody)!=str)):
                replacedBody = cfg['workflows'][flow_index]['flow']['testbed']['request']['body']['value'].replace('"','\\"')
                replacedNewLine= replacedBody.replace('\n','\\n')
            elif(requestBody is not None):
                replacedBody = requestBody.replace('"','\\"')
                replacedNewLine = replacedBody.replace('\n','\\n')
            
            if(cfg['workflows'][flow_index]['flow']['testbed']['request']['method'] =='POST'):
                jsonString = '[{"request": { "method": "' + cfg['workflows'][flow_index]['flow']['testbed']['request']['method']+'","path": "'+cfg['workflows'][0]['flow']['testbed']['request']['path']+'","body":"'+ replacedNewLine+'"},"response": { "status": '+converted_num +',"headers":' + replacedHeaders+',"body": "' +replaceadditional+ '"}}]'
            else:
                jsonString = '[{"request": { "method": "' + cfg['workflows'][flow_index]['flow']['testbed']['request']['method']+'","path": "'+cfg['workflows'][flow_index]['flow']['testbed']['request']['path']+'","query_params":'+replacedquery+'},"response": { "status": '+converted_num +',"headers":' + replacedHeaders+',"body": "' +replaceadditional+ '"}}]'
        
        infoFileLogger.info(jsonString)
        return jsonString

    def load(mock_data):
        if mock_data[0] == '.':
            if len(mock_data) > 1: # prevents 'otbctl load -f . foo bar'
                infoDualLogger.info("Usage: 'otbctl load -f' plus file name(s), or 'otbctl load -f .' for all mocks in current directory.")
                exit()
            else:
                mock_data = [] # remove '.', add files.
                for filename in os.listdir():
                    mock_data.append(filename)
        for file in mock_data:
            if validators.url(file) == True: # checks if arg from user is a URL.
                file = github_service.addMockFromGitHub(file)
                
            infoDualLogger.info(f'Loading Mocks from File -> {file}')
            try:
                server_url = testbed.context +"/mocks"
            except TypeError:
                errorDualLogger.error("Context must be set first. usage: otbctl setcontext")
                exit()
            method='POST'
            try:
                filereader = open(file, 'r')
            except FileNotFoundError:
                errorDualLogger.error(f"Mock data file {file} not found")
                continue
            regexMatch = re.search('^\[\{\\\"request\\\"\:', filereader.readline())
            if regexMatch is None: # validating file contents then file type.
                errorDualLogger.error(f"Error: JSON file {file} is formatted incorrectly.")
                continue
            elif not file.endswith(".json"):
                errorDualLogger.error(f"Error: File type of {file} must be JSON.")
                continue
            Lines = filereader.readlines()
            count = 0
            # Strips the newline character
            for line in Lines:
                count += 1
                payload = line.strip()
                jsonRe = json.dumps(payload)
                infoFileLogger.info(f"Adding Mock to mock server.....{jsonRe}")
                headers = {
                    'Content-Type': 'application/json'
                }
            # response = requests.request(method, server_url, headers=headers, data=payload)
            # infoDualLogger.info(response.text)

    def delMocks():
        try:
            server_url = testbed.context +"/reset"
        except TypeError:
            errorDualLogger.error("Context not set, no mocks to delete. usage: otbctl setcontext")
            exit()
        response = requests.request("POST", server_url)
        if response.status_code == 400:
            errorDualLogger.error(f'400 response from server {response.url}')
            sys.exit
        elif response.status_code == 200:  
            infoDualLogger.info('200 OK') 
            infoDualLogger.info(response.text)
    
    def lockMock(mock_ids):
        if '.' in mock_ids:
            if len(mock_ids) > 1:
                infoDualLogger.info("Usage: 'otbctl lock -m' with mock IDs or . for all mocks.")
                exit()
            else:
                mock_ids = [] # remove '.'
                for mock in testbed.allMocks(): # add all mock IDs on server to list
                    mock_ids.append(mock['state']['id'])
        try:
            server_url = testbed.context + "/mocks/lock"
        except:
            errorDualLogger.error("Context must be set first. usage: otbctl setcontext")
        response = requests.post(server_url, json=mock_ids)
        if response.status_code == 400:
            errorDualLogger.error(f'400 response from server {response.url}')
            sys.exit
        elif response.status_code == 200:  
            infoDualLogger.info(f"Locking mock ID(s): {mock_ids}")
            infoDualLogger.info("Locked mocks are protected from 'otbctl reset all' command.\nRun 'otbctl get' to see locked status for all mocks.")

    def unlockMock(mock_ids):
        if '.' in mock_ids:
            if len(mock_ids) > 1:
                infoDualLogger.info("Usage: 'otbctl unlock -m' with mock IDs or . for all mocks.")
                exit()
            else:
                mock_ids = [] # remove '.'
                for mock in testbed.allMocks(): # add all mock IDs on server to list
                    mock_ids.append(mock['state']['id'])
        try:
            server_url = testbed.context + "/mocks/unlock"
        except:
            errorDualLogger.error("Context must be set first. usage: otbctl setcontext")
        response = requests.post(server_url, json=mock_ids)
        if response.status_code == 400:
            errorDualLogger.error(f'400 response from server {response.url}')
            sys.exit
        elif response.status_code == 200:  
            infoDualLogger.info(f"Unlocking mock ID(s): {mock_ids}")
            infoDualLogger.info("Unlocked mocks can be reset with 'otbctl reset all'.\nRun 'otbctl get' to see locked status for all mocks.")

class_instance = testbed()