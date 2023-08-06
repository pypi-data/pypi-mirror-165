from abc import ABC, abstractmethod
from typing import TypeVar, Generic


I = TypeVar('I')
O = TypeVar('O')

class IAModel(ABC,Generic[I,O]):

    @abstractmethod
    def apply(self,input:I)->O:
        pass
