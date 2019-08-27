from skimage import io
lena = io.imread("lena.bmp")

### The first part: Binarizing the image ###
lena_binarized = lena.copy()
for i in range(len(lena_binarized)):
    for j in range(len(lena_binarized[i])):
        if(lena_binarized[i][j] >= 128):
            lena_binarized[i][j] = 255
        else:
            lena_binarized[i][j] = 0
io.imsave("binarized.png", lena_binarized)

### The second part: Calculating the histogram ###
import numpy as np
pix_count = np.zeros((256,), dtype=int)
for i in lena:
    for j in i:
        pix_count[j] += 1
print(list(pix_count))
pix_count = list(pix_count)

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
name = "bar"
plt.bar(range(len(pix_count)), pix_count, color = '#fccf0d', edgecolor='#000000', width=2.0, lw=0.6)
plt.title("Lena hw2-2")
plt.xlabel("Grey level value")
plt.ylabel("Appearing times")
fig = plt.gcf()
plt.savefig(name + '.png', dpi=130)

### The third part: Finding the connected components ###
# bfs
import numpy as np
size, threshold = 512, 500
def valid_range(i, j):
    return (i in range(0, size)) and (j in range(0, size))
def bfs(img, i, j):
    global color, decision_map
    queue, count = [(i, j)], 0
    upper, lower, left, right = 512, -1, 512, -1
    centroid_x, centroid_y = 0, 0
    delta_x, delta_y = [1, 0, -1, 0], [0, 1, 0, -1]
    decision_map[i][j] = color
    while(len(queue) != 0):
        # print(queue)
        # print(decision_map)
        temp = queue.pop()
        x, y = temp[0], temp[1]
        centroid_x += x
        centroid_y += y
        upper, lower, left, right = (
            x if(x < upper) else upper, x if(x > lower) else lower, 
            y if(y < left) else left, y if(y > right) else right
        )
        
        for d in range(4):
            if((valid_range(x + delta_x[d], y + delta_y[d]))
            and (decision_map[x + delta_x[d]][y + delta_y[d]] == 0)
            and (img[x + delta_x[d]][y + delta_y[d]] == img[x][y])):
                queue = [(x + delta_x[d], y + delta_y[d])] + queue
                decision_map[x + delta_x[d]][y + delta_y[d]] = color
        count += 1
    if(count < threshold):
        decision_map[decision_map == color] = -1
        return False
    else:
        color += 10
    return upper, lower, left, right, int(centroid_x / count), int(centroid_y / count)
# finding connected components
img = lena_binarized.copy()
# img = np.array([[0, 255, 0, 255], [0, 255, 0, 255], [0, 255, 255, 255], [0, 255, 0, 0]])
decision_map = np.zeros(img.shape)
bounding_boxes, centroids = [], []
print(decision_map)
color = 1
for i in range(len(img)):
    for j in range(len(img[i])):
        if(decision_map[i][j] == 0):
            temp = bfs(img, i, j)
            if(temp != False):    
                bounding_boxes.append(temp[0:4])
                centroids.append(temp[4:6])
np.save("decision_map.npy", decision_map)
decision_map = np.load("decision_map.npy")
print(decision_map, bounding_boxes, centroids)

# generating image colored by connected components
decision_map[decision_map == -1] = 255
decision_map = decision_map.astype(int)

io.imshow(decision_map)
io.imsave("connected_component.png", 255 - decision_map)
# drawing bounding boxes and centroids
cr = 0
name = "bounding_box_with_centroids"
from skimage.draw import line_aa
bounding_img = 255 - decision_map.copy()
for i in bounding_boxes:
    rr, cc, val= line_aa(i[0], i[2], i[1], i[2])
    bounding_img[rr, cc] = cr * val
    rr, cc, val= line_aa(i[0], i[3], i[1], i[3])
    bounding_img[rr, cc] = cr * val
    rr, cc, val= line_aa(i[0], i[2], i[0], i[3])
    bounding_img[rr, cc] = cr * val
    rr, cc, val= line_aa(i[1], i[2], i[1], i[3])
    bounding_img[rr, cc] = cr * val
io.imsave(name + ".png", bounding_img)

from skimage.draw import circle
bounding_img = io.imread(name + ".png")
for i in centroids:
    rr, cc = circle(i[0], i[1], 5)
    bounding_img[rr, cc] = cr
io.imsave(name + ".png", bounding_img)

