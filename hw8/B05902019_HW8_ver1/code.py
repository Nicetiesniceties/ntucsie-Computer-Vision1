#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Read lena.bmp
from skimage import io
lena = io.imread("lena.bmp")
# io.imshow(lena)
height = len(lena)
width = len(lena[0])


# In[27]:


# start noising
import numpy as np
grayImg = lena.copy()
img_Gaul10 = np.zeros(grayImg.shape, dtype=int)
img_Gaul30 = np.zeros(grayImg.shape, dtype=int)
img_Salt005 = np.zeros(grayImg.shape, dtype=int)
img_Salt01 = np.zeros(grayImg.shape, dtype=int)

for i in range(height):
    for j in range(width):
        img_Gaul10[i, j] = grayImg[i, j] + 10 * np.random.normal(0.0, 1.0, None)
        img_Gaul30[i, j] = grayImg[i, j] + 30 * np.random.normal(0.0, 1.0, None)
        if(np.random.uniform(0., 1., None) < 0.05):
            img_Salt005[i, j] = 0
        elif(np.random.uniform(0., 1., None) > 1 - 0.05):
            img_Salt005[i, j] = 255
        else:
            img_Salt005[i, j] = grayImg[i, j]
        if(np.random.uniform(0., 1., None) < 0.1):
            img_Salt01[i, j] = 0
        elif(np.random.uniform(0., 1., None) > 1 - 0.1):
            img_Salt01[i, j] = 255
        else:
            img_Salt01[i, j] = grayImg[i, j]
img_Gaul10 = np.clip(img_Gaul10, 0, 255)
img_Gaul30 = np.clip(img_Gaul30, 0, 255)
io.imsave("lena_Gaul30.png", img_Gaul30)
io.imsave("lena_Gaul10.png", img_Gaul10)
io.imsave("lena_Salt005.png", img_Salt005)
io.imsave("lena_Salt01.png", img_Salt01)
# io.imshow(img_Gaul30)


# In[69]:


from tqdm import tqdm
filter33 = np.array([[1, 1], [0, 0], [1, 0], [0, 1], [-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1]] )
filter55 = np.array([[1, 1], [0, 0], [1, 0], [0, 1], [-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1], 
            [1, 2], [1, -2], [0, 2], [0, -2], [-1, 2], [-1, -2], [2, 2], [2, -2], [-2, 2], [-2, -2], 
            [-2, -1], [-2, 1], [-2, 0], [2, 0], [2, -1], [2, 1]] )
# box filter
print(height, width)
def box_filter(img, filterxx):
    temp = img.copy()
    for i in tqdm(range(height)):
        for j in range(width):
            filter_applied = [i, j] + filterxx
            # print(filter_applied)
            SUM = 0
            count = 0
            out_of_range = False
            for x, y in filter_applied:
                if((x in range(0, height)) and (y in range(0, width))):
                    SUM += temp[x][y]
                    count += 1
                else:
                    out_of_range = True
                    break
            if not out_of_range:
                temp[i][j] = SUM / count
    return temp
io.imsave("box_filter3X3_on_Gaul10.png", box_filter(img_Gaul10, filter33))
io.imsave("box_filter3X3_on_Gaul30.png", box_filter(img_Gaul30, filter33))
io.imsave("box_filter3X3_on_Salt005.png", box_filter(img_Salt005, filter33))
io.imsave("box_filter3X3_on_Salt01.png", box_filter(img_Salt01, filter33))

io.imsave("box_filter5X5_on_Gaul10.png", box_filter(img_Gaul10, filter55))
io.imsave("box_filter5X5_on_Gaul30.png", box_filter(img_Gaul30, filter55))
io.imsave("box_filter5X5_on_Salt005.png", box_filter(img_Salt005, filter55))
io.imsave("box_filter5X5_on_Salt01.png", box_filter(img_Salt01, filter55))


# In[70]:


def median(x):
    x = sorted(x)
    listlength = len(x) 
    num = round(listlength / 2)
    middlenum = x[num]
    return middlenum
# median filter
def median_filter(img, filterxx):
    temp = img.copy()
    for i in tqdm(range(height)):
        for j in range(width):
            filter_applied = [i, j] + filterxx
            # print(filter_applied)
            SUM = []
            out_of_range = False
            for x, y in filter_applied:
                if((x in range(0, height)) and (y in range(0, width))):
                    SUM.append(temp[x][y])
                else:
                    out_of_range = True
                    break
            if not out_of_range:
                temp[i][j] = int(median(SUM))
    return temp
io.imsave("median_filter3X3_on_Gaul10.png", median_filter(img_Gaul10, filter33))
io.imsave("median_filter3X3_on_Gaul30.png", median_filter(img_Gaul30, filter33))
io.imsave("median_filter3X3_on_Salt005.png", median_filter(img_Salt005, filter33))
io.imsave("median_filter3X3_on_Salt01.png", median_filter(img_Salt01, filter33))

io.imsave("median_filter5X5_on_Gaul10.png", median_filter(img_Gaul10, filter55))
io.imsave("median_filter5X5_on_Gaul30.png", median_filter(img_Gaul30, filter55))
io.imsave("median_filter5X5_on_Salt005.png", median_filter(img_Salt005, filter55))
io.imsave("median_filter5X5_on_Salt01.png", median_filter(img_Salt01, filter55))


# In[71]:


def blank_image(height, width):
	return np.array([[0 for i in range(width)] for j in range(height)])
def dilation(img, kernel):
	print("---dilation start---")
	return_img = blank_image(height, width)
	for i in tqdm(range(height)):
		for j in range(width):
			temp_max = 0
			for x, y in kernel:
				if((i - x) in range(0, width) and (j - y) in range(0, height)):
					temp = img[i - x][j - y] + kernel_value(x, y)
					if(temp >= temp_max):
						temp_max = temp
			return_img[i][j] = temp_max
	print("---dilation end---")
	return(return_img)
def erosion(img, kernel):
	return_img = blank_image(height, width)
	print("---erosion start---")
	for i in tqdm(range(height)):
		for j in range(width):
			temp_min = 255
			for x, y in kernel:
				if((i + x) in range(0, width) and (j + y) in range(0, height)):
					temp = img[i + x][j + y] - kernel_value(x, y)
					if(temp <= temp_min):
						temp_min = temp
			return_img[i][j] = temp_min
	print("---erosion end---")
	return return_img
def opening(img, kernel):
	temp = erosion(img, kernel)
	temp = dilation(temp, kernel)
	return temp
def closing(img, kernel):
	temp = dilation(img, kernel)
	temp = erosion(temp, kernel)
	return temp
def opening_then_closing(img, kernel):
    temp = opening(img, kernel)
    temp = closing(img, kernel)
    return temp
def closing_then_opening(img, kernel):
    temp = closing(img, kernel)
    temp = opening(img, kernel)
    return temp
def kernel_value(x, y):
	# for this task, the kernel values are always 0
	return 0


# In[16]:


import numpy as np
kernel = np.array([  [0, 0], [0, 1], [0, 2], [0, -1], [0, -2], [1, 0], 
		  [1, 1], [1, 2], [1, -1], [1, -2],  [-1, 0], [-1, 1], 
		  [-1, 2], [-1, -1], [-1, -2], [2, 0], [2, 1], [2, -1],  
		  [-2, 0], [-2, 1], [-2, -1] ])

io.imsave("opening_then_closing_on_Gaul10.png", opening_then_closing(img_Gaul10, kernel))
io.imsave("opening_then_closing_on_Gaul30.png", opening_then_closing(img_Gaul30, kernel))
io.imsave("opening_then_closing_on_Salt005.png", opening_then_closing(img_Salt005, kernel))
io.imsave("opening_then_closing_on_Salt01.png", opening_then_closing(img_Salt01, kernel))

io.imsave("closing_then_opening_on_Gaul10.png", closing_then_opening(img_Gaul10, kernel))
io.imsave("closing_then_opening_on_Gaul30.png", closing_then_opening(img_Gaul30, kernel))
io.imsave("closing_then_opening_on_Salt005.png", closing_then_opening(img_Salt005, kernel))
io.imsave("closing_then_opening_on_Salt01.png", closing_then_opening(img_Salt01, kernel))


# In[104]:


from skimage import io
import numpy as np
import os
import math
lena = io.imread('lena.bmp')
namelist = os.listdir(".")
mu = np.sum(lena) / lena.size
VS = np.sum(np.power(lena - mu, 2)) / lena.size
print('mu =', mu, ', VS =', VS)
for i in namelist:
    if(not '.png' in i):
        continue
    temp = io.imread(i)
    mu_N = np.sum(temp - lena) / temp.size
    VN = np.sum(np.power(temp - lena - mu_N, 2)) / temp.size
    # print(temp - lena - mu_N)
    SNR = 20 * math.log10(math.sqrt(VS) / math.sqrt(VN))
    print(i, mu_N, VN, SNR)


# In[111]:


# ![SNR](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw8/SNR.png)
from skimage import io
import numpy as np
import os
import math
lena = io.imread('lena.bmp')
namelist = os.listdir(".")
for i in namelist:
    if(not '.png' in i):
        continue
    print(i)
    print("![](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw8/" + i + ")\n")
    print("<div style="page-break-after: always;"></div>")


# ![SNR](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw8/SNR.png)
