from abc import ABC, abstractmethod
from typing import TypeVar, Generic


A = TypeVar('A')
O = TypeVar('O')

class Reader(ABC,Generic[A,O]):

    @abstractmethod
    def read(self,args:A)->O:
        pass