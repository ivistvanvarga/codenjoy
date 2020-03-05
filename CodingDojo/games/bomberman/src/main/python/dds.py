#!/usr/bin/env python3

###
# #%L
# Codenjoy - it's a dojo-like platform from developers to developers.
# %%
# Copyright (C) 2018 Codenjoy
# %%
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/gpl-3.0.html>.
# #L%
###

from time import time
from random import choice
from board import Board
from element import Element
from direction import Direction
from point import Point
#from com.codenjoy.dojo import bomberman
#import src.main.python.direction as direct
import sys


  
class StepProposal:
    steps = []
    def __init__(self,state, deep):
        self._state = state
        self._deep = deep
        self._step = state.getOperator()
        self._utilityscore=-1*sys.maxsize
        self._evaluated = 1
    
    def get_step(self):
        return self._step
    
    def get_utilityscore(self):
        return self._utilityscore
    
    @classmethod
    def getPath(cls,node):
        if node._parrent is None:
            if node.getOperator() is not None: 
                return [node.getOperator()] 
            else:
                return  []
        else:
           return [node.getOperator()]+TreeSerch.getPath(node._parrent)

class MinMax(StepProposal):
    def __init__(self, state, deep):
        super().__init__(state, deep)
        if self._deep <= 0:
            self._utilityscore = self._state.getMinMaxUtilityScore()
        elif self._state.isFinalState():
            self._step = self._state.getOperator()
            self._utilityscore=self._state.getMinMaxUtilityScore()
            print("fin")
        else:
            for op in self._state.getOperators():
                if self._state.isApplicable(op):
                    print("deep"+str(deep)+op.to_string()+":"+str(self._state.isApplicable(op)))
                    newMinMax = MinMax(self._state.apply(op),self._deep-1)
                    if newMinMax._utilityscore > self._utilityscore:
                        self._utilityscore = newMinMax._utilityscore
                        self._step = newMinMax.get_step()
                    self._evaluated += newMinMax._evaluated
    
class TreeSerch(StepProposal):
    
    def __init__(self, state, deep=2,findAll=False):
        super().__init__(state, deep)
        self._closed = []
        self._terminal = []
        self._queue =[state]
        self._findAll=findAll
    
    def serch(self):
        
        while len(self._queue)>0:
            akt = self._queue.pop(0)
            if akt is None:
                break
            elif akt.isFinalState() and akt not in self._terminal:
                self._terminal.append(akt)
                self._step = akt.getOperator()
                if not self._findAll:
                    break
            elif akt._deep >= self._deep:
                
                break
            for op in akt.getOperators():
                new = akt.apply(op)
                if(new not in self._queue and new not in self._closed and new not in self._terminal):
                    self._queue.append(new)   
            self._closed.append(akt)
        return self._terminal
            
    def get_best(self):
        
        bestone = self._state
        for i in self.serch():
            if i != bestone and i.getMinMaxUtilityScore() >= bestone.getMinMaxUtilityScore():
                bestone = i
        return bestone
                 
            

class BombermanBoard(Board):
    operators=[Direction('RIGHT'),
    Direction('LEFT'),
    Direction('UP'),
    Direction('DOWN'),
    Direction('ACT'),
    Direction("NULL")]
    
    def __init__(self,board_string,parrent=None,operator=None,deep=0):
        super().__init__(board_string)
        bomberman=self.get_bomberman()
        self._operators=[]
        self._parrent = parrent
        self._operator = operator
        self._deep = deep
        self._operators = []
        
        if operator is None or operator in [ Direction('NULL'),Direction('STOP')]:
            self._bomberman = bomberman
        elif  operator in [ Direction('ACT')]:
            self._bomberman = bomberman
            string_remove = self._string.replace(self.get_at(bomberman.get_x(),bomberman.get_y()).get_char(), Element('NONE').get_char())
            x, y = self._bomberman.get_x(),self._bomberman.get_y()
            super().__init__(u''.join([string_remove[:self._xy2strpos(x,y)],
                        Element('BOMB_BOMBERMAN').get_char(),
                        string_remove[self._xy2strpos(x,y)+1:]]))
        else:
            self._bomberman = Point(operator.change_x(bomberman.get_x()),operator.change_y(bomberman.get_y()))
            if self.is_at(bomberman.get_x(),bomberman.get_y(),Element('BOMB_BOMBERMAN')):
                string_remove = self._string.replace(self.get_at(bomberman.get_x(),bomberman.get_y()).get_char(), Element('BOOM').get_char())
            else:  
                string_remove = self._string.replace(self.get_at(bomberman.get_x(),bomberman.get_y()).get_char(), Element('NONE').get_char())
            x, y = self._bomberman.get_x(),self._bomberman.get_y()
            
            super().__init__(u''.join([string_remove[:self._xy2strpos(x,y)],
                        Element('BOMBERMAN').get_char(),
                        string_remove[self._xy2strpos(x,y)+1:]]))
            for op in BombermanBoard.operators:
                if op not in self._operators and op != self._operator.inverted() and self.isApplicable(op):
                    self._operators.append(op) 
            
            #self._string[self._size * self._bomberman.get_y() + self._bomberman.get_x()] = Element('BOMBERMAN').get_char()

    def isApplicable(self, operator):
        if (operator == Direction('ACT') and 
            (self.is_near(self._bomberman.get_x(),self._bomberman.get_y(),Element("OTHER_BOMBERMAN"))
             or
             self.is_near(self._bomberman.get_x(),self._bomberman.get_y(),Element("DESTROY_WALL"))
             or self.is_near(self._bomberman.get_x(),self._bomberman.get_y(),Element("MEAT_CHOPPER"))
            )
            ):
            return True
        elif operator in [ Direction('NULL')] and self.is_my_bomberman_dead():
            return True
        elif  operator == Direction('STOP')  and self.get_at(self._bomberman.get_x(),self._bomberman.get_y()) != Element('BOMB_BOMBERMAN'):
            return True

        elif self.get_at(operator.change_x(self._bomberman.get_x()),operator.change_y(self._bomberman.get_y())) == Element('NONE'):
            return True
        return False
    
    def getMinMaxUtilityScore(self):
        score = 0    
        if self._bomberman in self.get_bombs()and self._parrent is None:
            score-= 500
        try:
            if len(self.get_future_blasts())>1 and self._bomberman in self.get_future_blasts()and self._parrent is None:
               return -5000
        except TypeError:
            pass
        finally:
            pass
        if self._bomberman in self.get_meat_choppers():
            score-= 100
        if self._operator == Direction('ACT'):
            surrounding = [
                Point(Direction('LEFT').change_x(self._bomberman.get_x()),Direction('LEFT').change_y(self._bomberman.get_y())),
                Point(Direction('RIGHT').change_x(self._bomberman.get_x()),Direction('RIGHT').change_y(self._bomberman.get_y())),
                Point(Direction('UP').change_x(self._bomberman.get_x()),Direction('UP').change_y(self._bomberman.get_y())),
                Point(Direction('DOWN').change_x(self._bomberman.get_x()),Direction('DOWN').change_y(self._bomberman.get_y())),
            ]
            for i in surrounding:
                if i in self.get_destroy_walls():
                    score+=100
                if i in self.get_meat_choppers():
                    score+=200
                if i in self.get_other_bombermans():
                    score+=1000
                if i in self.get_bombs():
                    return -5000
        if self._parrent is not None:
            score += self._parrent.getMinMaxUtilityScore()
        return score
    
    def isFinalState(self):
        if self.is_my_bomberman_dead():
            return True
        elif (self._bomberman not in self.get_future_blasts() and self._bomberman not in self.get_meat_choppers() and 
              self._parrent is not None and self._parrent._string != self._string
              ):
            return True
        return False
    
    def apply(self, operator):
        return BombermanBoard(board_string=self._string,parrent=self,operator=operator,deep=self._deep+1)
    
    def getOperator(self):
        return self._operator
    
    def getOperators(self):
        return [op for op in (BombermanBoard.operators) if self.isApplicable(op)]   
    
    def __eq__(self, otherElement):
        return super().__eq__(otherElement) and  self._bomberman == otherElement._bomberman
    

class DirectionSolver:
    """ This class should contain the movement generation algorythm."""

    def __init__(self):
        self._direction = None
        self._board = None
        self._last = None
        self._count = 0

    def get(self, board_string):
        """ The function that should be implemented."""
        self._board = BombermanBoard(board_string=board_string)
        
        _command = self.find_direction2()
        print("Sending Command {}".format(_command))

        return _command
    
    def find_direction2(self):
        suggestion = Direction('NULL').to_string()
        if self._board.is_my_bomberman_dead():
            return suggestion
        suggestion = TreeSerch.getPath(TreeSerch(state=self._board,findAll=True,deep=5).get_best())
        #if suggestion[0] == Direction('ACT'):
        #    return ','.join([s.__str__() for s in (suggestion[:2])])
        
        
        return ','.join([s.__str__() for s in (suggestion[:2])])

    def find_direction(self):
        """ This is an example of direction solver subroutine."""
        _direction = Direction('NULL').to_string()
        if self._board.is_my_bomberman_dead():
            print("Bomberman is dead. Sending 'NULL' command...")
            return _direction
        # here's how we find the current Point of our bomberman
        _bm = self._board.get_bomberman()
        _bm_x, _bm_y = _bm.get_x(), _bm.get_y()
        # Let's check whether our bomberman is not surrounded by walls
        if 4 == self._board.count_near(_bm_x, _bm_y, Element('DESTROY_WALL')):
            print("It seems like walls surround you. Self-destroying.")
            return Direction('ACT').to_string()  # Let's drop a bomb then
        # print(self._board.to_string())
        print("Found your Bomberman at {}".format(_bm))
        # here's how we get the list of barriers Points
        _barriers = self._board.get_barriers()
        _deadline = time() + 30
        while time() < _deadline:
            # here we get the random direction choise
            __dir = Direction(choice(('LEFT', 'RIGHT', 'DOWN', 'UP')))
            # now we calculate the coordinates of potential point to go
            _x, _y = __dir.change_x(_bm.get_x()), __dir.change_y(_bm.get_y())
            # if there's no barrier at random point
            if not self._board.is_barrier_at(_x, _y):
                # here we count the attempt to choose the way
                self._count += 1
                # and check whether it's not the one we just came from
                if not self._last == (_x, _y) or self._count > 5:
                    # but we will go back if there were no others twice
                    _direction = __dir.to_string()
                    self._last = _bm.get_x(), _bm.get_y()
                    self._count = 0
                    break
        else:  # it seem that we are surrounded
            print("It's long time passed. Let's drop a bomb")
            _direction = Direction('ACT').to_string()  # let's drop a bomb  :)
        return _direction


if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")
