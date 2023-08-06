# -*- coding: utf-8 -*-
import copy
import requests
import logging

from urlparse import urljoin
from manoutils.config.ConfigManager import configMgr
from manoutils.common.constant import BASE1_HEADERS
from manoutils.common.common import ignore_case_get

logger = logging.getLogger(__name__)


class ExsysClient(object):
    def __init__(self):
        self.exsysType = None
        self.exsysTypes = None
        self.msbIp = None
        self.msbPort = None
        self.baseUrl = None
        self.resource = None
        self.headers = None

    def setDefault(self, exsysType):
        if exsysType.lower() in ["cmoss","pmoss","fmoss"]:
            self.exsysType = "oss"
        else:
            self.exsysType = exsysType
        if self.exsysType == "sec":
            self.exsysTypes = self.exsysType
        else:
            self.exsysTypes = (self.exsysType + "es") if self.exsysType[-1]=="s" else (self.exsysType + "s")
        self.msbIp = configMgr.getManoIp()
        self.msbPort = configMgr.getManoPort()
        self.baseUrl = "http://%s:%s/" % (self.msbIp, self.msbPort)
        self.resource = "/api/fcaps/v1/{}".format(self.exsysTypes)
        self.url = urljoin(self.baseUrl, self.resource)
        self.headers = copy.copy(BASE1_HEADERS)

    def getExsys(self, exsysType, exsysId, exsysTenant=''):
        self.setDefault(exsysType=exsysType)
        url = self.url + "/{}".format(exsysId) + "?tenant={}".format(exsysTenant)
        rsp = requests.get(url=url, headers=self.headers, verify=False, timeout=10)
        if rsp.ok:
            if exsysType.lower() in ["cmoss", "pmoss", "fmoss", "oss", "sec", "vnfm", "nfvo"]:
                exsys = rsp.json()
                exsys = exsys if exsys else dict()
            else:
                exsys = ignore_case_get(rsp.json(), "{}_list".format(self.exsysType), list())
                exsys = exsys[0] if exsys else dict()
            return exsys
        else:
            return dict()

    def getExsyses(self, exsysType, exsysId=''):
        self.setDefault(exsysType=exsysType)
        url = self.url + "?search_by={}".format(exsysId)
        rsp = requests.get(url=url, headers=self.headers, verify=False, timeout=10)
        if rsp.ok:
            return ignore_case_get(rsp.json(), "{}_list".format(self.exsysType), list())
        else:
            return list()

    def getExsysField(self, exsysType, exsysId='', exsysTenant='', key=''):
        exsys = self.getExsys(exsysType=exsysType, exsysId=exsysId, exsysTenant=exsysTenant)
        return ignore_case_get(exsys, key)

    def getExsysIds(self, exsysType):
        exsysIds = list()
        exsyses = self.getExsyses(exsysType=exsysType)
        for exsys in exsyses:
            exsysId = ignore_case_get(exsys, "{}id".format(self.exsysType))
            exsysIds.append(exsysId)
            exsysIds = list(set(exsysIds))
        return exsysIds

    def getExsysId(self, exsysType, exsys):
        return ignore_case_get(exsys, "{}id".format(exsysType))


