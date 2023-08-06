# -*- coding: utf8 -*-
"""
Funcion de logger 
"""

import sys, os
import logging
import traceback

class LoggerHub:
    def __init__(self, app_identifier, file_logs = None):
        # Create a custom self.logger
        self.logger = logging.getLogger(app_identifier)
        self.logger.setLevel(logging.DEBUG)
        # Create handlers
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)

        if file_logs != None:
            log_filename = file_logs
            os.makedirs(os.path.dirname(log_filename), exist_ok=True)
                

            f_handler = logging.FileHandler(log_filename, 'a')
            f_format = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            f_handler.setFormatter(f_format)
            self.logger.addHandler(f_handler)

    def infolog(self, msg):   
        try:
            self.logger.info(msg)
        except:
            print(msg)

    def debuglog(self, msg):   
        try:
            self.logger.debug(msg)
        except:
            print(msg)

    def errorlog(self, msg):   
        try:
            self.logger.error(msg)
        except:
            print(msg)

    def generic_exception(self, error_msg=None, func_name=None, raise_ex=False):
        """
        Return a raise exception captured and send the error to the log
        """
        if error_msg is not None:
            self.errorlog(error_msg)
        
        error = self.traceback_expcetion(exception=error_msg,
                                         func_name=func_name)
        self.errorlog(error)
        if raise_ex:
            raise Exception(error)
    
    def traceback_expcetion(self, exception, func_name):
        """
        gets the traceability of an exception and assembles a message with all necessary to find the exception.

        :param exception: Exception which has been triggered 
        :type exception: Exception / str
        :param func_name: name of the function where the exception has been raised
        :type func_name: str
        :return: returns a message to trace an exception
        :rtype: str
        """
        try:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            traceback_extract_tb_list = traceback.extract_tb(exc_tb)
            traceback_list = list(filter(lambda frame_summary: func_name.split('.')[-1] == frame_summary.name,
                                        traceback_extract_tb_list))

            traceback_error = traceback_list[0] if len(
                traceback_list) > 0 else traceback_list[-1]

            error = 'Type Exception: %s | Message: %s | Function: %s | Num_line: %s | Exception_code: %s | File: %s' % (
                exc_type, exception, func_name, traceback_error.lineno,
                traceback_error.line, traceback_error.filename)

            return error
        except Exception as e:
            self.errorlog("Error : %s" % e)

logger = LoggerHub(app_identifier="Backend_Generator", file_logs=None)