import time
import os, sys


def affichage(tab,x,y) :
    for i in range(x):
        for j in range(y):
            print(tab[i][j], "|",end="")
        print()
    print()

"""
tab = [[0,0],[0,0]]
affichage(tab,2,2)
sys.stdout.flush()
time.sleep(1)

os.system('clear')

tab = [[0,0],[0,1]]
affichage(tab,2,2)
sys.stdout.flush()
time.sleep(1)

os.system('clear')

tab = [[0,0],[1,0]]
affichage(tab,2,2)
"""


"""
print("Progression :   0%", end="")
for i in range(1, 101):
    sys.stdout.flush()
    time.sleep(0.1)
    print("\b" * 4, str(i).rjust(3), "%", sep="", end="")
print()
"""

print("test",end="")
time.sleep(1)
for i in range(0, 101):
    print("\rProgression :", str(i).rjust(3) + "%", end="")
    sys.stdout.flush()
    time.sleep(0.1)
print()
