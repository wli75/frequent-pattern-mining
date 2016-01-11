#!/usr/bin/python
from collections import OrderedDict

files = ["patterns/pattern-0.txt", "patterns/pattern-1.txt", "patterns/pattern-2.txt", "patterns/pattern-3.txt", "patterns/pattern-4.txt"]

for fileN in range(0, len(files)):
	fileName = files[fileN]
	with open(fileName) as file:
		freqItemset = OrderedDict()
		closedItemset = OrderedDict()

		for line in file:
			pos = line.find("\t")
			freqItemset[ line[pos+1:].strip() ] = int( line[0:pos] )

		# group freqItems according to their support
		# once a freqItem with a distinct support is identified,
		# classify the recently found group of freqItems (they share the same support) as closed or not
		sameSup = [ freqItemset.items()[0][0] ]
		sup = freqItemset.items()[0][1]
		for i in range( 1, len(freqItemset) ):
			if freqItemset.items()[i][1] == sup:
				sameSup.append( freqItemset.items()[i][0] )
			else: # freqItemset.items()[i][1] != sup
				for j in range( 0, len(sameSup) ):
					item1Fields = sameSup[j].split(" ")
					isClosed = True
					for k in range( 0, len(sameSup) ):
						if k != j:
							item2Fields = sameSup[k].split(" ")
							match = 0
							for item1 in item1Fields:
								for item2 in item2Fields:
									if item1 == item2:
										match += 1
										break
							if match == len(item1Fields):
								isClosed = False
								break
					if isClosed:
						closedItemset[ sameSup[j] ] = sup

				sameSup = [ freqItemset.items()[i][0] ]
				sup = freqItemset.items()[i][1]
		for j in range( 0, len(sameSup) ): # classify the last batch of freqItems as closed or not
			item1Fields = sameSup[j].split(" ")
			isClosed = True
			for k in range( 0, len(sameSup) ):
				if k != j:
					item2Fields = sameSup[k].split(" ")
					match = 0
					for item1 in item1Fields:
						for item2 in item2Fields:
							if item1 == item2:
								match += 1
								break
					if match == len(item1Fields):
						isClosed = False
						break
			if isClosed:
				closedItemset[ sameSup[j] ] = sup

		# write the closed frequent itemsets into the pattern files
		fN = "closed-" + str(fileN) + ".txt"
		f = open("closed/" + fN, "w")
		for i in range( 0, len(closedItemset) ):
			f.write( str( closedItemset.items()[i][1] ) )
			f.write( "\t" )
			f.write( closedItemset.items()[i][0] )
			f.write( "\n" )

