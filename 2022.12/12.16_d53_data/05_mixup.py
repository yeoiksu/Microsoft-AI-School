import requests
import numpy as np
import io
import cv2
import matplotlib.pyplot as plt
from PIL import Image

def get_image_from_url(url):
    response = requests.get(url)
    img_pil = Image.open(io.BytesIO(response.content))

    return np.array(img_pil)

# mixup 함수
def mixup(x1, x2, y1, y2, lamdba_ = 0.7):  # 앞에 70%, 뒤에 30%
    x = lamdba_ * x1 + (1-lamdba_) * x2
    y = lamdba_ * y1 + (1-lamdba_) * y2
    return x, y

# get image from image url
cat_url = "http://s10.favim.com/orig/160416/cute-cat-sleep-omg-Favim.com-4216420.jpeg"
dog_url = "http://s7.favim.com/orig/150714/chien-cute-dog-golden-retriever-Favim.com-2956014.jpg"

cat_img = get_image_from_url(cat_url)
dog_img = get_image_from_url(dog_url)

x, y = mixup(cat_img, dog_img, np.array([1, 0]), np.array([0, 1]))
plt.axis('off')
plt.imshow(x.astype(int)), y
plt.show()

