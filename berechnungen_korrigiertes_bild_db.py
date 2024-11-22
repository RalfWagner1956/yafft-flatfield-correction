''' This program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt
'''


import numpy as np
from scipy import ndimage

def KeineKanaltrennung_bg(kkt_bg, Faktor, sigma_bg):

    kkt_bg = np.clip(kkt_bg, 1, Faktor)  # Werte = Null vermeiden

    kkt_bg = (kkt_bg / np.max(kkt_bg)) * Faktor  # Normalisierung auf 'Faktor' Farben

    kkt_bg = ndimage.gaussian_filter(kkt_bg, sigma=sigma_bg)  # FlatBild weichzeichnen

    mittelwert = np.mean(kkt_bg)  # mittelwert bilden

    return kkt_bg, mittelwert


def KeineKanaltrennung_cor(kkt_fg, kkt_bg, Faktor, mittelwert):

    np.clip(kkt_fg, 1, Faktor, kkt_fg)  # Werte = Null vermeiden

    kkt_fg = (kkt_fg / np.max(kkt_fg)) * Faktor  # Normalisierung auf Faktor Farben

    kkt_cor = np.where((kkt_fg * mittelwert / kkt_bg < Faktor),
                       kkt_fg * mittelwert / kkt_bg, kkt_fg)

    np.clip(kkt_cor, 1, Faktor, kkt_cor)
    kkt_fg = (kkt_fg / np.max(kkt_fg)) * Faktor
    kkt_bg = (kkt_bg / np.max(kkt_bg)) * Faktor
    kkt_cor = (kkt_cor / np.max(kkt_cor)) * Faktor  # Normalisierung auf 65536 Farben

    kkt_cor = kkt_cor * (np.sum(kkt_fg) / np.sum(kkt_cor))  # Helligkeit zum Originalbild angleichen

    np.clip(kkt_cor, 1, Faktor, kkt_cor)

    return kkt_cor, kkt_fg, kkt_bg


def MitKanaltrennung_bg(mkt_bg, Faktor, sigma_bg):

    np.clip(mkt_bg, 1, Faktor, mkt_bg)  # Werte = Null vermeiden

    mkt_bg[:, :, 0] = (mkt_bg[:, :, 0] / np.max(mkt_bg[:, :, 0])) * Faktor  # Normalisierung auf 65536 Farben
    mkt_bg[:, :, 1] = (mkt_bg[:, :, 1] / np.max(mkt_bg[:, :, 1])) * Faktor
    mkt_bg[:, :, 2] = (mkt_bg[:, :, 2] / np.max(mkt_bg[:, :, 2])) * Faktor

    mkt_bg[:, :, 0] = ndimage.gaussian_filter(mkt_bg[:, :, 0], sigma=sigma_bg)  # FlatBild weichzeichnen
    mkt_bg[:, :, 1] = ndimage.gaussian_filter(mkt_bg[:, :, 1], sigma=sigma_bg)
    mkt_bg[:, :, 2] = ndimage.gaussian_filter(mkt_bg[:, :, 2], sigma=sigma_bg)

    R_BG_mean = np.mean(mkt_bg[:, :, 0])  # mittelwerte bilden
    G_BG_mean = np.mean(mkt_bg[:, :, 1])
    B_BG_mean = np.mean(mkt_bg[:, :, 2])

    return mkt_bg, R_BG_mean, G_BG_mean, B_BG_mean


def MitKanaltrennung_cor(mkt_fg, mkt_bg, mkt_cor, Faktor, R_BG_mean, G_BG_mean, B_BG_mean):

    np.clip(mkt_fg, 1, Faktor, mkt_fg)  # Werte = Null vermeiden

    mkt_fg[:, :, 0] = (mkt_fg[:, :, 0] / np.max(mkt_fg[:, :, 0])) * Faktor  # Normalisierung auf 65536 Farben
    mkt_fg[:, :, 1] = (mkt_fg[:, :, 1] / np.max(mkt_fg[:, :, 1])) * Faktor
    mkt_fg[:, :, 2] = (mkt_fg[:, :, 2] / np.max(mkt_fg[:, :, 2])) * Faktor

    mkt_cor[:, :, 0] = np.where(((mkt_fg[:, :, 0]) * R_BG_mean / (mkt_bg[:, :, 0]) < Faktor),
                                (mkt_fg[:, :, 0]) * R_BG_mean / (mkt_bg[:, :, 0]), (mkt_fg[:, :, 0]))
    mkt_cor[:, :, 1] = np.where(((mkt_fg[:, :, 1]) * G_BG_mean / (mkt_bg[:, :, 1]) < Faktor),
                                (mkt_fg[:, :, 1]) * G_BG_mean / (mkt_bg[:, :, 1]), (mkt_fg[:, :, 1]))
    mkt_cor[:, :, 2] = np.where(((mkt_fg[:, :, 2]) * B_BG_mean / (mkt_bg[:, :, 2]) < Faktor),
                                (mkt_fg[:, :, 2]) * B_BG_mean / (mkt_bg[:, :, 2]), (mkt_fg[:, :, 2]))

    np.clip(mkt_cor, 1, Faktor, mkt_cor)

    mkt_fg = (mkt_fg / np.max(mkt_fg)) * Faktor
    mkt_bg = (mkt_bg / np.max(mkt_bg)) * Faktor
    mkt_cor = (mkt_cor / np.max(mkt_cor)) * Faktor  # Normalisierung auf 65536 Farben

    mkt_cor = mkt_cor * (np.sum(mkt_fg) / np.sum(mkt_cor))  # Helligkeit zum Originalbild angleichen

    np.clip(mkt_cor, 1, Faktor, mkt_cor)

    return mkt_cor, mkt_fg, mkt_bg
