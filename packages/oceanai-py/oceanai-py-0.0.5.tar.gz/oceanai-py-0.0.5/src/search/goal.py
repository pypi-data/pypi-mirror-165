from src.math.functions.function import Function
from src.sort.order import Order
from typing import TypeVar, Generic

T = TypeVar('T')
P = TypeVar('P')

class Goal(Function[T,P],Generic[T,P]):

    def __init__(self,name,order:Order[P]) -> None:
        super().__init__(name)
        self.order = order

    def getOrder(self)->Order[P]:
        return self.order

    def compare(self,x:T,y:T):
        return self.order.compare(self.apply(x),self.apply(y))
    
    def init():
        pass