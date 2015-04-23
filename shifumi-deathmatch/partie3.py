from client import *
import math
from random import randint
from elgamal import *
#------------------------------------------
#USEFULL functions :
#------------------------------------------




NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP4/'
urlPartie='shifumi-deathmatch/'
urlRep='verify/'+NOM



urlPK='PK/'+NOM



server = Server(base_url=urlTp+urlPartie)
#------------------------------------------
#------------------------------------------

#on:

ON='insert-coin/'+NOM

# moves :

PIERRE = 88275625857605
FEUILLE = 19779480974019653
CISEAUX = 18939445432636760


#start

START = 'start/'+NOM


#move

MOVE = 'move'


#result

RESULT = 'result'




#TP


el = Elgamal()

el.generateKeys()

print(m = el.encrypt(1236))
print(el.decrypt(m))
