import cv2
import numpy as np

def compare_images(i1, i2):
    i1 = cv2.imread(i1)
    i2 = cv2.imread(i2)
    rows, cols, _ = i1.shape
    result_img = np.zeros((rows, cols, 3), dtype=np.uint8)
    red_pixels = 0
    for i in range(rows):
        for j in range(cols):
            if (i1[i, j] == [0, 255, 0]).all() and (i2[i, j] == [0, 0, 0]).all():
                result_img[i, j] = [0, 0, 255]
                red_pixels += 1
    cv2.imwrite('comparison.png', result_img)
    return red_pixels

red_pixels = compare_images('watermap.png', 'slopemap.png')
print("Number of red pixels:", red_pixels)
