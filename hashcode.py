import sys
from random import randrange

def calcScore(a, b, c):
    return (a * pow(b, 5)) / pow(c, 2)

debug = False

B, L, D = list(map(int, input().replace("\n", "").split(" ")))
scores = list(map(int, input().replace("\n", "").split(" ")))

taken_books = [False] * B

libraries = []

count = 0
while True:
    line = sys.stdin.readline()
    if not line or line == "\n":
        break

    l = {}
    l["id"] = count
    count += 1
    l["n"], l["signup"], l["bpd"] = list(map(int, line.replace("\n", "").split(" ")))
    
    line = sys.stdin.readline()
    l["books"] = list(map(int, line.split(" ")))
    l["books"] = sorted(l["books"], key = lambda i: scores[i], reverse=True)
    
    s = 0
    for i in range(l["n"]):
        s += scores[l["books"][i]]

    l["score"] = calcScore(s, l["bpd"], l["signup"])

    l["index"] = 0

    libraries.append(l)

libraries = sorted(libraries, key = lambda i: i['score'], reverse=True)

#if debug:
    #print(libraries)

active_libs = []

signing = libraries[0]["signup"]
actually_sign = 0

scanned_libs = {}
for i in range(L):
    scanned_libs[i] = []

done_libs = []

for day in range(D):
    if debug:
        print("Day:", day, "signing:", signing, "Actually signing", actually_sign)
        print("Scanned Libs", scanned_libs)

    if signing == 0:
        active_libs.append(libraries[actually_sign])

        actually_sign = actually_sign + 1
        if actually_sign < L:
            if debug:
                print("Actu sign", actually_sign)

            signing = libraries[actually_sign]["signup"]
    elif debug:
        print("Waiting for signing")

    for i in range(len(active_libs)):
        l = active_libs[i]
        
        # manda l['lpb'] libri con criterio
        j = 0
        taken_today = 0
        while taken_today < l["bpd"]:
            book_used = l["index"] + j
            if debug:
                print("book:", book_used)

            if book_used >= len(l["books"]):
                done_libs.append(l)
                if debug:
                    print("Done library", i)
                break

            elif not taken_books[l["books"][book_used]]:
                book = l["books"][book_used]
                taken_books[book] = True # Prendo

                if debug:
                    print("I'm adding", book)

                scanned_libs[l["id"]].append(book)
                taken_today += 1
            
            elif debug:
                print(book_used, "already taken")

            j += 1
        
        l["index"] += l["bpd"]

    signing -= 1
    if debug:
        print("act libs", active_libs)
        print("done libs", done_libs)
        print("\n\n")

    for done in done_libs:
        active_libs.remove(done)
    done_libs = []

if debug:
    print("scanned libs", scanned_libs)

n_libs = 0
for key in scanned_libs.keys():
    if len(scanned_libs[key]) > 0:
        n_libs += 1

print(n_libs)

for key in scanned_libs.keys():
    if len(scanned_libs[key]) > 0:
        print(key, len(scanned_libs[key]))
        
        for x in scanned_libs[key]:
            print(x, end=" ")

        print()

