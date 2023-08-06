# -*- coding: utf-8 -*-
import os
import gzip
import json
import logging
import chardet

from manoutils.log.wraplog import wraplog

logger = logging.getLogger(__name__)


class FileOperator(object):
    def createDir(self, dirName):
        if not os.path.exists(dirName):
            os.makedirs(dirName, 0o0777)
        return dirName

    @wraplog
    def clearDir(self, dirName, days=''):
        if not os.path.exists(dirName):
            return
        if days:
            if len(os.listdir(dirName)) == 0:
                cmd = 'find %s | xargs rm -rf' % dirName
                os.system(cmd)
            else:
                cmd = 'find %s -mtime +%s | xargs rm -rf' % (dirName, days)
                os.system(cmd)
        else:
            cmd = 'find %s | xargs rm -rf' % dirName
            os.system(cmd)

    @wraplog
    def deleteFile(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

    def readFile(self, fileName):
        if not fileName:
            return
        encoding = 'utf-8'
        with open(fileName, 'rb') as f:
            encoding = chardet.detect(f.read()).get("encoding")
        with open(fileName, 'rb') as f:
            content = json.JSONDecoder().decode(f.read().decode(encoding))
            # content = json.JSONDecoder().decode(f.read().decode('utf-8-sig'))
        return content

    def writeFile(self, fileName, fileContent):
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName, 'wb') as f:
            f.write(fileContent)
        return fileName

    def readBigFile(self, fileName):
        if not fileName:
            return
        with open(fileName, 'rb') as f:
            content = json.JSONDecoder().decode(f.read().decode('utf-8'))
        return content

    def writeBigFile(self, fileName, fileContent):
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName, 'wb+') as f:
            for chunk in fileContent.chunks():
                f.write(chunk)
        return fileName

    def getFileNames(self, dirName):
        if not dirName:
            return list()
        allFileNames = list()
        for rootDirName, subDirNames, fileNames in os.walk(dirName):
            for i in range(len(fileNames)):
                fileNames[i] = os.path.join(rootDirName, fileNames[i])
            allFileNames = allFileNames + fileNames
        return allFileNames

    def getSubDirNames(self, dirName):
        if not dirName:
            return list()
        allSubDirNames = list()
        for rootDirName, subDirNames, fileNames in os.walk(dirName):
            for i in range(len(subDirNames)):
                subDirNames[i] = os.path.join(rootDirName, subDirNames[i])
            allSubDirNames = allSubDirNames + subDirNames
        return allSubDirNames

    def ungzipFile(self, fileName):
        if not fileName:
            return
        # XXXXX_VM_V2.0.0_20200731T000000_001.json.gz_20200731001000_20200731001010_001.gz
        if '.json.gzip' in fileName.lower()[-10:]:
            # outputFile = fileName.replace('.json.gzip', '.json')
            outputFileName = fileName[::-1].replace('.json.gzip'[::-1], '.json'[::-1], 1)[::-1]
        elif '.json.gz' in fileName.lower()[-10:]:
            # outputFile = fileName.replace('.json.gz', '.json')
            outputFileName = fileName[::-1].replace('.json.gz'[::-1], '.json'[::-1], 1)[::-1]
        elif '.gzip' in fileName.lower()[-10:]:
            # outputFile = fileName.replace('.gzip', '.json')
            outputFileName = fileName[::-1].replace('.gzip'[::-1], '.json'[::-1], 1)[::-1]
        elif '.gz' in fileName.lower()[-10:]:
            # outputFile = fileName.replace('.gz', '.json')
            outputFileName = fileName[::-1].replace('.gz'[::-1], '.json'[::-1], 1)[::-1]
        else:
            return fileName
        gzipFileName = gzip.GzipFile(mode="rb", fileobj=open(fileName, 'rb'))
        with open(outputFileName, 'wb') as f:
            f.write(gzipFileName.read())
        return outputFileName

    def ungzipFiles(self, fileNames):
        if not fileNames:
            return list()
        ungzipFileNames = list()
        for fileName in fileNames:
            try:
                ungzipFileNames.append(self.ungzipFile(fileName=fileName))
            except:
                logger.error("ungzipFiles Error; fileName={}".format(fileName))
        return ungzipFileNames

    def gzipFile(self, fileName):
        outputFileName = fileName + ".gzip"
        with open(fileName, 'rb') as f_in:
            with  gzip.open(outputFileName, 'wb') as f_out:
                f_out.writelines(f_in)
        return outputFileName

    def gzipFiles(self, fileNames):
        outputFileNames = list()
        for fileName in fileNames:
            outputFileName = self.gzipFile(fileName=fileName)
            outputFileNames.append(outputFileName)
        return outputFileNames

    def readFiles(self, fileNames):
        if not fileNames:
            return list()
        fileContents = list()
        for fileName in fileNames:
            try:
                fileContents.append(self.readFile(fileName))
            except:
                logger.error("readFiles Error; fileName={}".format(fileName))
        return fileContents
