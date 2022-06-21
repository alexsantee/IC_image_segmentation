import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import imageio
from skimage import morphology
from scipy import ndimage

filename = "54HC32_RCA_8825_die_120nmpp_4xsmaller.jpg"
MEDIAN_RADIUS = 12
VALUE_THRESHOLD = 220
SAT_THRESHOLD = 0.05
CLOSING_SIZE = 5

img = imageio.imread(filename)
X, Y, _ = img.shape
#img = img[:X//2,:Y//2] # for testing uses one quarter of the image for more performance
img_hsv = mpl.colors.rgb_to_hsv(img)

hist, bins = np.histogram(img_hsv[:,:,1], bins="auto")
plt.plot(bins[:-1], hist)
plt.show()

# At first the program tries to extract the metal layer, but it has a lot of
# grains of dust that appear as black circles
# The method of extraction is using HSV's value, because metal is mostly white
# A median filter is applied here to avoid the dust, but it also loses fine
# traces of the layer, so a not blurred threshold is OR'd to this median

# Metal layer is mostly white, so it has a large value
img_sat = img_hsv[:,:,1]
img_val = img_hsv[:,:,2]
# Median filter gets rid of dust particles, but loses resolution
median_img_sat = ndimage.median_filter(img_sat, size=MEDIAN_RADIUS)
median_img_val = ndimage.median_filter(img_val, size=MEDIAN_RADIUS)

# uses threshold to extract metal layer
size = img_val.shape[:2]
v_thres     = (img_val>VALUE_THRESHOLD)*np.ones(size, dtype="bool")
s_thres     = (img_sat<  SAT_THRESHOLD)*np.ones(size, dtype="bool")
v_med_thres = (median_img_val>VALUE_THRESHOLD)*np.ones(size, dtype="bool")
#s_med_thres = (median_img_sat<  SAT_THRESHOLD)*np.ones(size, dtype="bool")

metal = (v_thres & s_thres) | v_med_thres# & s_med_thres)

plt.imshow(v_thres, cmap="gray"); plt.title("Value threshold")
plt.show()
plt.imshow(s_thres, cmap="gray"); plt.title("Saturation threshold")
plt.show()
plt.imshow(v_med_thres, cmap="gray"); plt.title("Median blur value threshold")
plt.show()
plt.imshow(metal, cmap="gray"); plt.title("Final metal layer")
plt.show()

# The next step uses morphology operators to get a better segmentation

# opening elliminates too small particles
img_closing = morphology.binary_closing(metal, morphology.disk(CLOSING_SIZE))
plt.imshow(img_closing, cmap="gray"); plt.title("After closing")
plt.show()

# comparison of closing with manual translation
ref_filename = "manual_segmentation/54HC32_metal_4xsmaller.gif"
ref_img = imageio.imread(ref_filename)
ref_metal = (ref_img[:,:,0] > 0)

plt.imshow(ref_metal, cmap="gray")
plt.show()

tp = np.sum(img_closing & ref_metal)/(X*Y)
tn = np.sum(np.logical_not(img_closing) & np.logical_not(ref_metal))/(X*Y)
fp = np.sum(img_closing & np.logical_not(ref_metal))/(X*Y)
fn = np.sum(np.logical_not(img_closing) & ref_metal)/(X*Y)

print("True positive:",  tp)
print("True negative:",  tn)
print("Correct ratio:", tp+tn)
print("False positive:", fp)
print("False negative:", fn)
print("Incorrect ratio:", fp+fn)

