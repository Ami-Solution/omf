import json, math, random

# DISTRIBUTION FEEDER FUNCTIONS
def refactorNames(inputFeeder):
	newNameKey = {}
	newNameArray = []
	newKeyID = 0
	for key in inputFeeder['tree']:
		if 'name' in inputFeeder['tree'][key]:
			oldName = inputFeeder['tree'][key]['name']
			newName = inputFeeder['tree'][key]['object'] + str(newKeyID)
			newKeyID += 1
			inputFeeder['tree'][key]['name'] = newName
			newNameKey.update({oldName:newName})
			newNameArray.append(newName)
	return newNameKey, newNameArray

def distPseudomizeNames(inputFeeder):
	newNameKey = {}
	newKeyID = 0
	for key in inputFeeder['tree']:
		if 'name' in inputFeeder['tree'][key]:
			oldName = inputFeeder['tree'][key]['name']
			newName = inputFeeder['tree'][key]['object'] + str(newKeyID)
			newKeyID += 1
			inputFeeder['tree'][key]['name'] = newName
			newNameKey.update({oldName:newName})
	return newNameKey

def distRandomizeNames(inputFeeder):
	newNameArray = []
	newKeyID = 0
	for key in inputFeeder['tree']:
		if 'name' in inputFeeder['tree'][key]:
			newName = inputFeeder['tree'][key]['object'] + str(newKeyID)
			newKeyID += 1
			inputFeeder['tree'][key]['name'] = newName
			newNameArray.append(newName)
	return newNameArray

def distRandomizeLocation(inputFeeder):
	inputFeeder['nodes'] = []
	inputFeeder['links'] = []
	inputFeeder['hiddenNodes'] = []
	inputFeeder['hiddenLinks'] = []
	for key in inputFeeder['tree']:
		if ('longitude' in inputFeeder['tree'][key]) or ('latitude' in inputFeeder['tree'][key]):
			inputFeeder['tree'][key]['longitude'] = random.randint(0,1000)
			inputFeeder['tree'][key]['latitude'] = random.randint(0,1000)
	return inputFeeder['tree']

def distTranslateLocation(inputFeeder, translation, rotation):
	inputFeeder['nodes'] = []
	inputFeeder['links'] = []
	inputFeeder['hiddenNodes'] = []
	inputFeeder['hiddenLinks'] = []
	for key in inputFeeder['tree']:
		if ('longitude' in inputFeeder['tree'][key]) or ('latitude' in inputFeeder['tree'][key]):
			inputFeeder['tree'][key]['longitude'] += translation*math.cos(rotation)
			inputFeeder['tree'][key]['latitude'] += translation*math.sin(rotation)
	return inputFeeder['tree']

def distAddNoise(inputFeeder, noisePerc):
	for key in inputFeeder['tree']:
		for prop in inputFeeder['tree'][key]:
			value = inputFeeder['tree'][key][prop]
			try: 
				complex(value)
				value = float(value)
				randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
				inputFeeder['tree'][key][prop] += str(randNoise)
			except ValueError:
				continue
	return inputFeeder['tree']

def distShuffleLoads(inputFeeder, shufPerc):
	tlParents = []
	tnParents = []
	houseParents = []
	zipParents = []
	for key in inputFeeder['tree']:
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'triplex_line'):
			tlParents.append(inputFeeder['tree'][key]['parent'])
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'triplex_node'):
			tnParents.append(inputFeeder['tree'][key]['parent'])
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'house'):
			houseParents.append(inputFeeder['tree'][key]['parent'])
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'ZIPload'):
			zipParents.append(inputFeeder['tree'][key]['parent'])
	tlIdx = 0
	tnIdx = 0
	houseIdx = 0
	zipIdx = 0
	for key in inputFeeder['tree']:
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'triplex_line'):
			if random.randint(0,100)/100.0 < shufPerc:
				random.shuffle(tkParents)
				inputFeeder['tree'][key]['parent'] = tlParents[tlIdx]
				tlIdx += 1
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'triplex_node'):
			if random.randint(0,100)/100.0 < shufPerc:
				random.shuffle(tnParents)
				inputFeeder['tree'][key]['parent'] = tnParents[tnIdx]
				tnIdx += 1
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'house'):
			if random.randint(0,100)/100.0 < shufPerc:
				random.shuffle(houseParents)
				inputFeeder['tree'][key]['parent'] = houseParents[houseIdx]
				houseIdx += 1
		if ('parent' in inputFeeder['tree'][key]) and (inputFeeder['tree'][key]['object'] == 'ZIPload'):
			if random.randint(0,100)/100.0 < shufPerc:
				random.shuffle(zipParents)
				inputFeeder['tree'][key]['parent'] = zipParents[zipIdx]
				zipIdx += 1
	return inputFeeder['tree']


def distModifyConductorLengths():
	pass

def distSmoothLoads():
	pass



# TRANSMISSION NETWORK FUNCTIONS
def refactorNames(inputNetwork):
	newBusKey = {}
	newBusArray = []
	newKeyID = 0
	for dic in inputNetwork['bus']:
		for each in dic:
			idx = int(each) - 1
			for key in inputNetwork['bus'][idx]:
				for prop in inputNetwork['bus'][idx][key]:
					if 'bus_i' in prop:
						oldBus = inputNetwork['bus'][idx][key]['bus_i']
						newBus = 'bus' + str(newKeyID)
						newKeyID += 1
						inputNetwork['bus'][idx][key]['bus_i'] = newBus
						newBusKey.update({oldBus:newBus})
						newBusArray.append(newBus)
	# for dic in inputNetwork['bus']:
	# 	for key in dic:
	# 		key = int(key) - 1
	# 		for bus in inputNetwork['bus'][key]:
	# 			if 'bus_i' in inputNetwork['bus'][key][bus]:
	# 				oldBus = inputNetwork['bus'][key][bus]['bus_i']
	# 				newBus = 'bus' + str(newKeyID)
	# 				newKeyID += 1
	# 				inputNetwork['bus'][key][bus]['bus_i'] = newBus
	# 				newBusKey.update({oldBus:newBus})
	# 				newBusArray.append(newBus)
	# for key in inputNetwork['bus'][0]:
	# 	if 'bus_i' in inputNetwork['bus'][0][key]:
	# 		oldBus = inputNetwork['bus'][0][key]['bus_i']
	# 		newBus = 'bus' + str(newKeyID)
	# 		newKeyID += 1
	# 		inputNetwork['bus'][0][key]['bus_i'] = newBus
	# 		newBusKey.update({oldBus:newBus})
			# newBusArray.append(newBus)
	return newBusKey, newBusArray

def tranPseudomizeNames(inputNetwork):
	newBusKey = {}
	newKeyID = 0
	for dic in inputNetwork['bus']:
		for each in dic:
			idx = int(each) - 1
			for key in inputNetwork['bus'][idx]:
				for prop in inputNetwork['bus'][idx][key]:
					if 'bus_i' in prop:
						oldBus = inputNetwork['bus'][idx][key]['bus_i']
						newBus = 'bus' + str(newKeyID)
						newKeyID += 1
						inputNetwork['bus'][idx][key]['bus_i'] = newBus
						newBusKey.update({oldBus:newBus})
	# for dic in inputNetwork['bus']:
	# 	for key in dic:
	# 		key = int(key) - 1
	# 		for bus in inputNetwork['bus'][key]:
	# 			if 'bus_i' in inputNetwork['bus'][key][bus]:
	# 				oldBus = inputNetwork['bus'][key][bus]['bus_i']
	# 				newBus = 'bus' + str(newKeyID)
	# 				newKeyID += 1
	# 				inputNetwork['bus'][key][bus]['bus_i'] = newBus
	# 				newBusKey.update({oldBus:newBus})
	return newBusKey

def tranRandomizeNames(inputNetwork):
	newBusArray = []
	newKeyID = 0
	for dic in inputNetwork['bus']:
		for each in dic:
			idx = int(each) - 1
			for key in inputNetwork['bus'][idx]:
				for prop in inputNetwork['bus'][idx][key]:
					if 'bus_i' in prop:
						newBus = 'bus' + str(newKeyID)
						newKeyID += 1
						inputNetwork['bus'][idx][key]['bus_i'] = newBus
						newBusArray.append(newBus)
	# for key in inputNetwork['bus'][0]:
	# 	if 'bus_i' in inputNetwork['bus'][0][key]:
	# 		newBus = 'bus' + str(newKeyID)
	# 		newKeyID += 1
	# 		inputNetwork['bus'][0][key]['bus_i'] = newBus
	# 		newBusArray.append(newBus)
	return newBusArray

def tranRandomizeLocation(inputNetwork):
	# inputNetwork['bus'] = []
	# inputNetwork['gen'] = []
	# inputNetwork['branch'] = []
	for dic in inputNetwork['bus']:
		for each in dic:
			idx = int(each) - 1
			for key in inputNetwork['bus'][idx]:
				for prop in inputNetwork['bus'][idx][key]:
					if 'longitude' in prop:
						inputNetwork['bus'][idx][key]['longitude'] = random.randint(-200,200)
						inputNetwork['bus'][idx][key]['latitude'] = random.randint(-200,200)
	# for dic in inputNetwork['bus']:
	# 	for key in dic:
	# 		key = int(key) - 1
	# 		for bus in inputNetwork['bus'][key]:
	# 			if 'longitude' in inputNetwork['bus'][key][bus]:
	# 				inputNetwork['bus'][key][bus]['longitude'] = random.randint(-200,200)
	# 				inputNetwork['bus'][key][bus]['latitude'] = random.randint(-200,200)
	# for key in inputNetwork['bus'][0]:
	# 	if ('longitude' in inputNetwork['bus'][0][key]) or ('latitude' in inputNetwork['bus'][0][key]):
	# 		inputNetwork['bus'][0][key]['longitude'] = random.randint(-200,200)
	# 		inputNetwork['bus'][0][key]['latitude'] = random.randint(-200,200)
	return inputNetwork['bus']

def tranTranslateLocation(inputNetwork, translation, rotation):
	# inputNetwork['bus'] = []
	# inputNetwork['gen'] = []
	# inputNetwork['branch'] = []
	for dic in inputNetwork['bus']:
		for each in dic:
			idx = int(each) - 1
			for key in inputNetwork['bus'][idx]:
				for prop in inputNetwork['bus'][idx][key]:
					if 'longitude' in prop:
						inputNetwork['bus'][idx][key]['longitude'] = translation*math.cos(rotation)
						inputNetwork['bus'][idx][key]['latitude'] = translation*math.sin(rotation)
	# for dic in inputNetwork['bus']:
	# 	for key in dic:
	# 		key = int(key) - 1
	# 		for bus in inputNetwork['bus'][key]:
	# 			if 'longitude' in inputNetwork['bus'][key][bus]:
	# 				inputNetwork['bus'][key][bus]['longitude'] = translation*math.cos(rotation)
	# 				inputNetwork['bus'][key][bus]['latitude'] = translation*math.sin(rotation)
	# for key in inputNetwork['bus'][0]:
	# 	if ('longitude' in inputNetwork['bus'][0][key]) or ('latitude' in inputNetwork['bus'][0][key]):
	# 		inputNetwork['bus'][0][key]['longitude'] = translation*math.cos(rotation)
	# 		inputNetwork['bus'][0][key]['latitude'] = translation*math.sin(rotation)
	return inputNetwork['bus']

def tranAddNoise(inputNetwork, noisePerc):
	for array in inputNetwork:
		if (array == 'bus') or (array == 'gen') or (array == 'branch'):
			for dic in inputNetwork[array]:
				for each in dic:
					idx = int(each) - 1
					for key in inputNetwork[array][idx]:
						for prop in inputNetwork[array][idx][key]:
							if ('_bus_' not in prop) and ('status' not in prop):
								value = inputNetwork[array][idx][key][prop]
								try: 
									complex(value)
									value = float(value)
									randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
									inputNetwork[array][idx][key][prop] += str(randNoise)
								except ValueError:
									continue
	# for each in inputNetwork:
	# 	if (each == 'bus') or (each == 'gen') or (each == 'branch'):
	# 		for key in inputNetwork[each][0]:
	# 			for prop in inputNetwork[each][0][key]:
	# 				if ('_bus_' not in prop) and ('status' not in prop):
	# 					value = inputNetwork[each][0][key][prop]
	# 					try: 
	# 						complex(value)
	# 						value = float(value)
	# 						randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
	# 						inputNetwork[each][0][key][prop] += str(randNoise)
	# 					except ValueError:
	# 						continue
	# for key in inputNetwork['bus'][0]:
	# 	for prop in inputNetwork['bus'][0][key]:
	# 		if ('_bus_' not in prop) and ('status' not in prop):
	# 			value = inputNetwork['bus'][0][key][prop]
	# 			try: 
	# 				complex(value)
	# 				value = float(value)
	# 				randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
	# 				inputNetwork['bus'][0][key][prop] += str(randNoise)
	# 			except ValueError:
	# 				continue
	# for key in inputNetwork['gen'][0]:
	# 	for prop in inputNetwork['gen'][0][key]:
	# 		if ('_bus_' not in prop) and ('status' not in prop):
	# 			value = inputNetwork['gen'][0][key][prop]
	# 			try: 
	# 				complex(value)
	# 				value = float(value)
	# 				randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
	# 				inputNetwork['gen'][0][key][prop] += str(randNoise)
	# 			except ValueError:
	# 				continue
	# for key in inputNetwork['branch'][0]:
	# 	for prop in inputNetwork['branch'][0][key]:
	# 		if ('_bus_' not in prop) and ('status' not in prop):
	# 			value = inputNetwork['branch'][0][key][prop]
	# 			try: 
	# 				complex(value)
	# 				value = float(value)
	# 				randNoise = random.randint(value - noisePerc*value, value + noisePerc*value)
	# 				inputNetwork['branch'][0][key][prop] += str(randNoise)
	# 			except ValueError:
	# 				continue
	return inputNetwork


def tranModifyConductorLengths():
	pass

def tranShuffleLoads(shufPerc):
	pass



def _tests():
	# DISTRIBUTION FEEDER TESTS
	FNAME = "simpleMarketMod.omd"
	with open(FNAME, "r") as inFile:
		inputFeeder = json.load(inFile)


	# Testing distPseudomizeNames
	nameKeyDict = distPseudomizeNames(inputFeeder)
	# print nameKeyDict
	FNAMEOUT = "simplePseudo.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)

	# Testing distRandomizeNames
	randNameArray = distRandomizeNames(inputFeeder)
	# print randNameArray
	FNAMEOUT = "simpleName.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)

	# Testing distRandomizeLocation
	newLocation = distRandomizeLocation(inputFeeder)
	# print newLocation
	FNAMEOUT = "simpleLocation.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)

	# Testing distTranslateLocation
	translation = 20
	rotation = 20
	transLocation = distTranslateLocation(inputFeeder, translation, rotation)
	# print transLocation
	FNAMEOUT = "simpleTranslation.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)

	# Testing distAddNoise
	noisePerc = 0.2
	noises = distAddNoise(inputFeeder, noisePerc)
	# print noises
	FNAMEOUT = "simpleNoise.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)

	# Testing distShuffleLoads
	shufPerc = 0.5
	shuffle = distShuffleLoads(inputFeeder, shufPerc)
	# print shuffle
	FNAMEOUT = "simpleShuffle.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputFeeder, outFile, indent=4)



	# TRANSMISSION NETWORK TESTS
	FNAME = "case9.omt"
	with open(FNAME, "r") as inFile:
		inputNetwork = json.load(inFile)


	# Testing tranPseudomizeNames
	busKeyDict = tranPseudomizeNames(inputNetwork)
	# print busKeyDict
	FNAMEOUT = "casePseudo.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputNetwork, outFile, indent=4)

	# Testing tranRandomizeNames
	randBusArray = tranRandomizeNames(inputNetwork)
	# print randBusArray
	FNAMEOUT = "caseName.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputNetwork, outFile, indent=4)

	# Testing tranRandomizeLocation
	newLocation = tranRandomizeLocation(inputNetwork)
	# print newLocation
	FNAMEOUT = "caseLocation.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputNetwork, outFile, indent=4)

	# Testing tranTranslateLocation
	translation = 20
	rotation = 20
	transLocation = tranTranslateLocation(inputNetwork, translation, rotation)
	# print transLocation
	FNAMEOUT = "caseTranslation.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputNetwork, outFile, indent=4)

	# Testing tranAddNoise
	noisePerc = 0.2
	noises = tranAddNoise(inputNetwork, noisePerc)
	# print noises
	FNAMEOUT = "caseNoise.omd"
	with open(FNAMEOUT, "w") as outFile:
		json.dump(inputNetwork, outFile, indent=4)



if __name__ == '__main__':
	_tests()