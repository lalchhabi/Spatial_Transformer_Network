# from PIL import Image
# import glob


# image_list = []
# resized_list = []

# for filename in glob.glob("/home/chhabilal/Desktop/treeleaf/OCR_project/Spatial_Transformer_Networks/aligned_images/*.png"):
#     img = Image.open(filename)
#     image_list.append(img)
#     print(len(filename))
# # for image in image_list:
# #     image = image.resize((1024,768))
# #     resized_list.append(image)


# # for(i,new) in enumerate(resized_list):
# #     new.save('{}{}{}'.format("/home/chhabilal/Desktop/treeleaf/OCR_project/Spatial_Transformer_Networks/resized_images",i+1,".jpg"))



###### 2

from tokenize import Imagnumber
import cv2
import glob
import os

inputFolder = 'aligned_images'
os.mkdir('Resized Folder')

i = 1
for img in glob.glob(inputFolder + "/*.jpg"):
    image = cv2.imread(img)
    imgResized = cv2.resize(image, (1024, 768))
    cv2.imwrite("Resized Folder/%i.jpg" %1, imgResized )

    i +=1
    cv2.waitKey(10)

cv2.destroyAllWindows()
