#!/usr/bin/env python
# coding: utf-8

# Read lena.bmp
from skimage import io
lena = io.imread("lena.bmp")
# io.imshow(lena)
height = len(lena)
width = len(lena[0])
# Binarize
binarized_lena = lena.copy()
for i in range(height):
    for j in range(width):
        if(binarized_lena[i][j] >= 128):
            binarized_lena[i][j] = 1
        else:
            binarized_lena[i][j] = 0

# shrinking lena
shrink_lena = [[]]
for i in range(0, height, 8):
    now = shrink_lena[-1]
    for j in range(0, width, 8):
        if((i % 8 == 0) and (j % 8 == 0)):
            now.append(binarized_lena[i][j])
    shrink_lena.append([])
# print(shrink_lena)

import numpy as np
height = int(height / 8)
width = int(width / 8)
# initialize an array

frame = []
for i in range(height + 2):
    frame.append([])
    for j in range(width + 2):
        frame[-1].append(0)
print(np.array(frame).shape)
# put in a 0, 0 frame
for i in range(height):
    for j in range(width):
        frame[i + 1][j + 1] = shrink_lena[i][j]

def yokoi(f):
    if(f == ['r', 'r', 'r', 'r']):
        return 5
    else:
        return f.count('q')


ans = [[]]
delta_c = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
delta_d = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
delta_e = np.array([[0, 1], [-1, 0], [0, -1], [1, 0]])
for i in range(1, height + 2 - 1):
    for j in range(1, width + 2 - 1):
        if(frame[i][j] == 0):
            print(' ', end = '')
        else:
            f = []
            for d in range(4):
                Type = 'chiu'
                o = np.array([i, j])
                b, c, d, e = o, o + delta_c[d] , o + delta_d[d], o + delta_e[d]
                # print(b, c, d, e)
                b, c, d, e = frame[b[0]][b[1]], frame[c[0]][c[1]], frame[d[0]][d[1]], frame[e[0]][e[1]]
                if(b == c and (d != b or e != b)):
                    Type = 'q'
                elif(b == c):
                    Type = 'r'
                else:
                    Type = 's'
                f.append(Type)
            ans = yokoi(f)
            print(' ' if(ans == 0) else ans, end = '')
    print()
