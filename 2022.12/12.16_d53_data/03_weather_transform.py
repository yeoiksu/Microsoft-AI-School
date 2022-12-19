import cv2
import random
import albumentations as A

# define a function to visualize the image
def visualize(image):
    cv2.imshow("Visualization", image)
    cv2.waitKey(0)

# load the image from the disk
image = cv2.imread("./2022.12/12.16_d53_data/data/weather.png")

# visualize the original image
# visualize(image)

# random rain
transform = A.Compose([
    # A.RandomRain(brightness_coefficient= 0.7, drop_width= 1, 
    # blur_value= 3, p= 1)  # 비
    # A.RandomSnow(brightness_coeff= 2.5, 
    #     snow_point_lower= 0.1, snow_point_upper= 0.3, p= 1) # 눈
    # A.RandomSunFlare(flare_roi= (0, 0, 1, 0.5), angle_lower= 0.3, p= 1)  #  눈뽕
    # A.RandomShadow(num_shadows_lower= 2, num_shadows_upper= 2,
    #         shadow_dimension= 5,shadow_roi= (0, 0.5, 1, 1) , p= 1)  # 그림자
    A.RandomFog(fog_coef_lower= 0.3, fog_coef_upper= 0.8, alpha_coef= 0.03, p= 1)  # 안개
])
transformed = transform(image= image)
visualize(transformed['image'])