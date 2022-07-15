import matplotlib.pyplot as plt
import imageio.v2 as imageio
from skimage import morphology
from skimage.segmentation import flood_fill
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

from k_means import *

filename = "54HC32_RCA_8825_die_120nmpp.jpg"
metal_indexes = (4,) # which images generated from metal.py to use
N_CLUSTERS = 3
SUBSET_SIZE=1000
DOWNSAMPLING = 4
METAL_DILATION_SIZE = 10//DOWNSAMPLING
VIA_DILATION_SIZE   = 10//DOWNSAMPLING

# reading input image
img = imageio.imread(filename)
img  =  img[::DOWNSAMPLING,::DOWNSAMPLING,:]
X, Y, _ = img.shape
# reading metal masks
mask = np.zeros((X,Y), dtype=np.bool8)
for i in metal_indexes:
    mask = np.logical_or(mask, imageio.imread(f"metal/{i}.gif"))

# use dilation as margin of error for metal
mask = morphology.binary_dilation(mask, morphology.disk(METAL_DILATION_SIZE))
# apply metal as mask (every via is below metal)
mask = np.reshape(np.repeat(mask, 3), (X,Y,3))
img = img*(mask > 0)

# k_mean clustering
img_2d = np.reshape(img, (X * Y, 3))
subset = shuffle(img_2d, n_samples=SUBSET_SIZE)
kmeans = KMeans(n_clusters=N_CLUSTERS).fit(subset)
labels = kmeans.predict(img_2d)
print(f'{kmeans.cluster_centers_ = }')
clustered_img = kmeans.cluster_centers_[labels].reshape(X, Y, -1) / 255.0
plt.imshow(clustered_img)
plt.show()

labels2d = labels.reshape(X,Y)
for cluster in range(N_CLUSTERS):
    via = (labels2d == cluster)

    plt.imshow(via, cmap="gray")
    plt.show()
    # flood fill to get just covered regions
    via = flood_fill(via, (0,0), True)
    via = np.logical_not(via)
    # dilation to recover lost area of contour from flood_fill
    via = morphology.binary_dilation(via, morphology.disk(VIA_DILATION_SIZE))
    imageio.imwrite(f"via/{cluster}.gif", 255*via.astype(np.uint8))
