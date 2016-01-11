#!/usr/bin/python
from collections import OrderedDict
import math
import itertools

files = ["topic-0.txt", "topic-1.txt", "topic-2.txt", "topic-3.txt", "topic-4.txt"]

#-------------------------------

# Read in the vocab into an array
vocabMap = []
with open("vocab.txt") as file:
	for line in file:
		fields = line.strip().split("\t")
		vocabMap.append(fields[1])

#-------------------------------

# Generate Ck based on Lk-1
def apriori_gen(Lkminus1):
	Ck = OrderedDict()
	for i in range(0, len(Lkminus1)):
		l1 = Lkminus1.items()[i][0]
		for j in range(i+1, len(Lkminus1)):
			l2 = Lkminus1.items()[j][0]

			pos1 = l1.rfind(" ")
			pos2 = l2.rfind(" ")

			if pos1 == -1 and pos2 == -1:
				Ck[ l1 + " " + l2 ] = 0
			else:
				if l1[0:pos1] == l2[0:pos2]:
					c = l1 + " " + l2[pos2+1:]
					if not has_infrequent_subset(c, Lkminus1):
						Ck[c] = 0

	return Ck

#-------------------------------

# Check whether a candidate k-itemset has an infrequent (k-1)-itemset
def has_infrequent_subset(c, Lkminus1):
	fields = c.split(" ")

	for i in range( 0, len(fields)-1 ):
		subset = ""
		for j in range( 0, len(fields)-1 ):
			if i != j:
				subset += fields[j] + " "
		subset += fields[ len(fields) - 1 ]
		if subset not in Lkminus1:
			return True
	return False

#-------------------------------

# Main function

for fileN in range(0, len(files)):
	fileName = files[fileN]
	with open(fileName) as file:
		numOfTransactions = 0
		freqItemset = OrderedDict()

		iCount = [0] * len(vocabMap)
		for line in file:
			numOfTransactions += 1
			fields = [int(n) for n in line.strip().split(" ")]
			for field in fields:
				iCount[field] += 1

		# determine min_sup
		min_sup = int( math.ceil( numOfTransactions * 0.01 ) )

		# determine L1
		L = OrderedDict()
		for i in range( 0, len(iCount) ):
			if iCount[i] >= min_sup:
				L[ str(i) ] = iCount[i]
		freqItemset.update(L)

		# determine L2, L3, ...
		while len(L) != 0:
			Ck = apriori_gen(L)
			if len(Ck) == 0:
				break

			file.seek(0)
			for line in file: # iterate through transaction in db
				tFields = [ int(n) for n in line.strip().split(" ") ]

				k = len( Ck.items()[0][0].split(" ") )

				for w in itertools.combinations(tFields, k):
					c = ""
					for subW in sorted(w):
						c += str(subW) + " "
						if c.strip() in Ck:
							Ck[ c.strip() ] += 1

			L = OrderedDict()
			for i in range( 0, len(Ck) ):
				if Ck.items()[i][1] >= min_sup:
					L[ Ck.items()[i][0] ] = Ck.items()[i][1]

			freqItemset.update(L)

		# write the frequent itemsets into the pattern files
		fN = "pattern-" + str(fileN) + ".txt"
		f = open("patterns/" + fN, "w")
		for key, value in sorted(freqItemset.items(), key=lambda (k,v): (v,k), reverse=True):
			f.write( str(value) )
			line = ""
			fields = key.split(" ")
			for field in fields:
				line += vocabMap[int(field)] + " "
			f.write( "\t" + line.strip() + "\n" )

