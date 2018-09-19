import wikipedia
import time

def get_perms(prof):
    perms = set()
    perms.add(prof)

    prof = prof.replace("-", " ")
    p = prof.split()

    f = p[0]
    l = p[-1]

    mids = []
    mid_i = []
    if (len(p) > 2):
        mids += p[1:-1]
        for m in mids:
            mid_i.append(m[0])

    if "{0} {1}".format(f, l) != prof:
        perms.add("{0} {1}".format(f, l))
    perms.add("{0} {1}".format(f[0], l))
    perms.add("{0}. {1}".format(f[0], l))
    if mids:
        perms.add("{0} {1} {2}".format(f, ".".join(mid_i)+".", l))
        perms.add("{0} {1} {2}".format(f, "".join(mid_i), l))
        perms.add("{0} {1} {2}".format(f[0], mid_i[0], l))
    perms.add("{0} {1}".format(l, f[0]))

    return perms

file = open("professor_list.txt", "r")
contents = file.read()
file.close()

for prof in contents.split("\n")[280:-1]:
    try:
        wiki = wikipedia.page(prof)
        results = wikipedia.search(prof)

        title = results[0]
        perms = get_perms(prof)

        print title, perms

        html = wiki.html().encode("utf-8")
        if title in perms and (html.lower().find("robot") > -1 or html.lower().find("comput") > -1 or html.lower().find("engineer") > -1):
            file = open( "wiki_htmls/{0}.html".format(prof.replace(".", "").replace(" ", "_").lower()), "w" )
            file.write(html)
            file.close()

            print prof
        else:
            file = open( "questionable_wiki_htmls/{0}.html".format(prof.replace(".", "").replace(" ", "_").lower()), "w" )
            file.write(html)
            file.close()

            print "questionable page for " + prof

    except:
        print "no page for " + prof

    time.sleep(1)
