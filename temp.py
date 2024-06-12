import cv2
from matplotlib import pyplot as plt

# Read the image using OpenCV
image = cv2.imread('screenie3.png')

# Convert the image from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = image[645:664,320:398]

plt.imshow(image)
plt.show()