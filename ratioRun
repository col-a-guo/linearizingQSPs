# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:23:03 2020

@author: Collin Guo
"""

import math

import random as random


class Rat(object):
    def __init__(self, decks, winrates, loserates, counterrates, players, initialDist):
        """
        Initialize the chain instance.
        
        Players each have a randomly generated deck. Iterating the chain makes a random pair of players face each other.
        
        The losing player has a chance to change (typically high% for related decks, counters to winning deck, and the winning deck)
        
        As number of players approaches infinity, approaches equivalent to continuous "powers" of a 3-dimensional tensor (see https://www.overleaf.com/read/xhrfpsswwgpm for tensor conversions)
        
        We'll have two matrices - one for the movement chance of the losing player, based on their own deck, and one based
        on the winner's. It is assumed these are unrelated.
            
        Initialize: Randomly generate possible player ratios and the current ratio based on initialDist.
        
        Parameters
        ----------
        players: int
            Number of players
 
        decks: int
            number of decks
        
        winrates: list of lists
            n x n matrix of ints 0 to 1 giving winrate (first index chance to win vs second index).
            
        loserates: list of lists
            n x n matrix of ints 0 to 1: if you lose while playing x deck, you will switch to y deck at this rate.
            
        counterrates: list of lists
            n x n matrix of ints 0 to 1: if you lose while playing against x deck, you will switch to y deck at this rate.
        
        initialDist: list
            List of probabilities of being in a given deck.
            
        playerCount: list
            List of the number of players with a given deck (indexed as decks)
            
        """
        self.decks = decks
        self.winrates = winrates
        self.loserates = loserates
        self.counterrates = counterrates
        self.players = players
        self.initialDist = initialDist.copy()
        self.playerCount = []
        self.bumps = 0
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
            rand = random.randint(1,self.players)
            deck1 = 0
            deck2 = 0
            deck = 0
            while deck < self.decks:
                rand -= self.playerCount[deck]
                if rand <= 0:
                    deck1 = deck
                    deck = 1000000000000
                deck += 1
            deck = 0
            rand = random.randint(1,self.players)
            while deck < self.decks:
                rand -= self.playerCount[deck]
                if rand <= 0:
                    deck2 = deck
                    deck = 1000000000000
                deck += 1
            gameRoll = random.uniform(0,1)
            if gameRoll < self.winrates[deck1][deck2]:
                winDeck = deck1
                loseDeck = deck2
            else:
                winDeck = deck2
                loseDeck = deck1
            loserateRoll = random.uniform(0,1)
            counterrateRoll = random.uniform(0,1)
            loseI = 0
            rollI = 0
            counterI = 0
            flag = 0
            while rollI < self.decks:
                counterI += self.counterrates[winDeck][rollI]
                if counterrateRoll < counterI:
                    if tempCount[loseDeck] > 0:
                        tempCount[loseDeck] -= 1
                        tempCount[rollI] += 1
                    else:
                        self.bumps += 1
                    rollI = self.decks+1
                    flag = 1
                rollI += 1
            rollI = 0
            while rollI < self.decks:
                loseI += self.loserates[loseDeck][rollI]
                if loserateRoll < loseI:        
                    if flag == 0:
                        if tempCount[loseDeck] > 0:
                            tempCount[loseDeck] -= 1
                            tempCount[winDeck] += 1
                        else:
                            self.bumps += 1
                    rollI = self.decks+1
                rollI += 1
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
 
