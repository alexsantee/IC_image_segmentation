# IC_image_segmentation
Automating identification of layers from Integrated Circuit pictures from Project5474

The goal of the project is to automatically identify different layers and electrical components from an integrated circuit picture. These layers are the regions filled with metal, polycristaline silicon, and P or N doped regions. They are used to build components like transistors, resistors and capacitors and then joined to make a complex circuit.

The images are from project5474.org, which contains a large number of high resolution images of simple integrated circuits, like single logic gates. These are some examples of the High Speed CMOS family.

![54HC32](https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/54HC32_RCA_8825_die_120nmpp.jpg/467px-54HC32_RCA_8825_die_120nmpp.jpg)
![54HC00](https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/54HC00_NS_8632_die_120nmpp.jpg/578px-54HC00_NS_8632_die_120nmpp.jpg)
![74HC00](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/74HCT00_RCA_419_die_120nmpp.jpg/482px-74HCT00_RCA_419_die_120nmpp.jpg)
![74HC02](https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/74HC02_Motorola_8302.jpg/629px-74HC02_Motorola_8302.jpg)

For the layer identification, the methods applied are a median filter, in attempt to remove dust present in the images, followed by a threshold, intending to separate and have an initial identification of the layers. In the next step a morphological closing is applied to improve the segmented sections obtained before and allow for a better shape-based layer identification. This has already been applied for the metal layer.

## Usage

Currently the code is divided in two scripts, `metal.py` and ` via.py`, which extracts the desired layer to a folder with it's name. At the beginning of the scripts there are some settings like image filename, number of clusters for k-means and how much to downsample large images. The identification of which k-mean cluster is the desired layer is still manual.

To execute the algorithm first adjust the settings at `metal.py` and execute it, then identify which picture is the metal layer at the `/metal/` folder. The number of the cluster should be used for the settings of `via.py`, which writes it's result at the `/via/` folder.

## First attempts for metal extraction

At first we have tried to extract the metal layer, since it is clearly visible as a bright white through all the image. To extract this bright white we initially used the threshold method in the HSV space, in which white has a low saturation and a high value.

![high_value](/images/value_thres.png)
![low_saturation](/images/sat_thres.png)

However this method had some visible defects because of the black circles which were present in the image (they are present because of dust particles on the lenses during the lithography process). To avoid them we tried a median filter to get a image without the black circles and then used an union operation with the original extraction to not lose details. The results were not that great so we tried a closing operation to eliminate small elements and holes

![median_filter](/images/median_val.png)
![combination](/images/combination.png)
![after_closing](/images/metal_closing.png)

To more precisely evaluate these results we used a manual segmentation of the image and look at where it was right and what it missed.

![reference](/images/reference.png)
![evaluation](/images/evaluation.png)

```
True positive:   20.75 %
True negative:   55.44 %
Correct ratio:   76.19 %
False positive:   0.14 %
False negative:  23.67 %
Incorrect ratio: 23.81 %
```

With this comparison it is possible to see the results were good for the bigger chunks of metal, but it failed to recognize the metal under the wire bondings (which were black) and some smaller layers. Fortunately it has very low false-positives, which could make an electrical connection that shouldn't exist be present.

## K-mean metal extraction

The results using threshold were slow because of the median filter and did not had a very good correct ratio. So we tried a k-means algorithm to see how it would recognize the metal layer, the result were still full of holes so we used a closing operation too. The segmentation was much better.

![kmean_metal](/images/6_cluster_metal.png)
![kmean_metal_eval](/images/6_cluster_metal_evaluation.png)

```
True positive:   27.21 %
True negative:   55.58 %
Correct ratio:   82.79 %
False positive:  0.16 %
False negative:  17.05 %
Incorrect ratio: 17.21 %
```

There was no manual segmentation of other images, but the metal layer extraction looked ok.

![5400_metal](/images/5400_kmean_metal.png)
![7400_metal](/images/7400_kmean_metal.png)

## Flood fill via Extraction

Vias appear as dark rings close inside the metal layer and, since we already got the metal layer, we can use it as a mask to extract the vias. The masked image is then segmented with a k-mean algorithm which can identify the dark regions at the metal layer.

A first try to get the vias is to flood-fill the outside of the image because then only the encircled regions, characteristic of vias, will not get flooded. This set of pixels is then complimented so that vias are 1 and dilated to compensate for border loss during flood fill.

The result is shown in the image below. It is not perfect, but the most visible vias seem to be properly extracted.

![via_floodfill](/images/via_floodfill.png)

