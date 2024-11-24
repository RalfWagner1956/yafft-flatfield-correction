# yafft
yafft means 'just another flatfield tool'. It is written in python and is intended to help in a flatfield correction of mainly those images that are taken through a microscope. 

The program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt

It works in the following way:

First specify the flatfield file(s) in the first file input dialog. These images are called 'flats'. It is possible to use only one or more flatfield files.
In case of more than one file these are averaged by the program and the averaged image will be used for correction.

Next specify whether dark frames shall be used or not. If "yes" the dark frames are averaged resulting in a masterdark frame. This masterdark frame is later 
subtracted from the lights in order to reduce random noise. This is useful for long exposure times of the lights (> 1s). Dark frames are taken with the same ISO and same exposure time as the light frames, but
no light is allowed to reach the sensor. You might just put the cap on the lense or otherwise darken the scene.

Now you are asked to specify whether dark-flat frames shall be used or not. If "yes" the dark-flat frames are averaged resulting in a masterdark frame. This masterdarkflat frame is later 
subtracted from the flats in order to reduce random noise. This is useful for long exposure times of the flats (> 1s). Dark-flat frames are taken with the same ISO and same exposure time as the flat frames, but
no light is allowed to reach the sensor. You might just put the cap on the lense or otherwise darken the scene.

Next specify whether bias frames shall be used or not. If "yes" the bias frames are averaged resulting in a masterbias frame. This masterbias frame is later 
subtracted from the flats in order to reduce random noise. This is useful for short exposure times of the flats (< 1s). Bias frames are taken with the same ISO as the light frames and with shortes possible exposure time, but
no light is allowed to reach the sensor. You might just put the cap on the lense or otherwise darken the scene.

In the following dialog you are asked if the light frames (the images that shall be corrected) shall be averaged or not. In case of "yes" the single light frames are averaged and you will öbtain a noise reduced picture. If the answer is "no",
each single light frame will corrected individually and saved. This is useful if the single lights later shall be focus stacked with a stacking software.

Last you must specify the variable 'sigma'. It is used to blur the flat file. Without this step the resulting image will be unintentionally sharpened.
The higher the value of sigma the more the flat file will be blured and the the light image will be less corrected. For most cases a value between 2 and 10 is good.

In the file input dialogs you are able to load .jpg, .tif or raw files (.nef, .cr2). The lights you will load must be of the same format as the flat files. The result will be stored in this way:
- if a .jpg is processed, then the result will be stored also in .jpg format
- if a .tif is processed, then the result will be stored also in .tif format
- if a raw file (either .nef or .cr2) is processed, then the result will be stored in .tif format

Processing of images is done in two ways:
- rgb channels are processed witout separation of channels.
- rgb channels are processed separately.
Depending on the input images once the method separated channels or the method without separation will give the better correction.

At the end of the program a preview of the corrected image is given in comparison with the uncorrected, original image for both methods.
The corrected images are stored in the same directory as the light images. If "cs" occurs in the new filename this means that you are here dealing with result of the rgb channel separation process and if "nocs" is in the filename you are here dealing with the result obtained with no rgb channel separation. It is your choice which method will fit better to your needs.

yafft_dateitypen.py is the main file.
Download a windows .exe file here: https://www.dr-ralf-wagner.de/Forum/yafft.exe
