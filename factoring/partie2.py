from client import *
import math
import os
from random import randint
from factorisation import *
from multiprocessing import *
#------------------------------------------
#USEFULL functions :
#------------------------------------------
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, \
                                               divmod(lastremainder,\
                                                      remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), \
        lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a
#------------------------------------------
#------------------------------------------




NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP4/'
urlPartie='factoring/'
urlRep='submit/'+NOM




server = Server(base_url=urlTp+urlPartie)
#------------------------------------------
#------------------------------------------

#------------------------------------------
# TOOLS
#------------------------------------------

#------------------------------------------
#------------------------------------------

#------------------------------------------
# TP
#------------------------------------------


urlN = 'get/'




if __name__=="__main__":
    niveau = '3'
    classe = 'B'
    resQuery = server.query(url=urlN+niveau+'/'+classe)
    print(resQuery)
    ident = resQuery['id']
    N = resQuery['n']
    L = factor(N)
    print(L)
    while(i<len(L)):
        cnt=L.count(L[i])
        print(L[i],end=" ")
        i+=cnt
        print('\n')
    res = server.query(url=urlRep,parameters={'id':ident,'factors':L})

    print(res)

