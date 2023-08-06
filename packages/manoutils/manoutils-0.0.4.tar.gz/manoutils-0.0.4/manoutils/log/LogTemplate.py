# -*- coding: utf-8 -*-
import logging
import inspect

from manoutils.config.ConfigManager import configMgr
from manoutils.common.constant import BASE1_HEADERS

logger = logging.getLogger(__name__)


class LogTemplate(object):
    def __init__(self):
        pass

    def receive_req(self, desc="", request="", ext_msg=""):
        try:
            method = request.method
            url = "https://{}{}".format(request.get_host(), request.get_full_path())
            headers = "Content-Type: {}, ".format(request.META.get("CONTENT_TYPE"))
            if request.META.get("HTTP_X_AUTH_TOKEN"):
                headers = headers + "X-Auth-Token: {}, ".format(request.META.get("HTTP_X_AUTH_TOKEN"))
            if request.META.get("HTTP_X_AUTH_USERNAME"):
                headers = headers + "X-Auth-Username: {}, ".format(request.META.get("HTTP_X_AUTH_USERNAME"))
            if request.META.get("HTTP_X_AUTH_PASSWORD"):
                headers = headers + "X-Auth-Password: {}, ".format(request.META.get("HTTP_X_AUTH_PASSWORD"))
            if len(str(request.data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = request.data
            message = "Receive {} request: method: {}, url {}, headers: {}, data: {} ".format(desc,method,url,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.info(message)
        except:
            pass

    def response_req(self, desc="", status="", headers=BASE1_HEADERS, data="", ext_msg="", result=""):
        try:
            if result:
                status = result.get_code()
                data = result.get_result()
                # headers = BASE1_HEADERS
            if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = data
            message = "Response {} : status_code: {}, headers: {}, body: {} ".format(desc,status,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.info(message)
        except:
            pass


    def before_send_req(self, desc="", method="", url="", headers=BASE1_HEADERS, data="", ext_msg=""):
        try:
            if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                message_data = '***data too big to print***'
            else:
                message_data = data
            message = "Send {} request: method: {},  url: {}, headers: {}, body: {} ".format(desc,method,url,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.info(message)
        except:
            pass

    def after_send_req(self, desc="", request="", ext_msg=""):
        try:
            try:
                data = request.json()
                if len(str(data)) > configMgr.getConfigItem("LOG_MAX_LENGTH"):
                    message_data = '***data too big to print***'
                else:
                    message_data = data
            except:
                message_data = ""
            headers = request.headers
            status_code = request.status_code
            message = "Receive {} response: status_code: {}, headers: {}, body: {} ".format(desc,status_code,headers,message_data)
            if ext_msg:
                message = message + ext_msg
            logger.info(message)
        except:
            pass

