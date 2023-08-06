# -*- coding: utf-8 -*-
import json
import copy
import threading
import logging
import requests

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from fcaps.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}

class EsBody(object):
    def __init__(self):
        self._esBody = {}
        self._queryCmds = list()
        self._filterCmds = list()
        self._aggsCmds = list()
        self._sortCmds = list()
        self._extCmds = list()

    def addQueryCmd(self, logic="must", cmd=None):
        if isinstance(cmd, dict):
            if logic in ["must", "should", "must_not"]:
                self._queryCmds.append({"logic":logic, "cmd":cmd})

    def addSortCmd(self, cmd=None):
        if isinstance(cmd, dict):
            self._sortCmds.append(cmd)

    def addAggsCmd(self, name=None, cmd=None, deepth=1):
        if isinstance(cmd, dict):
            self._aggsCmds.append({"name":name, "cmd":cmd, "deepth":deepth})

    def addExtCmd(self, cmd):
        if isinstance(cmd, dict):
            self._extCmds.append(cmd)

    def makeQueryBody(self):
        body = {"bool":{"must":[], "should":[], "must_not":[]}}
        for queryCmd in self._queryCmds:
            logic = queryCmd["logic"]
            cmd = queryCmd["cmd"]
            body["bool"][logic].append(cmd)
        return body

    def makeSortBody(self):
        for cmd in self._sortCmds:
            # e.g: cmd={"date":{"order": "asc"}}
            # e.g: cmd={"date":{"order": "desc"}}
            return cmd
        return dict()

    def makeAggsBody(self):
        '''
        :return:
            {
                "aggs": {
                    "aggName1": {
                        "avg": {
                            "field": "aggValue1"
                        },
                        "aggs": {
                            "aggName2": {
                                "avg": {
                                    "field": "aggValue2"
                                }
                            }
                        }
                    }
                }
            }
        '''
        body = dict()
        for deepth in range(-15, 0):
            deepth = -deepth
            for cmd in self._aggsCmds:
                if str(deepth) == str(cmd["deepth"]):
                    aggsName = copy.deepcopy(cmd["name"])
                    aggsCmd = copy.deepcopy(cmd["cmd"])
                    aggsCmd.update(body)
                    body = copy.deepcopy({"aggs": {aggsName: aggsCmd}})
        return body

    def makeExtBody(self):
        body = dict()
        for cmd in self._extCmds:
            body.update(cmd)
        return body

    def makeBody(self):
        self._esBody["query"] = self.makeQueryBody()
        self._esBody["sort"] = self.makeSortBody()
        self._esBody.update(self.makeAggsBody())
        self._esBody.update(self.makeExtBody())
        return self._esBody


class EsRequest(object):
    def __init__(self):
        super(EsRequest, self).__init__()
        self._index = None
        self._docType = None
        self._body = None
        self._action = "search"

    def getIndex(self):
        return self._index

    def setIndex(self, index):
        self._index = index.lower()

    def getDocType(self):
        return self._docType

    def setDocType(self, docType):
        self._docType = docType.lower()

    def getBody(self):
        return self._body

    def setBody(self, body):
        self._body = body

    def getAction(self):
        return self._action

    def setAction(self, action="search"):
        self._action = action.lower()


class EsOperator(object):
    def __init__(self):
        super(EsOperator, self).__init__()
        self._client = None
        self._esNodes = list()

    def setNodes(self, nodes):
        if not isinstance(nodes, list):
            return
        for node in nodes:
            if not isinstance(node, dict):
                continue
            esNode = dict()
            esNode.update({"host":ignore_case_get(node, "esIp")})
            esNode.update({"port":ignore_case_get(node, "esPort")})
            self._esNodes.append(esNode)

    def getNodes(self):
        return self._esNodes

    def getClient(self):
        if self._client:
            return self._client
        nodes = self.getNodes()
        if not nodes:
            raise Exception("get ElasticSearch client error!")
        self._client =  Elasticsearch(nodes, timeout=10)
        return self._client

    def getEsUrl(self):
        nodes=self.getNodes()
        for node in nodes:
            return "http://{}:{}/".format(node["host"], node["port"])

    def makeEsReq(self, *args, **kwargs):
        return dict()

    def makeEsReqs(self, *args, **kwargs):
        return list()

    def sendEsReq(self, esReq, extArgs={}):
        if isinstance(esReq, EsRequest):
            client = self.getClient()
            if esReq.getAction().lower() == "create":
                rsp = client.index(index=esReq.getIndex(), doc_type=esReq.getDocType(), body=esReq.getBody(), **extArgs)
                return rsp
            elif esReq.getAction().lower() == "search":
                rsp = client.search(index=esReq.getIndex(), doc_type=esReq.getDocType(), body=esReq.getBody(), **extArgs)
                return rsp
            elif esReq.getAction().lower() == "delete":
                rsp = client.delete(index=esReq.getIndex(), doc_type=esReq.getDocType(), **extArgs)
                return rsp
            elif esReq.getAction().lower() == "delete_by_query":
                rsp = client.delete_by_query(index=esReq.getIndex(), doc_type=esReq.getDocType(), body=esReq.getBody(), **extArgs)
                return rsp

    def sendEsReqs(self, esReqs, extArgs={}):
        for esReq in esReqs:
            try:
                self.sendEsReq(esReq, extArgs=extArgs)
            except Exception as e:
                logger.error(e.message)

    def sendEsReqByHttp(self, esReq, extArgs={}):
        if isinstance(esReq, EsRequest):
            url = self.getEsUrl()
            url = url + "{}/{}/".format(esReq.getIndex(), esReq.getDocType())
            logger.debug("sendEsReqByHttp url={}".format(url))
            logger.debug("sendEsReqByHttp esReq.getIndex={}".format(esReq.getIndex()))
            logger.debug("sendEsReqByHttp esReq.getDocType={}".format(esReq.getDocType()))
            logger.debug("sendEsReqByHttp esReq.getBody={}".format(esReq.getBody()))
            logger.debug("sendEsReqByHttp esReq.getAction={}".format(esReq.getAction()))
            if esReq.getAction().lower() == "create":
                rsp = requests.post(url=url, data=json.dumps(esReq.getBody()), headers=HEADERS, timeout=10)
                if rsp.ok:
                    return rsp.json()
                else:
                    return dict()
            elif esReq.getAction().lower() == "search":
                url = url + "_search"
                rsp = requests.post(url=url, data=json.dumps(esReq.getBody()), headers=HEADERS, timeout=10)
                if rsp.ok:
                    return rsp.json()
                else:
                    return dict()
            elif esReq.getAction().lower() == "delete_by_query":
                url = url + "_delete_by_query"
                rsp = requests.post(url=url, data=json.dumps(esReq.getBody()), headers=HEADERS, timeout=10)
                if rsp.ok:
                    return rsp.json()
                else:
                    return dict()

    def sendEsReqsByHttp(self, esReqs, extArgs={}):
        for esReq in esReqs:
            try:
                self.sendEsReqByHttp(esReq, extArgs=extArgs)
            except Exception as e:
                logger.error(e.message)


    def bulkCreateSync(self, esReqs):
        try:
            PmEsTask(esClient=self.getClient(), esReqs=esReqs).start()
        except Exception as e:
            logger.error(e.message)

    def bulkCreate(self, esReqs):
        bodys = [{
            "_index": esReq.getIndex(),
            "_type": esReq.getDocType(),
            "_source": esReq.getBody()
        } for esReq in esReqs]
        rsp = helpers.bulk(self.getClient(), bodys)
        return rsp


pmEsSemaphore=threading.Semaphore(10)
class PmEsTask(threading.Thread):
    def __init__(self, esClient, esReqs):
        super(PmEsTask, self).__init__()
        self.esClient = esClient
        self.esReqs = esReqs

    def run(self):
        logger.debug("PmEsTask start")
        try:
            if not pmEsSemaphore.acquire(blocking=False):
                return
            bodys = [{
                "_index": esReq.getIndex(),
                "_type": esReq.getDocType(),
                "_source": esReq.getBody()
            } for esReq in self.esReqs]
            rsp = helpers.bulk(self.esClient, bodys)
            logger.debug("PmEsTask create data: count={}".format(rsp))
            pmEsSemaphore.release()
        except Exception as e:
            logger.error(e.message)
            pmEsSemaphore.release()
