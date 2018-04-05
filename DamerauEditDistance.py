import csv

def readInFiles():
	with open('dictionary.txt') as f:
		dictionary = f.read().splitlines() #dictionary is a list
	
	with open('correct.txt') as f:
		correct = f.read().splitlines() #correct answers

	with open('misspell.txt') as f:
		misspell = f.read().splitlines() #misspell words

	return(dictionary, correct, misspell)	

def DamerauEditDistance(misspellWord, dictWord):
	lengthMisspelled = len(misspellWord)
	lengthDictWord = len(dictWord)
	A = []
	for i in range(0, lengthDictWord + 1):
		A.append([0] * (lengthMisspelled + 1))
	for j in range(0, lengthDictWord + 1):
		A[j][0] = j
	for k in range(1, lengthMisspelled + 1):
		A[0][k] = k
	for column in range(1, lengthDictWord + 1):
		for row in range(1, lengthMisspelled + 1):
			if(dictWord[column-1] == misspellWord[row-1]):
				A[column][row] = A[column - 1][row - 1]
			elif(column >= 2 and row >= 2):
				if(dictWord[column-2] == misspellWord[row-1] and dictWord[column-1] == misspellWord[row-2]):
					A[column][row] = 1 + min(A[column - 2][row - 2], A[column - 1][row], A[column][row - 1], A[column - 1][row - 1])
				else:
					A[column][row] = 1 + min(A[column - 1][row - 1], A[column - 1][row], A[column][row - 1])
			else:
 				A[column][row] = 1 + min(A[column - 1][row - 1], A[column - 1][row], A[column][row - 1])
	return (A[lengthDictWord][lengthMisspelled])		

def neighbourhood(misspell, dictionary):
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
		minEdit = 10000000
		correctedWords[misspellWord].append(1)
		for dictWord in dictionary:
			editNumber = DamerauEditDistance(misspellWord, dictWord)
			if (editNumber < minEdit):
				minEdit = editNumber
				correctedWords[misspellWord] = correctedWords[misspellWord][:1]
				correctedWords[misspellWord].append(dictWord)
			elif(editNumber == minEdit):
				correctedWords[misspellWord].append(dictWord)
		print (correctedWords[misspellWord])
	return (correctedWords, nonAttempted)

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
	text_file = open("DamerauEditDistance.txt", "w")
	text_file.write("precision: %f\n" % precision)
	text_file.write("recall: %f\n" % recall)
	text_file.write("nonAttemptedWord: %d" %nonAttempted)
	text_file.close()


def misspellCorrectCorresponding(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(misspell)):
		correctAnswer[misspell[i]] = correct[i]
	return correctAnswer

def writeInCsv(correctedWords, correctAnswer):
	writeCsv = []
	for key, value in correctedWords.items():
		writeCsvRow = []
		writeCsvRow.append(key)
		writeCsvRow.append(correctAnswer[key])
		writeCsvRow.extend(value)
		writeCsv.append(writeCsvRow)
	with open("DamerauEditDistance.csv", "w", newline = '') as f:
		writer = csv.writer(f)
		writer.writerows(writeCsv)
		f.close()

def main():
	(dictionary, correct, misspell) = readInFiles()
	(correctedWords, nonAttempted) = neighbourhood(misspell, dictionary)
	correctAnswer = misspellCorrectCorresponding(misspell, correct)
	evaluate(correctAnswer, correctedWords, nonAttempted)
	writeInCsv(correctedWords, correctAnswer)

if __name__ == '__main__':
    main()
