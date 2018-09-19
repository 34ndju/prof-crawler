def get_perms(prof):
    perms = []
    perms.append(prof)

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
        perms.append("{0} {1}".format(f, l))
    perms.append("{0} {1}".format(f[0], l))
    perms.append("{0}. {1}".format(f[0], l))
    if mids:
        perms.append("{0} {1} {2}".format(f, ".".join(mid_i)+".", l))
        perms.append("{0} {1} {2}".format(f, "".join(mid_i), l))
        perms.append("{0} {1} {2}".format(f[0], mid_i[0], l))
    perms.append("{0} {1}".format(l, f[0]))

    return perms


file = open("professor_list.txt", "r")
contents = file.read()
file.close()

file = open("new_professor_list.txt", "w")

for prof in contents.split("\n"):
    if len(prof) > 0:
        perms = get_perms(prof)
        for p in perms:
            file.write(p)
            file.write("\n")
file.close()
