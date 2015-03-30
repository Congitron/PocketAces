import handAnalyzer

def factorial(value):
        total = value
        for n in range(value - 1, 1, -1):
            total *= n
        return total
    
hA = handAnalyzer.HandAnalyzer()
list = [0,1,2,3,4,5,6]
combos = hA.combos(list, 5)
for combo in combos:
    print str(combo)