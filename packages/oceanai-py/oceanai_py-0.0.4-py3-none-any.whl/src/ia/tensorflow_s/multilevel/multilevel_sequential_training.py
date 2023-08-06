import tensorflow as tf
from src.ia.train.dataset import Dataset
from src.ia.train.multilevel.miltilevel_training import MiltilevelTraining
from src.ia.train.training_goal import TrainingGoal
from src.ia.tensorflow_s.multilevel.sequential_data_parser import SequentialDataParser
from src.ia.tensorflow_s.sequential_model import SequentialModel
from src.ia.tensorflow_s.sequential_space import SequentialSpace
from typing import TypeVar, Generic,List


I = TypeVar('I')
O = TypeVar('O')
P = TypeVar('P')

class MultilevelSequentialTraining(Generic[I,O,P],MiltilevelTraining[I,O,tf.Tensor or List,tf.Tensor or List,P]):
    
    def __init__(self, goal: TrainingGoal[I, O, P], parser: SequentialDataParser[I, O],compile, fit ,iters=30, name='MultilevelSequentialTraining'):
        super().__init__(goal, parser, iters, name)
        self.fit=fit
        self.compile=compile
    

    def train(self,space: SequentialSpace, dataset: Dataset[tf.Tensor or List,tf.Tensor or List]) -> SequentialModel:
        print('> generating model')
        model = space.generate()
        print('> compiling model')
        print(self.compile)
        model.compile(optimizer=self.compile['optimizer'],loss=self.compile['loss'],metrics=self.compile['metrics'])
        print('> fitting model')
        model.fit(x=dataset.inputs,y=dataset.outputs,epochs=self.fit['epochs'],batch_size=self.fit['batchSize'])
        return model