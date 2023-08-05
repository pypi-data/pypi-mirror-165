from src.io.reader import Reader
from typing import List

class FileReader(Reader[str,List[str]]):
    
    def read(self, file: str) -> List[str]:
        data  = []
        with open(file,'r') as f:
            data= f.read()
        
        return data