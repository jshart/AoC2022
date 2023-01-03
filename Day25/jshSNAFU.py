class SNAFU:
    def __init__(self, input):
        # lets reverse the string - this lets us process the units first [0]
        # then the 5's [1] etc in increasing order, rather than having to do all
        # the loops backwards
        self.input = input[::-1]
        self.cols = []
        self.total = 0

    def convertToDec(self):
        power = 1
        # print("SNAFU number:{}".format(self.input))
        for c, i in enumerate(self.input):
            # print("P:{} V:{}".format(power, i))
            match i:
                case '=':
                    self.cols.append(-(power*2))
                case '-':
                    self.cols.append(-power)
                case '0':
                    self.cols.append(0)
                case '1':
                    self.cols.append(1*power)
                case '2':
                    self.cols.append(2*power)

            power *= 5

        self.total = 0
        for i in self.cols:
            # print("C:{}".format(i))
            self.total += i

        return self.total

    def printDecimal(self):
        for i in self.cols:
            print("C:{}".format(i))
        print("In dec:{}".format(self.total))


def convertToBase5(dec):
    snafu = []
    while dec > 0:
        d = dec % 5
        snafu.append(d)
        dec = dec//5
    return snafu[::-1]


def convertToSNAFU(dec):
    snafu = []

    # start by mappping to base 5
    while dec > 0:
        d = dec % 5
        snafu.append(d)
        dec = dec//5

    # next loop through and convert to SNAFU, but making the -1/-2 stuff
    for c, i in enumerate(snafu):

        # if this col is greater than 3, we need to increase the *next col* and reduce this one
        if i >= 3:
            # deal with the "overflow" case where we need to add an extra column to the number
            if c >= len(snafu)-1:
                snafu.append(0)
            snafu[c+1] += 1

            if i == 5:  # really not sure why the 5 maps to a 0 (but it does and it works, so moving on... )
                snafu[c] = 0
            elif i == 4:
                snafu[c] = -1
            elif i == 3:
                snafu[c] = -2

    # Finally just map it all into a string so we can see it in the right format
    str = ''
    for c, i in enumerate(snafu):
        match i:
            case -2:
                str += '='
            case -1:
                str += '-'
            case 0:
                str += '0'
            case 1:
                str += '1'
            case 2:
                str += '2'

    # and reverse the string back to the original order
    return str[::-1]


if __name__ == "__main__":
    print("File executed directly")

    print("#### TEST 1 convert SNAFU to dec")
    s = SNAFU("1=0")
    s.convertToDec()
    s.printDecimal()

    print("#### TEST 2 convert dec to SNAFU")
    v = 314159265
    print("SNAFU: {}".format(convertToBase5(v)))
    print("SNAFU: {}".format(convertToSNAFU(v)))
