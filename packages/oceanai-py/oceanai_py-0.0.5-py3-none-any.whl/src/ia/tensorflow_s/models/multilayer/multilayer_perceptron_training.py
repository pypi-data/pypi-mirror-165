from typing import List
import tensorflow as tf
from src.ia.ia_model import IAModel
from src.ia.train.training_goal import TrainingGoal
from src.ia.tensorflow_s.multilevel.multilevel_sequential_training import MultilevelSequentialTraining
from src.ia.tensorflow_s.models.multilayer.multilayer_dataset_parser import MultilayerDataParser
from src.ia.tensorflow_s.models.multilayer.multilayer_perceptron_space import MultilayerPerceptronArgs
from src.ia.tensorflow_s.models.multilayer.multilayer_perceptron_space import MultilayerPerceptronSpace

class MultilayerPerceptronTraining(MultilevelSequentialTraining[List[List[int]],List[List[int]],List[int]]):
    
    def __init__(self,args:MultilayerPerceptronArgs, goal: TrainingGoal[List[List[int]], List[List[int]], List[int]], compile, fit, iters=30, name='MultilevelPerceptronTraining'):
        super().__init__(goal, MultilayerDataParser(args.outputs), compile, fit, iters, name)
        self.space = MultilayerPerceptronSpace(args)
        
    def apply(self):
        return super().apply(self.space)