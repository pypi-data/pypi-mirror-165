from __future__ import annotations as _annotations
import inspect as _inspect
import logging as _logging
import re as _re
from typing import Callable as _Callable
from io import StringIO as _StringIO
import os as _os
import SimpleWorkspace as _sw
import gzip as _gzip

class RotatingLogReader:
    def __init__(self, logPath: str):
        """
        @param logPath:
            the full path to a live log, such as /var/log/apache/access.log,
            The parser handles already rotated files behind the scenes
        """

        self.logPath = _os.path.realpath(logPath)
        self.logFileName = _os.path.basename(self.logPath)
        self.logBaseDirectory = _os.path.dirname(self.logPath)
        self._internalBuffer = None

    def To_String(self):
        """
        @returns All logs dumped to a string
        """
        strBuilder = _StringIO()
        def writeFunc(line:str):
            strBuilder.write(line)
            return False
        self.Read(writeFunc)
        return strBuilder.getvalue()

    def To_File(self, outputPath):
        """
        Dumps all logs as one file
        """


        with open(outputPath, "w") as fp:
            def writeFunc(line: str):
                fp.write(line)
                return False
            self.Read(writeFunc)
        return

    def GetRelatedLogFilePaths(self) -> list[str]:
        """
        @returns list of paths to the log itself + all of its rotated files, sorted newest to oldest logs example [log.txt, log.txt.1, log.txt.2.gz]
        """
        logFiles = {}
        def logFilesFiltering(path: str):
            currentLogname = _os.path.basename(path)
            if(self.logFileName not in currentLogname):
                return
            if(self.logFileName == currentLogname):
                logFiles[0] = path
                return
            escLogName = _re.escape(self.logFileName)
            match = _sw.Utility.RegexMatch(f"/^{escLogName}\.(\d+)/", currentLogname)[0]
            logFiles[int(match[1])] = path
            return
        _sw.Directory.ListFiles(self.logBaseDirectory, callback=logFilesFiltering, includeDirs=False, maxRecursionDepth=1)

        sortedLogFiles = []
        sortedKeyList = sorted(logFiles.keys())
        for i in sortedKeyList:
            sortedLogFiles.append(logFiles[i])

        return sortedLogFiles

    def Read(self, satisfiedCondition: _Callable[[str], bool]):
        """
        @param satisfiedCondition: recieves log line as param, return true to stop reading further
        """
        oldestToNewestLogs = self.GetRelatedLogFilePaths()
        oldestToNewestLogs.reverse()

        for logPath in oldestToNewestLogs:
            fp = None
            if(logPath.endswith(".gz")):
                fp = _gzip.open(logPath, "rt")
            else:
                fp = open(logPath, "r")
            
            for line in fp:
                if satisfiedCondition(line):
                    break

            fp.close()
        return

