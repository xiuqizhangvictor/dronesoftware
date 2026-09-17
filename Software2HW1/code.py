import cv2
import numpy as np

filename = "OPHANIM.png"
img = cv2.imread(filename) #read image
#this image is a small piece of art I created, its very low pixel, and every single pixel is some sort of red, will be fun to manipulate it
#in real world (oil painting experience) each object may have multiple hues, but I will keep it at a more elementary level here


#------------------------------------------------------------------------------------------------------
#1: get rid of the red, reviewing whats done in class
img[:, :, 2] = 0 #rgb channel
cv2.imwrite("1_nored_RGBchannel.png", img) #outputing the image
#this is way too dark, 

img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Use cv2 codes to convert color spaces
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imwrite("1_nored1_grayscale.png", img_gry) #export grayscale
#Looks exactly the same as removing rgb channel, still wayyy to dark

img_gry_brighter = cv2.add(img_gry, 100) #adds brightness only
cv2.imwrite("1_nored2_grayscale_brighter.png", img_gry_brighter)
img_gry_brighter_better = cv2.convertScaleAbs(img_gry, 1.05, 10) #also changes intensity with formula of 2nd argument times pixel plus third argument
cv2.imwrite("1_nored3_grayscale_brighter_better.png", img_gry_brighter_better)
#Yooo this is kinda tuff

img = cv2.imread(filename)
img_hsv_nored = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy() #to not mess up with following
img_hsv_nored[:, :, 1] = 0 #[row, column, channel], in hsv hue is 0 sat is 1 val is 2, : means all
img_hsv_nored = cv2.cvtColor(img_hsv_nored, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("1_nored4_hsv.png", img_hsv_nored)
#Very interesting, I thought this picture has red only, but apparaently it also has purple
#NONONONONO  cv2 write only understands BGR, so we have to conver it back!!!!!!!!!!!!!!!!!!!!!!!!
#setting saturation to zero looks more red than removing red channel, huh
#------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------
#2: change the whole image to purple hue
img = cv2.imread(filename)
img_hsv_purple = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_purple[:, :, 0] = 150
img_hsv_purple = cv2.cvtColor(img_hsv_purple, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("2_purple.png", img_hsv_purple)

#Numpy is lowkey messing me up in thsi question and the last few
#So lowkey when we create an array and use it, we actually contaignmate the array unless we use .copy()
#the safe solution will be to read the original file again in every question instance, will keep this in mind
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#3: make the whole image brighter
img = cv2.imread(filename)
img_hsv_bright_add = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_bright_add[:, :, 2] += 50
img_hsv_bright_add = cv2.cvtColor(img_hsv_bright_add, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("3_brighterhsv.png", img_hsv_bright_add)
#it is indeed brighter, but some parts just become black?????
#this is called unit 8 overflow so it cycles back
#I used cv2.add to solve that issue since it caps the brightness at 255
img = cv2.imread(filename)
img_hsv_bright_add_fix = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_bright_add_fix[:, :, 2] = cv2.add(img_hsv_bright_add_fix[:, :, 2], 50)
img_hsv_bright_add_fix = cv2.cvtColor(img_hsv_bright_add_fix, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("3_brighterhsv2_fix.png", img_hsv_bright_add_fix)

img = cv2.imread(filename)
img_hsv_bright_mul = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_bright_mul[:, :, 2] = cv2.convertScaleAbs(img_hsv_bright_mul[:, :, 2], alpha=1.5)
img_hsv_bright_mul = cv2.cvtColor(img_hsv_bright_mul, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("3_brighterhsv3_multiply.png", img_hsv_bright_mul)
#why is it all black, oh theres a dsct argument, ill just specify alpha=, beta=
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#4: make the whole image more saturated
img = cv2.imread(filename)
img_hsv_sat_add = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_sat_add[:, :, 1] = cv2.add(img_hsv_sat_add[:, :, 1], 50)
img_hsv_sat_add = cv2.cvtColor(img_hsv_sat_add, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("4_sathsv_add.png", img_hsv_sat_add)

img = cv2.imread(filename)
img_hsv_sat_mul = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
img_hsv_sat_mul[:, :, 1] = cv2.convertScaleAbs(img_hsv_sat_mul[:, :, 1], alpha=1.5)
img_hsv_sat_mul = cv2.cvtColor(img_hsv_sat_mul, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("4_sathsv_mul.png", img_hsv_sat_mul)
#------------------------------------------------------------------------------------------------------


#Masking base on saturation and value
#H: 0–179
#S: 0–255
#V: 0–255

#------------------------------------------------------------------------------------------------------
#5: split the parts that are "Dark enough"
img = cv2.imread(filename)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
#our mask will only be based on hue, and we will export those parts out
dark_mask = cv2.inRange(img_hsv[:, :, 2], 0, 120)
#this only outputs a 255 or 0 mask depends on if the value is in range
img_darkonly = cv2.bitwise_and(img_hsv, img_hsv, mask=dark_mask)
img_darkonly = cv2.cvtColor(img_darkonly, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("5_dark_mask.png", img_darkonly)

#bitwise is actually a cool function, they compare the binary of each pixel to the mask and decide if we leave it or cut it out
#AND: filter
#OR: combine the area
#NOT: reverse the area
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#6: split the parts that are "Red enough"
img = cv2.imread(filename)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
#there will be 2 masks, so bitwise or will be used, we need to ensure a hue value and a saturation value
# red_mask_left = cv2.inRange(img_hsv[:, :, 0], 0, 20)
# red_mask_right =cv2.inRange(img_hsv[:, :, 0], 159, 179)
# red_mask = cv2.bitwise_or(red_mask_left, red_mask_right) #combine the area of the 2 masks

#Apparaently I just use 2 mask for all 3 value in a list [h, s, v]
mask_left = cv2.inRange(img_hsv, np.array([0, 220, 120]), np.array([20, 255, 255]))
mask_right = cv2.inRange(img_hsv, np.array([159, 220, 120]), np.array([179, 255, 255]))
red_mask = cv2.bitwise_or(mask_left, mask_right)
#well list itsef dont work [], I have to add a np.array([]) for it to work
img_redonly = cv2.bitwise_and(img_hsv, img_hsv, mask=red_mask)
img_redonly = cv2.cvtColor(img_redonly, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("6_red_mask.png", img_redonly)
#yay multi dimensional thresholds
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#7:changing its hue base on saturation
img = cv2.imread(filename)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()
#should I use a 2 dimensional for loop to change every single pixel?????
#well chatgpt told me not to, but apparaently numpy can do a mapping on the entire vector
#holy shit thankfully im in linear algebra lmfao
#We are using matrix lol

hue_from_sat = img_hsv.copy()
sat_arr = img_hsv[:, :, 1].copy()
#extract the sat array, ready to convert it into new hue array
mapped_hue_arr = sat_arr.astype(np.float32) * 179//255
#unit8 cannot handle this multiplication, so we change its type to float32

hue_from_sat[:, :, 0] = mapped_hue_arr
#apply the transformed array onto the hue
img_hfs = cv2.cvtColor(hue_from_sat, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("7_hfs.png", img_hfs)
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
#8:changing its hue base on value
#Im not learning any new stuff here but I just want to see the effect now
img = cv2.imread(filename)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()

hue_from_val = img_hsv.copy()
val_arr = img_hsv[:, :, 2].copy()
mapped_hue_arr = val_arr.astype(np.float32) * 179//255
hue_from_val[:, :, 0] = mapped_hue_arr
img_hfv = cv2.cvtColor(hue_from_val, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("8_hfv.png", img_hfv)
#------------------------------------------------------------------------------------------------------

#I am extremly satisfied at this point
#Also very fun how the red eyeball at the bottom left corner is like unchanged

#------------------------------------------------------------------------------------------------------
#9:big challenge, split the object that has a "Clear enough boundary", "Detect and separate regions enclosed by strong boundaries" --chatgpt
#------------------------------------------------------------------------------------------------------
#chat told me to use grayscale to find edges, but nah, I m gona use HSV because if u check the hsv no red and the grayscale no red they are so different
img = cv2.imread(filename)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).copy()

pseudo_gs = img_hsv[:, :, 2].copy()
edges = cv2.Canny(pseudo_gs, 100, 200).copy()
#I dont need to convert this back, since apparaently imwrite understands single channel pictures
cv2.imwrite("9_edgemap.png", edges)

#converting the edges into enclosed areas
contour, hiearchy= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
objects = cv2.drawContours(np.zeros_like(edges), contour, contourIdx=-1, color=255, thickness=cv2.FILLED)
cv2.imwrite("9_objects.png", objects)

#bitwising the mask onto the original
object_only = cv2.bitwise_and(img_hsv, img_hsv, mask=objects)
object_only = cv2.cvtColor(object_only, cv2.COLOR_HSV2BGR).copy()
cv2.imwrite("9_objects2_final.png", object_only)