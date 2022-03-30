# программа, которая запускается в командной строке с параметрами, вычисляет значения корней квадратного уравнения и выводит их на печать.
# На вход программе подаются коэффициенты a, b и c.
# На печать должно выводиться два корня квадратного уравнения.

import sys
a=int(sys.argv[1])
b=int(sys.argv[2])
c=int(sys.argv[3])

#print(a, b, c)
D=(b*b-4*a*c)**0.5
x1=(-b+D)/(2*a)
x2=(-b-D)/(2*a)
print(int(x1), '\n', int(x2))
