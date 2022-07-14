import matplotlib.pyplot as plt
import imageio.v2 as imageio
from skimage import morphology
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

from k_means import *

filename = "54HC32_RCA_8825_die_120nmpp.jpg"
N_CLUSTERS = 5
SUBSET_SIZE=1000
DOWNSAMPLING = 10
CLOSING_SIZE = 20//DOWNSAMPLING

# reading input image
img = imageio.imread(filename)
img = img[::DOWNSAMPLING,::DOWNSAMPLING,:]
X, Y, _ = img.shape

# k_mean clustering
img_2d = np.reshape(img, (X * Y, 3))
subset = shuffle(img_2d, n_samples=SUBSET_SIZE)
kmeans = KMeans(n_clusters=N_CLUSTERS).fit(subset)
labels = kmeans.predict(img_2d)
print(f'{kmeans.cluster_centers_ = }')
clustered_img = kmeans.cluster_centers_[labels].reshape(X, Y, -1) / 255.0
plt.imshow(clustered_img)
plt.show()

# comparison of our extraction with manual translation
ref_filename = "manual_segmentation/54HC32_metal.gif"
ref_img = imageio.imread(ref_filename)
ref_img = ref_img[::DOWNSAMPLING,::DOWNSAMPLING,:]
ref_metal = ref_img[:, :, 0] > 0

labels2d = labels.reshape(X,Y)
for cluster in range(N_CLUSTERS):
    metal = (labels2d == cluster)
    # closing elliminates holes in the set
    metal = morphology.binary_closing(metal, morphology.disk(CLOSING_SIZE))
    plt.imshow(metal, cmap="gray")
    plt.show()

    # verifies results with reference for true and false positives and negatives
    tp = metal & ref_metal
    tn = np.logical_not(metal) & np.logical_not(ref_metal)
    fp = metal & np.logical_not(ref_metal)
    fn = np.logical_not(metal) & ref_metal

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
    print()

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
