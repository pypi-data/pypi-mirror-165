from operator import index


class Scanner():

    def __init__(self,line) -> None:
        self.line=line
        self.index=0


    def readNextWord(self):
        word = ""
        while self.index < len(self.line) and self.line[self.index]==' ':
            self.index += 1
        while self.index < len(self.line) and self.line[index] != ' ':
            word += self.line[self.index]
        return word
    
    def nextInt(self):
        return int(self.readNextWord())

    def nextDouble(self):
        return float(self.readNextWord().replace(",","."))