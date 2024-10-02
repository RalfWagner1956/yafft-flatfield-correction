# yafft
yafft means 'just another flatfield tool'. It is written in python and is intended to help in a flatfield correction of mainly images that are taken through a microscope. It works in the following way:
First specify the flatfield file(s). These images are called 'flats'.It is possible to use only one or more flatfield files.
In case of more than 1 file these are averaged by the program and the averaged image will be used for correction.
Second specify the images that must be corrected. These images are called 'lights'. You can use 1 ore more images.
Third specify the variable 'sigma'. It is used to blur the flat file. Without this step the resulting image will be unintentionally sharpened.
The higher the value of sigma the mor the flat file will be blured and the the light image will be less corrected. For most casrs a value between 2 and 10 is good.
