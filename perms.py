def all_perms(str):
    for perm in all_perms(str[1:]):
        for i in range(len(perm)+1):
            #nb str[0:1] works in both string and list contexts
            print perm[:i] + str[0:1] + perm[i:]
            print i

all_perms('1267')