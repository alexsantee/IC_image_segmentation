import imageio as iio
import numpy as np
import random

def k_means(num_cluster, dataset, iter_num, random_seed):
    # get image shape
    R,X,Y = dataset.shape
    # initializes k_mean pixel clusters
    pixels = np.empty((X,Y), dtype=np.uint8)
    # initializes random centroids
    centroids = np.empty((num_cluster,R), dtype=np.uint8)
    random.seed(random_seed)
    ids = np.sort(random.sample(range(0, X*Y), num_cluster))
    for i,v in enumerate(ids):
        x = v% X
        y = v//X
        centroids[i] = dataset[:,x,y]

    # repeatedly calculates k_means
    distances = np.empty((num_cluster))
    data32 = dataset.astype(np.int32) # bigger integer so that it doesnt explode at square
    for _ in range(iter_num):
        # classifies every pixel
        for i in range(X):
            for j in range(Y):
                # gets distance from centroid
                for idx,val in enumerate(centroids):
                    # converts to uint16 to avoid overflow
                    distances[idx] = np.sum(np.square(data32[:,i,j]-val))
                pixels[i,j] = np.argmin(distances)
        # recalculates centroids
        for i in range(num_cluster):
            k_mask = (pixels == i)
            num_elements = np.sum(k_mask)
            if num_elements > 0:
                for j in range(R):
                    centroids[i,j] = np.sum(k_mask*data32[j,:,:])/num_elements
    return pixels, centroids

### Creates sets of attributes
def img_to_atributes(img):
    X,Y,_ = img.shape
    attr = np.empty((3,X,Y), dtype=np.uint8)
    attr[0] = img[:,:,0]
    attr[1] = img[:,:,1]
    attr[2] = img[:,:,2]
    return attr

### Generates output image
def paint_clusters(clusters, centroids):
    X,Y = clusters.shape
    out_img = np.empty((X,Y,3), dtype=np.uint8)
    for i in range(X):
        for j in range(Y):
            out_img[i,j,:] = centroids[clusters[i,j]]
    return out_img
