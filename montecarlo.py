import numpy as np
import pandas as pd

class Die:
    '''
    A die has sides and weights, and can be rolled to select a face. Each side contains a unique symbol. 
    Symbols may be all alphabetic or all numeric. The weights are just numbers, not a normalized probability 
    distribution. The die has one behavior, which is to be rolled one or more times.
    '''
    def __init__(self, sides):
        '''
        Initializes the Die Class.
        
        INPUTS:
        sides - np.array of unique alphabetic or numeric sides
        '''
        if not isinstance(sides, np.ndarray):
            raise TypeError
        
        if not len(np.unique(sides))==len(sides):
            raise ValueError
        
        self.sides = sides
        self.__diedf = pd.DataFrame({'sides':sides, 'weights':[1]*len(sides)})
    
    def change_weight(self, side, weight):
        '''
        Changes the weight of a given die side.
        
        INPUTS:
        side - int, float, or str side that must be in self.sides
        weight - numerical weight value to place in private data frame
        '''
        if not np.isin(side, self.sides):
            raise IndexError
        if not (isinstance(weight, float) or isinstance(weight, int)):
            if isinstance(weight, str):
                if not weight.isnumeric():
                    raise TypeError
                
        index = self.__diedf.index[self.__diedf['sides']==side].to_list()[0]
        self.__diedf['weights'][index] = float(weight)
    
    def roll(self, n=1):
        '''
        Rolls the die a given number of times.
        
        INPUTS:
        n - int number of times to roll die with replacement
        OUTPUTS:
        list of die outcomes
        '''
        return self.__diedf.sample(n, replace=True, weights=self.__diedf['weights'])['sides'].to_list()
    
    def state(self):
        '''
        Returns the state of the private data frame. The returned value is a deep copy of the data frame.
        
        OUTPUTS:
        private data frame
        '''
        return self.__diedf.copy()
    
    
class Game:
    
    def __init__(self, dice):
        