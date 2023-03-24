class Test:
    def __init__(self):
        def A():
            self.a = 1
        def Add():
            self.a += 1
        A()
        Add()
        print(self.a)

test = Test()
