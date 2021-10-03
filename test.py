import copy


a = [(1, 3), (2, 3)]

if (1, 3) in a:
    a.remove((1, 3))
print(a)

b = []
if b and b[1]:
    print('+')

c = {(2, 3): [(2, 7), (4, 7)]}

print(copy.deepcopy(c))
d = copy.copy(c)

d[(2, 3)].remove((2, 7))
print((2, 4) == (2, 4))
print(c)

print([4, 6]+[4, 8])
