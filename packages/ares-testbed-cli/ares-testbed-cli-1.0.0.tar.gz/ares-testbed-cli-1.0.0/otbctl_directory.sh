#!/usr/bin/env bash

# Creating the .otbctl directory
# ----- Mac Directory Example -------
# - /Users/<user>/
#   - .otbctl
#       - .env
#       - config
#           - logging.conf
#       - logs
#           - error
#           - info

# ~ : going to the home directory
cd ~
if ! [[ -d ~/.otbctl ]]; then mkdir .otbctl; fi
# if this directory does NOT exist, create it

cd .otbctl
touch .env
if ! [[ -d ~/.otbctl/config ]]; then mkdir config; fi
if ! [[ -d ~/.otbctl/logs ]]; then mkdir logs; fi
if ! [[ -d ~/.otbctl/testbed ]]; then mkdir testbed; fi

cd testbed # storing YAML mocks/JSON data taken from GitHub
if ! [[ -d ~/.otbctl/testbed/mocks ]]; then mkdir mocks; fi
if ! [[ -d ~/.otbctl/testbed/data ]]; then mkdir data; fi

cd ../config
touch logging.conf

cd ../logs
if ! [[ -d ~/.otbctl/logs/error ]]; then mkdir error; fi
if ! [[ -d ~/.otbctl/logs/info ]]; then mkdir info; fi

# Writing logging.conf
printf "# Doc: https://docs.python.org/3/library/logging.config.html
#-------------------- SET UP ----------------------------------------
# - creating loggers, handlers, + formatters

[loggers]
keys=root, infoFile, infoConsole, infoDual, errorFile, errorConsole, errorDual

[handlers]
keys=infoFileHandler, errorFileHandler, consoleHandler

[formatters]
keys=fileFormatter, consoleFormatter

#-------------------- LOGGERS ----------------------------------------
# - level: setting logging type
# - qualname: name to instantiate logger in code -> logging.getLogger('<qualname>')
# - handlers: assigning handlers to logger
# - propagate: logging messages don't repeat as it moves up the chain

[logger_root]
level=DEBUG
handlers=infoFileHandler, errorFileHandler, consoleHandler

[logger_infoFile]
level=DEBUG
qualname=infoFile
handlers=infoFileHandler
propagate=0

[logger_infoConsole]
level=DEBUG
qualname=infoConsole
handlers=consoleHandler
propagate=0

[logger_infoDual]
level=DEBUG
qualname=infoDual
handlers=infoFileHandler, consoleHandler
propagate=0

[logger_errorFile]
level=DEBUG
qualname=errorFile
handlers=errorFileHandler
propagate=0

[logger_errorConsole]
level=DEBUG
qualname=errorConsole
handlers=consoleHandler
propagate=0

[logger_errorDual]
level=DEBUG
qualname=errorDual
handlers=errorFileHandler, consoleHandler
propagate=0

#-------------------- HANDLERS ----------------------------------------
# - class: type of handler
# - formatter: assigning formatter to handler
# - args: choosing a folder and file to store log messages
#   - 1st Argument: naming the file after a timestamp (e.g. 2022_06_21.log)
#   - a: append log messages to file
#   - w: create a new file and place log messages inside

[handler_infoFileHandler]
class=FileHandler
formatter=fileFormatter
args=(__import__('datetime').datetime.now().strftime(__import__('os').path.expanduser('~') + '/.otbctl/logs/info/%%%%Y_%%%%m_%%%%d.log'), 'a')

[handler_errorFileHandler]
class=FileHandler
formatter=fileFormatter
args=(__import__('datetime').datetime.now().strftime(__import__('os').path.expanduser('~') + '/.otbctl/logs/error/%%%%Y_%%%%m_%%%%d.log'), 'a')

[handler_consoleHandler]
class=StreamHandler
formatter=consoleFormatter

#-------------------- FORMATTERS ----------------------------------------
# - format: changing how the log message will be displayed
#   - asctime: gives time
#   - levelname: gives type of log
#   - message: displays message

[formatter_fileFormatter]
format=%%(asctime)s - %%(levelname)s - %%(message)s

[formatter_consoleFormatter]
format=%%(message)s" > ~/.otbctl/config/logging.conf

# printf "text to insert into file" > filename_example.txt
#   > : overwrites the text in the file
#   >> : appends new text to the text in the file