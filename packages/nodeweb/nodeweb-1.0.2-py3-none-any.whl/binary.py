class binary:
    def __init__(self,initial:str):
        self.list = []
        for i in initial.replace('0b',''):
            if i == '1':
                self.list.append(True)
            else:
                self.list.append(False)
    def add(self,num):
        bs = '0b'
        for n in self.list:
            if n:
                bs += '1'
            else:
                bs += '0'
        bi = int(bs,2)
        bi += num.changeToInt()
        bs = bin(bi)
        self.list = []
        for x in bs.replace('0b',''):
            if x == '1':
                self.list.append(True)
            else:
                self.list.append(False)
    def changeToStr(self):
        bi2 = '0b'
        for y in self.list:
            if y:
                bi2 += '1'
            else:
                bi2 += '0'
        return bi2
    def changeToInt(self):
        return int(self.changeToStr())
