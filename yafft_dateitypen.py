''' This program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt
'''


import os
import rawpy
import numpy as np
import imageio.v2 as imageio

import display_result_db
import file_io_db
import berechnungen_korrigiertes_bild_db as berechnungen
import master_files_calculation

import tkinter as tk
from tkinter import simpledialog



# Hier beginnt die Schleife zum Aufrufen der Inputdialoge und des Werts für Sigma

root = tk.Tk()

file_io_db.message_flatfield_open(root)

root.title("Select Flatfield Files")
path_bg = file_io_db.open_file_dialog()

answer_darks = file_io_db.message_dark_open()
print ('answer darks =', answer_darks)
if answer_darks == 'yes' :
    root.title("Select Dark Files")
    path_darks = file_io_db.open_dark_file_dialog()

answer_dark_flats = file_io_db.message_dark_flats_open()

if answer_dark_flats == 'yes' :
    root.title("Select Dark Flat Files")
    path_dark_flats = file_io_db.open_dark_flat_file_dialog()

answer_bias = file_io_db.message_bias_open()

if answer_bias == 'yes' :
    root.title("Select BIAS Files")
    path_bias = file_io_db.open_bias_file_dialog()

answer_stack_lights = file_io_db.message_stack_lights_open()
file_io_db.message_lightdata_open(root)

root.title("Select Raw Files")
filenames = file_io_db.open_multiplefile_dialog()

sigma_bg = simpledialog.askinteger(title="Weichzeichnungsfaktor Sigma",
                                  prompt="Wert für Sigma eingeben, empfohlen sind Werte zwischen 2 und 10")

root.destroy()
root.mainloop() # Inputdialoge beenden

#Hier beginnen die Berechnungen:

# mkt : Mit Kanaltrennung
# kkt : Keine Kanaltrennung


if sigma_bg < 1 or sigma_bg > 50:
    sigma_bg = 2

# Verschiedene Umrechnungen zu Pfad- und Dateinamen

bg_name = os.path.basename(path_bg[0])
directory = os.path.dirname(os.path.abspath(path_bg[0]))
os.chdir(directory)
dateiname, dateierweiterung = os.path.splitext(bg_name)

raw_erweiterungen = ('.CR2', '.cr2', '.NEF', '.nef')
raw_tif_erweiterungen = ('.CR2', '.cr2', '.NEF', '.nef', '.tif', '.TIF')
tif_erweiterungen = ('.tif', '.TIF')

# Anpassung der Faktoren für .jpg und .raw oder .tif

Faktor = 0
if dateierweiterung in raw_tif_erweiterungen:
    Faktor = 65535
else:
    Faktor = 255
#print('Faktor =', Faktor)

# Berechnungen mit RAW Dateien:

if dateierweiterung in raw_erweiterungen:
    with rawpy.imread(path_bg[0]) as raw:
        kkt_cor = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # kkt_cor als eigenständige Variable definieren, kein Pointer

if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
        kkt_cor = imageio.imread(path_bg[0])

if dateierweiterung in raw_tif_erweiterungen:  # also ein .tif!
        kkt_cor = imageio.imread(path_bg[0])


if answer_darks == 'yes':
        masterdark_kkt = master_files_calculation.KeineKanaltrennung_dark(path_darks, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print ('masterdark_median-kkt =', np.median(masterdark_kkt))

        masterdark_mkt = master_files_calculation.MitKanaltrennung_dark(path_darks, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print('masterdark_median-mkt =', np.median(masterdark_mkt))

if answer_dark_flats == 'yes':
        masterdarkflat_kkt = master_files_calculation.KeineKanaltrennung_dark_flats(path_dark_flats, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print('masterdarkflat_median-kkt =', np.median(masterdarkflat_kkt))

        masterdarkflat_mkt = master_files_calculation.MitKanaltrennung_dark_flats(path_dark_flats, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print('masterdarkflat_median-mkt =', np.median(masterdarkflat_mkt))

if answer_bias == 'yes':
        masterbias_kkt = master_files_calculation.KeineKanaltrennung_bias(path_bias, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print('masterbias_median-kkt =', np.median(masterbias_kkt))

        masterbias_mkt = master_files_calculation.MitKanaltrennung_bias(path_bias, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen)
        #print('masterbias_median-mkt =', np.median(masterbias_mkt))



kkt_bg = 0
for bg_file in path_bg:

        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(bg_file) as raw:
                kkt_bg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                                      output_bps=16)  # Flatbild einlesen

        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                kkt_bg_temp16 = imageio.imread(bg_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                kkt_bg_temp16 = imageio.imread(bg_file)

        if answer_dark_flats == 'yes':
                kkt_bg_temp16 = kkt_bg_temp16 - masterdarkflat_kkt #Masterdarkflat abziehen

        if answer_bias == 'yes' and answer_dark_flats == 'no':
                kkt_bg_temp16 = kkt_bg_temp16 - masterbias_kkt # Masterbias abziehen


        kkt_bg_temp32 = kkt_bg_temp16.astype(np.int32)
        kkt_bg = np.add(kkt_bg, kkt_bg_temp32)
kkt_bg = kkt_bg / len(path_bg)

kkt_bg, mittelwert = berechnungen.KeineKanaltrennung_bg(kkt_bg, Faktor, sigma_bg)


if answer_stack_lights == 'no':

        for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

            ohneEndung = filename[:-4]  # Dateiendungen abspalten

            if dateierweiterung in raw_erweiterungen:
                with rawpy.imread(filename) as raw:
                    kkt_fg = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                            use_camera_wb=True, output_bps=16)

            if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    kkt_fg = imageio.imread(filename)

            if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                    kkt_fg = imageio.imread(filename)

            if answer_darks == 'yes':
                kkt_fg = kkt_fg - masterdark_kkt

            kkt_cor, kkt_fg, kkt_bg = berechnungen.KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert)

            if dateierweiterung in raw_tif_erweiterungen:  # also ein raw oder ein tif!
                    imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                    + '_einzelne lights _nocs' + '.tif', kkt_cor.astype('uint16'))
            if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                    + '_einzelne lights _nocs' + '.jpg', kkt_cor.astype('uint8'))


if answer_stack_lights == 'yes':
        shape = np.shape(kkt_bg)
        kkt_fg = np.zeros(shape)


        for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

            ohneEndung = filename[:-4]  # Dateiendungen abspalten

            if dateierweiterung in raw_erweiterungen:
                with rawpy.imread(filename) as raw:
                    kkt_fg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                         use_camera_wb=True, output_bps=16)

            if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    kkt_fg_temp16 = imageio.imread(filename)

            if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                    kkt_fg_temp16 = imageio.imread(filename)

            if answer_darks == 'yes':
                kkt_fg_temp16 = kkt_fg_temp16 - masterdark_kkt


            kkt_fg_temp32 = kkt_fg_temp16.astype(np.int32)
            kkt_fg = kkt_fg + kkt_fg_temp32

        kkt_fg = kkt_fg / len(filenames)
        kkt_cor, kkt_fg, kkt_bg = berechnungen.KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert)

        if dateierweiterung in raw_tif_erweiterungen:  # also ein raw oder ein tif!
            imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                + '_gemittelte lights _nocs' + '.tif', kkt_cor.astype('uint16'))
        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                + '_gemittelte lights _nocs' + '.jpg', kkt_cor.astype('uint8'))



shape = np.shape(kkt_fg)
mkt_cor = np.zeros(shape)

mkt_bg = np.zeros(shape)

for bg_file in path_bg:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(bg_file) as raw:
                    mkt_bg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                              use_camera_wb=True, output_bps=16)  # Flatbild einlesen

        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    mkt_bg_temp16 = imageio.imread(bg_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                    mkt_bg_temp16 = imageio.imread(bg_file)

        mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)

        if answer_dark_flats == 'yes':
           mkt_bg_temp16 = mkt_bg_temp16 - masterdarkflat_mkt  # Masterdarkflat abziehen

           mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)

        if answer_bias == 'yes' and answer_dark_flats == 'no':
            mkt_bg_temp16 = mkt_bg_temp16 - masterbias_mkt # Masterbias abziehen

            mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)


        mkt_bg[:, :, 0] = mkt_bg[:, :, 0] + mkt_bg_temp32[:, :, 0]
        mkt_bg[:, :, 1] = mkt_bg[:, :, 1] + mkt_bg_temp32[:, :, 1]
        mkt_bg[:, :, 2] = mkt_bg[:, :, 2] + mkt_bg_temp32[:, :, 2]

mkt_bg[:, :, 0] = mkt_bg[:, :, 0] / len(path_bg)
mkt_bg[:, :, 1] = mkt_bg[:, :, 1] / len(path_bg)
mkt_bg[:, :, 2] = mkt_bg[:, :, 2] / len(path_bg)

mkt_bg, R_BG_mean, G_BG_mean, B_BG_mean = berechnungen.MitKanaltrennung_bg(mkt_bg, Faktor, sigma_bg)

if answer_stack_lights == 'no':
            for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

                ohneEndung = filename[:-4]  # Dateiendungen abspalten

                if dateierweiterung in raw_erweiterungen:
                        with rawpy.imread(filename) as raw:
                            mkt_fg = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                                     output_bps=16)

                if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                        mkt_fg = imageio.imread(filename)

                if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                        mkt_fg = imageio.imread(filename)


                if answer_darks == 'yes':
                        mkt_fg = mkt_fg - masterdark_mkt

                mkt_cor, mkt_fg, mkt_bg = berechnungen.MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean, G_BG_mean, B_BG_mean)

                if dateierweiterung in raw_tif_erweiterungen:  # also ein raw oder ein tif!
                    imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                           + '_einzelne lights _cs' + '.tif', mkt_cor.astype('uint16'))
                if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    imageio.imsave(ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                            + '_einzelne lights _cs' + '.jpg', mkt_cor.astype('uint8'))


if answer_stack_lights == 'yes':

        shape = np.shape(kkt_bg)
        mkt_fg = np.zeros(shape)

        for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen
            ohneEndung = filename[:-4]  # Dateiendungen abspalten

            if dateierweiterung in raw_erweiterungen:
                with rawpy.imread(filename) as raw:
                    mkt_fg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                         use_camera_wb=True, output_bps=16)

            if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                    mkt_fg_temp16 = imageio.imread(filename)

            if dateierweiterung in tif_erweiterungen:  # also ein .tif!
                    mkt_fg_temp16 = imageio.imread(filename)

            if answer_darks == 'yes':
                mkt_fg_temp16 = mkt_fg_temp16 - masterdark_mkt

            mkt_fg_temp32 = mkt_fg_temp16.astype(np.int32)
            mkt_fg = mkt_fg + mkt_fg_temp32

        mkt_fg = mkt_fg / len(filenames)
        mkt_cor, mkt_fg, mkt_bg = berechnungen.MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean,
                                                                        G_BG_mean, B_BG_mean)

        if dateierweiterung in raw_tif_erweiterungen:  # also ein raw oder ein tif!
                imageio.imsave( ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                        + '_gemittelte lights _cs' + '.tif', mkt_cor.astype('uint16'))


        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
                imageio.imsave( ohneEndung + '_darks=' + answer_darks + '_darkflats=' + answer_dark_flats + '_bias=' + answer_bias
                        + '_gemittelte lights _cs' + '.jpg', mkt_cor.astype('uint8'))




display_result_db.display_result(dateierweiterung, raw_tif_erweiterungen, filename, sigma_bg, kkt_cor, mkt_cor, kkt_fg, mkt_fg)
