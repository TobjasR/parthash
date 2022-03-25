#!/usr/bin/env python3
import os, sys, crypt, multiprocessing

wordlist_file = "/usr/share/wordlists/rockyou.txt"
print("wordlist:", wordlist_file)
lnum = sum(1 for _ in open(wordlist_file))
print("word count:", lnum, end = "\r\n")
salt = "12FPfchIwc0lx4NyQUgft1"
print("hash salt:", salt, end = "\r\n")
part = "S.duDROjCdLtaOdrc2ulrPwJ"
print("hash part:", part, end = "\r\n")
done = 0

# for testing purposes:
# $6$12FPfchIwc0lx4Ny$S.duDROjCdLtaOdrc2ulrPwJ20TJjedzwZjetoKGDggdQ6mZdF61lawdAKv5s3FB7G65AQ7cZip.YJUpnrZzE.
#pwd = "partyhard"
#print("pwd:", pwd, end = "\r\n")
#full = crypt.crypt(pwd, "$6$" + salt)
#print("full:", full, end = "\r\n")
#print("(part in full):", str(part in full), end = "\r\n")

def is_pass(word):
    h4sh = crypt.crypt(word, "$6$" + salt)
    if (part in h4sh):
        print("\n++++++ PASSWORD FOUND:", word, "++++++", flush=True, end = "\r\n")
        return True
    else:
        return False

# for testing purposes:
#print("++++++ TESTING FOR :", pwd, "++++++", end = "\r\n")
#print("is_pass('" + pwd + "'):", is_pass(pwd), end = "\r\n")

print("--- BEGINNING TO CRACK ---", end = "\r\n")

pool = multiprocessing.Pool(50)
results = []

with open(wordlist_file) as wordlist:
    while (w := wordlist.readline()):
        r = pool.apply_async(is_pass, [w.strip()])
        results.append(r)
        
        # don't let the queue grow too long
        if len(results) == 1000:
            results[0].wait()

        while results and results[0].ready():
            done += 1
            perc = round(done / lnum * 100, 3)
            print(f"{perc:.3f}", "% through wordlist", end = "\r", flush=True)
            r = results.pop(0)
            if r.get():
                sys.exit()

    for r in results:
        r.wait()
        if r.get():
            print("NOT FOUND", end = "\r\n")
            sys.exit()
