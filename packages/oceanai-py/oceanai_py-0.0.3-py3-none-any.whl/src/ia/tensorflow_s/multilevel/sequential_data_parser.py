import tensorflow as tf
from src.ia.train.multilevel.dataparser import DataParcer
from typing import TypeVar, Generic,List


I = TypeVar('I')
O = TypeVar('O')

class SequentialDataParser(DataParcer[I,O,tf.Tensor or List,tf.Tensor or List],Generic[I,O]):


    def parseInputs(inputs: I) -> tf.Tensor or List:
        pass

    def parseOutputs(outputs: O) -> tf.Tensor or List:
        pass

    def restoreOutputs(outputs: tf.Tensor or List) -> O:
        pass

