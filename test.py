import math
list = [1,2,3,4]
list2 =[0,3,4,5]
a = 4
b= math.sqrt(reduce (lambda x , y: x+y, map(lambda x: x*x, list)))
print a
print b
