from typing import List, TypeVar, Generic

T = TypeVar('T')

class Space(Generic[T]):

    def isFeasible(x:T)->bool:
        pass

    def Feasibility(x:T):
        pass

    def restore(x:T)->T:
        pass

    def generate()->T:
        pass

    def pick(self,total)->T:
        result:T = []
        for i in range(total):
            result.append(self.generate())
        return result

    def repair(self,pop:List)->T:
        result = []
        for item in pop:
            result.append(self,self.restore(item))
        return result
