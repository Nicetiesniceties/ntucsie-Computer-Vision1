#!/usr/bin/env python
# coding: utf-8

# In[22]:
import numpy as np

def yokoi(f):
    if(f == ['r', 'r', 'r', 'r']):
        return 5
    else:
        return f.count('q')


# In[23]:


def yokoi_operator(shrink_lena, height, width):
    frame = []
    for i in range(height + 2):
        frame.append([])
        for j in range(width + 2):
            frame[-1].append(0)
    # print(np.array(frame).shape)
    # put in a 0, 0 frame
    for i in range(height):
        for j in range(width):
            frame[i + 1][j + 1] = shrink_lena[i][j]
    ans = [[]]
    delta_c = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    delta_d = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    delta_e = np.array([[0, 1], [-1, 0], [0, -1], [1, 0]])
    after_yokoi = []
    for i in range(1, height + 2 - 1):
        temp = []
        for j in range(1, width + 2 - 1):
            if(frame[i][j] == 0):
                # print(' ', end = '')
                temp.append(0)
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
                temp.append(ans)
                # print(' ' if(ans == 0) else ans, end = '')
        # print()
        after_yokoi.append(temp)
    return after_yokoi


# In[24]:


def pair_relationship(yokoi_img, height, width):
    frame = np.zeros((height + 2, width + 2), dtype = int)
    ans = np.zeros((height, width), dtype = object)
    for i in range(height):
        for j in range(width):
            frame[i + 1][j + 1] = yokoi_img[i][j]
    for i in range(height):
        for j in range(width):
            if(frame[i + 1][j + 1] == 1):
                if(frame[i + 1 + 1][j + 1] == 1 or
                  frame[i + 1][j + 1 + 1] == 1 or
                  frame[i + 1 - 1][j + 1] == 1 or
                  frame[i + 1][j + 1 - 1] == 1):
                    ans[i][j] = 'p'
            elif(frame[i + 1][j + 1] == 0):
                ans[i][j] = 0
            else:
                ans[i][j] = 'q'
    # print(frame)
    return ans


# In[25]:


## shrink_operator and marked p
'''
neighbor = [
    [[0, 1], [-1, 1], [-1, 0]]
    [[-1, 0], [-1, -1], [0, -1]]
    [[0, -1], [1, -1], [1, 0]]
    [[-1, 0], [1, 1], [0, 1]]
]
'''
def shrinking_operator(paired_img, shrink_lena, height, width):
    frame = np.zeros((66, 66), dtype = object)
    ans = np.zeros((64, 64), dtype = int)
    for i in range(height):
        for j in range(width):
            frame[i + 1][j + 1] = shrink_lena[i][j]
    for i in range(height):
        for j in range(width):
            if(paired_img[i][j] == 'p' and 1 == frame[i + 1][j + 1]):
                a = (1 == frame[i + 1 + 0][j + 1 + 1] and (frame[i + 1 - 1][j + 1 + 1] != 1 or frame[i + 1 - 1][j + 1 + 0] != 1))
                b = (1 == frame[i + 1 - 1][j + 1 + 0] and (frame[i + 1 - 1][j + 1 - 1] != 1 or frame[i + 1 + 0][j + 1 - 1] != 1))
                c = (1 == frame[i + 1 + 0][j + 1 - 1] and (frame[i + 1 + 1][j + 1 - 1] != 1 or frame[i + 1 + 1][j + 1 + 0] != 1))
                d = (1 == frame[i + 1 + 1][j + 1 + 0] and (frame[i + 1 + 1][j + 1 + 1] != 1 or frame[i + 1 + 0][j + 1 + 1] != 1))
                if(int(a) + int(b) + int(c) + int(d) == 1):
                    frame[i + 1][j + 1] = 0
    for i in range(height):
        for j in range(width):
            shrink_lena[i][j]= frame[i + 1][j + 1]
    return shrink_lena
def compare_list(a, b):
    h = len(a)
    w = len(a[0])
    for i in range(h):
        for j in range(w):
            if(a[i][j] != b[i][j]):
                return False
    return True


# In[29]:


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
shrink_lena = []
for i in range(0, height, 8):
    now = []
    for j in range(0, width, 8):
        if((i % 8 == 0) and (j % 8 == 0)):
            now.append(binarized_lena[i][j])
    shrink_lena.append(now)
# print(shrink_lena)

output = np.zeros((64, 64), dtype = int)

for i in range(64):
    for j in range(64):
        if(shrink_lena[i][j] == 1):
            output[i][j] = 255
io.imsave("shrink.png", output)


# In[30]:


from tqdm import tqdm
import numpy as np
height = len(shrink_lena)
width = len(shrink_lena[0])

last_shrink_lena = [[0] * 64] * 64
pbar = tqdm(total=0)
while(1):
    pbar.update(1)
    
    for i in range(height):
        for j in range(width):
            last_shrink_lena[i][j] = shrink_lena[i][j]
            
    after_yokoi = yokoi_operator(shrink_lena, height, width)
    paired = pair_relationship(after_yokoi, height, width)
    shrink_lena = shrinking_operator(paired, shrink_lena, height, width)
    
    output = np.asarray(shrink_lena, dtype = int) * 255
    last_output = io.imread("thinning.png")
    if(np.array_equal(output, last_output)):
        break
    else:
        io.imsave("thinning.png", output)
pbar.close()


# In[ ]:




