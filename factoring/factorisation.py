# To change this template, choose Tools | Templates
# and open the template in the editor.

import random
import queue
import sys
import math



index = 0
def beep():
    print("\a")
def gcd(a,b):
    while b:
        a,b=b,a%b
    return a



def rabin_miller(p,tours=500):
    if(p<2):
        return False
    if(p!=2 and p%2==0):
        return False
    s=p-1
    while(s%2==0):
        s = s>>1
    for i in range(tours):
        a=random.randrange(p-1)+1
        temp=s
        mod=pow(a,temp,p)
        while(temp!=p-1 and mod!=1 and mod!=p-1):
            mod=(mod*mod)%p
            temp=temp*2
        if(mod!=p-1 and temp%2==0):
            return False
    return True

def pollard(n):
    if(n%2==0):
        return 2;
    global index
    x=random.randint(1,n-1)
    y=x
    c=random.randint(1,n-x)
    d=1
    while(d==1):
        x=(x*x+c)%n
        y=(y*y+c)%n
        y=(y*y+c)%n
        d=gcd(abs(x-y),n)
        if(d==n):
            break;
        sys.stdout.write('\r')
        index+=1
    sys.stdout.write("iterations = {0} ".format(index))
    sys.stdout.flush()

    return d;



def factor(n):
    Q_1=queue.Queue(maxsize=0)
    Q_2=[]
    Q_1.put(n)
    i = 0
    while(not Q_1.empty()):
        l=Q_1.get()
        sys.stdout.write('\r')
        sys.stdout.write("test de : {0} \n".format(l))
        sys.stdout.flush()
        if(rabin_miller(l,tours=20)):
            print(i ,"- ajout de ",l,end="\n\n")
            Q_2.append(l)
            i+=1
            continue
        d=pollard(l)
        sys.stdout.write('\r')
        sys.stdout.write("Traitement de {0} ".format(d))
        sys.stdout.flush()
        if(d==l):
            Q_1.put(l)
        else:
            Q_1.put(d)
            Q_1.put(l//d)
    return Q_2

