import os 
import os.path as osp
import glob

image_path1 = "C:/Users/user/Documents/04.projects/dataset_birds_x/train/images"
image_path2 = "C:/Users/user/Documents/04.projects/dataset_birds_x/valid/images"
img_paths = glob.glob(osp.join(image_path2, "*.png"))

drone, airplane, helicopter, bird, balloon, nothing = 0, 0, 0, 0, 0, 0

for img_path in img_paths:
    if "drone" in img_path:
        drone+=1
    elif "airplane" in img_path:
        airplane+=1
    elif "helicopter" in img_path:
        helicopter+=1
    elif "balloon" in img_path:
        balloon +=1
    elif "bird" in img_path:
        bird +=1
        print(img_path)
    else:
        nothing+=1

print("Total. of images :\t", len(img_paths))
print("No. of drone :\t\t", drone)
print("No. of airplane :\t", airplane)
print("No. of helicopter :\t", helicopter)
print("No. of bird :\t\t", bird)
print("No. of balloon :\t", balloon)
print("No. of nothing :\t", nothing)
print("Total. of images :\t", drone+airplane+helicopter+bird+balloon+nothing)
