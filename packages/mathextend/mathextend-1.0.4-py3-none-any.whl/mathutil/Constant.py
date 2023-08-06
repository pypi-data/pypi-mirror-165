import decimal


def pi(n: int)->decimal.Decimal:
    decimal.setcontext(decimal.Context(prec=n, rounding=decimal.ROUND_HALF_DOWN))
    return decimal.Decimal(round(
        3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803, n))+decimal.Decimal(0)


decimal.setcontext(decimal.Context(prec=97, rounding=decimal.ROUND_HALF_DOWN))
pi_n = decimal.Decimal(
    3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421)+decimal.Decimal(0)
decimal.setcontext(decimal.Context(prec=2, rounding=decimal.ROUND_HALF_DOWN))
pi_approximate_rate = decimal.Decimal(round(22/7, 2))+decimal.Decimal(0)
pi05 = 3.14159
decimal.setcontext(decimal.Context(prec=6, rounding=decimal.ROUND_HALF_DOWN))
pi_density = decimal.Decimal(round(355/113, 6))+decimal.Decimal(0)
pi10 = 3.1415926535
pi15 = 3.141592653589793
decimal.setcontext(decimal.Context(prec=20, rounding=decimal.ROUND_HALF_DOWN))
pi20 = decimal.Decimal(3.14159265358979323846)+decimal.Decimal(0)
decimal.setcontext(decimal.Context(prec=25, rounding=decimal.ROUND_HALF_DOWN))
pi25 = decimal.Decimal(3.1415926535897932384626433)+decimal.Decimal(0)
decimal.setcontext(decimal.Context(prec=30, rounding=decimal.ROUND_HALF_DOWN))
pi30 = decimal.Decimal(3.141592653589793238462643383279)+decimal.Decimal(0)


def e(n: int)->decimal.Decimal:
    decimal.setcontext(decimal.Context(prec=n, rounding=decimal.ROUND_HALF_DOWN))
    return decimal.Decimal(round(
        2.71828182845904523536028747135266249775724709369995957496696762772407663035354759457138, n))+decimal.Decimal(0)


decimal.setcontext(decimal.Context(prec=97, rounding=decimal.ROUND_HALF_DOWN))
e_n = decimal.Decimal(
    2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251)+decimal.Decimal(0)
e05 = 2.71828
e10 = 2.7182818284
e15 = 2.718281828459045
decimal.setcontext(decimal.Context(prec=20, rounding=decimal.ROUND_HALF_DOWN))
e20 = decimal.Decimal(2.71828182845904523536)+decimal.Decimal(0)
decimal.setcontext(decimal.Context(prec=25, rounding=decimal.ROUND_HALF_DOWN))
e25 = decimal.Decimal(2.7182818284590452353602874)+decimal.Decimal(0)
decimal.setcontext(decimal.Context(prec=30, rounding=decimal.ROUND_HALF_DOWN))
e30 = decimal.Decimal(2.718281828459045235360287471352)+decimal.Decimal(0)
