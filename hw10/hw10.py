#!/usr/bin/env python
# coding: utf-8

# In[1]:


from skimage import io
import numpy as np
lena = io.imread('lena.bmp')
height = len(lena)
width = len(lena[0])


# In[2]:


def blank_image(height, width, value):
    temp = np.zeros((height, width), dtype = int)
    return temp + value


# In[19]:


from tqdm import tqdm
import math
def laplace_type1(img, threshold):
    return_img = blank_image(height, width, 255)
    temp = lena.copy()
    gradient = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            gradient[i][j] = temp[i + 1][j] * 1 + temp[i][j - 1] * 1 + temp[i][j + 1] * 1 + temp[i - 1][j] * 1 + temp[i][j] * (-4)  
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            if(gradient[i][j] > threshold):
                return_img[i][j] = 0
    return return_img


def laplace_type2(img, threshold):
    return_img = blank_image(height, width, 255)
    temp = lena.copy()
    gradient = blank_image(height, width, 0)
    io.imshow(gradient)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            gradient[i][j] = (temp[i + 1][j] * 1 + temp[i][j - 1] * 1 + temp[i][j + 1] * 1 + temp[i - 1][j] * 1
                              + temp[i + 1][j + 1] * 1 + temp[i + 1][j - 1] * 1+ temp[i - 1][j + 1] * 1 + temp[i - 1][j - 1] * 1)
            gradient[i][j] -= temp[i][j] * 8
            gradient[i][j] = gradient[i][j] * 1/3
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            if(gradient[i][j] > threshold):
                return_img[i][j] = 0
    return return_img


def minimum_variance_laplacian(img, threshold):
    return_img = blank_image(height, width, 255)
    temp = lena.copy()
    gradient = blank_image(height, width, 255)
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            gradient[i][j] = (temp[i + 1][j] * (-1) + temp[i][j - 1] * (-1) + temp[i][j + 1] * (-1) + temp[i - 1][j] * (-1)
                              + temp[i + 1][j + 1] * 2 + temp[i + 1][j - 1] * 2 + temp[i - 1][j + 1] * 2 + temp[i - 1][j - 1] * 2)
            gradient[i][j] -= temp[i][j] * 4
            gradient[i][j] = gradient[i][j] * 1/3
    for i in tqdm(range(1, height - 1)):
        for j in range(1, width - 1):
            if(gradient[i][j] > threshold):
                return_img[i][j] = 0
    return return_img


def laplacian_of_gaussian(img, threshold):
    return_img = blank_image(height, width, 255)
    temp = lena.copy()
    gradient = blank_image(height, width, 0)
    kernel = [
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0], 
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0], 
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], 
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1], 
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1], 
        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], 
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0], 
    ]
    for i in tqdm(range(5, height - 5)):
        for j in range(5, width - 5):
            for x in range(-5, 6):
                for y in range(-5, 6):
                    gradient[i][j] += temp[i + x][j + y] * kernel[5 + x][5 + y] * 1
    for i in tqdm(range(5, height - 5)):
        for j in range(5, width - 5):
            if(gradient[i][j] > threshold):
                return_img[i][j] = 0
    return return_img

def difference_of_gaussian(img, threshold):
    return_img = blank_image(height, width, 0)
    temp = lena.copy()
    gradient = blank_image(height, width, 0)
    kernel = [
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1], 
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3], 
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4], 
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6], 
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7], 
        [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1], 
    ]
    for i in tqdm(range(5, height - 5)):
        for j in range(5, width - 5):
            for x in range(-5, 6):
                for y in range(-5, 6):
                    gradient[i][j] += temp[i + x][j + y] * kernel[5 + x][5 + y] * 1
    for i in tqdm(range(5, height - 5)):
        for j in range(5, width - 5):
            if(gradient[i][j] > threshold):
                return_img[i][j] = 255
    # get the border white
    for i in range(0, height):
        for j in range(height - 5, height):
            return_img[i][j] = 255
            return_img[j][i] = 255
    for i in range(0, height):
        for j in range(0, 5):
            return_img[i][j] = 255
            return_img[j][i] = 255
    return return_img


# In[20]:


io.imsave("laplace_type1.png", laplace_type1(lena, 15))
io.imsave("laplace_type2.png", laplace_type2(lena, 15))
io.imsave("minimum_variance_laplacian.png", minimum_variance_laplacian(lena, 19))
io.imsave("laplacian_of_gaussian.png", laplacian_of_gaussian(lena, 8000))
io.imsave("difference_of_gaussian.png", difference_of_gaussian(lena, 10000))


# In[ ]:


'''for actually compute the Gaussian distribution
kernel1 = blank_image(11, 11, 0)
    kernel2 = blank_image(11, 11, 0)
    kernel = blank_image(11, 11, 0)
    sum1 = 0
    sum2 = 0
    for i in range(11):
        for j in range(11):
            kernel1[i][j] = (2 * math.pi * 9) * math.exp(-(i ** 2 + j ** 2) / (2 * 9))
            kernel2[i][j] = (2 * math.pi * 1) * math.exp(-(i ** 2 + j ** 2) / (2 * 1))
            sum1 += kernel1[i][j]
            sum2 += kernel2[i][j]
    print(kernel1, kernel2)
    print(sum1, sum2)
    for i in range(11):
        for j in range(11):
            kernel1[i][j] /= sum1
            kernel2[i][j] /= sum2
            print(kernel1[i][j], kernel1[i][j] / sum1)
            kernel[i][j] = kernel2[i][j] - kernel1[i][j]
                       
    print(kernel)
'''

