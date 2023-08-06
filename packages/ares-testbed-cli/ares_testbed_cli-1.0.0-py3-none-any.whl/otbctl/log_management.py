import os
import time
import logging.config


class log_management():

    def remove_files_by_path(path, days):
        infoDualLogger = class_instance.get_info_logger_inside_class()
        files_count = 0
        deleted_files_count = 0

        # If user gives no amount of days, then 7 is the default
        if type(days) == type(None):
            days = "7"

        seconds = int(days) * 24 * 60 * 60

        infoDualLogger.info(f"Starting process to remove files from: {path}")
        # Checking to see if the path given was found
        if os.path.exists(path):
            # Retrieving all the files and looping through each one
            for file in os.listdir(path):
                # Ignoring the .gitkeep files
                if file.startswith('.gitkeep'):
                    continue
                else:
                    files_count += 1
                    file_path = os.path.join(path, file)

                    # Determining if the file should get deleted
                    if class_instance.get_file_age(file_path) > seconds:
                        class_instance.remove_file(file_path)
                        deleted_files_count += 1

        else:
            infoDualLogger.info(f'"{path}" is not found')

        if files_count > 0:
            infoDualLogger.info(f"Total log files: {files_count}")
            infoDualLogger.info(
                f"Total log files deleted: {deleted_files_count}")
        else:
            infoDualLogger.info("No files found")

    def get_file_age(self, path):
        # Getting file age: time that has passed - creation time of the file
        file_age = time.time() - os.stat(path).st_ctime
        return file_age

    def remove_file(self, path):
        infoDualLogger = class_instance.get_info_logger_inside_class()

        if not os.remove(path):
            infoDualLogger.info(f"{path} is removed successfully")

        else:
            infoDualLogger.info(f"Unable to delete the {path}")

    # This will be used inside this class
    def get_info_logger_inside_class(self):
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('infoDual')

    # These will be used outside this class
    def get_info_file_logger():
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('infoFile')

    def get_info_console_logger():
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('infoConsole')

    def get_info_dual_logger(): # goes to both file and console.
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('infoDual')

    def get_error_file_logger():
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('errorFile')

    def get_error_console_logger():
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('errorConsole')

    def get_error_dual_logger(): # goes to both file and console.
        log_config_file = f"{os.path.expanduser('~')}/.otbctl/config/logging.conf"
        logging.config.fileConfig(log_config_file)
        return logging.getLogger('errorDual')


class_instance = log_management()