import os
import rawpy
import numpy as np
import imageio.v2 as imageio

import display_result
import file_io
import berechnungen_korrigiertes_bild as berechnungen

import tkinter as tk
from tkinter import simpledialog



# Hier beginnt die Schleife zum Aufrufen der Inputdialoge und des Werts für Sigma

root = tk.Tk()

file_io.message_flatfield_open(root)

root.title("Select Flatfield File")
path_bg = file_io.open_file_dialog()

file_io.message_lightdata_open(root)

root.title("Select Raw Files")
filenames = file_io.open_multiplefile_dialog()

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

print('Faktor =', Faktor)


# Berechnungen mit RAW Dateien:

if dateierweiterung in raw_erweiterungen:

    with rawpy.imread(path_bg[0]) as raw:
        kkt_cor = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # mkt_cor als eigenständige Variable definieren, kein Pointer

    kkt_bg = 0
    for bg_file in path_bg:
        with rawpy.imread(bg_file) as raw:
            kkt_bg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                                      output_bps=16)  # Flatbild einlesen
        kkt_bg_temp32 = kkt_bg_temp16.astype(np.int32)
        kkt_bg = np.add(kkt_bg, kkt_bg_temp32)
    kkt_bg = kkt_bg / len(path_bg)


    kkt_bg, mittelwert = berechnungen.KeineKanaltrennung_bg(kkt_bg, Faktor, sigma_bg)
 
    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten
#+_cor+_nocs
        with rawpy.imread(filename) as raw:
            kkt_fg = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                         use_camera_wb=True, output_bps=16)

        kkt_cor, kkt_fg, kkt_bg = berechnungen.KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert)

        imageio.imsave(ohneEndung + '_cor_nocs' + '.tif', kkt_cor.astype('uint16'))

    with rawpy.imread(path_bg[0]) as raw:
        mkt_cor = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # mkt_cor als eigenständige Variable definieren, kein Pointer

    mkt_bg = 0
    for bg_file in path_bg:
        with rawpy.imread(bg_file) as raw:
                mkt_bg_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                              use_camera_wb=True, output_bps=16)  # Flatbild einlesen
        mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)
        mkt_bg = mkt_bg + mkt_bg_temp32

    mkt_bg = mkt_bg / len(path_bg)

    mkt_bg, R_BG_mean, G_BG_mean, B_BG_mean = berechnungen.MitKanaltrennung_bg(mkt_bg, Faktor, sigma_bg)


    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten

        with rawpy.imread(filename) as raw:
            mkt_fg = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                                     output_bps=16)

        mkt_cor, mkt_fg, mkt_bg = berechnungen.MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean, G_BG_mean, B_BG_mean)

        imageio.imsave(ohneEndung + '_cor_cs' + '.tif', mkt_cor.astype('uint16'))

# Berechnungen mit .jpg Dateien:

if dateierweiterung not in raw_tif_erweiterungen: # also ein .jpg!

    kkt_cor = imageio.imread(bg_name)

    kkt_bg = 0
    for bg_file in path_bg:
        kkt_bg_temp16 = imageio.imread(bg_file)
        kkt_bg_temp32 = kkt_bg_temp16.astype(np.int32)
        kkt_bg = np.add(kkt_bg, kkt_bg_temp32)
    kkt_bg = kkt_bg / len(path_bg)

    kkt_bg, mittelwert = berechnungen.KeineKanaltrennung_bg(kkt_bg, Faktor, sigma_bg)

    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten

        kkt_fg = imageio.imread(filename)

        kkt_cor, kkt_fg, kkt_bg = berechnungen.KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert)

        imageio.imsave(ohneEndung + '_cor_nocs' +  '.jpg', kkt_cor.astype('uint8'))

    mkt_cor = imageio.imread(bg_name)

    mkt_bg = 0
    for bg_file in path_bg:
        mkt_bg_temp16 = imageio.imread(bg_file)
        mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)
        mkt_bg = np.add(mkt_bg, mkt_bg_temp32)
    mkt_bg = mkt_bg / len(path_bg)

    mkt_bg, R_BG_mean, G_BG_mean, B_BG_mean = berechnungen.MitKanaltrennung_bg(mkt_bg, Faktor, sigma_bg)

    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten

        mkt_fg = imageio.imread(filename)

        mkt_cor, mkt_fg, mkt_bg = berechnungen.MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean, G_BG_mean, B_BG_mean)

        imageio.imsave(ohneEndung + '_cor_cs' +  '.jpg', mkt_cor.astype('uint8'))

# Berechnungen mit ,tif Dateien:

if dateierweiterung in tif_erweiterungen:
    kkt_cor = imageio.imread(bg_name)

    kkt_bg = 0

    for bg_file in path_bg:
        kkt_bg_temp16 = imageio.imread(bg_file)
        kkt_bg_temp32 = kkt_bg_temp16.astype(np.int32)
        kkt_bg = np.add(kkt_bg, kkt_bg_temp32)
    kkt_bg = kkt_bg / len(path_bg)

    kkt_bg, mittelwert = berechnungen.KeineKanaltrennung_bg(kkt_bg, Faktor, sigma_bg)

    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten

        kkt_fg = imageio.imread(filename)

        kkt_cor, kkt_fg, kkt_bg = berechnungen.KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert)

        imageio.imsave(ohneEndung + '_cor_nocs' +  '.tif', kkt_cor.astype('uint16'))

    mkt_cor = imageio.imread(bg_name)

    mkt_bg = 0
    for bg_file in path_bg:
        mkt_bg_temp16 = imageio.imread(bg_file)
        mkt_bg_temp32 = mkt_bg_temp16.astype(np.int32)
        mkt_bg = np.add(mkt_bg, mkt_bg_temp32)
    mkt_bg = mkt_bg / len(path_bg)

    mkt_bg, R_BG_mean, G_BG_mean, B_BG_mean = berechnungen.MitKanaltrennung_bg(mkt_bg, Faktor, sigma_bg)

    for filename in filenames:  # Alle Dateinamen im aktuellen Verzeichnis einlesen

        ohneEndung = filename[:-4]  # Dateiendungen abspalten

        mkt_fg = imageio.imread(filename)

        mkt_cor, mkt_fg, mkt_bg = berechnungen.MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean, G_BG_mean, B_BG_mean)

        imageio.imsave(ohneEndung + '_cor_cs' +  '.tif', mkt_cor.astype('uint16'))


display_result.display_result(dateierweiterung, raw_tif_erweiterungen, filename, sigma_bg, kkt_cor, mkt_cor, kkt_fg, mkt_fg)
