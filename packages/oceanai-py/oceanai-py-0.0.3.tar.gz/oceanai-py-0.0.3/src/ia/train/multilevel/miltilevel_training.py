from src.search.space.space import Space
from src.ia.ia_model import IAModel
from src.math.functions.function import Function
from src.ia.train.training_goal import TrainingGoal
from src.ia.train.multilevel.multilevel_ia_model import MiltilevelIAModel
from src.ia.train.prospect import Prospect
from src.ia.train.dataset import Dataset
from src.ia.train.multilevel.dataparser import DataParcer
from typing import TypeVar, Generic,List


I = TypeVar('I')
O = TypeVar('O')
P = TypeVar('P')
D = TypeVar('D')
R = TypeVar('R')

class MiltilevelTraining(Generic[D,R,I,O,P],Function[Space[IAModel[I,O]],IAModel[D,R]]):

    def __init__(self,goal:TrainingGoal[D,R,P],parser:DataParcer[D,R,I,O],iters=30, name='MultilevelTraining'):
        super().__init__(name, goal.deterministic)
        self.goal=goal
        self.parser=parser
        self.iters=iters

    def apply(self, space:Space[IAModel[I,O]]) -> IAModel[D,R]:
        print('> running trainning')
        self.goal.init()
        models:List[Prospect[D,R,P]] = []
        for i in range(self.iters):
            print('> running iter '+str(i))
            print('> getting trainning set')
            dataset : Dataset[D,R] = self.goal.getTrainingSet()
            print('> training a new model')
            model : IAModel[D,R] = MiltilevelIAModel[D,R,I,O](self.train(space,Dataset[I,O](
                self.parser.parseInputs(dataset.inputs),self.parser.parseOutputs(dataset.outputs)
            )),self.parser)
            print('> evaluating model')
            performance:P = self.goal.apply(model)
            prospect: Prospect[D,R,P] = Prospect[D,R,P](i,model,performance,self.goal)
            print('> iter '+str(i)+' finished, a new model was trained, its performance is: '+str(performance))
            models.append(prospect)
        print('> results: ')
        for i in range(len(models)):
            print('> performance iter '+str(i + 1)+': '+ str(models[i].performance))
        return self.choose(models)

    def train(self,space:Space[IAModel[I,O]],dataset: Dataset[I,O])->IAModel[I,O]:
        pass

    def choose(self,prospects:List[Prospect[D,R,P]])->IAModel[D,R]:
        print('> choosing best model')
        best =prospects[0]
        for prospect in prospects:
            if prospect.compare(best) > 0:
                best = prospect
        print('> best model: iter '+str(best.iter))
        return best.model