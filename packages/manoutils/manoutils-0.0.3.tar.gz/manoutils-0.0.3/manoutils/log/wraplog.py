# -*- coding: utf-8 -*-
import logging
import inspect

from manoutils.config.ConfigManager import configMgr

logger = logging.getLogger(__name__)

def wraplog(func, logger=logger):
    def wrapper(*args, **kw):
        class_name = ""
        var_names = func.__code__.co_varnames
        func_name = func.__code__.co_name
        file_name = func.__code__.co_filename
        frame = inspect.currentframe()
        local_vars = frame.f_locals
        message="[function:{}] [args:".format(func_name)
        # message = "[file:{}] [function:{}] [args:".format(file_name, func_name)
        for i in range(0,len(local_vars["args"])):
            if str(var_names[i]) == "self":
                class_name = local_vars["args"][i].__class__.__name__
                message = "[class:{}] ".format(class_name) + message
        message_args = list()
        for arg in local_vars["args"]:
            if len(str(arg)) < configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_args.append(arg)
            else:
                message_args.append('***Arg too big to print***')
        message_kw = dict()
        for k,v in local_vars["kw"].items():
            if len(str(v)) < configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_kw.update({k: v})
            else:
                message_kw.update({k: '***Arg too big to print***'})
        message = message + ' args={}, kw={} '.format(message_args, message_kw)
        message = "Enter " + message + "]"
        logger.debug(message)
        ret = func(*args, **kw)
        message_ret = ret
        if len(str(message_ret)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
            message_ret = '***Return value too big to print***'
        if class_name:
            logger.debug("Leave [class:{}] [function:{}] [return:{}]".format(class_name, func_name, message_ret))
        else:
            logger.debug("Leave [function:{}] [return:{}]".format(func_name, message_ret))
        return ret
    return wrapper
