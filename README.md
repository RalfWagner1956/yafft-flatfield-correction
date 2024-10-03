# yafft
yafft means 'just another flatfield tool'. It is written in python and is intended to help in a flatfield correction of mainly images that are taken through a microscope. It works in the following way:

First specify the flatfield file(s) in the first file input dialog. These images are called 'flats'.It is possible to use only one or more flatfield files.
In case of more than 1 file these are averaged by the program and the averaged image will be used for correction.

Second specify the images that must be corrected in the second file input dialog. These images are called 'lights'. You can use 1 ore more images.

Third specify the variable 'sigma'. It is used to blur the flat file. Without this step the resulting image will be unintentionally sharpened.
The higher the value of sigma the more the flat file will be blured and the the light image will be less corrected. For most cases a value between 2 and 10 is good.

In the file input dialogs you are able to load .jpg, .tif or raw files (.nef, .cr2). The lights you will load must be of the same format as the flat files. The result will be stored in this way:
- if a .jpg is processed, then the result will be stored also in .jpg format
- if a .tif is processed, then the result will be stored also in .tif format
- if a raw file (either .nef or .cr2) is processed, then the result will be stored in .tif format

Processing of images is done in two ways:
- rgb channels are processed witout separation of channels.
- rgb channels are processed separately.
Depending on the input images once the method separated channels or the method without separation will give the better correction

At the end of the program a preview of the corrected image is given in comparison with the uncorrected, original image for both methods.
The corrected images are stored in the same directory as the light images.

