import csv

def readInFiles():
	with open('dictionary.txt') as f:
		dictionary = f.read().splitlines() #dictionary is a list
	
	with open('correct.txt') as f:
		correct = f.read().splitlines() #correct answers

	with open('misspell.txt') as f:
		misspell = f.read().splitlines() #misspell words

	return(dictionary, correct, misspell)	

def correctAnswerDic(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(misspell)):
		correctAnswer[misspell[i]] = correct[i]
	return correctAnswer	

def nGramsDistance(misspellWord, dictionaryWord):
	misspellWordSubstring = []
	dictionarySubstring = []
	for i in range(0, len(misspellWord) - 1):
		misspellWordSubstring.append(misspellWord[i : i+2])
	for i in range(0, len(dictionaryWord) - 1):
		dictionarySubstring.append(dictionarySubstring[i : i+2])
	countSame = 0
	for i in range(0, len(misspellWordSubstring)):
		for j in range(0, len(dictionarySubstring)):
			if (misspellWordSubstring[i] == dictionarySubstring[j]):
				countSame += 1
	if(misspellWord[0] == dictionaryWord[0]):
		countSame += 1
	if(misspellWord[-1] == dictionaryWord[-1]):
		countSame += 1
	nGramsDistance = len(misspellWordSubstring) + len(dictionaryWord) + 4 - 2 * countSame
	return nGramsDistance	

def nGramsDistanceMethod(misspell, dictionary):
	correctedWords = {}
	nonAttempted = 0
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
		minDistance = 10000000000
		correctedWords[misspellWord].append(1)
		for dictionaryWord in dictionary:
			distance = nGramsDistance(misspellWord, dictionaryWord)
			if(distance < minDistance):
				minDistance = distance
				correctedWords[misspellWord] = correctedWords[misspellWord][1:]
				correctedWords[misspellWord].append(dictionaryWord)
			elif(distance == minDistance):
				correctedWords[misspellWord].append(dictionaryWord)
		print(correctedWords[misspellWord])
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
	text_file = open("NGDistance.txt", "w")
	text_file.write("precision: %f\n" % precision)
	text_file.write("recall: %f" % recall)
	text_file.write("nonAttemptedWord: %d" %nonAttempted)
	text_file.close()
	return (precision, recall)	

def writeInCsv(correctedWords, correctAnswer):
	writeCsv = []
	for key, value in correctedWords.items():
		writeCsvRow = []
		writeCsvRow.append(key)
		writeCsvRow.append(correctAnswer[key])
		writeCsvRow.extend(value)
		
def writeInCsv(correctedWords, correctAnswer):
	writeCsv = []
	for key, value in correctedWords.items():
		writeCsvRow = []
		writeCsvRow.append(key)
		writeCsvRow.append(correctAnswer[key])
		writeCsvRow.extend(value)
		writeCsv.append(writeCsvRow)
	with open("NGDistance.csv", "w", newline = '') as f:
		writer = csv.writer(f)
		writer.writerows(writeCsv)
		f.close()


def main():
	(dictionary, correct, misspell) = readInFiles()
	correctAnswer = correctAnswerDic(misspell, correct)
	(correctedWords, nonAttempted) = nGramsDistanceMethod(misspell, dictionary)
	print (correctedWords)
	(precision, recall) = evaluate(correctAnswer, correctedWords, nonAttempted)
	writeInCsv(correctedWords, correctAnswer)
	print(precision)
	print(recall)	


if __name__ == '__main__':	
    main()