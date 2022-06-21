# IC_image_segmentation
Automating identification of layers from Integrated Circuit pictures from Project5474

The goal of the project is to automatically identify different layers and electrical components from an integrated circuit picture. These layers are the regions filled with metal, polycristaline silicon, and P or N doped regions. They are used to build components like transistors, resistors and capacitors and then joined to make a complex circuit.

The images are from project5474.org, which contains a large number of high resolution images of simple integrated circuits, like single logic gates. These are some examples of the High Speed CMOS family.

![54HC32](https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/54HC32_RCA_8825_die_120nmpp.jpg/467px-54HC32_RCA_8825_die_120nmpp.jpg)
![54HC00](https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/54HC00_NS_8632_die_120nmpp.jpg/578px-54HC00_NS_8632_die_120nmpp.jpg)
![74HC00](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/74HCT00_RCA_419_die_120nmpp.jpg/482px-74HCT00_RCA_419_die_120nmpp.jpg)
![74HC02](https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/74HC02_Motorola_8302.jpg/629px-74HC02_Motorola_8302.jpg)

For the layer identification, the methods applied are a median filter, in attempt to remove dust present in the images, followed by a threshold, intending to separate and have an initial identification of the layers. In the next step a morphological closing is applied to improve the segmented sections obtained before and allow for a better shape-based layer identification. This has already been applied for the metal layer.