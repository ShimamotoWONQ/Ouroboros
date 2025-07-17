#!/usr/bin/env python3

class Matrix:
    """Simple matrix implementation for 2D arrays"""
    def __init__(self, rows, cols, elements=None):
        self.rows = rows
        self.cols = cols
        if elements:
            self.data = elements[:rows * cols]
        else:
            self.data = [0] * (rows * cols)
    
    def __getitem__(self, row):
        return MatrixRow(self, row)
    
    def __setitem__(self, row, value):
        start = row * self.cols
        end = start + self.cols
        self.data[start:end] = value[:self.cols]

class MatrixRow:
    """Row accessor for Matrix"""
    def __init__(self, matrix, row):
        self.matrix = matrix
        self.row = row
    
    def __getitem__(self, col):
        return self.matrix.data[self.row * self.matrix.cols + col]
    
    def __setitem__(self, col, value):
        self.matrix.data[self.row * self.matrix.cols + col] = value