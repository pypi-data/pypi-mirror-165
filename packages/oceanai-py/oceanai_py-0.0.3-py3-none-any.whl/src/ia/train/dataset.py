from typing import TypeVar, Generic


I = TypeVar('I')
O = TypeVar('O')

class Dataset(Generic[I,O]):
    
    def __init__(self,inputs:I,outputs:O) -> None:
        self.inputs=inputs
        self.outputs = outputs
