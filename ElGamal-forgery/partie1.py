from client import *
import math
from random import randint
from factorisation import *
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
urlPartie='ElGamal-forgery/'
urlRep='verify/'+NOM



urlPK='PK/'+NOM



server = Server(base_url=urlTp+urlPartie)
#------------------------------------------
#------------------------------------------



resDict=server.query(url=urlPK)
p=resDict['p']
g=resDict['g']
h=resDict['h']
q=p-1


e = randint(1,q)


v = 0
while gcd(v,q) != 1:
    v = randint(1,q)

r = pow(g,e,p)*pow(h,v,p) % p
s = (-r) * modinv(v,q) % q

print(r)
print(s)
m = e*s%q

print(m)


dicRep ={'m': m, 'signature': (r,s) }




rep=server.query(url=urlRep,parameters=dicRep)

print(rep)
