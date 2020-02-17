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


class State:
    operators = []

    def __init__(self):
        self._state=None
    
    def __init__(self,state):
        self._state=state
        self._operator=None
    
    def __init__(self,state,op):
        self._state=state
        self._operator=op

    def getOperators(self):
        return State.operators

    def applicable(self, operator):
        pass

    def apply(self, operator):
        pass

    def isFinalState(self):
        pass

    def getMinMaxUtilityScore(self):
        pass
    
    def getOperator(self):
        return self._operator

class BombermanState(State):
    State.operators=[
        Direction('RIGHT'),
        Direction('LEFT'),
        Direction('UP'),
        Direction('DOWN'),
        Direction('ACT'),
        Direction("NULL")
    ]
    def __init__(self, board_string,bomberman):
        super().__init__(Board(board_string),None)
        self._board_string=board_string
        self._bomberman = bomberman
    
    def __init__(self, board_string,bomberman,op):
        super().__init__(Board(board_string),op)
        self._board_string=board_string
        self._bomberman = bomberman
    
        
    def getOperators(self):
        return State.operators

    def isApplicable(self, operator):
        _no_go = self._state.get_barriers()+self._state.get_meat_choppers()
     
        if operator == Direction("NULL") and self._state.is_my_bomberman_dead():
            return True
        elif (operator not in [ Direction("NULL")] and
            Point(operator.change_x(self._bomberman.get_x()), operator.change_y(self._bomberman.get_y())) not in _no_go and
            self._state.get_at(operator.change_x(self._bomberman.get_x()), operator.change_y(self._bomberman.get_y())).get_char != ' '
            and not self._state.is_my_bomberman_dead()):
            print("ME")
            return True
        
        elif (
            (operator == Direction('ACT') and (
              Point(self._bomberman.get_x(),self._bomberman.get_y()) not in self._state.get_bombs()
            ) or (
                4 == self._state.count_near(self._bomberman.get_x(), self._bomberman.get_y(), Element('DESTROY_WALL')) + 
                self._state.count_near(self._bomberman.get_x(), self._bomberman.get_x(), Element('WALL'))
                ))
             and not self._state.is_my_bomberman_dead()):
            return True

        return False

    def apply(self, operator):
        #if operator != Direction('ACT'):
        bomberman=Point(operator.change_x(self._bomberman.get_x()),operator.change_y(self._bomberman.get_y()))
        return BombermanState(self._board_string,bomberman,operator)

    def isFinalState(self):
        return self._state.is_my_bomberman_dead()

    def getMinMaxUtilityScore(self):
        bomberman_point = None
        score = 0
        if self._operator is None:
            bomberman_point = Point(self._bomberman.get_x(),self._bomberman.get_y())
        else:    
            bomberman_point = Point(self._operator.change_x(self._bomberman.get_x()), self._operator.change_y(self._bomberman.get_y()))
        if bomberman_point in self._state.get_bombs():
            score-= -500
        try:
            if len(self._state.get_future_blasts())>1 and bomberman_point in self._state.get_future_blasts():
               score-= -500
        except TypeError:
            pass
        finally:
            pass
        if bomberman_point in self._state.get_meat_choppers():
            score+=-100
        surrounding = [
            Point(Direction('LEFT').change_x(bomberman_point.get_x()),Direction('LEFT').change_y(bomberman_point.get_y())),
            Point(Direction('RIGHT').change_x(bomberman_point.get_x()),Direction('RIGHT').change_y(bomberman_point.get_y())),
            Point(Direction('UP').change_x(bomberman_point.get_x()),Direction('UP').change_y(bomberman_point.get_y())),
            Point(Direction('DOWN').change_x(bomberman_point.get_x()),Direction('DOWN').change_y(bomberman_point.get_y())),
        ]
        for i in surrounding:
            if i in self._state.get_destroy_walls():
                score+=100
            if i in self._state.get_meat_choppers():
                score+=200
            if i in self._state.get_other_bombermans():
                score+=1000
            if i in self._state.get_bombs():
                return -500
        return score

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
            

    
class DirectionSolver:
    """ This class should contain the movement generation algorythm."""

    def __init__(self):
        self._direction = None
        self._board = None
        self._last = None
        self._count = 0

    def get(self, board_string):
        """ The function that should be implemented."""
        self._board = Board(board_string)
        self._test = BombermanState(board_string=board_string,bomberman=self._board.get_bomberman(),op=None)
        _testMinMax = MinMax(state=self._test,deep=2)
        print( _testMinMax.get_step().to_string()+":"+ str(_testMinMax.get_utilityscore()))
        _command=_testMinMax.get_step().to_string()
        #_command = self.find_direction()
        #_command=Direction("STOP").to_string()
        print("Sending Command {}".format(_command))

        return _command

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
