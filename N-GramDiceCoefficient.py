import csv

def read_in_files():
	with open('dictionary.txt') as f:
		dictionary = f.read().splitlines()
	
	with open('correct.txt') as f:
		correct = f.read().splitlines()

	with open('misspell.txt') as f:
		misspell = f.read().splitlines()

	return(dictionary, correct, misspell)

def n_grams_distance(misspellWord, dictionaryWord):
	misspellWordDistance = []
	dictionaryWordDistance = []
	for i in range(0, len(misspellWord) - 1):
		misspellWordDistance.append(misspellWord[i:i+2])
	for i in range(0, len(dictionaryWord) - 1):
		dictionaryWordDistance.append(dictionaryWord[i:i+2])
	countSame = 0
	for i in range(0, len(misspellWordDistance)):
		for j in range(0, len(dictionaryWordDistance)):
			if(misspellWordDistance[i] == dictionaryWordDistance[j]):
				countSame += 1
		if(misspellWord[0] == dictionaryWord[0]):
			countSame += 1
		if(misspellWord[len(misspellWord) -1] == dictionaryWord[len(dictionaryWord) -1]):
			countSame += 1
	nGramSimilarity = float(2*countSame) / float(len(misspellWord) + len(dictionaryWord) + 4)
	return nGramSimilarity

def n_grams_distance_method(misspell, dictionary):
	correctedWords = {}
	for misspellWord in misspell:
		print(misspellWord)
		maxDistance = float(-5)
		if misspellWord in correctedWords:
			del correctedWords[misspellWord][:]
		else:
			correctedWords[misspellWord] = []
		if misspellWord in dictionary:
			correctedWords[misspellWord].append(misspellWord)
			correctedWords[misspellWord].append(0)
			continue
		for dictionaryWord in dictionary:
			distance = n_grams_distance(misspellWord, dictionaryWord)
			if(distance > maxDistance):
				maxDistance = distance
				del correctedWords[misspellWord][:]
				correctedWords[misspellWord].append(dictionaryWord)
			elif(distance == maxDistance):
				correctedWords[misspellWord].append(dictionaryWord)
	return correctedWords

def evaluation(correctAnswer, correctedWords):
	countMatch = 0
	precisionTotalCount = 0
	recallTotalCount = 0
	for key, value in correctedWords.items():
		for i in range(0, len(value)):
			precisionTotalCount += len(value)
			recallTotalCount += 1
			if(value[i] == correctAnswer[key]):
				countMatch += 1
				break
	precision = float(countMatch) / float(precisionTotalCount)
	recall = float(countMatch) / float(recallTotalCount)
	return (precision, recall)

'''
def write_in_csv(misspell, correctedWords, dictionary):

	with open("correct_dic_output.csv", "wb") as f:
		writer = csv.writer(f)
		for word in dictionary:
			writer.writerow([word])

	with open("correctDic.csv", "wb") as f:
		writer = csv.writer(f)
		for key, value in correctedWords.items():
			writer.writerow([key, value])
'''

def writeInCsv(correctAnswer, correctedWords):
	csvFile = []
	for key, value in correctedWords.items():
		csvRow = []
		csvRow.append(key)
		csvRow.append(correctAnswer[key])
		csvRow.extend(value)
		csvFile.append(csvRow)
	with open("NGramDiceCoefficient.csv", "w", newline = '') as f:
		writer = csv.writer(f)
		writer.writerows(csvFile)
		f.close()


def correct_answer(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(misspell)):
		correctAnswer[misspell[i]] = correct[i]
	return correctAnswer

def main():
	(dictionary, correct, misspell) = read_in_files()
	correctAnswer = correct_answer(misspell, correct)
	correctedWords = n_grams_distance_method(misspell, dictionary)
	writeInCsv(correctAnswer, correctedWords)
	(precision, recall) = evaluation(correctAnswer, correctedWords)
	#write_in_csv(misspell, correctedWords, dictionary)
	print(precision)
	print(recall)	
	text_file = open("NGramDiceCoefficient.txt", "w")
	text_file.write("precision: %f\n" % precision)
	text_file.write("recall: %f" % recall)
	text_file.close()

if __name__ == '__main__':
    main()
