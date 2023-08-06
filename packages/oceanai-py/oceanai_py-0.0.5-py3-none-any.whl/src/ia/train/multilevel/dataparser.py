from abc import ABC, abstractmethod
from typing import TypeVar, Generic


I = TypeVar('I')
O = TypeVar('O')
R = TypeVar('R')
D = TypeVar('D')

class DataParcer(ABC,Generic[D,R,I,O]):
    
    @abstractmethod
    def parseInputs(self,inputs:D)->I:
        pass

    @abstractmethod
    def parseOutputs(self,outputs:R)->O:
        pass

    @abstractmethod
    def restoreOutputs(self,outputs:O)->R:
        pass