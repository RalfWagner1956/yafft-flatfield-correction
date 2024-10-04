''' This program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt
'''


def display_result(dateierweiterung, raw_tif_erweiterungen, filename, sigma_bg, kkt_cor, mkt_cor, kkt_fg, mkt_fg):

    import matplotlib.pyplot as plt
    import os

    if dateierweiterung in raw_tif_erweiterungen:
        teiler = 65535
    else:
        teiler = 255

    fig = plt.figure(frameon=False, layout='compressed')
    title_file = (os.path.basename(filename))
    title_file = title_file + '  sigma = ' + str(sigma_bg)
    fig.suptitle(title_file, fontsize=16)
    w = 1920 / fig.dpi * 0.8
    h = 1080 / fig.dpi * 0.8
    fig.set_size_inches(w, h)

    fig1 = fig.add_subplot(2, 2, 1)
    plt.title("RGB zusammen")
    fig1.imshow(kkt_cor / teiler)
    fig1.axis('off')

    fig2 = fig.add_subplot(2, 2, 2)
    plt.title("RGB getrennt")
    fig2.imshow(mkt_cor / teiler)
    fig2.axis('off')

    fig3 = fig.add_subplot(2, 2, 3)
    plt.title("Original RGB zusammen")
    fig3.imshow(kkt_fg / teiler)
    fig3.axis('off')

    fig4 = fig.add_subplot(2, 2, 4)
    plt.title("Original RGB getrennt")
    fig4.imshow(mkt_fg / teiler)
    fig4.axis('off')

    plt.show()
