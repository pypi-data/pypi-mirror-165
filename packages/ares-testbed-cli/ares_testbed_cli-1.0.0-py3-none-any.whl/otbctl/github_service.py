import json
from unicodedata import category
from dotenv import dotenv_values
from github import Github
import re, os, pathlib, datetime as dt
from .log_management import log_management

infoDualLogger = log_management.get_info_dual_logger()
errorDualLogger = log_management.get_error_dual_logger()

# when user provides a URL to a GitHub file, connects to GH API
#   and uses personal authentication token to get file contents and save locally,
#   to add mock config (YAML) or data (JSON) to mock server. 
# NOTE: only works for files on branch 'main'.

class github_service():

    def configureGitHubToken(token):
        f = open(".env", "w")
        f.write(f"GITHUB_TOKEN={token}")

    def addMockFromGitHub(github_url):    
        try:
            env = dotenv_values(".env")
            token = env['GITHUB_TOKEN']
        except:
            infoDualLogger.info("No GitHub token found.\nConfigure with `otbctl ghtoken -t *your personal access token here*`")
            exit()
        hostname = "github.optum.com" # /api/v3 must be appended per GitHub REST API docs.
        github = Github(base_url=f"https://{hostname}/api/v3", login_or_token=token)

        split_url = re.split("\/", github_url) # split_url is a list        
        org = github.get_organization(split_url[3])
        repository = org.get_repo(split_url[4])

        # extract path of file in repo from the GH link provided by user.
        #   e.g. https://github.optum.com/ + org or user name + repo name + /blob/branchname + {filepath we need}
        if 'blob' in split_url: # could also be done using regex
            blob_index = split_url.index('blob') + 1 # skip 'blob' and branch name in path
            list_length = len(split_url)
            filepath = '/' # append dir levels divided by /
            file_xtn = pathlib.Path(split_url[list_length - 1]).suffix # get file suffix from URL
            for dir in split_url:
                dirlevel_index = split_url.index(dir)
                if dirlevel_index <= blob_index < list_length:
                    pass
                elif dirlevel_index < list_length - 1:
                    filepath += dir + '/'
                else:
                    filepath += dir
        else:
            errorDualLogger.error("GitHub URL must be a direct file link.\ne.g. https://github.domain.com/orgname/reponame/blob/main/filepath/file.yaml")
            exit()
        
        filename = pathlib.Path(filepath).stem
        file_content = repository.get_contents(filepath)
        decoded_file = file_content.decoded_content.decode()

        if file_xtn == '.yaml':
            category = 'mocks'
            writer = (f"# added at {dt.datetime.now()} from {github_url}\n" + decoded_file)
        elif file_xtn == '.json':
            category = 'data'
            writer = decoded_file

        localpath = f"{os.path.expanduser('~')}/.otbctl/testbed/{category}/{filename}{file_xtn}"
        f = open(localpath, "w")
        f.write(writer)
        f.close()

        return localpath

class_instance = github_service()
