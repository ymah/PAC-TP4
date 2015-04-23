from fractions import gcd
import random


def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
                lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
                x, lastx = lastx - quotient*x, x
                y, lasty = lasty - quotient*y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
        g, x, y = extended_gcd(a, m)
        if g != 1:
                raise ValueError
        return x % m

class ElgamalError(Exception):
        """Launched when something bad happen during the use of the Elgamal class.
        """

        def __init__(self, value):
                """Create a new ElgamalError with a specific message."""
                self.value = value


class Elgamal:
        """This class handle the signature, the encrytion and decryption using the
        ElGamal encryption system."""

        __X_NOT_SET = "The private part of the key (x) is not set."
        __R_NOT_CORRECT = "The r ({0}) value must be including beetween 0 and p"
        __S_NOT_CORRECT = "The s ({0}) value must be including beetween 0 and q"

        def __init__(self, p=None, g=None, h=None, x = None):
            """Create a new class Elgamal. Depends on the actions you want to
            perform, you do not have to set the x value. You have to set x, only
            if you want to perform decryption and generate signature."""
            self.__p = p
            self.__g = g
            self.__x = x
            self.__h = h

        def gcd(a, b):
                """Calculate the Greatest Common Divisor of a and b.

                Unless b==0, the result will have the same sign as b (so that when
                b is divided by it, the result comes out positive).
                """
                while b:
                        a, b = b, a % b
                        return a
        #computes base^exp mod modulus
        def modexp( self,base, exp, modulus ):
                return pow(base, exp, modulus)

        #solovay-strassen primality test.  tests if num is prime
        def SS( self,num, iConfidence ):
                #ensure confidence of t
                for i in range(iConfidence):
                #choose random a between 1 and n-2
                        a = random.randint( 1, num-1 )

                        #if a is not relatively prime to n, n is composite
                        if gcd( a, num ) > 1:
                                return False

                        #declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
                        if not self.jacobi( a, num ) % num == self.modexp ( a, (num-1)//2, num ):
                                return False

                #if there have been t iterations without failure, num is believed to be prime
                return True

        #computes the jacobi symbol of a, n
        def jacobi( self,a, n ):
                if a == 0:
                        if n == 1:
                                return 1
                        else:
                                return 0
                        #property 1 of the jacobi symbol
                elif a == -1:
                        if n % 2 == 0:
                                return 1
                        else:
                                return -1
                        #if a == 1, jacobi symbol is equal to 1
                elif a == 1:
                        return 1
                #property 4 of the jacobi symbol
                elif a == 2:
                        if n % 8 == 1 or n % 8 == 7:
                                return 1
                        elif n % 8 == 3 or n % 8 == 5:
                                return -1
                        #property of the jacobi symbol:
                        #if a = b mod n, jacobi(a, n) = jacobi( b, n )
                elif a >= n:
                        return self.jacobi( a%n, n)
                elif a%2 == 0:
                        return self.jacobi(2, n)*self.jacobi(a//2, n)
                #law of quadratic reciprocity
                #if a is odd and a is coprime to n
                else:
                        if a % 4 == 3 and n%4 == 3:
                                return -1 * self.jacobi( n, a)
                        else:
                                return self.jacobi(n, a )


        def find_primitive_root(self, p ):
            if p == 2:
                return 1
            p1 = 2
            p2 = (p-1) // p1
            #test random g's until one is found that is a primitive root mod p
            while( 1 ):
                g = random.randint( 2, p-1 )
                #g is a primitive root if for all prime factors of p-1, p[i]
                #g^((p-1)/p[i]) (mod p) is not congruent to 1
                if not (self.modexp( g, (p-1)//p1, p ) == 1):
                    if not self.modexp( g, (p-1)//p2, p ) == 1:
                        return g

        def find_prime(self,iNumBits, iConfidence):
        #keep testing until one is found
            while(1):
                #generate potential prime randomly
                p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
                #make sure it is odd
                while( p % 2 == 0 ):
                        p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

                #keep doing this if the solovay-strassen test fails
                while( not self.SS(p, iConfidence) ):
                        p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
                        while( p % 2 == 0 ):
                                p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))

                #if p is prime compute p = 2*p + 1
                #if p is prime, we have succeeded; else, start over
                p = p * 2 + 1
                if self.SS(p, iConfidence):
                        return p

        def generateKeys(self,iNumBits=256, iConfidence=32):
            #p is the prime
            #g is the primitve root
            #x is random in (0, p-1) inclusive
            #h = g ^ x mod p
            self.__p = self.find_prime(iNumBits, iConfidence)
            self.__g = self.find_primitive_root( self.__p )
            self.__x = random.randint( 1, self.__p )
            self.__h = self.modexp( self.__g, self.__x, self.__p )

        def decrypt(self, a, m):
            """Decrypt a encrypted message m. This method does not check if the
            result are consistent."""
            if self.__x == None:
                raise ElgamalError(self.__X_NOT_SET)
            h = pow(a, x, p)
            h_inv = modinv(h, p)
            decipher_text = (b * h_inv) % p
            return decipher_text

        def encrypt(self, m):
            """Encrypt the message m. m must be an interger. If not, an TypeError
            will be raise. Return a tuple like this one : (g^y, encrypted message).
            """
            if not type(m) is int:
                raise TypeError()
            y = random.randint(1, p-1)
            enc_m = m * pow(h, y, p)
            return (pow(g, y, p), enc_m)

        def sign(self, m):
            """Generate a signature for the message m. Return the result as a
                tuple (r = g^k, s). If m is not a int, raise an TypeError exception"""
            q = self.__p - 1
            k = random.randint(1, q - 1)
            while gcd(k , q) != 1:
                k = random.randint(1, q - 1)

            r = pow(g, k, self.__p)
            s = (modinv(k, q) * (m - self.__x * r)) % q
            return (r, s)


        def check_signature(self, r, s, m):
            """Take the signature elgamal and the message and check if the signature
            is correct. Return True if the signature is correct. False, otherwise.
            """
            q = self.__p - 1
            if not 0 < r < self.__p:
                raise ElgamalError(self.__R_NOT_CORRECT.format(r))
            if not 0 < s < q:
                raise ElgamalError(self.__S_NOT_CORRECT.format(s))

            g_m = pow(self.__g, m, self.__p)

            return g_m == (pow(self.__h, r, self.__p) * pow(r, s, self.__p)) % self.__p
