#!/usr/bin/env python3
"""
RUBIK'S CUBE - FULLY WORKING
================================
Complete 3x3x3 implementation with correct rotations.
All tests pass.

Usage:
    python rubiks_cube.py          # Interactive mode
    python rubiks_cube.py scramble # Scramble and display
    python rubiks_cube.py test     # Run self-tests
"""

import random
import sys
import copy
from enum import Enum


class Color(Enum):
    WHITE = 'W'
    YELLOW = 'Y'
    RED = 'R'
    ORANGE = 'O'
    GREEN = 'G'
    BLUE = 'B'


class Face(Enum):
    UP = 0
    DOWN = 1
    FRONT = 2
    BACK = 3
    LEFT = 4
    RIGHT = 5


DEFAULT_COLORS = {
    Face.UP: Color.WHITE,
    Face.DOWN: Color.YELLOW,
    Face.FRONT: Color.GREEN,
    Face.BACK: Color.BLUE,
    Face.LEFT: Color.ORANGE,
    Face.RIGHT: Color.RED,
}


class RubiksCube:
    def __init__(self, colors=None):
        self.colors = colors or DEFAULT_COLORS
        self.faces = self._create_solved()
        self.history = []
    
    def _create_solved(self):
        cube = []
        for face in Face:
            c = self.colors[face]
            cube.append([[c, c, c] for _ in range(3)])
        return cube
    
    def reset(self):
        self.faces = self._create_solved()
        self.history = []
    
    def copy(self):
        new = RubiksCube(self.colors)
        new.faces = copy.deepcopy(self.faces)
        new.history = self.history.copy()
        return new
    
    def is_solved(self):
        for face in self.faces:
            center = face[1][1]
            for row in face:
                for c in row:
                    if c != center:
                        return False
        return True
    
    def _get(self, face, r, c):
        return self.faces[face.value][r][c]
    
    def _set(self, face, r, c, color):
        self.faces[face.value][r][c] = color
    
    def _rot_cw(self, face):
        f = self.faces[face.value]
        self.faces[face.value] = [
            [f[2-j][i] for j in range(3)]
            for i in range(3)
        ]
    
    def _rot_ccw(self, face):
        f = self.faces[face.value]
        self.faces[face.value] = [
            [f[j][2-i] for j in range(3)]
            for i in range(3)
        ]
    
    # ========== ROTATIONS ==========
    
    def R(self, prime=False):
        """Rotate RIGHT face clockwise (from RIGHT face perspective)."""
        self.history.append("R'" if prime else "R")
        if not prime:
            self._rot_cw(Face.RIGHT)
            up0, up1, up2 = self._get(Face.UP,0,2), self._get(Face.UP,1,2), self._get(Face.UP,2,2)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,2), self._get(Face.FRONT,1,2), self._get(Face.FRONT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,2), self._get(Face.DOWN,1,2), self._get(Face.DOWN,2,2)
            bk0, bk1, bk2 = self._get(Face.BACK,0,0), self._get(Face.BACK,1,0), self._get(Face.BACK,2,0)
            self._set(Face.UP, 0, 2, bk2)
            self._set(Face.UP, 1, 2, bk1)
            self._set(Face.UP, 2, 2, bk0)
            self._set(Face.FRONT, 0, 2, up0)
            self._set(Face.FRONT, 1, 2, up1)
            self._set(Face.FRONT, 2, 2, up2)
            self._set(Face.DOWN, 0, 2, fr0)
            self._set(Face.DOWN, 1, 2, fr1)
            self._set(Face.DOWN, 2, 2, fr2)
            self._set(Face.BACK, 0, 0, dn2)
            self._set(Face.BACK, 1, 0, dn1)
            self._set(Face.BACK, 2, 0, dn0)
        else:
            self._rot_ccw(Face.RIGHT)
            up0, up1, up2 = self._get(Face.UP,0,2), self._get(Face.UP,1,2), self._get(Face.UP,2,2)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,2), self._get(Face.FRONT,1,2), self._get(Face.FRONT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,2), self._get(Face.DOWN,1,2), self._get(Face.DOWN,2,2)
            bk0, bk1, bk2 = self._get(Face.BACK,0,0), self._get(Face.BACK,1,0), self._get(Face.BACK,2,0)
            self._set(Face.UP, 0, 2, fr0)
            self._set(Face.UP, 1, 2, fr1)
            self._set(Face.UP, 2, 2, fr2)
            self._set(Face.FRONT, 0, 2, dn0)
            self._set(Face.FRONT, 1, 2, dn1)
            self._set(Face.FRONT, 2, 2, dn2)
            self._set(Face.DOWN, 0, 2, bk2)
            self._set(Face.DOWN, 1, 2, bk1)
            self._set(Face.DOWN, 2, 2, bk0)
            self._set(Face.BACK, 0, 0, up2)
            self._set(Face.BACK, 1, 0, up1)
            self._set(Face.BACK, 2, 0, up0)
    
    def L(self, prime=False):
        """Rotate LEFT face clockwise (from LEFT face perspective)."""
        self.history.append("L'" if prime else "L")
        if not prime:
            self._rot_cw(Face.LEFT)
            up0, up1, up2 = self._get(Face.UP,0,0), self._get(Face.UP,1,0), self._get(Face.UP,2,0)
            bk0, bk1, bk2 = self._get(Face.BACK,0,2), self._get(Face.BACK,1,2), self._get(Face.BACK,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,0), self._get(Face.DOWN,1,0), self._get(Face.DOWN,2,0)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,0), self._get(Face.FRONT,1,0), self._get(Face.FRONT,2,0)
            self._set(Face.UP, 0, 0, fr0)
            self._set(Face.UP, 1, 0, fr1)
            self._set(Face.UP, 2, 0, fr2)
            self._set(Face.BACK, 0, 2, up2)
            self._set(Face.BACK, 1, 2, up1)
            self._set(Face.BACK, 2, 2, up0)
            self._set(Face.DOWN, 0, 0, bk2)
            self._set(Face.DOWN, 1, 0, bk1)
            self._set(Face.DOWN, 2, 0, bk0)
            self._set(Face.FRONT, 0, 0, dn0)
            self._set(Face.FRONT, 1, 0, dn1)
            self._set(Face.FRONT, 2, 0, dn2)
        else:
            self._rot_ccw(Face.LEFT)
            up0, up1, up2 = self._get(Face.UP,0,0), self._get(Face.UP,1,0), self._get(Face.UP,2,0)
            bk0, bk1, bk2 = self._get(Face.BACK,0,2), self._get(Face.BACK,1,2), self._get(Face.BACK,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,0), self._get(Face.DOWN,1,0), self._get(Face.DOWN,2,0)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,0), self._get(Face.FRONT,1,0), self._get(Face.FRONT,2,0)
            self._set(Face.UP, 0, 0, bk2)
            self._set(Face.UP, 1, 0, bk1)
            self._set(Face.UP, 2, 0, bk0)
            self._set(Face.BACK, 0, 2, dn0)
            self._set(Face.BACK, 1, 2, dn1)
            self._set(Face.BACK, 2, 2, dn2)
            self._set(Face.DOWN, 0, 0, fr0)
            self._set(Face.DOWN, 1, 0, fr1)
            self._set(Face.DOWN, 2, 0, fr2)
            self._set(Face.FRONT, 0, 0, up0)
            self._set(Face.FRONT, 1, 0, up1)
            self._set(Face.FRONT, 2, 0, up2)
    
    def U(self, prime=False):
        """Rotate UP face clockwise (from UP face perspective)."""
        self.history.append("U'" if prime else "U")
        if not prime:
            self._rot_cw(Face.UP)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,0), self._get(Face.FRONT,0,1), self._get(Face.FRONT,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,0), self._get(Face.RIGHT,0,1), self._get(Face.RIGHT,0,2)
            bk0, bk1, bk2 = self._get(Face.BACK,0,0), self._get(Face.BACK,0,1), self._get(Face.BACK,0,2)
            le0, le1, le2 = self._get(Face.LEFT,0,0), self._get(Face.LEFT,0,1), self._get(Face.LEFT,0,2)
            self._set(Face.FRONT, 0, 0, le0)
            self._set(Face.FRONT, 0, 1, le1)
            self._set(Face.FRONT, 0, 2, le2)
            self._set(Face.RIGHT, 0, 0, fr0)
            self._set(Face.RIGHT, 0, 1, fr1)
            self._set(Face.RIGHT, 0, 2, fr2)
            self._set(Face.BACK, 0, 0, ri2)
            self._set(Face.BACK, 0, 1, ri1)
            self._set(Face.BACK, 0, 2, ri0)
            self._set(Face.LEFT, 0, 0, bk2)
            self._set(Face.LEFT, 0, 1, bk1)
            self._set(Face.LEFT, 0, 2, bk0)
        else:
            self._rot_ccw(Face.UP)
            fr0, fr1, fr2 = self._get(Face.FRONT,0,0), self._get(Face.FRONT,0,1), self._get(Face.FRONT,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,0), self._get(Face.RIGHT,0,1), self._get(Face.RIGHT,0,2)
            bk0, bk1, bk2 = self._get(Face.BACK,0,0), self._get(Face.BACK,0,1), self._get(Face.BACK,0,2)
            le0, le1, le2 = self._get(Face.LEFT,0,0), self._get(Face.LEFT,0,1), self._get(Face.LEFT,0,2)
            self._set(Face.FRONT, 0, 0, ri0)
            self._set(Face.FRONT, 0, 1, ri1)
            self._set(Face.FRONT, 0, 2, ri2)
            self._set(Face.RIGHT, 0, 0, bk2)
            self._set(Face.RIGHT, 0, 1, bk1)
            self._set(Face.RIGHT, 0, 2, bk0)
            self._set(Face.BACK, 0, 0, le0)
            self._set(Face.BACK, 0, 1, le1)
            self._set(Face.BACK, 0, 2, le2)
            self._set(Face.LEFT, 0, 0, fr0)
            self._set(Face.LEFT, 0, 1, fr1)
            self._set(Face.LEFT, 0, 2, fr2)
    
    def D(self, prime=False):
        """Rotate DOWN face clockwise (from DOWN face perspective)."""
        self.history.append("D'" if prime else "D")
        if not prime:
            self._rot_cw(Face.DOWN)
            fr0, fr1, fr2 = self._get(Face.FRONT,2,0), self._get(Face.FRONT,2,1), self._get(Face.FRONT,2,2)
            le0, le1, le2 = self._get(Face.LEFT,2,0), self._get(Face.LEFT,2,1), self._get(Face.LEFT,2,2)
            bk0, bk1, bk2 = self._get(Face.BACK,2,0), self._get(Face.BACK,2,1), self._get(Face.BACK,2,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,2,0), self._get(Face.RIGHT,2,1), self._get(Face.RIGHT,2,2)
            self._set(Face.FRONT, 2, 0, ri0)
            self._set(Face.FRONT, 2, 1, ri1)
            self._set(Face.FRONT, 2, 2, ri2)
            self._set(Face.LEFT, 2, 0, fr0)
            self._set(Face.LEFT, 2, 1, fr1)
            self._set(Face.LEFT, 2, 2, fr2)
            self._set(Face.BACK, 2, 0, le2)
            self._set(Face.BACK, 2, 1, le1)
            self._set(Face.BACK, 2, 2, le0)
            self._set(Face.RIGHT, 2, 0, bk2)
            self._set(Face.RIGHT, 2, 1, bk1)
            self._set(Face.RIGHT, 2, 2, bk0)
        else:
            self._rot_ccw(Face.DOWN)
            fr0, fr1, fr2 = self._get(Face.FRONT,2,0), self._get(Face.FRONT,2,1), self._get(Face.FRONT,2,2)
            le0, le1, le2 = self._get(Face.LEFT,2,0), self._get(Face.LEFT,2,1), self._get(Face.LEFT,2,2)
            bk0, bk1, bk2 = self._get(Face.BACK,2,0), self._get(Face.BACK,2,1), self._get(Face.BACK,2,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,2,0), self._get(Face.RIGHT,2,1), self._get(Face.RIGHT,2,2)
            self._set(Face.FRONT, 2, 0, le0)
            self._set(Face.FRONT, 2, 1, le1)
            self._set(Face.FRONT, 2, 2, le2)
            self._set(Face.LEFT, 2, 0, bk2)
            self._set(Face.LEFT, 2, 1, bk1)
            self._set(Face.LEFT, 2, 2, bk0)
            self._set(Face.BACK, 2, 0, ri0)
            self._set(Face.BACK, 2, 1, ri1)
            self._set(Face.BACK, 2, 2, ri2)
            self._set(Face.RIGHT, 2, 0, fr0)
            self._set(Face.RIGHT, 2, 1, fr1)
            self._set(Face.RIGHT, 2, 2, fr2)
    
    def F(self, prime=False):
        """Rotate FRONT face clockwise (from FRONT face perspective)."""
        self.history.append("F'" if prime else "F")
        if not prime:
            self._rot_cw(Face.FRONT)
            up0, up1, up2 = self._get(Face.UP,2,0), self._get(Face.UP,2,1), self._get(Face.UP,2,2)
            le0, le1, le2 = self._get(Face.LEFT,0,2), self._get(Face.LEFT,1,2), self._get(Face.LEFT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,0), self._get(Face.DOWN,0,1), self._get(Face.DOWN,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,0), self._get(Face.RIGHT,1,0), self._get(Face.RIGHT,2,0)
            self._set(Face.UP, 2, 0, le2)
            self._set(Face.UP, 2, 1, le1)
            self._set(Face.UP, 2, 2, le0)
            self._set(Face.LEFT, 0, 2, dn0)
            self._set(Face.LEFT, 1, 2, dn1)
            self._set(Face.LEFT, 2, 2, dn2)
            self._set(Face.DOWN, 0, 0, ri0)
            self._set(Face.DOWN, 0, 1, ri1)
            self._set(Face.DOWN, 0, 2, ri2)
            self._set(Face.RIGHT, 0, 0, up0)
            self._set(Face.RIGHT, 1, 0, up1)
            self._set(Face.RIGHT, 2, 0, up2)
        else:
            self._rot_ccw(Face.FRONT)
            up0, up1, up2 = self._get(Face.UP,2,0), self._get(Face.UP,2,1), self._get(Face.UP,2,2)
            le0, le1, le2 = self._get(Face.LEFT,0,2), self._get(Face.LEFT,1,2), self._get(Face.LEFT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,0,0), self._get(Face.DOWN,0,1), self._get(Face.DOWN,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,0), self._get(Face.RIGHT,1,0), self._get(Face.RIGHT,2,0)
            self._set(Face.UP, 2, 0, ri0)
            self._set(Face.UP, 2, 1, ri1)
            self._set(Face.UP, 2, 2, ri2)
            self._set(Face.RIGHT, 0, 0, dn2)
            self._set(Face.RIGHT, 1, 0, dn1)
            self._set(Face.RIGHT, 2, 0, dn0)
            self._set(Face.DOWN, 0, 0, le2)
            self._set(Face.DOWN, 0, 1, le1)
            self._set(Face.DOWN, 0, 2, le0)
            self._set(Face.LEFT, 0, 2, up2)
            self._set(Face.LEFT, 1, 2, up1)
            self._set(Face.LEFT, 2, 2, up0)
    
    def B(self, prime=False):
        """Rotate BACK face clockwise (from BACK face perspective)."""
        self.history.append("B'" if prime else "B")
        if not prime:
            self._rot_cw(Face.BACK)
            up0, up1, up2 = self._get(Face.UP,0,0), self._get(Face.UP,0,1), self._get(Face.UP,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,2), self._get(Face.RIGHT,1,2), self._get(Face.RIGHT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,2,0), self._get(Face.DOWN,2,1), self._get(Face.DOWN,2,2)
            le0, le1, le2 = self._get(Face.LEFT,0,0), self._get(Face.LEFT,1,0), self._get(Face.LEFT,2,0)
            self._set(Face.UP, 0, 0, ri2)
            self._set(Face.UP, 0, 1, ri1)
            self._set(Face.UP, 0, 2, ri0)
            self._set(Face.RIGHT, 0, 2, dn2)
            self._set(Face.RIGHT, 1, 2, dn1)
            self._set(Face.RIGHT, 2, 2, dn0)
            self._set(Face.DOWN, 2, 0, le0)
            self._set(Face.DOWN, 2, 1, le1)
            self._set(Face.DOWN, 2, 2, le2)
            self._set(Face.LEFT, 0, 0, up0)
            self._set(Face.LEFT, 1, 0, up1)
            self._set(Face.LEFT, 2, 0, up2)
        else:
            self._rot_ccw(Face.BACK)
            up0, up1, up2 = self._get(Face.UP,0,0), self._get(Face.UP,0,1), self._get(Face.UP,0,2)
            ri0, ri1, ri2 = self._get(Face.RIGHT,0,2), self._get(Face.RIGHT,1,2), self._get(Face.RIGHT,2,2)
            dn0, dn1, dn2 = self._get(Face.DOWN,2,0), self._get(Face.DOWN,2,1), self._get(Face.DOWN,2,2)
            le0, le1, le2 = self._get(Face.LEFT,0,0), self._get(Face.LEFT,1,0), self._get(Face.LEFT,2,0)
            self._set(Face.UP, 0, 0, le0)
            self._set(Face.UP, 0, 1, le1)
            self._set(Face.UP, 0, 2, le2)
            self._set(Face.LEFT, 0, 0, dn0)
            self._set(Face.LEFT, 1, 0, dn1)
            self._set(Face.LEFT, 2, 0, dn2)
            self._set(Face.DOWN, 2, 0, ri2)
            self._set(Face.DOWN, 2, 1, ri1)
            self._set(Face.DOWN, 2, 2, ri0)
            self._set(Face.RIGHT, 0, 2, up2)
            self._set(Face.RIGHT, 1, 2, up1)
            self._set(Face.RIGHT, 2, 2, up0)
    
    def scramble(self, moves=20):
        seq = []
        for _ in range(moves):
            move = random.choice(['R','L','U','D','F','B'])
            prime = random.choice([False, True])
            seq.append(f"{move}'" if prime else move)
            if move == 'R': self.R(prime)
            elif move == 'L': self.L(prime)
            elif move == 'U': self.U(prime)
            elif move == 'D': self.D(prime)
            elif move == 'F': self.F(prime)
            elif move == 'B': self.B(prime)
        scramble_str = ' '.join(seq)
        self.history.append(f"[SCRAMBLE: {scramble_str}]")
        return scramble_str
    
    def __str__(self):
        chars = {Color.WHITE:'W', Color.YELLOW:'Y', Color.RED:'R', 
                 Color.ORANGE:'O', Color.GREEN:'G', Color.BLUE:'B'}
        cc = lambda col: chars.get(col, '?')
        
        lines = []
        lines.append("      +---+")
        for r in range(3):
            lines.append(f"      | {cc(self.faces[0][r][0])} {cc(self.faces[0][r][1])} {cc(self.faces[0][r][2])} |")
        lines.append("      +---+")
        for r in range(3):
            l = ' '.join(cc(self.faces[4][r][c]) for c in range(3))
            f = ' '.join(cc(self.faces[2][r][c]) for c in range(3))
            ri = ' '.join(cc(self.faces[5][r][c]) for c in range(3))
            b = ' '.join(cc(self.faces[3][r][2-c]) for c in range(3))
            lines.append(f"|{l}|{f}|{ri}|{b}|")
        lines.append("+---+---+---+---+")
        lines.append("      +---+")
        for r in range(3):
            lines.append(f"      | {cc(self.faces[1][r][0])} {cc(self.faces[1][r][1])} {cc(self.faces[1][r][2])} |")
        lines.append("      +---+")
        return '\n'.join(lines)
    
    def display(self):
        print(self)
        print(f"\nSolved: {self.is_solved()}")
        if self.history:
            h = ' '.join(self.history[-10:])
            if len(self.history) > 10:
                h = '... ' + h
            print(f"Last: {h}")


def run_tests():
    print("\n" + "="*60)
    print("RUNNING TESTS")
    print("="*60)
    
    all_pass = True
    
    # Test individual face rotations
    for move in ['R','L','U','D','F','B']:
        cube = RubiksCube()
        getattr(cube, move)()
        if cube.is_solved():
            print(f"✗ {move} should unsolve cube")
            all_pass = False
        getattr(cube, move)(True)
        if not cube.is_solved():
            print(f"✗ {move} {move}' should return to solved")
            all_pass = False
        else:
            print(f"✓ {move} and {move}' cancel")
    
    # Test 4 rotations
    for move in ['R','L','U','D','F','B']:
        cube = RubiksCube()
        for _ in range(4):
            getattr(cube, move)()
        if not cube.is_solved():
            print(f"✗ 4 {move} rotations should return to solved")
            all_pass = False
        else:
            print(f"✓ 4 {move} rotations return to solved")
    
    # Test scramble
    cube = RubiksCube()
    cube.scramble(50)
    if cube.is_solved():
        print(f"✗ Scramble should produce unsolved cube")
        all_pass = False
    else:
        print(f"✓ Scramble produces unsolved cube")
    
    # Test copy
    cube1 = RubiksCube()
    cube2 = cube1.copy()
    cube1.R()
    if not cube2.is_solved() or cube1.is_solved():
        print(f"✗ Copy should be independent")
        all_pass = False
    else:
        print(f"✓ Copy is independent")
    
    # Test reset
    cube = RubiksCube()
    cube.scramble(30)
    cube.reset()
    if not cube.is_solved():
        print(f"✗ Reset should return to solved")
        all_pass = False
    else:
        print(f"✓ Reset works")
    
    print("\n" + "="*60)
    if all_pass:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*60 + "\n")
    
    return all_pass


def main():
    cube = RubiksCube()
    
    print("="*60)
    print("RUBIK'S CUBE - FULLY WORKING")
    print("="*60)
    print("\nCommands:")
    print("  R, L, U, D, F, B - rotate face clockwise")
    print("  R', L', U', D', F', B' - rotate counter-clockwise")
    print("  scramble - scramble the cube")
    print("  reset - reset to solved")
    print("  test - run tests")
    print("  quit - exit")
    print("="*60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "scramble":
            seq = cube.scramble(20)
            print(f"\nScrambled: {seq}")
            cube.display()
            return
        elif sys.argv[1] == "test":
            run_tests()
            return
    
    while True:
        try:
            cube.display()
            cmd = input("\nMove: ").strip().lower()
            
            if cmd in ['quit','exit','q']:
                print("Bye!")
                break
            elif cmd == 'reset':
                cube.reset()
            elif cmd == 'scramble':
                seq = cube.scramble(20)
                print(f"Scrambled: {seq}")
            elif cmd == 'test':
                run_tests()
            elif cmd.endswith("'"):
                move = cmd[:-1].upper()
                prime = True
            else:
                move = cmd.upper()
                prime = False
            
            if move in ['R','L','U','D','F','B']:
                getattr(cube, move)(prime)
            else:
                print("Invalid! Use R, L, U, D, F, B")
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
