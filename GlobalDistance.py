import csv

def read_in_files():
	with open('dictionary.txt') as f:
		dictionary = f.read().splitlines()
	
	with open('correct.txt') as f:
		correct = f.read().splitlines()

	with open('misspell.txt') as f:
		misspell = f.read().splitlines()

	return(dictionary, correct, misspell)

def Needleman_Wunsch_Algorithm(f, t, costOfMatch, costOfReplace, costOfInsertion, CostOfDelet):
	lf = len(f)
	lt = len(t)
	#initialize the 2d list which has lf+1 row and lt+1 column
	A = []
	for i in range(0, lf+1):
		A.append([0] * (lt+1))
	#initialize the first row and first column
	for j in range(0, lf+1):
		A[j][0] = j * costOfInsertion
	for k in range(1, lt+1):
		A[0][k] = k * CostOfDelet
	for j in range(1, lf+1):
		for k in range(1, lt+1):
			A[j][k] = max(A[j][k-1] + CostOfDelet, A[j-1][k] + costOfInsertion, matchOrReplace(f[j-1], t[k-1], costOfMatch, costOfReplace))
	return(A[lf][lt])

def matchOrReplace(a, b, costOfMatch, costOfReplace):
	if a == b:
		return costOfMatch
	else:
		return costOfReplace

def misspelled_dictionary_corresponding(misspell, correct):
	correctAnswer = {}
	for i in range(0, len(correct)):
		correctAnswer[misspell[i]] = correct
	return correctAnswer


def evaluate(correctAnswer, correctedWords, nonAttempted):
	countPrecisionCorrect = 0
	countRecallCorrect = 0
	countTotalKey = 0
	countTotalValue = 0
	for key, value in correctedWords.items():
		countTotalKey += 1
		countTotalValue += len(value)
		for word in value:
			if(word == correctAnswer[key]):
				countRecallCorrect += 1
				countPrecisionCorrect += 1
				break
	precision = float(countPrecisionCorrect) / float(countTotalKey)
	recall = float(countRecallCorrect) / float(countTotalValue)
	return(precision, recall)

def neighbourhood_method(misspell, dictionary):
	costOfMatch = 1
	costOfReplace = -1
	costOfInsertion= -1
	CostOfDelet = -1
	correctedWords = {}
	nonAttempted = 0 #the word is in the dictionary. The system does not try to correct it.
	for misspellWord in misspell:
		writeincsv = []
		writeincsv.append(misspellWord)
		print(misspellWord)
		correctedWords[misspellWord] = []
		if misspellWord in dictionary:
			correctedWords[misspellWord].append(misspellWord)
			writeincsv.append(misspellWord)
			nonAttempted += 1
			continue
		maxDistance = -10000
 	#put all words in if there are ties
		for dicWord in dictionary:
			distance = Needleman_Wunsch_Algorithm(misspellWord, dicWord, costOfMatch, costOfReplace, costOfInsertion, CostOfDelet)
			if(distance > maxDistance):
				maxDistance = distance
				correctedWords[misspellWord] = []
				correctedWords[misspellWord].append(dicWord)
			elif(distance == maxDistance):
				correctedWords[misspellWord].append(dicWord)
		for element in correctedWords[misspellWord]:
			writeincsv.append(element)
		with open('GloablDistance.csv', 'a', newline = '') as f:
			writer = csv.writer(f)
			writer.writerow(writeincsv)
	return (correctedWords, nonAttempted)

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

def main():
	with open("GloablDistance.csv", 'w', newline = '') as f:
		writer = csv.writer(f)
	(dictionary, correct, misspell) = read_in_files()
	(correctedWords, nonAttempted) = neighbourhood_method(misspell, dictionary)
	correctAnswer = misspelled_dictionary_corresponding(misspell, correct)
	(precision, recall) = evaluate(correctAnswer, correctedWords, nonAttempted)
	#write_in_csv(misspell, correctedWords, dictionary)
	print (precision)
	print (recall)
	


if __name__ == '__main__':	
    main()


