from abc import ABC, abstractmethod
from typing import TypeVar, Generic



A = TypeVar('A')
O = TypeVar('O')

class Writer(ABC,Generic[A,O]):

    @abstractmethod
    def write(self,args:A)->O:
        pass