from typing import List
import tensorflow as tf
from src.ia.tensorflow_s.multilevel.sequential_data_parser import SequentialDataParser
import numpy as np

class MultilayerDataParser(SequentialDataParser[List[List],List[List]]):

    def __init__(self,outputSize) -> None:
        super().__init__()
        self.outputSize = outputSize

    def parseInputs(self,inputs: List[List]) -> tf.Tensor or List:
        return tf.constant(inputs)
    
    def parseOutputs(self,outputs: List[List]) -> tf.Tensor or List:
        return tf.constant(outputs)

    def restoreOutputs(self,outputs: tf.Tensor or List) -> List[List]:
        predictions= outputs.numpy()
        """ results = [[]]
        index = 0
        for value in predictions:
            if index % self.outputSize == 0:
                results.append([])
            row = floor(index/self.outputSize)
            results[row].append(value)
            index =+ 1 """
        return predictions