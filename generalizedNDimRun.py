# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:11:31 2020

@author: r2d2go

"""
import math
import numpy as np

import random as random


class Rat(object):
    def __init__(self, decks, changerate, players, dim, initialDist):
        """
        Initialize the chain instance.
        
        We have (players) number of players, each with one of (decks) decks. 
        We then consider the expected outcome when (dim) of them interact.
        
        Initialize: Randomly generate possible player ratios and the current ratio based on initialDist.
        
        Parameters
        ----------
 
        decks: int
            number of decks
        
        changerate: dictionary
            Dictionary of change rates, indexed by coordinates on the tensor, seperated by dashes (e.g. "0-3" in a 4x4 matrix is the upper right corner).
            The last index indicates what the resulting change rate adds to.
        
        players: int
            Number of players
            
        dim: int 
            dimension of tensor
            
        initialDist: list
            List of probabilities of being in a given deck.
            
        playerCount: list
            List of the number of players with a given deck (indexed as decks)
            
        """
        self.decks = decks
        self.changerate = changerate
        self.players = players
        self.initialDist = initialDist.copy()
        self.playerCount = []
        self.bumps = 0
        self.dim = dim
        for deckI in range(decks):
            self.playerCount.append(0)
        for playerI in range(players):
            deckRand = random.uniform(0,1)
            deckI = 0
            distI = 0
            while distI < decks:
                deckI += initialDist[distI]
                if deckRand < deckI:
                    self.playerCount[distI] += 1
                    distI = decks+1
                distI += 1
        
    def advance(self, playerrat):
        """
        playerrat: float
            proportion of players being advanced
        """
        self.playerrat = playerrat
        gamecount = math.floor(self.playerrat*self.players)
        tempCount = self.playerCount.copy()
        
        for gameI in range(gamecount):
            listOfDecks = []
            for i in range(self.dim):
                listOfDecks.append(0)
            for i in range(self.dim):
                deck = 0
                rand = random.randint(1,self.players)   
                while deck < self.decks:
                    rand -= self.playerCount[deck]
                    if rand <= 0:
                        listOfDecks[i] = deck
                        deck = 1000000000000
                    deck += 1
            deckKey = ""
            for i in listOfDecks:
                deckKey += str(i)+"-"
            deckAdd = 0
            rollI = 0
            gameRoll = random.uniform(0,1)
            for i in listOfDecks:
                rollI += self.changerate[deckKey+str(i)]
                if gameRoll < rollI:
                    tempCount[i] -= 1
                    tempCount[deckAdd] += 1
                deckAdd += 1
            
        self.playerCount = tempCount
            
    def generate_states(self, runLength, playerrat):
        """
        Generates states for a run of length runLength.
 
        Parameters
        ----------
 
        runLength: int
            The number of future states to generate.
        """
        self.runLength = runLength
        self.playerrat = playerrat
        runList = []
        for i in range(runLength):
            runList.append(self.playerCount.copy())
            self.advance(playerrat)
        return runList
            
    def average(self, initialDist, runLength, runs, playerrat):
        """
        Generates a number of runs and finds the average ratio of players over time.
        
        Parameters
        ----------
 
        runs: int
            The number of runs to generate.
        
        """
        self.runs = runs
        self.runLength = runLength
        self.playerrat = playerrat
      
        longAverage = []
        blankState = []
        for deck in range (self.decks):
            blankState.append(0)
        for run in range(runLength):
            longAverage.append(blankState.copy())
        for run in range(runs):
            self.playerCount = []
            for deckI in range(self.decks):
                self.playerCount.append(0)
            for playerI in range(self.players):
                deckRand = random.uniform(0,1)
                deckI = 0
                distI = 0
                while distI < self.decks:
                    deckI += initialDist[distI]
                    if deckRand < deckI:
                        self.playerCount[distI] += 1
                        distI = self.decks+1
                    distI += 1
            runList = self.generate_states(runLength, playerrat)
            for state in range(runLength):
                for deckRat in range(self.decks):
                    longAverage[state][deckRat] += runList[state][deckRat]
        for deck in range(self.decks):
            for state in range(runLength):
                longAverage[state][deck] = longAverage[state][deck]/runs/self.players
        return(longAverage)
 