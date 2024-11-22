''' This program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt
'''


import numpy as np
import rawpy
import imageio.v2 as imageio



def KeineKanaltrennung_dark(path_darks, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):
    kkt_dark = 0
    for dark_file in path_darks:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(dark_file) as raw:
                kkt_dark_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                              use_camera_wb=True, output_bps=16)  # Darkbild einlesen
        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            kkt_dark_temp16 = imageio.imread(dark_file)

        if dateierweiterung in tif_erweiterungen:
            kkt_dark_temp16 = imageio.imread(dark_file)

        kkt_dark_temp32 = kkt_dark_temp16.astype(np.int32)
        kkt_dark = np.add(kkt_dark, kkt_dark_temp32)
    masterdark_kkt = kkt_dark / len(path_darks)
    return masterdark_kkt

def MitKanaltrennung_dark(path_darks, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):
    #darkarray initialisieren:
    if dateierweiterung in raw_erweiterungen:
        with rawpy.imread(path_darks[0]) as raw:
            mkt_dark = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # mkt_dark als eigenständige Variable definieren, kein Pointer
    if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            mkt_dark = imageio.imread(path_darks[0])

    if dateierweiterung in tif_erweiterungen:
            mkt_dark = imageio.imread(path_darks[0])

    shape = np.shape(mkt_dark)
    mkt_dark= np.zeros(shape)
    masterdark_mkt =  np.zeros(shape)


    for dark_file in path_darks:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(dark_file) as raw:
                mkt_dark_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                            use_camera_wb=True, output_bps=16)  # Darkbild einlesen
        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            mkt_dark_temp16 = imageio.imread(dark_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            mkt_dark_temp16 = imageio.imread(dark_file)

        mkt_dark_temp32 = mkt_dark_temp16.astype(np.int32)

        mkt_dark[:, :, 0] = np.add(mkt_dark[:, :, 0], mkt_dark_temp32[:, :, 0])
        mkt_dark[:, :, 1] = np.add(mkt_dark[:, :, 1], mkt_dark_temp32[:, :, 1])
        mkt_dark[:, :, 2] = np.add(mkt_dark[:, :, 2], mkt_dark_temp32[:, :, 2])


    masterdark_mkt[:, :, 0] = mkt_dark[:, :, 0] / len(path_darks)
    masterdark_mkt[:, :, 1] = mkt_dark[:, :, 1] / len(path_darks)
    masterdark_mkt[:, :, 2] = mkt_dark[:, :, 2] / len(path_darks)

    return masterdark_mkt


def KeineKanaltrennung_dark_flats(path_dark_flats, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):
    kkt_dark_flat = 0
    for dark_flat_file in path_dark_flats:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(dark_flat_file) as raw:
                kkt_dark_flat_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                              use_camera_wb=True, output_bps=16)  # Darkflatbild einlesen

        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            kkt_dark_flat_temp16 = imageio.imread(dark_flat_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            kkt_dark_flat_temp16 = imageio.imread(dark_flat_file)


        kkt_dark_flat_temp32 = kkt_dark_flat_temp16.astype(np.int32)
        kkt_dark_flat = np.add(kkt_dark_flat, kkt_dark_flat_temp32)

    masterdarkflat_kkt = kkt_dark_flat / len(path_dark_flats)

    return masterdarkflat_kkt

def MitKanaltrennung_dark_flats(path_dark_flats, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):

    if dateierweiterung in raw_erweiterungen:
        with rawpy.imread(path_dark_flats[0]) as raw:
            mkt_dark_flats= raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # mkt_dark_flats als eigenständige Variable definieren, kein Pointer

    if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
        mkt_dark_flats = imageio.imread(path_dark_flats[0]) # mkt_dark_flats als eigenständige Variable definieren, kein Pointer

    if dateierweiterung in tif_erweiterungen:  # also ein .tif!
        mkt_dark_flats = imageio.imread(path_dark_flats[0]) # mkt_dark_flats als eigenständige Variable definieren, kein Pointer


    shape = np.shape(mkt_dark_flats)
    mkt_dark_flats = np.zeros(shape)
    masterdarkflat_mkt =  np.zeros(shape)


    for dark_file_flat in path_dark_flats:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(dark_file_flat) as raw:
                mkt_dark_flat_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                            use_camera_wb=True, output_bps=16)  # Darkflatbild einlesen

        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            mkt_dark_flat_temp16 = imageio.imread(dark_file_flat) # Darkflatbild einlesen

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            mkt_dark_flat_temp16 = imageio.imread(dark_file_flat) # Darkflatbild einlesen


        mkt_dark_flat_temp32 = mkt_dark_flat_temp16.astype(np.int32)

        mkt_dark_flats[:, :, 0] = np.add(mkt_dark_flats[:, :, 0], mkt_dark_flat_temp32[:, :, 0])
        mkt_dark_flats[:, :, 1] = np.add(mkt_dark_flats[:, :, 1], mkt_dark_flat_temp32[:, :, 1])
        mkt_dark_flats[:, :, 2] = np.add(mkt_dark_flats[:, :, 2], mkt_dark_flat_temp32[:, :, 2])


    masterdarkflat_mkt[:, :, 0] = mkt_dark_flats[:, :, 0] / len(path_dark_flats)
    masterdarkflat_mkt[:, :, 1] = mkt_dark_flats[:, :, 1] / len(path_dark_flats)
    masterdarkflat_mkt[:, :, 2] = mkt_dark_flats[:, :, 2] / len(path_dark_flats)

    return masterdarkflat_mkt


def KeineKanaltrennung_bias(path_bias, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):
    kkt_bias = 0
    for bias_file in path_bias:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(bias_file) as raw:
                kkt_bias_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                  use_camera_wb=True, output_bps=16)  # Darkflatbild einlesen
        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            kkt_bias_temp16 = imageio.imread(bias_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            kkt_bias_temp16 = imageio.imread(bias_file)


        kkt_bias_temp32 = kkt_bias_temp16.astype(np.int32)
        kkt_bias = np.add(kkt_bias, kkt_bias_temp32)
    masterbias_kkt = kkt_bias / len(path_bias)
    return masterbias_kkt


def MitKanaltrennung_bias(path_bias, dateierweiterung, raw_erweiterungen, raw_tif_erweiterungen, tif_erweiterungen):
    if dateierweiterung in raw_erweiterungen:
        with rawpy.imread(path_bias[0]) as raw:
            mkt_bias= raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01, use_camera_wb=True,
                              output_bps=16)  # mkt_dark als eigenständige Variable definieren, kein Pointer
    if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            mkt_bias = imageio.imread(path_bias[0])

    if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            mkt_bias = imageio.imread(path_bias[0])

    shape = np.shape(mkt_bias)
    mkt_bias = np.zeros(shape)
    masterbias_mkt =  np.zeros(shape)


    for bias_file in path_bias:
        if dateierweiterung in raw_erweiterungen:
            with rawpy.imread(bias_file) as raw:
                mkt_bias_temp16 = raw.postprocess(gamma=(2.222, 3.0), no_auto_bright=True, auto_bright_thr=0.01,
                                            use_camera_wb=True, output_bps=16)  # BIASbild einlesen

        if dateierweiterung not in raw_tif_erweiterungen:  # also ein .jpg!
            mkt_bias_temp16 = imageio.imread(bias_file)

        if dateierweiterung in tif_erweiterungen:  # also ein .tif!
            mkt_bias_temp16 = imageio.imread(bias_file)

        mkt_bias_temp32 = mkt_bias_temp16.astype(np.int32)

        mkt_bias[:, :, 0] = np.add(mkt_bias[:, :, 0], mkt_bias_temp32[:, :, 0])
        mkt_bias[:, :, 1] = np.add(mkt_bias[:, :, 1], mkt_bias_temp32[:, :, 1])
        mkt_bias[:, :, 2] = np.add(mkt_bias[:, :, 2], mkt_bias_temp32[:, :, 2])


    masterbias_mkt[:, :, 0] = mkt_bias[:, :, 0] / len(path_bias)
    masterbias_mkt[:, :, 1] = mkt_bias[:, :, 1] / len(path_bias)
    masterbias_mkt[:, :, 2] = mkt_bias[:, :, 2] / len(path_bias)

    return masterbias_mkt





