from src.sort.order import Order
from src.ia.ia_model import IAModel
from src.ia.train.training_goal import TrainingGoal
from typing import TypeVar, Generic,List


I = TypeVar('I')
O = TypeVar('O')
P = TypeVar('P')

class Prospect(Generic[I,O,P]):

    def __init__(self,iter,model:IAModel[I,O],performance:P,goal: TrainingGoal[I,O,P]) -> None:
        self.iter = iter
        self.model = model
        self.performance = performance
        self.order = goal.getOrder()

    def compare(self,prospect):
        return self.order.compare(self.performance,prospect.performance)