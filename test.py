import random
msg = "d10"

new = []
temp = ""
for symbol in msg:
    try:
        x = int(symbol)
        temp = temp+symbol
    except:
        new.append(temp)
        new.append(symbol)
        temp = ""
new.append(temp)
new[0] = random.randint(1, int(new[2]))
new[1:]=new[3:]
x = 1
value = []
operator=[]
for i in new:
    x = x*-1
    if x < 0:
        value.append(i)
    else:
        operator.append(i)


result = value[0]

for op in operator:
    x = operator.index(op)
    print(result, op, value[x+1])
    if op == "+":
        result = result+int(value[x+1])
    if op == "-":
        result = result-int(value[x+1])
    if op == "/":
        result = result/int(value[x+1])
    if op == "*":
        result = result*int(value[x+1])

print(result, value[0])
