import tensorflow as tf
from typing import List

from src.ia.ia_model import IAModel

class SequentialModel(IAModel[List or tf.Tensor, List or tf.Tensor]):

    def __init__(self,model:tf.keras.Model) -> None:
        super().__init__()
        self.model = model

    def apply(self)->tf.Tensor or List:
        return self.model.predict()
    
    def getTensorFlowModel(self)->tf.keras.Model:
        return self.model