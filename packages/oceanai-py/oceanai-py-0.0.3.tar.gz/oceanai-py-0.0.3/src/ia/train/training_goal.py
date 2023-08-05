from src.search.goal import Goal
from src.sort.order import Order
from src.ia.ia_model import IAModel
from src.ia.train.dataset import Dataset
from typing import TypeVar, Generic


I = TypeVar('I')
O = TypeVar('O')
P = TypeVar('P')

class TrainingGoal(Generic[I,O,P],Goal[IAModel[I,O],P]):

    def __init__(self, name, dataset : Dataset[I,O], order: Order[P])-> None:
        super().__init__(name, order)
        self.dataset = dataset

    def getTrainingSet(self)->Dataset[I,O]:
        pass

    def apply(self,model: IAModel[I,O])->P:
        predictions = model.apply(self.dataset.inputs)
        return self.evaluate(self.dataset.outputs,predictions)
        
    def evaluate(self,outputs:O,predictions:O)->P:
        pass