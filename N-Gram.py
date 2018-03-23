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
	nGramDistance = len(misspellWordDistance) + len(dictionaryWordDistance) + 4 - countSame
	return nGramDistance

def n_grams_distance_method(misspell, dictionary):
	correctedWords = {}
	for misspellWord in misspell:
		print(misspellWord)
		writeincsv = []
		writeincsv.append(misspellWord)
		minDistance = 10000
		correctedWords[misspellWord] = []
		if misspellWord in dictionary:
			correctedWords[misspellWord].append(misspellWord)
			writeincsv.append(misspellWord)
			continue
		for dictionaryWord in dictionary:
			distance = n_grams_distance(misspellWord, dictionaryWord)
			if(distance < minDistance):
				minDistance = distance
				correctedWords[misspellWord] = []
				correctedWords[misspellWord].append(dictionaryWord)
			elif(distance == minDistance):
				correctedWords[misspellWord].append(dictionaryWord)
		for element in correctedWords[misspellWord]:
			writeincsv.append(element)
		with open('N-Gram.csv', 'a', newline = '') as f:
			writer = csv.writer(f)
			writer.writerow(writeincsv)
				
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

def correct_answer(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(misspell)):
		correctAnswer[misspell[i]] = correct[i]
	return correctAnswer

def main():
	with open("N-Gram.csv", 'w', newline = '') as f:
		writer = csv.writer(f)
	(dictionary, correct, misspell) = read_in_files()
	correctAnswer = correct_answer(misspell, correct)
	correctedWords = n_grams_distance_method(misspell, dictionary)
	(precision, recall) = evaluation(correctAnswer, correctedWords)
	#write_in_csv(misspell, correctedWords, dictionary)
	print(precision)
	print(recall)

if __name__ == '__main__':
    main()
