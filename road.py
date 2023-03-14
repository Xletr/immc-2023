import numpy as np
import cv2


def divide_image(image, block_width, block_height):
    img = cv2.imread(image)
    rows, cols, _ = img.shape
    binary_img = np.zeros((rows, cols), dtype=np.uint8)
    for i in range(0, rows, block_height):
        for j in range(0, cols, block_width):
            block = img[i:i + block_height, j:j + block_width]
            if np.any((block[:, :, 0] <= 70) & (block[:, :, 1] <= 80) & (block[:, :, 2] <= 70)):
                binary_img[i:i + block_height, j:j + block_width] = 0
                img[i:i + block_height, j:j + block_width] = (255, 255, 255)
            else:
                binary_img[i:i + block_height, j:j + block_width] = 0
                img[i:i + block_height, j:j + block_width] = (0, 0, 0)

    # Calculate the distance transform
    dist_transform = cv2.distanceTransform(binary_img, cv2.DIST_L2, 5)
    cv2.imwrite('roads.png', img[::block_height, ::block_width])

    return dist_transform


dist_transform = divide_image('slope.png', 20, 20)
