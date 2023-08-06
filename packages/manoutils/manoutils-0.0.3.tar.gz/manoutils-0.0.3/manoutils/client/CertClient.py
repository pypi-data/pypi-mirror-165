# -*- coding: utf-8 -*-
import copy
import requests
import logging

from urlparse import urljoin
from manoutils.config.ConfigManager import configMgr
from manoutils.common.constant import BASE1_HEADERS
from manoutils.common.common import ignore_case_get

logger = logging.getLogger(__name__)


class CertClient(object):
    def __init__(self):
        self.msbIp = configMgr.getManoIp()
        self.msbPort = configMgr.getManoPort()
        self.baseUrl = "http://%s:%s/" % (self.msbIp, self.msbPort)
        self.resource = "/api/fcaps/v1/certs"
        self.url = urljoin(self.baseUrl, self.resource)
        self.headers = copy.copy(BASE1_HEADERS)

    def getCert(self, certId):
        self.url = self.url + "/{}".format(certId)
        rsp = requests.get(url=self.url, headers=self.headers, verify=False, timeout=10)
        if rsp.ok:
            cert = rsp.json()
            cert = cert if cert else dict()
            return cert
        else:
            return dict()

    def getCerts(self, exsysId='', exsysType='', exsysTenant=''):
        self.url = self.url + "?exsysId={}&exsysType={}&exsysTenant=".format(exsysId, exsysType, exsysTenant)
        rsp = requests.get(url=self.url, headers=self.headers, verify=False, timeout=10)
        if rsp.ok:
            certs = ignore_case_get(rsp.json(), "certList", list())
            return certs
        else:
            return list()

