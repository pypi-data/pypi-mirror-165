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
        return int(self.changeToStr(),2)
def changeToStr(li:list):
    bi2 = '0b'
    for y in li:
        if y:
            bi2 += '1'
        else:
            bi2 += '0'
    return bi2
    
def changeToInt(li:list):
    return int(changeToStr(li),2)
    
def changeToBinList(string:str):
    for i in string.replace('0b',''):
        if i == '1':
            li.append(True)
        else:
            li.append(False)
    return li