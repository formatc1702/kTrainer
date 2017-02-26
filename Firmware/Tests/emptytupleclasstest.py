class test:
    def __init__(self, a, b=()):
        self.a = a
        self.b = b

test1 = test(1,(1,2,3))
test2 = test(3)

print(test1.a, test1.b)
print(test2.a, test2.b)

test2.b = (4,5,6)

print(test2.a, test2.b)
