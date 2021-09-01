import re
n = [i/4 +1/8 for i in range(4)]
m = [i/4 +1/8 for i in range(4)]
k = [i/4 +1/8 for i in range(4)]
sum = 0
counter = 0
for i in n:
    for j in n:
        for l in n:
            if (i**4 +j**4 +l**4 <=1):
                sum += -1*(l**2) *(1/64)
                print("z = {}|| z^2 = {}: ".format())
            else:
                pass
print(sum*8/12.9638)
            

