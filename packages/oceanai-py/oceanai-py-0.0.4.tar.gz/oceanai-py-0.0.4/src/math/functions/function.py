from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar('T')
S = TypeVar('S')

class Function(ABC,Generic[S,T]):

    def __init__(self,name,deterministic=True):
        self.name=name
        self.deterministic = deterministic
    
    @abstractmethod
    def apply(self,x:S)->T:
        pass