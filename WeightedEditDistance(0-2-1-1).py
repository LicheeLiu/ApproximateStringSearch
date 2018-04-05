import csv

def readInFiles():
	with open('dictionary.txt') as f:
		dictionary = f.read().splitlines() #dictionary is a list
	
	with open('correct.txt') as f:
		correct = f.read().splitlines() #correct answers

	with open('misspell.txt') as f:
		misspell = f.read().splitlines() #misspell words

	return(dictionary, correct, misspell)	

def NeedleWunschAlgorithm(misspellWord, dictWord, costOfMatch, costOfReplace, costOfInsertion, costOfDelete):
	lengthMisspelled = len(misspellWord)
	lengthDictWord = len(dictWord)
	A = []
	for i in range(0, lengthDictWord + 1):
		A.append([0] * (lengthMisspelled + 1))
	for j in range(0, lengthDictWord + 1):
		A[j][0] = j * costOfInsertion
	for k in range(1, lengthMisspelled + 1):
		A[0][k] = k * costOfDelete
	for column in range(1, lengthDictWord + 1):
		for row in range(1, lengthMisspelled + 1):
			A[column][row] = max(A[column][row - 1] + costOfDelete, A[column - 1][k] + costOfInsertion, A[column - 1][row - 1] + matchOrReplace(dictWord[column-1], misspellWord[row-1], costOfMatch, costOfReplace))
	return (A[lengthDictWord][lengthMisspelled])		

def matchOrReplace(char1, char2, costOfMatch, costOfReplace):
	if char1 == char2:
		return costOfMatch
	else:
		return costOfReplace

def GlobalDistance(misspell, dictionary):
	costOfMatch = 0
	costOfReplace = -2
	costOfInsertion = -1
	costOfDelete = -1
	nonAttempted = 0
	correctedWords = {}
	for misspellWord in misspell:
		print (misspellWord)
		if misspellWord in correctedWords:
			continue
		correctedWords[misspellWord] = []
		if misspellWord in dictionary:
			correctedWords[misspellWord].append(0)
			nonAttempted += 1
			correctedWords[misspellWord].append(misspellWord)
			continue	
		maxDistance = -1000000
		correctedWords[misspellWord].append(1)
		for dictWord in dictionary:
			distance = NeedleWunschAlgorithm(misspellWord, dictWord, costOfMatch, costOfReplace, costOfInsertion, costOfDelete)
			if (distance > maxDistance):
				maxDistance = distance
				correctedWords[misspellWord] = correctedWords[misspellWord][:1]
				correctedWords[misspellWord].append(dictWord)
			elif(distance == maxDistance):
				correctedWords[misspellWord].append(dictWord)
		print (correctedWords[misspellWord])
	return (correctedWords, nonAttempted)

def misspellCorrectCorresponding(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(misspell)):
		correctAnswer[misspell[i]] = correct[i]
	return correctAnswer

def evaluate(correctAnswer, correctedWords, nonAttempted):
	countPrecisionCorrect = 0
	countRecallCorrect = 0
	countPrecisionTotal = 0
	countRecallTotal = 0
	for key, value in correctedWords.items():
		if(value[0] != 0): #then this entry countribute to precision
			countPrecisionTotal += len(value) - 1 #responses for this misspelWord # -1 because the first attribute is nonAttemp mark
			for word in value: 
				if(word == correctAnswer[key]):
					countPrecisionCorrect += 1
					break
		countRecallTotal += 1
		for word in value:
			if(word == correctAnswer[key]):
				countRecallCorrect += 1
				break
	precision = float(countPrecisionCorrect) / float(countPrecisionTotal)
	recall = float(countRecallCorrect) / float(countRecallTotal)
	text_file = open("GD(0-2-1-1).txt", "w")
	text_file.write("precision: %f\n" % precision)
	text_file.write("recall: %f" % recall)
	text_file.write("nonAttemptedWord: %d" %nonAttempted)
	text_file.close()


def writeInCsv(correctedWords, correctAnswer):
	writeCsv = []
	for key, value in correctedWords.items():
		writeCsvRow = []
		writeCsvRow.append(key)
		writeCsvRow.append(correctAnswer[key])
		writeCsvRow.extend(value)
		writeCsv.append(writeCsvRow)
	with open("GlobalDistanceOuch0-2-1-1.csv", "w", newline = '') as f:
		writer = csv.writer(f)
		writer.writerows(writeCsv)
		f.close()

def main():
	(dictionary, correct, misspell) = readInFiles()
	(correctedWords, nonAttempted) = GlobalDistance(misspell, dictionary)
	correctAnswer = misspellCorrectCorresponding(misspell, correct)
	evaluate(correctAnswer, correctedWords, nonAttempted)
	writeInCsv(correctedWords, correctAnswer)



if __name__ == '__main__':	
    main()