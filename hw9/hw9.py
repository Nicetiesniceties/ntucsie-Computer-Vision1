#!/usr/bin/env python
# coding: utf-8

# In[6]:


from skimage import io
import numpy as np
lena = io.imread('lena.bmp')
height = len(lena)
width = len(lena[0])


# In[17]:


def blank_image(height, width, value):
    temp = np.zeros((height, width), dtype = int)
    return temp + value


# In[48]:


from tqdm import tqdm
import math
def robert(img, threshold):
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(height - 1)):
        for j in range(width - 1):
            r1 = img[i][j] * (-1) + img[i + 1][j + 1] * 1
            r2 = img[i + 1][j] * 1 + img[i][j + 1] * (-1)
            r = r1 ** 2 + r2 ** 2
            if(r > threshold ** 2):
                return_img[i][j] = 0
    return return_img
def prewitt(img, threshold):
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            p1 = img[i - 1][j - 1] * (-1) + img[i - 1][j] * (-1) + img[i - 1][j + 1] * (-1) + img[i + 1][j - 1] + img[i + 1][j] + img[i + 1][j + 1]
            p2 = img[i - 1][j - 1] * (-1) + img[i][j - 1] * (-1) + img[i + 1][j - 1] * (-1) + img[i - 1][j + 1] + img[i][j + 1] + img[i + 1][j + 1]
            p = p1 ** 2 + p2 ** 2
            if(p > threshold ** 2):
                return_img[i][j] = 0
    return return_img
def sobel(img, threshold):
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            s1 = img[i - 1][j - 1] * (-1) + img[i - 1][j] * (-2) + img[i - 1][j + 1] * (-1) + img[i + 1][j - 1] + img[i + 1][j] * 2 + img[i + 1][j + 1]
            s2 = img[i - 1][j - 1] * (-1) + img[i][j - 1] * (-2) + img[i + 1][j - 1] * (-1) + img[i - 1][j + 1] + img[i][j + 1] * 2 + img[i + 1][j + 1]
            s = s1 ** 2 + s2 ** 2
            if(s > threshold ** 2):
                return_img[i][j] = 0
    return return_img
def frei_and_chen(img, threshold):
    return_img = blank_image(height, width, 255)
    sqrt = math.sqrt(2)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            f1 = img[i - 1][j - 1] * (-1) + img[i - 1][j] * (-sqrt) + img[i - 1][j + 1] * (-1) + img[i + 1][j - 1] + img[i + 1][j] * sqrt + img[i + 1][j + 1]
            f2 = img[i - 1][j - 1] * (-1) + img[i][j - 1] * (-sqrt) + img[i + 1][j - 1] * (-1) + img[i - 1][j + 1] + img[i][j + 1] * sqrt + img[i + 1][j + 1]
            f = f1 ** 2 +f2 ** 2
            if(f > threshold ** 2):
                return_img[i][j] = 0
    return return_img
def kirsch(img, threshold):
    k = [-3, -3, -3,-3, -3, 5, 5, 5]
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            k_list = []
            for idx in range(8):
                k_list.append(img[i - 1][j - 1] * k[idx % 8] + img[i - 1][j] * k[(idx + 1) % 8] + img[i - 1][j + 1] * k[(idx + 2) % 8]
                    + img[i][j + 1] * k[(idx + 3) % 8] + img[i + 1][j + 1] * k[(idx + 4) % 8]
                    + img[i + 1][j] * k[(idx + 5) % 8] + img[i + 1][j - 1] * k[(idx + 6) % 8] + img[i][j - 1] * k[(idx + 7) % 8])
            if(max(k_list) > threshold):
                return_img[i][j] = 0
    return return_img
def robinson(img, threshold):
    r = [-1, 0, 1, 2, 1, 0, -1, -2]
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            r_list = []
            for idx in range(8):
                r_list.append(img[i - 1][j - 1] * r[idx % 8] + img[i - 1][j] * r[(idx + 1) % 8] + img[i - 1][j + 1] * r[(idx + 2) % 8]
                    + img[i][j + 1] * r[(idx + 3) % 8] + img[i + 1][j + 1] * r[(idx + 4) % 8]
                    + img[i + 1][j] * r[(idx + 5) % 8] + img[i + 1][j - 1] * r[(idx + 6) % 8] + img[i][j - 1] * r[(idx + 7) % 8])
            if(max(r_list) > threshold):
                return_img[i][j] = 0
    return return_img
def nevatia_babu(img, threshold):
    kernel = [ [-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2],
    [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1],
    [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0],
    [-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1],
    [-2, 2], [-1, 2], [0, 2], [1, 2], [2, 2] ] 
    g0 = [ 100, 100, 0, -100, -100, 100, 100, 0, -100, -100, 100, 100, 0, -100, -100, 100, 100, 0, -100, -100, 100, 100, 0, -100, -100]
    g1 = [ 100, 100, 100, 100, 100, 100, 100, 100, 78, -32, 100, 92, 0, -92, -100, 32, -78, -100, -100, -100, -100, -100, -100, -100, -100]
    g2 = [-100, -100, -100, -100, -100, 32, -78, -100, -100, -100, 100, 92, 0, -92, -100, 100, 100, 100, 78, -32, 100, 100, 100, 100, 100]
    g3 = [ 100, 100, 100, 32, -100, 100, 100, 92, -78, -100, 100, 100, 0, -100, -100, 100, 78, -92, -100, -100, 100, -32, -100, -100, -100]
    g4 = [ -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    g5 = [ 100, -32, -100, -100, -100, 100, 78, -92, -100, -100, 100, 100, 0, -100, -100, 100, 100, 92, -78, -100, 100, 100, 100, 32, -100]
    g = [g0, g1, g2, g3, g4, g5]
    return_img = blank_image(height, width, 255)
    for i in tqdm(range(2, height - 2)):
        for j in range(2, width - 2):
            g_list = []
            for g_idx in range(6):
                temp = 0
                for idx in range(25):
                    temp += img[i + kernel[idx][0]][j + kernel[idx][1]] * g[g_idx][idx]
                g_list.append(temp)
            if(max(g_list) > threshold):
                return_img[i][j] = 0
    return return_img


# In[49]:


io.imsave("robert.png", robert(lena, 12))
io.imsave("prewitt.png", prewitt(lena, 24))
io.imsave("sobel.png", sobel(lena, 38))
io.imsave("frei_and_chen.png", frei_and_chen(lena, 30))
io.imsave("kirsch.png", kirsch(lena, 135))
io.imsave("robinson.png", robinson(lena, 43))
io.imsave("nevatia_babu.png", nevatia_babu(lena, 12500))
