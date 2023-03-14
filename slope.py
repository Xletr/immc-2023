import numpy as np
import cv2


def divide_image(image, block_width, block_height, start_coordinates):
    # Load the image into memory
    img = cv2.imread(image)

    # Get image dimensions
    rows, cols, _ = img.shape
    binary_img = np.zeros((rows, cols), dtype=np.uint8)
    # Divide the image into blocks
    for i in range(0, rows, block_height):
        for j in range(0, cols, block_width):
            block = img[i:i + block_height, j:j + block_width]

            # Check if block contains white pixels
            if np.any((block[:, :, 0] <= 70) & (block[:, :, 1] <=80 ) & (block[:, :, 2] <= 70)):
                binary_img[i:i + block_height, j:j + block_width] = 0
                img[i:i + block_height, j:j + block_width] = (255, 255, 255)
            elif np.any((block[:, :, 2] > 200) & (block[:, :, 2] < 210) & (block[:, :, 1] > 230) & (block[:, :, 0] > 190) & (block[:, :, 0] < 195)):
                binary_img[i:i + block_height, j:j + block_width] = 1
                img[i:i + block_height, j:j + block_width] = (0, 255, 0)
            elif np.any((block[:, :, 2] > 220) & (block[:, :, 2] < 235) & (block[:, :, 1] > 190) & (block[:, :, 1] < 210) & (block[:, :, 0] > 150) & (block[:, :, 0] < 175)):
                binary_img[i:i + block_height, j:j + block_width] = 1
                img[i:i + block_height, j:j + block_width] = (0, 0, 255)
            else:
                binary_img[i:i + block_height, j:j + block_width] = 0
                img[i:i + block_height, j:j + block_width] = (0, 0, 0)

    # Calculate the distance transform
    dist_transform = cv2.distanceTransform(binary_img, cv2.DIST_L2, 5)

    # Color the starting blocks blue
    for start_x, start_y in start_coordinates:
        x = start_x * block_width
        y = start_y * block_height
        img[y:y + block_height, x:x + block_width] = (255, 0, 0)
    # Keep scanning the neighboring blocks until there are no blue blocks with neighboring black blocks

    while True:
        change_made = False
        for i in range(0, rows, block_height):
            for j in range(0, cols, block_width):
                block = img[i:i + block_height, j:j + block_width]
                if np.all(block == [255, 0, 0]):
                    for dx, dy in [(0, -block_height), (0, block_height), (-block_width, 0), (block_width, 0)]:
                        x = j + dx
                        y = i + dy
                        if x >= 0 and x < cols and y >= 0 and y < rows:
                            neighbor = img[y:y + block_height, x:x + block_width]
                            if np.all(neighbor == [0, 0, 0]) or np.all(neighbor == [0, 255, 0]) or np.all(neighbor == [0, 0, 255]):
                                img[y:y + block_height, x:x + block_width] = (255, 0, 0)
                                change_made = True
        if not change_made:
            break
        # Save the modified image
    cv2.imwrite('slopemap.png', img[::block_height, ::block_width])
    black_blocks = 0
    green_blocks = 0
    red_blocks = 0
    for i in range(0, rows, block_height):
        for j in range(0, cols, block_width):
            block = img[i:i + block_height, j:j + block_width]
            if np.all(block == [0, 0, 0]):
                black_blocks += 1
            if np.all(block == [0, 255, 0]):
                green_blocks += 1
            if np.all(block == [0, 0, 255]):
                red_blocks += 1


    print("Number of black blocks:", black_blocks)
    print("Number of green blocks:", green_blocks)
    print("Number of red blocks:", red_blocks)
    print("Total number of blocks:", (black_blocks+green_blocks+red_blocks))
    return dist_transform

dist_transform = divide_image('slope.png', 20, 20, [(15, 10), (5, 5), (5, 60), (30, 60), (50, 80), (120, 75), (100, 5)])