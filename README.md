Author: Hana Nur

Project Name: Monte Carlo Simulator

# Monte Carlo Simulator
A simple Monte Carlo simulator using a set of three related classes — a Die class, a Game class, 
and an Analyzer class.

The classes are related in the following way: Game objects are initialized with a Die object, and 
Analyzer objects are initialized with a Game object. In this simulator, a “die” can be any discrete 
random variable associated with a stochastic process, such as using a deck of card, flipping a coin, 
rolling an actual die, or speaking a language.

# Synopsis

Install the module using the command ```pip install montecarlo``` and begin by importing the necessary
Die, Game, and Analyzer classes. The Die class requires a numpy array to instantiate a Die object 
some methods output pandas DataFrames, so we will also import these modules.
```
import numpy as np
import pandas as pd
from montecarlo.montecarlo import Die, Game, Analyzer
```

Next, create a Die object to pass into a Game object. In this example, we create a 6-sided Die with sides
1-6. Side values must be alphanumeric.
```
sides = np.array([1,2,3,4,5,6])
die = Die(sides)
```
We can use the die to create a Game of n dice. In this example, we create a game of with 3 dice and 
roll the dice 10 times.
```
game = Game([die, die, die])
game.play(10)
print(game.last_play())

Outputs:
      dice-0  dice-1  dice-2
roll                        
0          4       5       2
1          2       1       2
2          1       2       4
3          3       1       1
4          2       5       1
5          1       3       2
6          3       1       4
7          5       3       1
8          3       4       1
9          3       6       6
```
Then, after playing a game, we can pass this game object to an Analyzer to analyze the outcomes. Here we
analyze how many jackpots occur in the outcomes.
```
a = Analyzer(game)
print(a.jackpot())

Outputs:
0
```
Unlucky! Zero jackpots are hit, better luck next time.

# API

## Die Class

A die has sides and weights, and can be rolled to select a face. Each side contains a unique 
symbol. Symbols may be all alphabetic or all numeric. The weights are just numbers, not a 
normalized probability distribution. The die has one behavior, which is to be rolled one 
or more times.

### **Die(sides)**
Instantiates a Die object.

**INPUTS:**
* sides - np.array of unique alphabetic or numeric sides

### **Die.change_weight(side, weight)**
Changes the weight of a given die side.

**INPUTS:**
* side - int, float, or str side that must be in self.sides
* weight - numerical weight value to place in private data frame

### **Die.roll(n=1)**
Rolls the die a given number of times.

**INPUTS:**
* n - (default 1) int number of times to roll die with replacement
**OUTPUTS:**
* list of die outcomes

### **Die.state()**
Returns the state of the private data frame. The returned value is a deep copy of the 
data frame.

**OUTPUTS:**
* copy of the private die data frame

## Game Class

A game consists of rolling of one or more similar dice (Die objects) one or more times.
Each game is initialized with a Python list that contains one or more dice. Game objects 
have a behavior to play a game, i.e. to roll all of the dice a given number of times. 
Game objects only keep the results of their most recent play.

### **Game(dice)**
Instantiates a Game object.

**INPUTS:**
* dice - list of die objects
    
### **Game.last_play(narrow=False)**
Returns a copy of the private play data frame to the user in narrow or wide form. 

**INPUTS:**
* narrow - (default False) bool determines narrow or wide form for return data frame default=False
**OUTPUTS:**
* copy of the private play data frame

### **Game.play(n)**
Takes an integer parameter to specify how many times the dice should be rolled and
saves the result of the play to a private data frame.

**INPUTS:**
* n - int number of times to roll dice

## Analyzer Class
 
An Analyzer takes the results of a single game and computes various descriptive 
statistical properties about it.
    
### **Analyzer(game)**
Instantiates an Analyzer object.
        
**INPUTS:**
* game - a game object to analyze

### **Analyzer.combos()**
Computes the distinct combinations of faces rolled, along with their 
counts. Combinations are order-independent and may contain repetitions.

**OUTPUTS:**
* data frame with MultiIndex of distinct combinations and a column for the associated counts

### **Analyzer.face_counts()**
Computes how many times a given face is rolled in each event and returns
a data frame of results.

**OUTPUTS:**
* data frame an index of the roll number, face values as columns, and count values in the cells (wide format)

### **Analyzer.jackpot()**
Computes how many times the game resulted in a jackpot rolls. Jackpot
rolls are outcomes in which all faces are the same for all dice.
 
**OUTPUTS:**
* int count of jackpot occurances

### **Analyzer.permutations()**
Computes the distinct permutations of faces rolled, along with their 
counts.
 
**OUTPUTS:**
* data frame with MultiIndex of distinct permutations and a column for the associated counts.