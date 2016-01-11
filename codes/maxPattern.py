#!/usr/bin/python
from collections import OrderedDict

files = ["patterns/pattern-0.txt", "patterns/pattern-1.txt", "patterns/pattern-2.txt", "patterns/pattern-3.txt", "patterns/pattern-4.txt"]

for fileN in range(0, len(files)):
	fileName = files[fileN]
	with open(fileName) as file:
		freqItemset = {}
		maxItemset = OrderedDict()

		max = 0
		for line in file:
			line = line.strip()
			num = line.count(" ")
			if num > max:
				max = num
			if num in freqItemset:
				freqItemset[num].append( line )
			else:
				freqItemset[num] = [line]

		for key, value in sorted(freqItemset.items(), reverse=True):
			if key == max:
				# classify all frequent n-itemset (where n is the max value) as maximal
				for i in range(0, len(value)):
					pos = value[i].find("\t")
					maxItemset[ value[i][pos+1:] ] = int( value[i][0:pos] )
			else:
				# classify frequent n-itemset (where n is not max) as maximal or not
				for i in range(0, len(value)):
					pos1 = value[i].find("\t")
					item1Fields = value[i][pos1+1:].split(" ")
					isMax = True
					for item2, value2 in maxItemset.items():
						item2Fields = item2.split(" ")
						match = 0
						for item1 in item1Fields:
							for item2 in item2Fields:
								if item1 == item2:
									match += 1
									break
						if match == len(item1Fields):
							isMax = False
							break
					if isMax:
						maxItemset[ value[i][pos1+1:] ] = int( value[i][0:pos1] )

		# write the maximal frequent itemsets into the pattern files
		fN = "max-" + str(fileN) + ".txt"
		f = open("max/" + fN, "w")
		for key, value in sorted(maxItemset.items(), key=lambda (k,v): (v,k), reverse=True):
			f.write( str(value) )
			f.write( "\t" )
			f.write( key )
			f.write( "\n" )

