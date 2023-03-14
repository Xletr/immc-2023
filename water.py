import numpy as np
import cv2
import concurrent.futures


def divide_image_block(img, block_width, block_height, binary_img, i, j):
    rows, cols, _ = img.shape
    block = img[i:i + block_height, j:j + block_width]
    if np.any((block[:, :, 0] > 220) & (block[:, :, 1] > 220) & (block[:, :, 2] > 220)):
        binary_img[i:i + block_height, j:j + block_width] = 0
        img[i:i + block_height, j:j + block_width] = (255, 255, 255)
    elif np.any((block[:, :, 0] > 180) & (block[:, :, 2] < 120)):
        binary_img[i:i + block_height, j:j + block_width] = 1
        img[i:i + block_height, j:j + block_width] = (0, 255, 0)
        for i_offset in range(-9, 10):
            for j_offset in range(-9, 10):
                i_new = i + i_offset * block_height
                j_new = j + j_offset * block_width
                if i_new >= 0 and i_new + block_height <= rows and j_new >= 0 and j_new + block_width <= cols:
                    block_new = img[i_new:i_new + block_height, j_new:j_new + block_width]
                    if np.all(block_new == [0, 0, 0]):
                        img[i_new:i_new + block_height, j_new:j_new + block_width] = (0, 255, 0)
    else:
        binary_img[i:i + block_height, j:j + block_width] = 0
        img[i:i + block_height, j:j + block_width] = (0, 0, 0)


def divide_image(image, block_width, block_height, start_coordinates):
    img = cv2.imread(image)
    rows, cols, _ = img.shape
    binary_img = np.zeros((rows, cols), dtype=np.uint8)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(divide_image_block, img, block_width, block_height, binary_img, i, j)
                   for i in range(0, rows, block_height) for j in range(0, cols, block_width)]
        concurrent.futures.wait(futures)

    dist_transform = cv2.distanceTransform(binary_img, cv2.DIST_L2, 5)

    for start_x, start_y in start_coordinates:
        x = start_x * block_width
        y = start_y * block_height
        img[y:y + block_height, x:x + block_width] = (255, 0, 0)

    while True:
        change_made = False
        for i in range(0, rows, block_height):
            for j in range(0, cols, block_width):
                block = img[i:i + block_height, j:j + block_width]
                if np.all(block == [255, 0, 0]):
                    for dx, dy in [(0, -block_height), (0, block_height), (-block_width, 0), (block_width, 0)]:
                        x = j + dx
                        y = i + dy
                        if 0 <= x < cols and 0 <= y < rows:
                            neighbor = img[y:y + block_height, x:x + block_width]
                            if np.all(neighbor == [0, 0, 0]) or np.all(neighbor == [0, 255, 0]):
                                img[y:y + block_height, x:x + block_width] = (255, 0, 0)
                                change_made = True
        if not change_made:
            break

    cv2.imwrite('watermap.png', img[::block_height, ::block_width])

    return dist_transform


dist_transform = divide_image('water.jpg', 20, 20, [(5, 5), (5, 50), (20, 50), (60, 84), (128, 75), (120, 5), (20, 5)])
