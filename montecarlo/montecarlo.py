import numpy as np
import pandas as pd

class Die:
    '''
    A die has sides and weights, and can be rolled to select a face. Each side contains a unique 
    symbol. Symbols may be all alphabetic or all numeric. The weights are just numbers, not a 
    normalized probability distribution. The die has one behavior, which is to be rolled one 
    or more times.
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
        self.__diedf = self.__diedf.set_index('sides')
    
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
                
        self.__diedf['weights'][side] = float(weight)
    
    def roll(self, n=1):
        '''
        Rolls the die a given number of times.
        
        INPUTS:
        n - int number of times to roll die with replacement
        OUTPUTS:
        list of die outcomes
        '''
        return self.__diedf.sample(n, replace=True, weights=self.__diedf['weights']).index.to_list()
    
    def state(self):
        '''
        Returns the state of the private data frame. The returned value is a deep copy of the 
        data frame.
        
        OUTPUTS:
        copy of the private die data frame
        '''
        return self.__diedf.copy()
    

class Game:
    '''
    A game consists of rolling of one or more similar dice (Die objects) one or more times.
    Each game is initialized with a Python list that contains one or more dice. Game objects 
    have a behavior to play a game, i.e. to roll all of the dice a given number of times. 
    Game objects only keep the results of their most recent play.
    '''
    def __init__(self, dice):
        self.dice = dice
        self.__playdf = pd.DataFrame()
    
    def play(self, n):
        '''
        Takes an integer parameter to specify how many times the dice should be rolled and
        saves the result of the play to a private data frame.

        INPUTS:
        n - int number of times to roll dice
        '''
        roll_outcomes = {}
        for i in range(len(self.dice)):
            roll_outcomes[i] = self.dice[i].roll(n)
        self.__playdf = pd.DataFrame(roll_outcomes)
    
    def last_play(self, narrow=False):
        '''
        Returns a copy of the private play data frame to the user in narrow or wide form. 

        INPUTS:
        narrow - bool determines narrow or wide form for return data frame default=False
        OUTPUTS:
        copy of the private play data frame
        '''
        if not isinstance(narrow, bool):
            raise ValueError
        
        df = self.__playdf.copy()
        df['roll'] = df.index
        if(narrow):
            df = pd.melt(df, id_vars = ['roll'], 
                    value_vars = [i for i in range(len(df.columns)-1)])
            df = df.rename({'variable': 'dice', 'value':'outcome'}, axis=1)
            df = df.set_index(['roll', 'dice'])
            return df
        df = df.set_index('roll')
        c = {}
        for i in df.columns:
            c[i]= 'dice-'+str(i)
        df = df.rename(c, axis=1)
        return df

class Analyzer:
    '''
    An Analyzer takes the results of a single game and computes various descriptive 
    statistical properties about it.
    '''
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError
        self.game = game
    
    def face_counts(self):
        return
    
    def jackpot(self):
        df = self.game.last_play()
        count = 0
        for c in df.columns:
            if len(df[c].unique())==1:
                count+=1
        return count
    
    def combos(self):
        df = self.game.last_play()
        combo = pd.DataFrame(np.sort(df.values, axis=1)).groupby([i for i in range(len(df.columns))]).value_counts()
        return pd.DataFrame(combo)
    
    def permutations(self):
        return pd.DataFrame(self.game.last_play().value_counts())