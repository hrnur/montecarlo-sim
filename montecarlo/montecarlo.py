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
        Instantiates a Die object.
        
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
        '''
        Instantiates a Game object.

        INPUTS:
        dice - list of die objects
        '''
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
        '''
        Instantiates an Analyzer object.

        INPUTS:
        game - a game object
        '''
        if not isinstance(game, Game):
            raise ValueError
        self.game = game
    
    def jackpot(self):
        '''
        Computes how many times the game resulted in a jackpot rolls. Jackpot
        rolls are outcomes in which all faces are the same for all dice.

        OUTPUTS:
        int count of jackpot occurances
        '''
        df = self.game.last_play()
        count = 0
        for i in df.index:
            if len(df.iloc[i].unique())==1:
                count+=1
        return count

    def face_counts(self):
        '''
        Computes how many times a given face is rolled in each event and returns
        a data frame of results.

        OUTPUTS:
        data frame an index of the roll number, face values as columns, and 
        count values in the cells (wide format)
        '''
        sides = list(self.game.dice[0].sides)
        df = self.game.last_play(False)
        fc = {k:[] for k in sides}
        
        for i in range(len(df)):
            unique, counts = np.unique(df.iloc[i], return_counts=True)
            for j in range(len(sides)):
                if sides[j] in list(unique):
                    index = list(unique).index(sides[j])
                    fc[sides[j]].append(counts[index])
                else:
                    fc[sides[j]].append(0)
        return pd.DataFrame(fc)
    
    def combos(self):
        '''
        Computes the distinct combinations of faces rolled, along with their 
        counts. Combinations are order-independent and may contain repetitions.

        OUTPUTS:
        data frame with MultiIndex of distinct combinations and a column for 
        the associated counts
        '''
        df = self.game.last_play()
        combo = pd.DataFrame(np.sort(df.values, axis=1)).groupby([i for i in range(len(df.columns))]).value_counts()
        return pd.DataFrame(combo)
    
    def permutations(self):
        '''
        Computes the distinct permutations of faces rolled, along with their 
        counts.

        OUTPUTS:
        data frame with MultiIndex of distinct permutations and a column for 
        the associated counts.
        '''
        return pd.DataFrame(self.game.last_play().value_counts())
