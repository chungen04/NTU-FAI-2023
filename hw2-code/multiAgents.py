# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        # food, ghost position
        score = successorGameState.getScore()
        eval_score = 0
        
        foods_dist = [manhattanDistance(newPos, x) for x in newFood.asList()]
        ghost_dist = [manhattanDistance(newPos, x.getPosition()) for x in newGhostStates]
        
        if(currentGameState.hasWall(*newPos)):
            eval_score -= 1.1
        
        if newPos in newFood.asList():
            eval_score += 3.1
            
        for ghost in newGhostStates:
            ghost_pos = ghost.getPosition()
            if(manhattanDistance(newPos, ghost_pos) <= 2):
                eval_score -= 15.2
                
        if len(foods_dist)!= 0:
            eval_score -= min(foods_dist)*0.15
        # print(eval_score)
        return score + eval_score
        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        actions = gameState.getLegalActions()
        successors = [gameState.generateSuccessor(0, action=action) for action in actions]
        
        max_value = -float('inf')
        max_choice = 0
        
        for x, successor in enumerate(successors):
            # first successor: ghost
            action_value = self.value(successor, 1, 0)
            if(action_value>max_value):
                max_choice = x
                max_value = action_value
            
        return actions[max_choice]
    
    def value(self, gameState, agent_idx, depth):
        #def value(state):
            # if the state is a terminal state: return the state’s utility
            # if the next agent is MAX: return max-value(state)
            # if the next agent is MIN: return min-value(state)
        
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(agent_idx == 0):
            return self.max_value(gameState, agent_idx, depth)        
        else:
            return self.min_value(gameState, agent_idx, depth)        
    
    def max_value(self, gameState, agent_idx, depth):
        # def max-value(state):
            # initialize v = -∞
            # for each successor of state:
                # v = max(v, value(successor))
            # return v 
        v = -float('inf')    
        
        actions = gameState.getLegalActions(agent_idx)
        successors = [gameState.generateSuccessor(agent_idx, action=action) for action in actions]
        
        for successor in successors:
            # successor is ghost
            v = max(v, self.value(successor, 1, depth))
        
        return v
    
    def min_value(self, gameState, agent_idx, depth): 
        # def min-value(state):
        #     initialize v = +∞
        #     for each successor of state:
        #          v = min(v, value(successor))
        #     return v
        
        v = float('inf')    
        
        actions = gameState.getLegalActions(agent_idx)
        successors = [gameState.generateSuccessor(agent_idx, action=action) for action in actions]
        
        for successor in successors:
            if(agent_idx + 1 != gameState.getNumAgents()):
                v = min(v, self.value(successor, agent_idx + 1, depth))
            else:
                # successor is pacman
                v = min(v, self.value(successor, 0, depth + 1))
        
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        actions = gameState.getLegalActions()
        successors = [gameState.generateSuccessor(0, action) for action in actions]
        
        max_value = float('-inf')
        max_choice = 0
        
        alpha = float('-inf')
        beta = float('inf') # passed to recursion
        
        for x, successor in enumerate(successors):
            # first successor: ghost
            action_value = self.value(successor, 1, 0, alpha, beta)
            if(action_value>max_value):
                max_choice = x
                max_value = action_value
                alpha = action_value # update alpha 
            
        return actions[max_choice] # cannot get back action correspond to successor...
        
    
    def value(self, gameState, agent_idx, depth, alpha, beta):
        # def value(state):
        #     if the state is a terminal state: return the state’s utility
        #     if the next agent is MAX: return max-value(state)
        #     if the next agent is MIN: return min-value(state)
        if(depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if(agent_idx == 0):
            return self.max_value(gameState, agent_idx, depth, alpha, beta)        
        else:
            return self.min_value(gameState, agent_idx, depth, alpha, beta)        
    
    def max_value(self, gameState, agent_idx, depth, alpha, beta):
        # def max-value(state, α, β):
        #     initialize v = -∞
        #     for each successor of state:
            #     v = max(v, value(successor, α, β))
            #     if v ≥ β return v
            #     α = max(α, v)
        #     return v
        
        v = float('-inf')  
        actions = gameState.getLegalActions(agent_idx)
        # successors should be generated one by one rather than all at once
        
        for action in actions:
            successor = gameState.generateSuccessor(agent_idx, action)
            # successor is ghost
            v = max(v, self.value(successor, 1, depth, alpha, beta))
            if(v > beta): # don't prune on equality
                return v
            alpha = max(alpha, v)
        return v
        

    def min_value(self, gameState, agent_idx, depth, alpha, beta):
        # def min-value(state , α, β):
        #     initialize v = +∞
        #     for each successor of state:
            #     v = min(v, value(successor, α, β))
            #     if v ≤ α return v
            #     β = min(β, v)
        #     return v
        
        v = float('inf')    
        actions = gameState.getLegalActions(agent_idx)
        
        for action in actions:
            successor = gameState.generateSuccessor(agent_idx, action)
            if(agent_idx + 1 != gameState.getNumAgents()):
                v = min(v, self.value(successor, agent_idx + 1, depth, alpha, beta))
            else:
                # successor is pacman
                v = min(v, self.value(successor, 0, depth + 1, alpha, beta))
            if(v < alpha): # don't prune on equality
                return v
            beta = min(beta, v)
        return v
        
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
