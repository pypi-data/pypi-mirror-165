from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Order(ABC,Generic[T]):

    @abstractmethod
    def compare(self, one:T, two:T):
        pass

    @abstractmethod
    def equals(self, one:T, two:T):
        pass