import sys, argparse, os
from cgi import test
from multiprocessing import context
from .otbctl_main  import otbcli
from .otbctl_server import testbed
from .log_management import log_management
from .github_service import github_service

infoDualLogger = log_management.get_info_dual_logger()
errorDualLogger = log_management.get_error_dual_logger()

def main():
    args = sys.argv[1:]
    otbctl_parsers(args)

def otbctl_parsers(args):

        parser = argparse.ArgumentParser(description='Optum Testbed CLI')
        subparsers = parser.add_subparsers(dest='subparser')

        parser_context = subparsers.add_parser('setcontext')
        parser_context.add_argument(
            '-s', '--server', dest='host', help='Set the context of the Optum TestBed Server e.g localhost:8080')

        parser_context = subparsers.add_parser('getcontext')
        parser_context.add_argument(
            dest='current', help='Get the current of the Optum TestBed Server e.g localhost:8080')

        parser_context = subparsers.add_parser('ghtoken')
        parser_context.add_argument(
            '-t', '--token', dest='token', help='Add GitHub personal access token to be saved in .env file'
        )

        parser_get = subparsers.add_parser('get')
        parser_get.add_argument(
            '-g', '--getmocks', dest='getmocks', help='Get the list of all the mocks')
        
        parser_init = subparsers.add_parser('add')
        parser_init.add_argument(
            '-f', '--filename', nargs='+', dest='config_yamls', help='Init Mock on server for a given config.yaml')
        
        parser_init = subparsers.add_parser('load')
        parser_init.add_argument(
            '-f', '--filename', nargs='+', dest='mock_data', help='Load Mock into server from the Data file')

        parser_init = subparsers.add_parser('reset')
        parser_init.add_argument(
            dest='all', help='Reset and Empty Mock Data from Optum TestBed Server e.g localhost:8080')

        parser_init = subparsers.add_parser('removelogs')
        parser_init.add_argument(
            dest='folder', help='Choose which logs to remove e.g. otbctl removelogs info -d 7')
        parser_init.add_argument(
            '-d', '--days-old', dest='days', help='Optional: choose the files to delete based on age e.g. delete files older than 7 days')

        parser_init = subparsers.add_parser('lock')
        parser_init.add_argument(
            '-m', '--mockid', nargs='+', dest='mock_ids', help='Provide 1 or more Mock IDs to lock. To retrieve Mock IDs: otbctl get'
        )

        parser_init = subparsers.add_parser('unlock')
        parser_init.add_argument(
            '-m', '--mockid', nargs='+', dest='mock_ids', help='Provide 1 or more Mock IDs to lock. To retrieve Mock IDs: otbctl get'
        )
        
        kwargs = vars(parser.parse_args())
        try:
            globals()[kwargs.pop('subparser')](**kwargs)
        except KeyError:
            errorDualLogger.error("Welcome to Optum Testbed CLI.\nUsage: 'otbctl -h' for help and info.")

def load(mock_data):
    if(mock_data is None):
        errorDualLogger.error('Please provide valid mock data file with -f option, refer documentation for data format')
    else:
        testbed.load(mock_data)

def setcontext(host):
    if( host is None):
        errorDualLogger.error('Please provide server name with the -s option e.g otbctl setcontext -s http://localhost:8080')
    else:
        infoDualLogger.info('Setting context...')
        otbcli.setContext(host)
        infoDualLogger.info(f' otbctl context set to -> {otbcli.getContext("otbctl-context")}')
         
def getcontext(current):
    if current != 'current': # to make usage more clear + strict
        errorDualLogger.error("Usage: 'otbctl getcontext current'.")
    else:
        infoDualLogger.info('Getting context...')
        infoDualLogger.info(f'otbctl context set to -> {otbcli.getContext("otbctl-context")}')

def ghtoken(token):
    if token is not None:
        github_service.configureGitHubToken(token)
    else:
        errorDualLogger.error("Usage: `otbctl ghtoken -t *your personal access token here*`")

def get(getmocks):
    if getmocks is not None:
        infoDualLogger.info(f'Getting Mock by ID -> {getmocks}')
        testbed.getMockbyID(getmocks)
    else:
        infoDualLogger.info('Getting Mocks...')
        testbed.getMocks()
        infoDualLogger.info("\nRun 'otbctl get -g mockid123' for more info on specific mock.")

def add(config_yamls):
    if config_yamls is not None:
        infoDualLogger.info('Adding Mock...')
        testbed.addMock(config_yamls)
    else:
        errorDualLogger.error("Please provide config yaml with -f option ")

def reset(all):
    # keyword all required in command, i.e. `obtctl reset all`
    infoDualLogger.info('Resetting and emptying mock data from test bed server...')
    testbed.delMocks()

def removelogs(folder, days):
    path = f"{os.path.expanduser('~')}/.otbctl/logs/{folder}"
    log_management.remove_files_by_path(path, days)

def lock(mock_ids):
    if mock_ids is not None:
        testbed.lockMock(mock_ids)
    else:
        errorDualLogger.error("Please provide 1 more more mock IDs with -m option")

def unlock(mock_ids):
    if mock_ids is not None:
        testbed.unlockMock(mock_ids)
    else:
        errorDualLogger.error("Please provide 1 more more mock IDs with -m option")

if __name__ == '__main__':
    main()