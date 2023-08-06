class Fraction:
    def __init__(self, numerator: int, denominator: int) -> None:
        self.__numerator = numerator
        self.__denominator = denominator

    def __int__(self):
        return int(round(self.__numerator / self.__denominator, 0))

    def __str__(self):
        return f'{self.__numerator}/{self.__denominator}'

    def __repr__(self):
        return f'{self.__numerator}/{self.__denominator}'

    def __abs__(self):
        return abs(round(self.__numerator / self.__denominator, 2))

    def __bool__(self):
        return True if self.__numerator != 0 else False

    def __float__(self):
        return round(self.__numerator / self.__denominator, 2)

    def divide(self):
        if self.__numerator == self.__denominator:
            self.__numerator = 1
            self.__denominator = 1
        for i in range((self.__numerator if self.__numerator >= self.__denominator else self.__denominator) + 1, 2, -1):
            if self.__numerator % i == 0 and self.__denominator % i == 0:
                self.__numerator //= i
                self.__denominator //= i
                break

    def __add__(self, other):
        for i in range(self.__denominator if self.__denominator >= other.__denominator else other.__denominator,
                       self.__denominator * other.__denominator):
            if i % self.__denominator == 0 and i % other.__denominator == 0:
                self.__denominator = i
                b = i // self.__denominator
                c = i // other.__denominator
                break
        self.__numerator *= b
        d = other.__numerator * c
        self.__numerator += d
        self.divide()

    def __subtract__(self, other):
        for i in range(self.__denominator if self.__denominator >= other.__denominator else other.__denominator,
                       self.__denominator * other.__denominator):
            if i % self.__denominator == 0 and i % other.__denominator == 0:
                self.__denominator = i
                b = i // self.__denominator
                c = i // other.__denominator
                break
        self.__numerator *= b
        d = other.__numerator * c
        self.__numerator -= d
        self.divide()

    def __multiply__(self, other):
        self.__denominator *= other.__denominator
        self.__numerator *= other.__numerator
        self.divide()

    def __division__(self, other):
        t = other.__numerator
        other.__denominator = other.__numerator
        other.__numerator = t
        self.__multiply__(other)

    def pprint(self, output_type):
        if output_type == 0:
            print('''\
 {0:d} 
-{1:<s}-
 {2:d}\
            '''.format(self.__numerator, "-" * len(str(self.__numerator if self.__numerator >= self.__denominator else self.__denominator)), self.__denominator))
        elif output_type == 1:
            print(self.__str__())


def create_fraction_from_numerator_and_denominator(numerator: int, denominator: int) -> Fraction:
    return Fraction(numerator, denominator)


def create_fraction_from_float(num: float) -> Fraction:
    denominator = 10 ** len(str(num).split('.')[1])
    numerator = int(denominator * num)
    return Fraction(numerator, denominator)


def create_fraction_from_string(string: str) -> Fraction:
    denominator = 10 ** len(string.split('.')[1])
    numerator = int(denominator * float(string))
    return Fraction(numerator, denominator)


def create_fraction_from_parent_list(*parent_list) -> Fraction:
    return Fraction(parent_list[0], parent_list[1])


def create_fraction_from_parent_dict(**parent_dict) -> Fraction:
    return Fraction(parent_dict['numerator'], parent_dict['denominator'])
