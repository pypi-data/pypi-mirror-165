# -*- coding: utf-8 -*-
import logging

from functools import reduce
from manoutils.common.common import ignore_case_get
from manoutils.client.ExsysClient import ExsysClient

logger = logging.getLogger(__name__)


class RegionManager(object):
    def get_infoid(self, info, infoType):
        if ignore_case_get(info, 'vimid'):
            return ignore_case_get(info, 'vimid')
        elif ignore_case_get(info, 'pimid'):
            return ignore_case_get(info, 'pimid')
        else:
            return info["%sid" % infoType]

    def localtion_in_area(self, area, location):
        # area = xibei  or xibei/shanxisheng]
        if len(area.split("/")) == 1:
            area1 = area.split("/")[0]
            area2 = ""
            if area1 == "":
                return True
        else:
            area1 = area.split("/")[0]
            area2 = area.split("/")[1]
        if len(location.split("/")) == 1:
            location1 = location.split("/")[0]
            location2 = ""
        else:
            location1 = location.split("/")[0]
            location2 = location.split("/")[1]
        if location1 == area1 and location2 == area2:
            return True
        elif location1 == area1 and len(location2) == 0:
            return True
        elif location1 == area1 and len(area2) == 0:
            return True
        elif location1 == area2:
            return True
        else:
            return False

    def localtion_in_areas(self, areas, location):
        if not areas:
            return True
        # areas = [xibei, xibei/shanxisheng]
        for area in areas:
            # area = xibei  or xibei/shanxisheng]
            if self.localtion_in_area(area=area, location=location):
                return True
        return False

    def filter_by_area(self, areas, infoType, rawInfos):
        infos = list()
        for info in rawInfos:
            location = ignore_case_get(info, "location")
            if self.localtion_in_areas(areas=areas, location=location):
                infos.append(info)
        return infos

    def filter_by_addedRes(self, addedResources, infoType, rawInfos):
        if not addedResources:
            return list()
        infos = list()
        for info in rawInfos:
            infoid = self.get_infoid(info=info, infoType=infoType)
            if infoid in addedResources:
                infos.append(info)
        return infos

    def areas_is_null(self, areas):
        if len(areas) == 0:
            return True
        elif len(areas) == 1 and areas[0] == "":
            return True
        else:
            return False

    def addedResources_is_null(self, addedResources):
        if len(addedResources) == 0:
            return True
        elif len(addedResources) == 1 and addedResources[0] == "":
            return True
        else:
            return False

    def get_infos(self, areas, addedResources, infoType, rawInfos=None):
        if rawInfos is None:
            rawInfos = ExsysClient().getExsyses(exsysType=infoType)
        if (self.areas_is_null(areas=areas)) and (not self.addedResources_is_null(addedResources=addedResources)):
            areaInfos = list()
        else:
            areaInfos = self.filter_by_area(areas=areas, infoType=infoType, rawInfos=rawInfos)
        addedInfos = self.filter_by_addedRes(addedResources=addedResources, infoType=infoType, rawInfos=rawInfos)
        infos = areaInfos + addedInfos
        # remove duplicate info
        infos = reduce(lambda x, y: x if y in x else x + [y], [[], ] + infos)
        return infos

    def get_infoids(self, areas, addedResources, infoType, rawInfoIds=None):
        infos = self.get_infos(areas=areas, addedResources=addedResources, infoType=infoType)
        infoids = list()
        for info in infos:
            infoid = self.get_infoid(info=info, infoType=infoType)
            if rawInfoIds:
                if infoid in rawInfoIds:
                    infoids.append(infoid)
            else:
                infoids.append(infoid)
        return infoids
