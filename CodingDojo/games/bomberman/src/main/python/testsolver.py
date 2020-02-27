
import unittest
from dds import BombermanBoard
from element import Element
from direction import Direction
from point import Point
from dds import StepProposal
from dds import TreeSerch
from builtins import len


class Testsolver(unittest.TestCase):
    board = "☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼#       #        #   #  &## #  ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼&☼ ☼ ☼#☼#☼☼                #    #   #    #☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼#☼#☼ ☼ ☼#☼☼            #      #     ## ## ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼☺☼#☼ ☼☼                       ###     ☼☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼#☼ ☼#☼ ☼☼ ##        #  # #            # ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼☼    ♥   &        #    # # #  ##☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼#☼☼                           # # ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼#☼☼                 #   #       # ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼☼#  #      &          #         ☼☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼#   #           ## #   #     # ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼#                      ### #   ☼☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼☼                ###   #        ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼#☼ ☼ ☼ ☼#☼#☼ ☼☼        #         #    #      &☼☼#☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼&☼ ☼ ☼#☼#☼☼    # #                   &    ☼☼#☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼&☼ ☼ ☼#☼☼##    #   #            &   ### ☼☼#☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼☼   #          #    &    ##     ☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼"
    board2 = "☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼ ###    #   #                # ☼☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼#☼☼#       #   ##            #    ☼☼#☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼ #      #    ## #     #        ☼☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼☼##        &#                  #☼☼#☼ ☼#☼ ☼ ☼ ☼&☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼☼         #        # &     #    ☼☼#☼#☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼   # #    &                    ☼☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼ ##  #  # #                    ☼☼#☼ ☼#☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼####                           ☼☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼☼      # #               # #    ☼☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼☼#      #           #     #    #☼☼&☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼☼#            #    #       #    ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼#☼☼#          # #   # #        #  ☼☼ ☼☺☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼ ☼ ☼☼#            # ##       # ### #☼☼#☼ ☼ ☼#☼&☼ ☼ ☼ ☼#☼ ☼ ☼ ☼#☼ ☼#☼&☼☼1           # &     # #        ☼☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼ ☼#☼ ☼#☼ ☼ ☼ ☼&☼☼  ♥            #           ##  ☼☼ ☼ ☼ ☼ ☼ ☼#☼ ☼ ☼ ☼ ☼#☼ ☼#☼ ☼ ☼ ☼☼       #   &         ####      ☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼☼"
    def test_ops(self):
        test = BombermanBoard(Testsolver.board)
        test2 = BombermanBoard(Testsolver.board2)
        print(test2)
        self.assertNotEqual(len(test.getOperators()),0)
        self.assertNotEqual(len(test2.getOperators()),0)
        
    def test_applicable_down(self):
        test = BombermanBoard(Testsolver.board)
        test2 = BombermanBoard(Testsolver.board2)
        self.assertTrue(test.isApplicable(Direction('DOWN')))
        self.assertTrue(test2.isApplicable(Direction('DOWN')))
        
    def test_applicable_up(self):
        test = BombermanBoard(Testsolver.board)
        test2 = BombermanBoard(Testsolver.board2)
        self.assertFalse(test.isApplicable(Direction('UP')))
        self.assertTrue(test2.isApplicable(Direction('UP')))
    
    def test_applicable_left(self):
        test = BombermanBoard(Testsolver.board)
        self.assertFalse(test.isApplicable(Direction('LEFT')))
    
    def test_applicable_right(self):
        test = BombermanBoard(Testsolver.board)
        self.assertFalse(test.isApplicable(Direction('RIGHT')))
        
    def test_constructor_down(self):
        test = BombermanBoard(Testsolver.board)
        self.assertTrue(Direction('DOWN') in test.getOperators())
    
    def test_constructor_down_applay(self):
        test1 = BombermanBoard(Testsolver.board)
        test2 = BombermanBoard(board_string=Testsolver.board,parrent=None,operator=Direction('DOWN'),deep=0)
        self.assertTrue(Point(27,7) == test2.get_bomberman())
    
    def test_constructor_ACT_applay(self):
        test2 = BombermanBoard(board_string=Testsolver.board,parrent=None,operator=Direction('ACT'),deep=0)
        p =test2.get_bomberman()
        self.assertTrue(test2.is_at(p.get_x(),p.get_y(),Element('BOMB_BOMBERMAN')))
        
    def test_constructor_down2_applay(self):
        test1 = BombermanBoard(Testsolver.board)
        test2 = BombermanBoard(board_string=Testsolver.board,parrent=None,operator=Direction('DOWN'),deep=0)
        test3 = BombermanBoard(board_string=test2._string,parrent=test2,operator=Direction('DOWN'),deep=0)
        self.assertTrue(Point(27,8) == test3.get_bomberman())
    
    def test_treeSource_one_step(self):
        test1 = BombermanBoard(Testsolver.board)
        suggest = TreeSerch(state=test1,deep=1).serch()
        self.assertTrue(Direction('DOWN') == suggest.pop().getOperator())
    
    def test_treeSource_two_step(self):
        test1 = BombermanBoard(Testsolver.board)
        suggest = TreeSerch(state=test1,deep=2,findAll=True).serch()        
        suggest_state = suggest.pop()
        self.assertTrue(Direction('DOWN') == suggest_state.getOperator())
    
    def test_treeSource_two_step2(self):
        test1 = BombermanBoard(Testsolver.board2)
        suggest = TreeSerch(state=test1,deep=2,findAll=True).serch()        
        suggest_state = suggest.pop()
        self.assertTrue(Direction('DOWN') == suggest_state.getOperator())
        
    def test_treeSource_getpath2(self):
        test1 = BombermanBoard(Testsolver.board2)
        suggest = TreeSerch(state=test1,deep=2,findAll=True).serch()        
        suggest_state = suggest.pop()
        self.assertTrue(Direction('DOWN') in TreeSerch.getPath(node=suggest_state))

if __name__ == '__main__':
    # Main module
    unittest.main()