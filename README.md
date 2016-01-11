#frequentPattern.py
==========================
Generate frequent itemsets from vocab.txt and topic-i.txt to patterns/pattern-i.txt (where 0 <= i <= 4) using Apriori.

##vocab.txt
A dictionary that maps a term to an index. 
format: index	term
Columns are separated by a tab.

##topi-i.txt
Input file of frequent pattern mining algorithms. Each line represents a transaction with indices of terms.
format: term1_index term2_index term3_index ...
Columns are separated by a space.

##pattern-i.txt
Output file of frequent pattern mining algorithms. Each line represents a transaction with frequent itemsets sorted in descending order of support count.
format: support_count	term1 term2 ...
support_count and term1 are separated by a tab, while terms are separated by a space.

##Usage
- topic-i.txt and vocab.txt should be at the same level as where frequentPattern.py is
- a directory called patterns should be created first
- command to run the script: python frequentPattern.py

#closedPattern.py
==========================
Generate closed patterns from patterns/pattern-i.txt to closed/closed-i.txt (where 0 <= i <= 4).

##closed-i.txt
The format is the same as pattern-i.txt.

##Usage
- frequentPattern.py should be run first to generate the required input files patterns/pattern-i.txt
- a directory called closed should be created first
- command to run the script: python closedPattern.py

#maxPattern.py
==========================
Generate max patterns from patterns/pattern-i.txt to max/max-i.txt (where 0 <= i <= 4).

##max-i.txt
The format is the same as pattern-i.txt.

##Usage
- frequentPattern.py should be run first to generate the required input files patterns/pattern-i.txt
- a directory called max should be created first
- command to run the script: python maxPattern.py

