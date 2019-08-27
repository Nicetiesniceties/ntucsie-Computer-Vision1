# Computer Vision Homework #1

> B05902019 資工三 蔡青邑

The following picture might be resized when showed in pdf file, so their original image files were attahced to my folder by me.





|                            Part 1                            |                            Part 2                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
|                         upside down                          |                         45$^o$rotate                         |
| ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/lena_upside_down.png) | ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/rotate.bmp) |
|                       right side left                        |                          shrink in                           |
| ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/lena_right_side_left.png) | ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/shrink.png) |
|                      diagonally rotate                       |                       binarized at 128                       |
| ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/lena_diagonally_rotate.png) | ![lena_upside_down](/Users/Njceties/Secrets/NTU Courses/NTU fifth semester/Computer Vision I/hw/hw1/binarize.bmp) |

# The code and methods I used

## Part 1: Python skimage library

> In this part , I dealt with `lena.bmp` by using `skimage.io` and make it subscriptable as a two dimensional-list. By doing so, the work for editing pixels is easy for `Python`'s certain syntax such as `:`, `[]` , and `for`.

```python
from skimage import io
# reading file
lena = io.imread("lena.bmp")
io.imshow(lena)
lena.shape
print(lena)
# upside down
lena_upside_down = lena.copy()[::-1]
io.imshow(lena_upside_down)
# right side left
lena_right_side_left = lena.copy()
for i in range(len(lena_right_side_left)):
    lena_right_side_left[i] = lena_right_side_left[i][::-1]
io.imshow(lena_right_side_left)
# diagonally rotate
lena_diagonally_rotate = lena.copy()
for i in range(len(lena_diagonally_rotate)):
    for j in range(len(lena_diagonally_rotate[i])):
        lena_diagonally_rotate[i][j] = lena[j][i]
io.imshow(lena_diagonally_rotate)
# save
io.imsave("lena_upside_down.png", lena_upside_down)
io.imsave("lena_right_side_left.png", lena_right_side_left)
io.imsave("lena_diagonally_rotate.png", lena_diagonally_rotate)
```

<div style="page-break-after: always;"></div>

## Part 2: Photoshop

> 這部分的圖都要先把圖片複製到一個新的ps檔案上才能開始編輯，否則圖層會被鎖住不能動。

### 45$^0$rotate 

`影像` > `影像旋轉` > `任意` > 改成45度即可

### Shrink In

`影像` > `影像尺寸` > 把尺寸都調成256

###  Binarize at 128

1. `影像` > `模式` > `灰階`

2. `影像` > `調整` > `臨界值` > 調成128