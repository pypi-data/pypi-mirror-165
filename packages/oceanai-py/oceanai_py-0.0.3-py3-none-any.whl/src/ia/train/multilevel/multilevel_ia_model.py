from src.ia.ia_model import IAModel
from src.ia.train.multilevel.dataparser import DataParcer
from typing import TypeVar, Generic,List


I = TypeVar('I')
O = TypeVar('O')
D = TypeVar('D')
R = TypeVar('R')

class MiltilevelIAModel(Generic[D,R,I,O],IAModel[D,R]):

    def __init__(self, model:IAModel[I,O],parser: DataParcer[D,R,I,O]) -> None:
        self.model = model
        self.parser = parser

    def apply(self,input: D)->R:
        return self.parser.restoreOutputs(self.model(self.parser.parseInputs(input)))

