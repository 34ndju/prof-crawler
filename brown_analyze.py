import csv
from collections import Counter

schools = {}


with open("brown_corpus.tsv", "rb") as tsvin:
    tsv = csv.reader(tsvin, delimiter='\t')

    header = next(tsv)
    a = [dict(zip(header, map(str, row))) for row in tsv]

    for key, value in a[0].iteritems():
        print key


    for row in a:
        univ = row["University"]
        if univ not in schools:
            schools[univ] = 0
        schools[univ] += 1


for school, count in schools.iteritems():
    print "{0}: {1}".format(count, school)
