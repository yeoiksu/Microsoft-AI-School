import pydicom
import matplotlib.pyplot as plt
import numpy as np
from pydicom.pixel_data_handlers.util import apply_modality_lut, apply_voi_lut

file_path = "./2022.12/12.08_d47_image/data/ID_0000_AGE_0060_CONTRAST_1_CT.dcm"
window_center = -600
window_width = 1600

# DICOM 파일 읽는 함수 -> pydicom.read_file(), pydicom.dcmread()
slice = pydicom.read_file(file_path)
print(slice)

s = int(slice.RescaleSlope)
b = int(slice.RescaleIntercept)
image = s * slice.pixel_array + b

plt.subplot(1,3,1)
plt.title("DICOM -> Array")
plt.imshow(image, cmap= 'gray')

slice.WindowCenter = window_center
slice.WindowWidth = window_width
image  = apply_modality_lut(image, slice)
image2 = apply_voi_lut(image, slice)

plt.subplot(1, 3, 2)
plt.title("apply_voi_lut")
plt.imshow(image2, cmap='gray')

# Normalization
image3 = np.clip(image, window_center-(window_width/2),
                 window_center+(window_width/2))
plt.subplot(1,3,3)
plt.title("normalizaition")
plt.imshow(image, cmap= 'gray')
plt.show()

# 참고사항 : https://pydicom.github.io/pydicom/stable/auto_examples/index.html
#           https://pydicom.github.io/pydicom/stable/tutorials/dataset_basics.html