import cv2

import matplotlib.pyplot as plt

# Read the image using OpenCV
image = cv2.imread('screenie2.png')

# Convert the image from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Plot the image using Matplotlib
plt.imshow(image)
plt.axis('off')
plt.show()