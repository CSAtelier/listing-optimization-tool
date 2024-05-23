import cv2
from matplotlib import pyplot as plt
img = cv2.imread("/Users/ardagulersoy/Desktop/Daily/listing-optimization-tool/screenie2.png", cv2.IMREAD_COLOR)
print(img.shape)
img = img[1110:1145,620:800]
plt.imshow(img)
plt.show()