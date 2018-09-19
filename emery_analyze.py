import csv

schools = {}
min_profs = 20

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

international = set()
with open("international.csv", "rb") as csvin:
    csvin = csv.reader(csvin)

    for row in csvin:
        international.add(row[0])

emery_schools = {}

with open("emery_corpus.csv", "rb") as csvin:
    csv = csv.reader(csvin)

    header = next(csv)
    a = [dict(zip(header, map(str, row))) for row in csv]

    for key, value in a[0].iteritems():
        print key

    for row in a:
        univ = row["affiliation"]
        if univ not in international:
            if univ not in emery_schools:
                emery_schools[univ] = 0
            emery_schools[univ] += 1

ranked = []
for school, count in emery_schools.iteritems():
    ranked.append( (school, count) )

universities = ""

ranked = sorted(ranked, key = lambda x: x[1], reverse = True)
for inst in ranked:
    if inst[1] > min_profs:
        print inst
        universities += inst[0] + "\n"

out = open("schools.txt", "w")
out.write(universities)
out.close()
