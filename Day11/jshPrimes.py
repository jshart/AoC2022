import math


class PrimeFactors:
    def __init__(self, input):
        self.input = input
        self.factors = []
        self.factorise()

    def print(self):
        print(" [Original Number is:{}] ".format(self.input), end='')

    # A function to print all prime factors of
    # a given number n
    # modified from here;
    # https://www.geeksforgeeks.org/print-all-prime-factors-of-a-given-number/
    def factorise(self):

        self.factors.clear()
        n = self.input

        # Print the number of two's that divide n
        while n % 2 == 0:
            self.factors.append(2)
            n = n / 2

        # n must be odd at this point
        # so a skip of 2 ( i = i + 2) can be used
        for i in range(3, int(math.sqrt(n))+1, 2):

            # while i divides n , print i and divide n
            while n % i == 0:
                self.factors.append(int(i))
                n = n / i

        # Condition if n is a prime
        # number greater than 2
        if n > 2:
            self.factors.append(int(n))

        print(self.factors, end='')

    # this reverses the factorisation and compiles the number
    # back into its complete int value
    def compile(self):
        a = 1
        for i in self.factors:
            a *= i

        self.input = a
        print(" [Compiled factors are:{}] ".format(a), end='')

    def multipleByPF(self, n):
        self.factors.extend(n)
        print(" [{}] ".format(self.factors), end='')
        self.compile()

    def isDivisibleBy(self, n):
        if n in self.factors:
            return True
        else:
            return False


if __name__ == "__main__":
    print("File executed directly")

    print("#### TEST 1: find PF's for first n ints")
    for i in range(2, 50):
        pf = PrimeFactors(i)
        pf.print()
        pf.factorise()
        if pf.isDivisibleBy(3):
            print(" [Divisibe by 3] ", end='')
        pf.compile()
        if pf.input != i:
            print("**** ERROR **** i {}!= input {}".format(i, pf.input))
        print()

    print("#### TEST 2: multiple by factorised number (10)")
    pf.print()
    pf.multipleByPF([5, 2])
    print()
    pf.factorise()

    print("#### TEST 3: factorise a really big number")
    pf = PrimeFactors(1000000000000)
    pf.factorise()

