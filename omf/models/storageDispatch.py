''' Calculate the costs and benefits of energy storage from a distribution utility perspective. '''
from __future__ import absolute_import
from __future__ import division

from builtins import next
from builtins import filter
from builtins import str
from builtins import range
from past.utils import old_div
import json, os, sys, tempfile, webbrowser, time, shutil, datetime, subprocess, traceback, csv, re, math
import multiprocessing
import collections
import numpy as np
from os.path import join as pJoin
from dateutil.parser import parse
from numpy import npv
from jinja2 import Template
from omf.models import __neoMetaModel__
from .__neoMetaModel__ import *
# import matplotlib.pyplot as plt #NOTE: used for debugging don't delete.
# OMF imports

# Model metadata:
modelName, template = metadata(__file__)
tooltip = 'storageDispatch helps figure out how to dispatch energy storage.'
hidden = True

def work(modelDir, inputDict):
	''' Run the model in a separate process. web.py calls this to run the model.
	This function will return fast, but results take a while to hit the file system.'''
	with open(pJoin(modelDir,"demand.csv"),"w") as demandFile:
		demandFile.write(inputDict['demandCurve'])
	dateArray = []
	with open(pJoin(modelDir,"demand.csv")) as inFile:
			reader = csv.DictReader(inFile)
			for row in reader:
				dateArray.append({'datetime': parse(row['timestamp'])})
	startDate = str(dateArray[0]['datetime'])[0:10]
	endDate = str(dateArray[len(dateArray)-1]['datetime'])[0:10]
	# print startDate, endDate
	airport = str(inputDict.get('airport', 'IAD'))
	
	weatherFilePath = modelDir + "/weather.csv"

	if not os.path.isfile(weatherFilePath):
		#build weather csv
		_downloadWeather(startDate, endDate, airport, modelDir)
		fileList = os.listdir(modelDir)
		filePtrn = re.compile("weather_(?P<loc>[A-Za-z0-9]+)_(?P<raw_date>[0-9]+_[0-9]+_[0-9]+).csv")
		matchedFiles = list(filter(filePtrn.match, fileList))
		matchedList = [filePtrn.match(x) for x in matchedFiles]
		fout = open(modelDir + "/" +"weather.csv","a")
		with open(modelDir + "/" + matchedFiles[0]) as file:
			next(file)
			for line in file:
				fout.write(line)
		for num in range(1,len(matchedFiles)):
			f = open(modelDir + "/" + matchedFiles[num])
			next(f) # skip the header
			next(f)
			for line in f:
				fout.write(line)
		fout.close()
		#Delete excess csv files
		for file in matchedFiles:
			os.remove(modelDir + "/" + file)

	dc = [] # dc means demandCurve
	with open(pJoin(modelDir,"demand.csv")) as inFile:
		reader = csv.DictReader(inFile)
		for row in reader:
			dc.append({'datetime': parse(row['timestamp']), 'power': float(row['power'])})
	wd = []
	with open(pJoin(modelDir,"weather.csv")) as inFile:
		reader = csv.DictReader(inFile)
		for row in reader:
			keyList = list(row.keys())
			for item in keyList:
				if item.startswith('Time'):
					time = item
			wd.append({'date': row['DateUTC<br />'], 'time': row[time] ,'temperature': float(row['TemperatureF'])})
	wdf = []
	for row in wd:
		time = row['date'][0:10] + ' ' + row['time'][0:11]
		date = datetime.datetime.strptime(time, "%Y-%m-%d %I:%M %p")
		wdf.append({'datetime':date, 'temperature': row['temperature']})
	hours = []
	for dcrow in dc:
		for wdfrow in wdf:
			year = wdfrow['datetime'].year
			day = wdfrow['datetime'].day
			month = wdfrow['datetime'].month
			hour = wdfrow['datetime'].hour
			minute = wdfrow['datetime'].minute
			if dcrow.get('temperature','none') == 'none':
				if (dcrow['datetime'].year == year and dcrow['datetime'].month == month and dcrow['datetime'].day == day and dcrow['datetime'].hour == hour and minute <= 10) or (dcrow['datetime'].year == year and dcrow['datetime'].month == month and dcrow['datetime'].day == day and dcrow['datetime'].hour - 1 == hour and minute >= 50):
					dcrow['temperature'] = wdfrow['temperature']
				elif (dcrow['datetime'].year == year and dcrow['datetime'].month == month and dcrow['datetime'].day-1 == day and dcrow['datetime'].hour == 0) and hour == 23 and minute >= 50:
					dcrow['temperature'] = wdfrow['temperature']
	tempScatterArray = []
	dayArray = []
	for row in dc:
		if row.get('temperature', 'none')=='none' or row.get('temperature','none') < -100:
			continue
		dayArray.append(row['temperature'])
		dayArray.append(row['power'] * 1000)
		tempScatterArray.append(dayArray)
		dayArray = []
	dayTemps= []
	tempsGroupedByDay = []
	for row in dc:
		hour = row['datetime'].hour
		if row.get('temperature', 'none')=='none' or row.get('temperature','none') < -100:
			row['temperature'] = None
		dayTemps.append(row['temperature'])
		if hour == 23:
			tempsGroupedByDay.append(dayTemps)
			dayTemps = []

	# Ready to run.
	outData = {}
	# Get variables.
	zipCode = inputDict.get('zipCode',22124)
	# Put demand data in to a file for safe keeping.
	with open(pJoin(modelDir,"demand.csv"),"w") as demandFile:
		demandFile.write(inputDict['demandCurve'])
	# Most of our data goes inside the dc "table"
	dc = []
	with open(pJoin(modelDir,"demand.csv")) as inFile:
		reader = csv.DictReader(inFile)
		for row in reader:
			dc.append({'datetime': parse(row['timestamp']), 'power': float(row['power'])})
	winterData = []
	summerData = []
	fallData = []
	springData = []
	dcbyDay = []
	dayDay = []
	day = {}
	for row in dc:
		hour = row['datetime'].hour
		day['power']=row['power']
		day['hour'] = hour
		day['month'] = row['datetime'].month
		dayDay.append(day)
		day = {}
		if hour == 23:
			dcbyDay.append(dayDay)
			dayDay = []
			day = {}
	maxPowers = []
	#Without pandas
	for dVals in dcbyDay:
		maxPowers.append(max(dVals, key=lambda x:x['power']))
	for row in maxPowers:
		month = row['month']
		hour = row['hour']
		if month >= 2 and month <= 4:
			springData.append(hour)
		elif month >= 5 and month <= 7:
			summerData.append(hour)
		elif month >= 8 and month <= 10:
			fallData.append(hour)
		else:
			winterData.append(hour)
	bins = []
	for i in range(0,25):
		bins.append(i)
	winterHist = list(np.histogram(winterData, bins)[0])
	springHist = list(np.histogram(springData, bins)[0])
	summerHist = list(np.histogram(summerData, bins)[0])
	fallHist = list(np.histogram(fallData, bins)[0])
	histBins = []
	for i in range(0,24):
		histBins.append(i)
	try:
		dc = []
		with open(pJoin(modelDir,"demand.csv")) as inFile:
			reader = csv.DictReader(inFile)
			for row in reader:
				dc.append({'datetime': parse(row['timestamp']), 'power': float(row['power'])})
	except:
			e = sys.exc_info()[0]
			if str(e) == "<type 'exceptions.SystemExit'>":
				pass
			else:
				errorMessage = "Demand CSV file is incorrect format."
				raise Exception(errorMessage)
	dayArray = []
	dcGroupedByDay = []
	dailyDemand = []
	demandCurve = []
	for row in dc:
		hour = row['datetime'].hour
		dayArray.append(row)
		dailyDemand.append(row['power']*1000)
		if hour == 23:
			dcGroupedByDay.append(dayArray)
			demandCurve.append(dailyDemand)
			dayArray = []
			dailyDemand = []
	dates = []
	for row in dc:
		hour = row['datetime'].hour
		if hour == 2:
			dates.append((str(row['datetime'].month) + '/' + str(row['datetime'].day) + '/' + str(row['datetime'].year)))
	tempSum = 0
	demandSum = 0
	productSum = 0
	tempSquaredSum = 0
	demandSquaredSum = 0
	length = len(tempScatterArray)
	for row in tempScatterArray:
		tempSum += row[0]
		demandSum += row[1]
		productSum += row[0] * row[1]
		tempSquaredSum += math.pow(row[0],2)
		demandSquaredSum += math.pow(row[1],2)
	m = old_div(((length*productSum) - (tempSum*demandSum)),(length*tempSquaredSum - math.pow(tempSum,2)))
	b = old_div(((demandSum*tempSquaredSum)-(tempSum*productSum)),(length*tempSquaredSum-math.pow(tempSum,2)))
	x1 = 2
	x2 = 110
	y1 = m * x1 + b
	y2 = m * x2 + b
	equation = 'y = ' + str(round(m,2)) + 'x + ' + str(round(b,2))
	pointOne = [x1, y1]
	pointTwo = [x2, y2]
	outData['regressionEquation'] = equation
	outData['regressionPointOne'] = pointOne
	outData['regressionPointTwo'] = pointTwo
	outData['dates'] = dates
	outData['demand'] = demandCurve
	outData['histBins'] = histBins
	outData['winterHist'] = winterHist
	outData['springHist'] = springHist
	outData['summerHist'] = summerHist
	outData['fallHist'] = fallHist
	outData['tempScatterArray'] = tempScatterArray
	outData['tempsGroupedByDay'] = tempsGroupedByDay
	# Stdout/stderr.
	outData["stdout"] = "Success"
	outData["stderr"] = ""
	return outData

def new(modelDir):
	''' Create a new instance of this model. Returns true on success, false on failure. '''
	defaultInputs = {
		"airport": 'IAD',
		"created": "2015-06-12 17:20:39.308239",
		"modelType": modelName,
		"demandCurve": open(pJoin(__neoMetaModel__._omfDir,"static","testFiles","FrankScadaShort.csv")).read(),
		"fileName": "FrankScadaShort.csv"
	}
	return __neoMetaModel__.new(modelDir, defaultInputs)

def _debugging():
	# Location
	modelLoc = pJoin(__neoMetaModel__._omfDir,"data","Model","admin","Automated Testing of " + modelName)
	# Blow away old test results if necessary.
	try:
		shutil.rmtree(modelLoc)
	except:
		# No previous test results.
		pass
	# Create New.
	new(modelLoc)
	# Pre-run.
	renderAndShow(modelLoc)
	# Run the model.
	runForeground(modelLoc, json.load(open(modelLoc + "/allInputData.json")))
	# Show the output.
	renderAndShow(modelLoc)

if __name__ == '__main__':
	_debugging()