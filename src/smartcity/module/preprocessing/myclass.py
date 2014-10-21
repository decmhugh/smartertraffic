class Robot:
    def __init__(self):
        self.__priv = "I am private"
        self._prot = "I am protected"
        self.pub = "I am public"
        print("__init__ has been executed!")
        print(self.__str__)
    a = 1

if __name__ == "__main__":
    x = Robot()
    y = Robot()
    y2 = y
    print(x.__priv)