import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import imageio.v2 as imageio
from skimage import morphology
from scipy import ndimage

from k_means import *

filename = "54HC32_RCA_8825_die_120nmpp.jpg"
DOWNSAMPLING = 10
MEDIAN_RADIUS = 12//DOWNSAMPLING
VALUE_THRESHOLD = 220
SAT_THRESHOLD = 0.05
CLOSING_SIZE = 1#5/DOWNSAMPLING

img = imageio.imread(filename)
img = img[::DOWNSAMPLING,::DOWNSAMPLING,:]
X, Y, _ = img.shape
# img = img[:X//2,:Y//2] # for testing uses one quarter of the image for more performance
img_hsv = mpl.colors.rgb_to_hsv(img)

hist, bins = np.histogram(img_hsv[:, :, 1], bins="auto")
plt.plot(bins[:-1], hist)
plt.show()

# At first the program tries to extract the metal layer, but it has a lot of
# grains of dust that appear as black circles
# The method of extraction is using HSV's value, because metal is mostly white
# A median filter is applied here to avoid the dust, but it also loses fine
# traces of the layer, so a not blurred threshold is OR'd to this median

# Metal layer is mostly white, so it has a large value
img_sat = img_hsv[:, :, 1]
img_val = img_hsv[:, :, 2]
# Median filter gets rid of dust particles, but loses resolution
median_img_sat = ndimage.median_filter(img_sat, size=MEDIAN_RADIUS)
median_img_val = ndimage.median_filter(img_val, size=MEDIAN_RADIUS)

# uses threshold to extract metal layer
size = img_val.shape[:2]
v_thres = (img_val > VALUE_THRESHOLD) * np.ones(size, dtype="bool")
s_thres = (img_sat < SAT_THRESHOLD) * np.ones(size, dtype="bool")
v_med_thres = (median_img_val > VALUE_THRESHOLD) * np.ones(size, dtype="bool")
# s_med_thres = (median_img_sat<  SAT_THRESHOLD)*np.ones(size, dtype="bool")

metal = (v_thres & s_thres) | v_med_thres  # & s_med_thres)

plt.imshow(v_thres, cmap="gray")
plt.title("Value threshold")
plt.show()
plt.imshow(s_thres, cmap="gray")
plt.title("Saturation threshold")
plt.show()
plt.imshow(v_med_thres, cmap="gray")
plt.title("Median blur value threshold")
plt.show()
plt.imshow(metal, cmap="gray")
plt.title("Final metal layer")
plt.show()

# The next step uses morphology operators to get a better segmentation

# opening elliminates too small particles
img_closing = morphology.binary_closing(metal, morphology.disk(CLOSING_SIZE))
plt.imshow(img_closing, cmap="gray")
plt.title("After closing")
plt.show()

# comparison of closing with manual translation
ref_filename = "manual_segmentation/54HC32_metal.gif"
ref_img = imageio.imread(ref_filename)
ref_img = ref_img[::DOWNSAMPLING,::DOWNSAMPLING,:]
ref_metal = ref_img[:, :, 0] > 0

plt.imshow(ref_metal, cmap="gray")
plt.show()

# verifies results with reference for true and false positives and negatives
tp = img_closing & ref_metal
tn = np.logical_not(img_closing) & np.logical_not(ref_metal)
fp = img_closing & np.logical_not(ref_metal)
fn = np.logical_not(img_closing) & ref_metal

r_tp = np.sum(tp) / (X * Y)
r_tn = np.sum(tn) / (X * Y)
r_fp = np.sum(fp) / (X * Y)
r_fn = np.sum(fn) / (X * Y)

print(f"True positive:   {100*(r_tp):.2f} %")
print(f"True negative:   {100*(r_tn):.2f} %")
print(f"Correct ratio:   {100*(r_tp+r_tn):.2f} %")
print(f"False positive:  {100*(r_fp):.2f} %")
print(f"False negative:  {100*(r_fn):.2f} %")
print(f"Incorrect ratio: {100*(r_fp+r_fn):.2f} %")

fig, axs = plt.subplots(2, 2)
plt.set_cmap("gray")
axs[0][0].set_title("true positives")
axs[0][0].imshow(tp)
axs[0][1].set_title("true negatives")
axs[0][1].imshow(tn)
axs[1][0].set_title("false positive")
axs[1][0].imshow(fp)
axs[1][1].set_title("false negatives")
axs[1][1].imshow(fn)
plt.show()

# k_mean clustering test
N_CLUSTERS = 5
attr = img_to_atributes(img)
print("k-mean start")
pixels, centroids = k_means(N_CLUSTERS, attr, 2, 1337)
print("k-mean end")
clustered_img = paint_clusters(pixels, centroids)
print("centroids:")
print(centroids)
plt.imshow(clustered_img)
plt.show()
