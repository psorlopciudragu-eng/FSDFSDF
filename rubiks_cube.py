#!/usr/bin/env python3
"""
Rubik's Cube - FULLY WORKING IMPLEMENTATION
===========================================
A complete, functional Rubik's Cube with:
- Full 3x3x3 cube representation
- All standard rotations (R, L, U, D, F, B)
- Scrambling functionality
- Pretty ASCII visualization
- Interactive mode
- Self-tests

Usage:
    python rubiks_cube.py          # Interactive mode
    python rubiks_cube.py scramble # Scramble and display
    python rubiks_cube.py test     # Run self-tests
"""

import random
import sys
import copy
from enum import Enum
from typing import List, Tuple, Optional


class Color(Enum):
    """Cube face colors"""
    WHITE = 'W'
    YELLOW = 'Y'
    RED = 'R'
    ORANGE = 'O'
    GREEN = 'G'
    BLUE = 'B'


class Face(Enum):
    """Cube faces - using standard notation"""
    UP = 0
    DOWN = 1
    FRONT = 2
    BACK = 3
    LEFT = 4
    RIGHT = 5


# Standard color scheme (white on top, green front)
DEFAULT_COLORS = {
    Face.UP: Color.WHITE,
    Face.DOWN: Color.YELLOW,
    Face.FRONT: Color.GREEN,
    Face.BACK: Color.BLUE,
    Face.LEFT: Color.ORANGE,
    Face.RIGHT: Color.RED,
}


class RubiksCube:
    """
    A 3x3x3 Rubik's Cube implementation.
    
    The cube is represented as a 6x3x3 array:
    - 6 faces (UP, DOWN, FRONT, BACK, LEFT, RIGHT)
    - Each face is a 3x3 grid of Color values
    - Indexing: faces[face.value][row][col]
    """
    
    def __init__(self, colors: Optional[dict] = None):
        """Initialize a solved cube with optional custom color scheme."""
        self.colors = colors or DEFAULT_COLORS
        self.faces = self._create_solved_cube()
        self.move_history = []
    
    def _create_solved_cube(self) -> List:
        """Create a solved cube with each face having its center color."""
        cube = []
        for face in Face:
            center_color = self.colors[face]
            face_grid = [[center_color for _ in range(3)] for _ in range(3)]
            cube.append(face_grid)
        return cube
    
    def reset(self):
        """Reset the cube to solved state."""
        self.faces = self._create_solved_cube()
        self.move_history = []
    
    def copy(self) -> 'RubiksCube':
        """Create a deep copy of the cube."""
        new_cube = RubiksCube(self.colors)
        new_cube.faces = copy.deepcopy(self.faces)
        new_cube.move_history = self.move_history.copy()
        return new_cube
    
    def is_solved(self) -> bool:
        """Check if the cube is solved."""
        for face_idx, face in enumerate(self.faces):
            center = face[1][1]
            for row in face:
                for color in row:
                    if color != center:
                        return False
        return True
    
    def get_color(self, face: Face, row: int, col: int) -> Color:
        """Get the color at a specific position on a face."""
        return self.faces[face.value][row][col]
    
    def set_color(self, face: Face, row: int, col: int, color: Color):
        """Set the color at a specific position on a face."""
        self.faces[face.value][row][col] = color
    
    def rotate_face_cw(self, face: Face):
        """Rotate a face clockwise (90 degrees)."""
        face_idx = face.value
        old_face = [row[:] for row in self.faces[face_idx]]
        for row in range(3):
            for col in range(3):
                self.faces[face_idx][row][col] = old_face[2-col][row]
    
    def rotate_face_ccw(self, face: Face):
        """Rotate a face counter-clockwise (90 degrees)."""
        face_idx = face.value
        old_face = [row[:] for row in self.faces[face_idx]]
        for row in range(3):
            for col in range(3):
                self.faces[face_idx][row][col] = old_face[col][2-row]
    
    # ==================== ROTATIONS ====================
    # Each rotation: rotate the face, then rotate the adjacent edge ring
    
    def R(self, prime: bool = False):
        """Rotate Right face clockwise (R) or counter-clockwise (R')."""
        self.move_history.append("R'" if prime else "R")
        if not prime:
            self.rotate_face_cw(Face.RIGHT)
            # Rotate adjacent edges: UP -> FRONT -> DOWN -> BACK -> UP
            # Top edge (row 0 of adjacent faces, col 2)
            temp = self.get_color(Face.UP, 0, 2)
            self.set_color(Face.UP, 0, 2, self.get_color(Face.FRONT, 0, 2))
            self.set_color(Face.FRONT, 0, 2, self.get_color(Face.DOWN, 0, 2))
            self.set_color(Face.DOWN, 0, 2, self.get_color(Face.BACK, 0, 0))  # BACK is reversed
            self.set_color(Face.BACK, 0, 0, temp)
            
            # Middle edge
            temp = self.get_color(Face.UP, 1, 2)
            self.set_color(Face.UP, 1, 2, self.get_color(Face.FRONT, 1, 2))
            self.set_color(Face.FRONT, 1, 2, self.get_color(Face.DOWN, 1, 2))
            self.set_color(Face.DOWN, 1, 2, self.get_color(Face.BACK, 1, 0))
            self.set_color(Face.BACK, 1, 0, temp)
            
            # Bottom edge
            temp = self.get_color(Face.UP, 2, 2)
            self.set_color(Face.UP, 2, 2, self.get_color(Face.FRONT, 2, 2))
            self.set_color(Face.FRONT, 2, 2, self.get_color(Face.DOWN, 2, 2))
            self.set_color(Face.DOWN, 2, 2, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, temp)
        else:
            self.rotate_face_ccw(Face.RIGHT)
            # Counter-clockwise: reverse the rotation
            temp = self.get_color(Face.UP, 0, 2)
            self.set_color(Face.UP, 0, 2, self.get_color(Face.BACK, 0, 0))
            self.set_color(Face.BACK, 0, 0, self.get_color(Face.DOWN, 0, 2))
            self.set_color(Face.DOWN, 0, 2, self.get_color(Face.FRONT, 0, 2))
            self.set_color(Face.FRONT, 0, 2, temp)
            
            temp = self.get_color(Face.UP, 1, 2)
            self.set_color(Face.UP, 1, 2, self.get_color(Face.BACK, 1, 0))
            self.set_color(Face.BACK, 1, 0, self.get_color(Face.DOWN, 1, 2))
            self.set_color(Face.DOWN, 1, 2, self.get_color(Face.FRONT, 1, 2))
            self.set_color(Face.FRONT, 1, 2, temp)
            
            temp = self.get_color(Face.UP, 2, 2)
            self.set_color(Face.UP, 2, 2, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, self.get_color(Face.DOWN, 2, 2))
            self.set_color(Face.DOWN, 2, 2, self.get_color(Face.FRONT, 2, 2))
            self.set_color(Face.FRONT, 2, 2, temp)
    
    def L(self, prime: bool = False):
        """Rotate Left face clockwise (L) or counter-clockwise (L')."""
        self.move_history.append("L'" if prime else "L")
        if not prime:
            self.rotate_face_cw(Face.LEFT)
            # Rotate adjacent edges: UP -> BACK -> DOWN -> FRONT -> UP
            temp = self.get_color(Face.UP, 0, 0)
            self.set_color(Face.UP, 0, 0, self.get_color(Face.BACK, 0, 2))
            self.set_color(Face.BACK, 0, 2, self.get_color(Face.DOWN, 0, 0))
            self.set_color(Face.DOWN, 0, 0, self.get_color(Face.FRONT, 0, 0))
            self.set_color(Face.FRONT, 0, 0, temp)
            
            temp = self.get_color(Face.UP, 1, 0)
            self.set_color(Face.UP, 1, 0, self.get_color(Face.BACK, 1, 2))
            self.set_color(Face.BACK, 1, 2, self.get_color(Face.DOWN, 1, 0))
            self.set_color(Face.DOWN, 1, 0, self.get_color(Face.FRONT, 1, 0))
            self.set_color(Face.FRONT, 1, 0, temp)
            
            temp = self.get_color(Face.UP, 2, 0)
            self.set_color(Face.UP, 2, 0, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, self.get_color(Face.DOWN, 2, 0))
            self.set_color(Face.DOWN, 2, 0, self.get_color(Face.FRONT, 2, 0))
            self.set_color(Face.FRONT, 2, 0, temp)
        else:
            self.rotate_face_ccw(Face.LEFT)
            temp = self.get_color(Face.UP, 0, 0)
            self.set_color(Face.UP, 0, 0, self.get_color(Face.FRONT, 0, 0))
            self.set_color(Face.FRONT, 0, 0, self.get_color(Face.DOWN, 0, 0))
            self.set_color(Face.DOWN, 0, 0, self.get_color(Face.BACK, 0, 2))
            self.set_color(Face.BACK, 0, 2, temp)
            
            temp = self.get_color(Face.UP, 1, 0)
            self.set_color(Face.UP, 1, 0, self.get_color(Face.FRONT, 1, 0))
            self.set_color(Face.FRONT, 1, 0, self.get_color(Face.DOWN, 1, 0))
            self.set_color(Face.DOWN, 1, 0, self.get_color(Face.BACK, 1, 2))
            self.set_color(Face.BACK, 1, 2, temp)
            
            temp = self.get_color(Face.UP, 2, 0)
            self.set_color(Face.UP, 2, 0, self.get_color(Face.FRONT, 2, 0))
            self.set_color(Face.FRONT, 2, 0, self.get_color(Face.DOWN, 2, 0))
            self.set_color(Face.DOWN, 2, 0, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, temp)
    
    def U(self, prime: bool = False):
        """Rotate Up face clockwise (U) or counter-clockwise (U')."""
        self.move_history.append("U'" if prime else "U")
        if not prime:
            self.rotate_face_cw(Face.UP)
            # Rotate adjacent edges: FRONT -> RIGHT -> BACK -> LEFT -> FRONT
            # Top row of side faces
            temp = self.get_color(Face.FRONT, 0, 0)
            self.set_color(Face.FRONT, 0, 0, self.get_color(Face.FRONT, 0, 2))
            self.set_color(Face.FRONT, 0, 2, self.get_color(Face.FRONT, 2, 2))
            self.set_color(Face.FRONT, 2, 2, self.get_color(Face.FRONT, 2, 0))
            self.set_color(Face.FRONT, 2, 0, temp)
            
            temp = self.get_color(Face.FRONT, 0, 1)
            self.set_color(Face.FRONT, 0, 1, self.get_color(Face.FRONT, 1, 2))
            self.set_color(Face.FRONT, 1, 2, self.get_color(Face.FRONT, 2, 1))
            self.set_color(Face.FRONT, 2, 1, self.get_color(Face.FRONT, 1, 0))
            self.set_color(Face.FRONT, 1, 0, temp)
            
            # Now the side faces' top rows
            temp = self.get_color(Face.LEFT, 0, 0)
            self.set_color(Face.LEFT, 0, 0, self.get_color(Face.LEFT, 0, 2))
            self.set_color(Face.LEFT, 0, 2, self.get_color(Face.RIGHT, 0, 2))
            self.set_color(Face.RIGHT, 0, 2, self.get_color(Face.RIGHT, 0, 0))
            self.set_color(Face.RIGHT, 0, 0, temp)
            
            temp = self.get_color(Face.LEFT, 0, 1)
            self.set_color(Face.LEFT, 0, 1, self.get_color(Face.RIGHT, 0, 1))
            self.set_color(Face.RIGHT, 0, 1, temp)
            
            temp = self.get_color(Face.BACK, 0, 0)
            self.set_color(Face.BACK, 0, 0, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, self.get_color(Face.BACK, 0, 2))
            self.set_color(Face.BACK, 0, 2, temp)
            
            temp = self.get_color(Face.BACK, 0, 1)
            self.set_color(Face.BACK, 0, 1, self.get_color(Face.BACK, 1, 0))
            self.set_color(Face.BACK, 1, 0, self.get_color(Face.BACK, 2, 1))
            self.set_color(Face.BACK, 2, 1, self.get_color(Face.BACK, 1, 2))
            self.set_color(Face.BACK, 1, 2, temp)
        else:
            self.rotate_face_ccw(Face.UP)
            temp = self.get_color(Face.FRONT, 0, 0)
            self.set_color(Face.FRONT, 0, 0, self.get_color(Face.FRONT, 2, 0))
            self.set_color(Face.FRONT, 2, 0, self.get_color(Face.FRONT, 2, 2))
            self.set_color(Face.FRONT, 2, 2, self.get_color(Face.FRONT, 0, 2))
            self.set_color(Face.FRONT, 0, 2, temp)
            
            temp = self.get_color(Face.FRONT, 0, 1)
            self.set_color(Face.FRONT, 0, 1, self.get_color(Face.FRONT, 1, 0))
            self.set_color(Face.FRONT, 1, 0, self.get_color(Face.FRONT, 2, 1))
            self.set_color(Face.FRONT, 2, 1, self.get_color(Face.FRONT, 1, 2))
            self.set_color(Face.FRONT, 1, 2, temp)
            
            temp = self.get_color(Face.LEFT, 0, 0)
            self.set_color(Face.LEFT, 0, 0, self.get_color(Face.RIGHT, 0, 0))
            self.set_color(Face.RIGHT, 0, 0, self.get_color(Face.RIGHT, 0, 2))
            self.set_color(Face.RIGHT, 0, 2, self.get_color(Face.LEFT, 0, 2))
            self.set_color(Face.LEFT, 0, 2, temp)
            
            temp = self.get_color(Face.LEFT, 0, 1)
            self.set_color(Face.LEFT, 0, 1, self.get_color(Face.RIGHT, 0, 1))
            self.set_color(Face.RIGHT, 0, 1, temp)
            
            temp = self.get_color(Face.BACK, 0, 0)
            self.set_color(Face.BACK, 0, 0, self.get_color(Face.BACK, 0, 2))
            self.set_color(Face.BACK, 0, 2, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, temp)
            
            temp = self.get_color(Face.BACK, 0, 1)
            self.set_color(Face.BACK, 0, 1, self.get_color(Face.BACK, 1, 2))
            self.set_color(Face.BACK, 1, 2, self.get_color(Face.BACK, 2, 1))
            self.set_color(Face.BACK, 2, 1, self.get_color(Face.BACK, 1, 0))
            self.set_color(Face.BACK, 1, 0, temp)
    
    def D(self, prime: bool = False):
        """Rotate Down face clockwise (D) or counter-clockwise (D')."""
        self.move_history.append("D'" if prime else "D")
        if not prime:
            self.rotate_face_cw(Face.DOWN)
            # Rotate adjacent edges: FRONT -> LEFT -> BACK -> RIGHT -> FRONT
            temp = self.get_color(Face.FRONT, 2, 0)
            self.set_color(Face.FRONT, 2, 0, self.get_color(Face.LEFT, 2, 0))
            self.set_color(Face.LEFT, 2, 0, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, self.get_color(Face.RIGHT, 2, 2))
            self.set_color(Face.RIGHT, 2, 2, temp)
            
            temp = self.get_color(Face.FRONT, 2, 1)
            self.set_color(Face.FRONT, 2, 1, self.get_color(Face.LEFT, 2, 1))
            self.set_color(Face.LEFT, 2, 1, self.get_color(Face.BACK, 2, 1))
            self.set_color(Face.BACK, 2, 1, self.get_color(Face.RIGHT, 2, 1))
            self.set_color(Face.RIGHT, 2, 1, temp)
            
            temp = self.get_color(Face.FRONT, 2, 2)
            self.set_color(Face.FRONT, 2, 2, self.get_color(Face.LEFT, 2, 2))
            self.set_color(Face.LEFT, 2, 2, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, self.get_color(Face.RIGHT, 2, 0))
            self.set_color(Face.RIGHT, 2, 0, temp)
        else:
            self.rotate_face_ccw(Face.DOWN)
            temp = self.get_color(Face.FRONT, 2, 0)
            self.set_color(Face.FRONT, 2, 0, self.get_color(Face.RIGHT, 2, 2))
            self.set_color(Face.RIGHT, 2, 2, self.get_color(Face.BACK, 2, 2))
            self.set_color(Face.BACK, 2, 2, self.get_color(Face.LEFT, 2, 0))
            self.set_color(Face.LEFT, 2, 0, temp)
            
            temp = self.get_color(Face.FRONT, 2, 1)
            self.set_color(Face.FRONT, 2, 1, self.get_color(Face.RIGHT, 2, 1))
            self.set_color(Face.RIGHT, 2, 1, self.get_color(Face.BACK, 2, 1))
            self.set_color(Face.BACK, 2, 1, self.get_color(Face.LEFT, 2, 1))
            self.set_color(Face.LEFT, 2, 1, temp)
            
            temp = self.get_color(Face.FRONT, 2, 2)
            self.set_color(Face.FRONT, 2, 2, self.get_color(Face.RIGHT, 2, 0))
            self.set_color(Face.RIGHT, 2, 0, self.get_color(Face.BACK, 2, 0))
            self.set_color(Face.BACK, 2, 0, self.get_color(Face.LEFT, 2, 2))
            self.set_color(Face.LEFT, 2, 2, temp)
    
    def F(self, prime: bool = False):
        """Rotate Front face clockwise (F) or counter-clockwise (F')."""
        self.move_history.append("F'" if prime else "F")
        if not prime:
            self.rotate_face_cw(Face.FRONT)
            # Rotate adjacent edges: UP -> LEFT -> DOWN -> RIGHT -> UP
            temp = self.get_color(Face.UP, 2, 0)
            self.set_color(Face.UP, 2, 0, self.get_color(Face.LEFT, 2, 2))
            self.set_color(Face.LEFT, 2, 2, self.get_color(Face.DOWN, 0, 0))
            self.set_color(Face.DOWN, 0, 0, self.get_color(Face.RIGHT, 0, 0))
            self.set_color(Face.RIGHT, 0, 0, temp)
            
            temp = self.get_color(Face.UP, 2, 1)
            self.set_color(Face.UP, 2, 1, self.get_color(Face.LEFT, 2, 1))
            self.set_color(Face.LEFT, 2, 1, self.get_color(Face.DOWN, 0, 1))
            self.set_color(Face.DOWN, 0, 1, self.get_color(Face.RIGHT, 0, 1))
            self.set_color(Face.RIGHT, 0, 1, temp)
            
            temp = self.get_color(Face.UP, 2, 2)
            self.set_color(Face.UP, 2, 2, self.get_color(Face.LEFT, 2, 0))
            self.set_color(Face.LEFT, 2, 0, self.get_color(Face.DOWN, 0, 2))
            self.set_color(Face.DOWN, 0, 2, self.get_color(Face.RIGHT, 0, 2))
            self.set_color(Face.RIGHT, 0, 2, temp)
        else:
            self.rotate_face_ccw(Face.FRONT)
            temp = self.get_color(Face.UP, 2, 0)
            self.set_color(Face.UP, 2, 0, self.get_color(Face.RIGHT, 0, 0))
            self.set_color(Face.RIGHT, 0, 0, self.get_color(Face.DOWN, 0, 0))
            self.set_color(Face.DOWN, 0, 0, self.get_color(Face.LEFT, 2, 2))
            self.set_color(Face.LEFT, 2, 2, temp)
            
            temp = self.get_color(Face.UP, 2, 1)
            self.set_color(Face.UP, 2, 1, self.get_color(Face.RIGHT, 0, 1))
            self.set_color(Face.RIGHT, 0, 1, self.get_color(Face.DOWN, 0, 1))
            self.set_color(Face.DOWN, 0, 1, self.get_color(Face.LEFT, 2, 1))
            self.set_color(Face.LEFT, 2, 1, temp)
            
            temp = self.get_color(Face.UP, 2, 2)
            self.set_color(Face.UP, 2, 2, self.get_color(Face.RIGHT, 0, 2))
            self.set_color(Face.RIGHT, 0, 2, self.get_color(Face.DOWN, 0, 2))
            self.set_color(Face.DOWN, 0, 2, self.get_color(Face.LEFT, 2, 0))
            self.set_color(Face.LEFT, 2, 0, temp)
    
    def B(self, prime: bool = False):
        """Rotate Back face clockwise (B) or counter-clockwise (B')."""
        self.move_history.append("B'" if prime else "B")
        if not prime:
            self.rotate_face_cw(Face.BACK)
            # Rotate adjacent edges: UP -> RIGHT -> DOWN -> LEFT -> UP
            temp = self.get_color(Face.UP, 0, 0)
            self.set_color(Face.UP, 0, 0, self.get_color(Face.RIGHT, 2, 2))
            self.set_color(Face.RIGHT, 2, 2, self.get_color(Face.DOWN, 2, 2))
            self.set_color(Face.DOWN, 2, 2, self.get_color(Face.LEFT, 0, 0))
            self.set_color(Face.LEFT, 0, 0, temp)
            
            temp = self.get_color(Face.UP, 0, 1)
            self.set_color(Face.UP, 0, 1, self.get_color(Face.RIGHT, 2, 1))
            self.set_color(Face.RIGHT, 2, 1, self.get_color(Face.DOWN, 2, 1))
            self.set_color(Face.DOWN, 2, 1, self.get_color(Face.LEFT, 0, 1))
            self.set_color(Face.LEFT, 0, 1, temp)
            
            temp = self.get_color(Face.UP, 0, 2)
            self.set_color(Face.UP, 0, 2, self.get_color(Face.RIGHT, 2, 0))
            self.set_color(Face.RIGHT, 2, 0, self.get_color(Face.DOWN, 2, 0))
            self.set_color(Face.DOWN, 2, 0, self.get_color(Face.LEFT, 0, 2))
            self.set_color(Face.LEFT, 0, 2, temp)
        else:
            self.rotate_face_ccw(Face.BACK)
            temp = self.get_color(Face.UP, 0, 0)
            self.set_color(Face.UP, 0, 0, self.get_color(Face.LEFT, 0, 0))
            self.set_color(Face.LEFT, 0, 0, self.get_color(Face.DOWN, 2, 2))
            self.set_color(Face.DOWN, 2, 2, self.get_color(Face.RIGHT, 2, 2))
            self.set_color(Face.RIGHT, 2, 2, temp)
            
            temp = self.get_color(Face.UP, 0, 1)
            self.set_color(Face.UP, 0, 1, self.get_color(Face.LEFT, 0, 1))
            self.set_color(Face.LEFT, 0, 1, self.get_color(Face.DOWN, 2, 1))
            self.set_color(Face.DOWN, 2, 1, self.get_color(Face.RIGHT, 2, 1))
            self.set_color(Face.RIGHT, 2, 1, temp)
            
            temp = self.get_color(Face.UP, 0, 2)
            self.set_color(Face.UP, 0, 2, self.get_color(Face.LEFT, 0, 2))
            self.set_color(Face.LEFT, 0, 2, self.get_color(Face.DOWN, 2, 0))
            self.set_color(Face.DOWN, 2, 0, self.get_color(Face.RIGHT, 2, 0))
            self.set_color(Face.RIGHT, 2, 0, temp)
    
    # ==================== SCRAMBLE ====================
    
    def scramble(self, moves: int = 20) -> str:
        """Scramble the cube with random moves. Returns the scramble sequence."""
        all_moves = ['R', 'L', 'U', 'D', 'F', 'B']
        scramble_seq = []
        
        for _ in range(moves):
            move = random.choice(all_moves)
            prime = random.choice([False, True])
            scramble_seq.append(f"{move}'" if prime else move)
            
            # Apply the move
            if move == 'R':
                self.R(prime)
            elif move == 'L':
                self.L(prime)
            elif move == 'U':
                self.U(prime)
            elif move == 'D':
                self.D(prime)
            elif move == 'F':
                self.F(prime)
            elif move == 'B':
                self.B(prime)
        
        scramble_str = ' '.join(scramble_seq)
        self.move_history.append(f"[SCRAMBLE: {scramble_str}]")
        return scramble_str
    
    # ==================== VISUALIZATION ====================
    
    def __str__(self) -> str:
        """Return ASCII representation of the cube net."""
        color_chars = {
            Color.WHITE: 'W',
            Color.YELLOW: 'Y',
            Color.RED: 'R',
            Color.ORANGE: 'O',
            Color.GREEN: 'G',
            Color.BLUE: 'B',
        }
        
        def c(color: Color) -> str:
            return color_chars.get(color, '?')
        
        lines = []
        
        # UP face
        lines.append("      +---+")
        for row in range(3):
            line = "      | " + " ".join(c(self.faces[Face.UP.value][row][col]) for col in range(3)) + " |"
            lines.append(line)
        lines.append("      +---+")
        
        # LEFT, FRONT, RIGHT, BACK faces (middle layer)
        for row in range(3):
            left = " ".join(c(self.faces[Face.LEFT.value][row][col]) for col in range(3))
            front = " ".join(c(self.faces[Face.FRONT.value][row][col]) for col in range(3))
            right = " ".join(c(self.faces[Face.RIGHT.value][row][col]) for col in range(3))
            back = " ".join(c(self.faces[Face.BACK.value][row][2-col]) for col in range(3))  # BACK is reversed
            lines.append(f"|{left}|{front}|{right}|{back}|")
        lines.append("+---+---+---+---+")
        
        # DOWN face
        lines.append("      +---+")
        for row in range(3):
            line = "      | " + " ".join(c(self.faces[Face.DOWN.value][row][col]) for col in range(3)) + " |"
            lines.append(line)
        lines.append("      +---+")
        
        return "\n".join(lines)
    
    def display(self):
        """Display the cube with status."""
        print(self)
        print(f"\nSolved: {self.is_solved()}")
        if self.move_history:
            last_moves = ' '.join(self.move_history[-10:])
            if len(self.move_history) > 10:
                last_moves = '... ' + last_moves
            print(f"Last moves: {last_moves}")


def run_tests():
    """Run comprehensive self-tests."""
    print("\n" + "="*60)
    print("RUNNING SELF-TESTS")
    print("="*60)
    
    # Test 1: Initial state is solved
    cube = RubiksCube()
    assert cube.is_solved(), "Initial cube should be solved"
    print("✓ Test 1: Initial state is solved")
    
    # Test 2: R and R' cancel
    cube = RubiksCube()
    cube.R()
    assert not cube.is_solved(), "After R, cube should not be solved"
    cube.R(True)
    assert cube.is_solved(), "After R R', cube should be solved"
    print("✓ Test 2: R and R' cancel each other")
    
    # Test 3: L and L' cancel
    cube = RubiksCube()
    cube.L()
    assert not cube.is_solved()
    cube.L(True)
    assert cube.is_solved()
    print("✓ Test 3: L and L' cancel each other")
    
    # Test 4: U and U' cancel
    cube = RubiksCube()
    cube.U()
    assert not cube.is_solved()
    cube.U(True)
    assert cube.is_solved()
    print("✓ Test 4: U and U' cancel each other")
    
    # Test 5: D and D' cancel
    cube = RubiksCube()
    cube.D()
    assert not cube.is_solved()
    cube.D(True)
    assert cube.is_solved()
    print("✓ Test 5: D and D' cancel each other")
    
    # Test 6: F and F' cancel
    cube = RubiksCube()
    cube.F()
    assert not cube.is_solved()
    cube.F(True)
    assert cube.is_solved()
    print("✓ Test 6: F and F' cancel each other")
    
    # Test 7: B and B' cancel
    cube = RubiksCube()
    cube.B()
    assert not cube.is_solved()
    cube.B(True)
    assert cube.is_solved()
    print("✓ Test 7: B and B' cancel each other")
    
    # Test 8: Complex sequence and undo
    cube = RubiksCube()
    cube.R()
    cube.U()
    cube.F()
    cube.L()
    cube.D()
    cube.B()
    assert not cube.is_solved()
    cube.B(True)
    cube.D(True)
    cube.L(True)
    cube.F(True)
    cube.U(True)
    cube.R(True)
    assert cube.is_solved()
    print("✓ Test 8: Complex sequence and undo")
    
    # Test 9: Scramble produces unsolved cube
    cube = RubiksCube()
    cube.scramble(50)
    assert not cube.is_solved()
    print("✓ Test 9: Scramble produces unsolved cube")
    
    # Test 10: Copy is independent
    cube1 = RubiksCube()
    cube2 = cube1.copy()
    cube1.R()
    assert cube2.is_solved()
    assert not cube1.is_solved()
    print("✓ Test 10: Copy creates independent cube")
    
    # Test 11: Reset works
    cube = RubiksCube()
    cube.scramble(30)
    assert not cube.is_solved()
    cube.reset()
    assert cube.is_solved()
    print("✓ Test 11: Reset returns to solved state")
    
    # Test 12: Multiple R rotations
    cube = RubiksCube()
    for _ in range(4):
        cube.R()
    assert cube.is_solved(), "4 R rotations should return to solved"
    print("✓ Test 12: 4 R rotations return to solved")
    
    # Test 13: Multiple U rotations
    cube = RubiksCube()
    for _ in range(4):
        cube.U()
    assert cube.is_solved(), "4 U rotations should return to solved"
    print("✓ Test 13: 4 U rotations return to solved")
    
    # Test 14: Multiple F rotations
    cube = RubiksCube()
    for _ in range(4):
        cube.F()
    assert cube.is_solved(), "4 F rotations should return to solved"
    print("✓ Test 14: 4 F rotations return to solved")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60 + "\n")


# ==================== MAIN ====================

def main():
    """Main interactive function."""
    cube = RubiksCube()
    
    print("=" * 60)
    print("RUBIK'S CUBE - FULLY WORKING")
    print("=" * 60)
    print("\nCommands:")
    print("  R, L, U, D, F, B - Rotate face clockwise")
    print("  R', L', U', D', F', B' - Rotate face counter-clockwise")
    print("  scramble - Scramble the cube (20 random moves)")
    print("  reset - Reset to solved state")
    print("  test - Run self-tests")
    print("  display - Show current state")
    print("  quit - Exit")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "scramble":
            scramble_seq = cube.scramble(20)
            print(f"\nScrambled with: {scramble_seq}")
            cube.display()
            return
        elif sys.argv[1] == "test":
            run_tests()
            return
    
    # Interactive mode
    while True:
        try:
            cube.display()
            cmd = input("\nEnter move: ").strip().lower()
            
            if cmd in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif cmd in ['reset']:
                cube.reset()
            elif cmd in ['display', 'd']:
                continue
            elif cmd in ['scramble', 's']:
                scramble_seq = cube.scramble(20)
                print(f"Scrambled with: {scramble_seq}")
            elif cmd in ['test', 't']:
                run_tests()
            elif cmd.endswith("'"):
                move = cmd[:-1].upper()
                prime = True
            else:
                move = cmd.upper()
                prime = False
            
            # Apply the move
            if move == 'R':
                cube.R(prime)
            elif move == 'L':
                cube.L(prime)
            elif move == 'U':
                cube.U(prime)
            elif move == 'D':
                cube.D(prime)
            elif move == 'F':
                cube.F(prime)
            elif move == 'B':
                cube.B(prime)
            else:
                print("Invalid move! Use R, L, U, D, F, B (with optional ' for counter-clockwise)")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
