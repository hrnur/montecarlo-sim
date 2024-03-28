import unittest
import numpy as np
import pandas as pd
from montecarlo_sim import Die, Game, Analyzer

class MontecarloTestSuite(unittest.TestCase):
    
    def test_die_init(self):
        message = 'Error: die not instantiated'
        d = Die(np.array([1,2,3]))
        return self.assertTrue(isinstance(d, Die), message)
    
    def test_die_change_weight(self):
        message = 'Error: weight does not match expected'
        d = Die(np.array([1,2,3]))
        d.change_weight(1,100)
        return self.assertEqual(d.state().loc[1].item(), 100, message)
    
    def test_die_roll(self): 
        message = 'Error: does not return list'
        d = Die(np.array([1,2,3]))
        return self.assertTrue(isinstance(d.roll(), list), message)
    
    def test_die_state(self):
        message = 'Error: does not return data frame'
        d = Die(np.array([1,2,3]))
        return self.assertTrue(isinstance(d.state(), pd.DataFrame), message)
    
    def test_game_init(self):
        message = 'Error: game not instantiated'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        g = Game([d1, d2])
        return self.assertTrue(isinstance(g, Game), message)
    
    def test_game_play(self):
        message = 'Error: number of rolls does not match expected'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        g = Game([d1, d2])
        g.play(3)
        return self.assertTrue(len(g.last_play())==3, message)
    
    def test_game_last_play(self):
        message = 'Error: does not return data frame'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        g = Game([d1, d2])
        g.play(3)
        return self.assertTrue(isinstance(g.last_play(), pd.DataFrame), message)
    
    def test_analyzer_init(self):
        message = 'Error: analyzer not instantiated'
        d1 = Die(np.array([1,2]))
        g = Game([d1, d1])
        a = Analyzer(g)
        return self.assertTrue(isinstance(a, Analyzer), message)
    
    def test_analyzer_jackpot(self):
        message = 'Error: jackpot count does not match expected'
        d1 = Die(np.array([1,2]))
        d2 = Die(np.array([1,2]))
        d1.change_weight(1,100000)
        d2.change_weight(1,100000)
        g = Game([d1, d2])
        g.play(1)
        a = Analyzer(g)
        return self.assertTrue(a.jackpot()==1, message)
    
    def test_analyzer_face_counts(self):
        message = 'Error: does not return data frame'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        d1.change_weight(1,10000)
        g = Game([d1, d2])
        g.play(3)
        a = Analyzer(g)
        return self.assertTrue(isinstance(a.face_counts(), pd.DataFrame), message)
    
    def test_analyzer_combos(self):
        message = 'Error: does not return data frame'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        g = Game([d1, d2])
        g.play(3)
        a = Analyzer(g)
        return self.assertTrue(isinstance(a.combos(), pd.DataFrame), message)
    
    def test_analyzer_permutations(self):
        message = 'Error: does not return data frame'
        d1 = Die(np.array([1,2,3]))
        d2 = Die(np.array([1,2,3]))
        g = Game([d1, d2])
        g.play(3)
        a = Analyzer(g)
        return self.assertTrue(isinstance(a.permutations(), pd.DataFrame), message)

    
if __name__ == '__main__':
    
    unittest.main(verbosity=3)