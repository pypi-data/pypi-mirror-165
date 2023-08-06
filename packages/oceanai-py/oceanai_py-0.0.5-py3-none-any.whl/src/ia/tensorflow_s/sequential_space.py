from typing import List
import tensorflow as tf
from tensorflow import keras
from src.search.space.space import Space
from src.ia.tensorflow_s.sequential_model import SequentialModel


class SequentialSpace(Space[SequentialModel]):

    def __init__(self,layers) -> None:
        super().__init__()
        self.layers = layers
    
    def isFeasible(model: SequentialModel) -> bool:
        return True

    def feasibility(model: SequentialModel):
        return 1
    
    def restore(model:SequentialModel):
        return model

    def generate(self)->SequentialModel:
        return keras.Sequential(self.layers)