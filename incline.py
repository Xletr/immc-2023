import numpy as np
import cv2


def divide_image(image, block_width, block_height, start_x, start_y):
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
            block_pixels = block.shape[0] * block.shape[1]
            red_pixels = np.sum((block[:, :, 0] > 20) & (block[:, :, 0] > 35) & (block[:, :, 1] > 90) & (block[:, :, 1] < 110) & (block[:, :, 2] > 160) & (block[:, :, 2] < 180))
            orange_pixels = np.sum((block[:, :, 0] > 160) & (block[:, :, 0] < 180) & (block[:, :, 1] > 190) & (block[:, :, 1] < 210) & (block[:, :, 2] > 220) & (block[:, :, 2] < 240))
            # red
            if red_pixels/block_pixels >= 0.001:
                binary_img[i:i + block_height, j:j + block_width] = 1
                img[i:i + block_height, j:j + block_width] = (0, 255, 0)
            # orange
            elif orange_pixels/block_pixels >= 0.001:
                binary_img[i:i + block_height, j:j + block_width] = 1
                img[i:i + block_height, j:j + block_width] = (0, 0, 255)
            else:
                binary_img[i:i + block_height, j:j + block_width] = 0
                img[i:i + block_height, j:j + block_width] = (0, 0, 0)

    # Calculate the distance transform
    dist_transform = cv2.distanceTransform(binary_img, cv2.DIST_L2, 5)

    # Save the modified image
    # Color the starting block blue
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
                            if np.all(neighbor == [0, 0, 0]):
                                img[y:y + block_height, x:x + block_width] = (255, 0, 0)
                                change_made = True
        if not change_made:
            break
    cv2.imwrite('inclinemap.jpg', img)
    return dist_transform


# Example usage
dist_transform = divide_image('incline.jpg', 40, 40, 5, 5)
