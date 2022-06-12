import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import imageio
from skimage import morphology
from scipy import ndimage

filename = "54HC32_RCA_8825_die_120nmpp_4xsmaller.jpg"
MEDIAN_RADIUS = 12
VALUE_THRESHOLD = 220

img = imageio.imread(filename)
X, Y, _ = img.shape
img = img[:X//2,:Y//2] # for testing uses one quarter of the image for more performance
img_hsv = mpl.colors.rgb_to_hsv(img)

hist, bins = np.histogram(img_hsv[:,:,2], bins="auto")
plt.plot(bins[:-1], hist)
plt.show()

# At first the program tries to extract the metal layer, but it has a lot of
# grains of dust that appear as black circles
# The method of extraction is using HSV's value, because metal is mostly white
# A median filter is applied here to avoid the dust, but it also loses fine
# traces of the layer, so a not blurred threshold is OR'd to this median

# Metal layer is mostly white, so it has a large value
img_val = img_hsv[:,:,2]
# Median filter gets rid of dust particles, but loses resolution
median_img_val = ndimage.median_filter(img_val, size=MEDIAN_RADIUS)

# uses threshold to extract metal layer
size = img_val.shape[:2]
v_thres = (img_val>VALUE_THRESHOLD)*np.ones(size, dtype="bool")
median_v_thres = (median_img_val>VALUE_THRESHOLD)*np.ones(size, dtype="bool")
thres_extraction = median_v_thres|v_thres

plt.imshow(v_thres, cmap="gray"); plt.title("value threshold")
plt.show()
plt.imshow(median_v_thres, cmap="gray"); plt.title("median filter value threshold")
plt.show()
plt.imshow(thres_extraction, cmap="gray"); plt.title("OR'd threshold")
plt.show()

# The next step uses morphology operators to get a better segmentation

# opening elliminates too small particles
img_opening = morphology.binary_opening(thres_extraction, morphology.disk(2))
plt.imshow(img_opening, cmap="gray"); plt.title("After opening")
plt.show()
