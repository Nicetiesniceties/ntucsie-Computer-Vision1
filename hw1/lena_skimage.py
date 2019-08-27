
# coding: utf-8

# In[11]:


from skimage import io
lena = io.imread("lena.bmp")
io.imshow(lena)
lena.shape
print(lena)


# In[12]:


lena_upside_down = lena.copy()[::-1]
io.imshow(lena_upside_down)


# In[13]:


lena_right_side_left = lena.copy()
for i in range(len(lena_right_side_left)):
    lena_right_side_left[i] = lena_right_side_left[i][::-1]
io.imshow(lena_right_side_left)


# In[14]:


lena_diagonally_rotate = lena.copy()
for i in range(len(lena_diagonally_rotate)):
    for j in range(len(lena_diagonally_rotate[i])):
        lena_diagonally_rotate[i][j] = lena[j][i]
io.imshow(lena_diagonally_rotate)


# In[15]:


io.imsave("lena_upside_down.png", lena_upside_down)
io.imsave("lena_right_side_left.png", lena_right_side_left)
io.imsave("lena_diagonally_rotate.png", lena_diagonally_rotate)

