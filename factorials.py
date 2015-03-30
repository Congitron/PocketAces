def factorial(value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
    
print factorial(3)
print factorial(4)
print factorial(5)

number = 0
for x in range(2500000):
    number += x

print number