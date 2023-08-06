# -*- coding: utf-8 -*-
import requests
import logging
import json

from enum import Enum
from urlparse import urljoin
from manoutils.client.CertClient import CertClient
from manoutils.client.ExsysClient import ExsysClient
from manoutils.client.TokenClient import TokenClient
from manoutils.log.LogTemplate import LogTemplate
from manoutils.common.common import ignore_case_get

logger = logging.getLogger(__name__)


class AuthType(Enum):
    NoAuth = 0
    OneAuth = 1
    TwoAuth = 2


class ExsysRequest(object):
    def __init__(self, exsysId, exsysType, exsysTenant=''):
        self.exsysId = exsysId
        self.exsysType = exsysType
        self.exsysTenant = exsysTenant
        self.exsystem = ExsysClient().getExsys(exsysType=self.exsysType, exsysId=self.exsysId, exsysTenant=self.exsysTenant)

    def makeSSLArgs(self):
        try:
            authType = ignore_case_get(self.exsystem, "authType")
            certId = ignore_case_get(self.exsystem, "certId")
            args = {"verify": False}
            if self.exsysType == "sec":
                authType = authType.encode('cp936')
            if str(authType).lower() == str(AuthType.OneAuth.value):
                cert = CertClient().getCert(certId=certId)
                cacertPath = ignore_case_get(cert, "cacertPath")
                if not cacertPath:
                    raise Exception("get cacertPath error")
                args.update({"verify": cacertPath})
            elif str(authType).lower() == str(AuthType.TwoAuth.value):
                cert = CertClient().getCert(certId=certId)
                cacertPath = ignore_case_get(cert, "cacertPath")
                clientcertPath = ignore_case_get(cert, "clientcertPath")
                clientkeyPath = ignore_case_get(cert, "clientkeyPath")
                if not cacertPath:
                    raise Exception("get cacertPath error")
                if not clientcertPath:
                    raise Exception("get clientcertPath error")
                if not clientkeyPath:
                    raise Exception("get clientkeyPath error")
                args.update({"verify": cacertPath})
                args.update({"cert": (clientcertPath, clientkeyPath)})
            else:
                args.update({"verify": False})
            return args
        except Exception as e:
            logger.error(e.message)
            return {"verify": False}

    def makeUrl(self, resource='', url=''):
        if url:
            return url
        if not resource:
            if self.exsysType.lower() == "cmoss":
                url = ignore_case_get(self.exsystem, "cmUrl")
            elif self.exsysType.lower() == "pmoss":
                url = ignore_case_get(self.exsystem, "pmUrl")
            elif self.exsysType.lower() == "fmoss":
                url = ignore_case_get(self.exsystem, "fmUrl")
            elif self.exsysType.lower() == "oss":
                url = ignore_case_get(self.exsystem, "cmUrl")
            else:
                url = ignore_case_get(self.exsystem, "url")
            return url
        else:
            if self.exsysType.lower() == "cmoss":
                baseUrl = ignore_case_get(self.exsystem, "cmUrl")
            elif self.exsysType.lower() == "pmoss":
                baseUrl = ignore_case_get(self.exsystem, "pmUrl")
            elif self.exsysType.lower() == "fmoss":
                baseUrl = ignore_case_get(self.exsystem, "fmUrl")
            elif self.exsysType.lower() == "oss":
                baseUrl = ignore_case_get(self.exsystem, "cmUrl")
            else:
                baseUrl = ignore_case_get(self.exsystem, "url")
            url = urljoin(baseUrl, resource)
            return url

    def makeHeaders(self, headers):
        if headers:
            return headers
            # if ignore_case_get(headers, "X-Auth-Token"):
            #     return headers
            # else:
            #     token = TokenClient().getToken(exsysId=self.exsysId, exsysType=self.exsysType)
            #     headers.update({"X-Auth-Token": token})
            #     return headers
        else:
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            token = TokenClient().getToken(exsysId=self.exsysId, exsysType=self.exsysType)
            headers.update({"X-Auth-Token": token})
            return headers

    def makeDesc(self, desc):
        if desc:
            if "->" not in desc:
                desc = "NFVO->{} {}".format(self.exsysType, desc)
        else:
            desc = "NFVO->{} ".format(self.exsysType)
        return desc

    def makeBody(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        return data

    def get(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="GET", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.get(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def post(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="POST", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.post(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def put(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="PUT", url=url, data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.put(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp

    def delete(self, resource='', data='', url='', headers='', timeout=10, desc='', ext_msg=''):
        sslArgs = self.makeSSLArgs()
        headers = self.makeHeaders(headers=headers)
        url = self.makeUrl(resource=resource, url=url)
        data = self.makeBody(data=data)
        desc = self.makeDesc(desc=desc)
        LogTemplate().before_send_req(desc=desc, method="DELETE", data=data, headers=headers, ext_msg=ext_msg)
        rsp = requests.delete(url=url, data=data, headers=headers, timeout=timeout, **sslArgs)
        LogTemplate().after_send_req(desc=desc, request=rsp, ext_msg=ext_msg)
        return rsp
