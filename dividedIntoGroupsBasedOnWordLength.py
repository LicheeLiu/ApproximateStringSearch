import csv

def readInCsv(filename):
	with open(filename, 'r') as f:
		result = [row for row in csv.reader(f.read().splitlines())]
	for row in result:
		if(row[-1] == 0):
			result.remove(row)
	return result 

def evaluation(result):
	countPrecisionTotal3 = 0
	countRecallTotal3 = 0
	countCorrect3 = 0
	countPrecisionTotal5 = 0
	countRecallTotal5= 0
	countCorrect5 = 0	
	countPrecisionTotal7 = 0
	countRecallTotal7 = 0
	countCorrect7 = 0	
	countPrecisionTotalmore = 0
	countRecallTotalmore = 0
	countCorrectmore = 0	
	for row in result:
		if(len(row[0]) <= 3):
			countRecallTotal3 += 1
			countPrecisionTotal3 += len(row) - 2
			for i in range(2, len(row)):
				if row[1] == row[i]:
					countCorrect3 += 1
					break
		elif(len(row[0]) <= 5):
			countRecallTotal5 += 1
			countPrecisionTotal5 += len(row) - 2
			for i in range(2, len(row)):
				if row[1] == row[i]:
					countCorrect5 += 1
					break
		elif(len(row[0]) <= 7):
			countRecallTotal7 += 1
			countPrecisionTotal7 += len(row) - 2
			for i in range(2, len(row)):
				if row[1] == row[i]:
					countCorrect7 += 1
					break
		else:
			countRecallTotalmore += 1
			countPrecisionTotalmore += len(row) - 2
			for i in range(2, len(row)):
				if row[1] == row[i]:
					countCorrectmore += 1
					break
	precision3 = float(countCorrect3)/float(countPrecisionTotal3)
	precision5 = float(countCorrect5) / float(countPrecisionTotal5)
	precision7 = float(countCorrect7) / float(countPrecisionTotal7)
	precisionMore = float(countCorrectmore) / float(countPrecisionTotalmore)
	recall3 = float(countCorrect3) / float(countRecallTotal3)
	recall5 = float(countCorrect5) / float(countRecallTotal5)
	recall7 = float(countCorrect7) / float(countRecallTotal7)
	recallMore = float(countCorrectmore) / float(countRecallTotalmore)
	text_file = open("NGramDiceCoefficient.txt", "w")
	text_file.write("precision3: %f\n" % precision3)
	text_file.write("recall3: %f\n" % recall3)
	text_file.write("precisionToatl3: %d\n" % countPrecisionTotal3)
	text_file.write("RecallTotal3: %d\n" % countRecallTotal3)
	text_file.write("precision5: %f\n" % precision5)
	text_file.write("recall5: %f\n" % recall5)	
	text_file.write("precisionToatl5: %d\n" % countPrecisionTotal5)
	text_file.write("RecallTotal5: %f\n" % countRecallTotal5)
	text_file.write("precision7: %f\n" % precision7)
	text_file.write("recall7: %f\n" % recall7)	
	text_file.write("precisionToatl7: %d\n" % countPrecisionTotal7)
	text_file.write("RecallTotal7: %f\n" % countRecallTotal7)
	text_file.write("precisionMore: %f\n" % precisionMore)
	text_file.write("recallMore: %f\n" % recallMore)
	text_file.write("precisionToatlMore: %d\n" % countPrecisionTotalmore)
	text_file.write("RecallTotalMore: %f\n" % countRecallTotalmore)	
	text_file.close()


def  main():
	result = readInCsv("NGramDiceCoefficient.csv")
	evaluation(result)

if __name__ == '__main__':	
    main()