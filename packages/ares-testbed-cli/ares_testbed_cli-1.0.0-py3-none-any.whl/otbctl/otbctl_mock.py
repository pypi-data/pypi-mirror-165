from dataclasses import dataclass
from distutils.log import error
from unittest import mock
from wsgiref.headers import Headers        
from numpy import source 
import requests, json, yaml
from munch import Munch
from .log_management import log_management

errorDualLogger = log_management.get_error_dual_logger()
infoDualLogger = log_management.get_info_dual_logger()

class mockapi():

    def mockit(config, flow_index = None):
        with open(config) as f:
                cfg = yaml.safe_load(f)
        if flow_index == None:
            ## if is Auth is true then its auth token service, only work on auth token and break
            if cfg['workflows']['flow']['source']['isAuthOnly']:
                    payload = class_instance.getAuth(cfg)
            else:
                    payload = class_instance.getData(cfg)
        else:
            if cfg['workflows'][flow_index]['flow']['source']['isAuthOnly']:
                    payload = class_instance.getAuth(cfg, flow_index)
            else:
                    payload = class_instance.getData(cfg, flow_index)
        return payload
        
    # Get Authorization Function
    def getAuth(self, cfg, flow_index = None):  
        payload = ""         
        headers = { }
        if flow_index == None:
            url = cfg['workflows']['flow']['source']['auth-endpoint']
            infoDualLogger.info(f"Getting Token from Auth Token URL {url}")
            for var in cfg['workflows']['flow']['source']['headers']:
                headers = var
        else:
            url = cfg['workflows'][flow_index]['flow']['source']['auth-endpoint']
            infoDualLogger.info(f"Getting Token from Auth Token URL {url}")
            for var in cfg['workflows'][flow_index]['flow']['source']['headers']:
                headers = var
        response = requests.request("POST", url, headers=headers, data=payload)
        infoDualLogger.info(f"Response Code from URL {url} is {response.status_code} OK")
        if response.status_code == 200:
            return response.text
        else:
            errorDualLogger.error(f"Received Error from Auth Service {response.status_code}")
            exit()

    # get Data Function for the give Source end point
    def getData(self, cfg, flow_index = None):
        payload=""
        querylist={}
        if flow_index == None:
            auth_payload = json.loads(class_instance.getAuth(cfg))    
            url = cfg['workflows']['flow']['source']['request']['api-endpoint']      
            if(cfg['workflows']['flow']['source']['request']['params'] is not None):
                for x in cfg['workflows']['flow']['source']['request']['params']:
                    querylist.update(x)
            queryParams = str(querylist)
            replacedquery = queryParams.replace('\'','"')
            infoDualLogger.info(f"Queries: {replacedquery}")
            token = auth_payload.get("access_token")
            headerlist = {'Authorization': "Bearer {}".format(token)}
            
            for y in cfg['workflows']['flow']['source']['request']['headers']:
                headerlist.update(y)
            payload =  cfg['workflows']['flow']['source']['request']['body']
            response = requests.request(cfg['workflows']['flow']['source']['request']['method'], url, headers= headerlist, data=payload)
        else:
            auth_payload = json.loads(class_instance.getAuth(cfg, flow_index))    
            url = cfg['workflows'][flow_index]['flow']['source']['request']['api-endpoint']      
            
            if(cfg['workflows'][flow_index]['flow']['source']['request']['params'] is not None):
                for x in cfg['workflows'][flow_index]['flow']['source']['request']['params']:
                    querylist.update(x)
            
            queryParams = str(querylist)
            replacedquery = queryParams.replace('\'','"')
            infoDualLogger.info(f"Queries: {replacedquery}")
            token = auth_payload.get("access_token")
            headerlist = {'Authorization': "Bearer {}".format(token)}
            
            for y in cfg['workflows'][flow_index]['flow']['source']['request']['headers']:
                headerlist.update(y)
            payload =  cfg['workflows'][flow_index]['flow']['source']['request']['body']
            response = requests.request(cfg['workflows'][flow_index]['flow']['source']['request']['method'], url, headers= headerlist, data=payload)
        if response.status_code == 200:
            infoDualLogger.info(f"Response Code from URL {url} is 200 OK")
        else:
            errorDualLogger.error(f"Error: Response Code from URL {url} is {response.status_code}.")
        return response.text
        
class_instance = mockapi()
