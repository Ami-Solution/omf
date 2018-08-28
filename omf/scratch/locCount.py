#!/usr/bin/env python

'''
Count the number of lines of code in this project. Ignores the data stores and libraries, etc.
2.5 kLOC as of 2012-10-24.
9.6 kLOC as of 2013-06-10.
99.3 kLOC as of 2015-09-10.
'''
from __future__ import print_function

from builtins import map
import os

def cleanList(inList):
	goodSuffixes = ['py','js','htm','html']
	libraries = ['..\static\d3.v3.js','..\static\highcharts.src.js','..\static\jquery-1.9.1.js']
	return [x for x in inList if (x.split('.')[-1] in goodSuffixes and x not in libraries)]

def lineCount(fileName):
    lines = 0
    for line in open(fileName):
        lines += 1
    return lines

def fileNameAndLineCount(fileName):
	return [fileName, lineCount(fileName)]

def recursiveFileList(direct):
	fileList = []
	for x in os.walk(direct):
		fileList = fileList + [x[0] + '/' + fPath for fPath in x[2]]
	return fileList

allSource = cleanList(recursiveFileList('..'))
lineCountList = list(map(lineCount, allSource))

print('Per-file breakdown:')
for pair in map(fileNameAndLineCount, allSource):
	print(pair[1], 'lines in', pair[0])

print('Total:', sum(lineCountList), 'lines.')