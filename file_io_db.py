''' This program is published under the
GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
https://www.gnu.org/licenses/gpl-3.0.txt
'''



from tkinter import filedialog
from tkinter import messagebox




def message_flatfield_open(root):
    messagebox.showinfo("Flatfield", "Flatfield Datei Öffnen")
    root.withdraw()

def open_file_dialog():

    path_bg = filedialog.askopenfilenames(title="Select Flatfield File", filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                                                      ("JPG", "*.JPG"), ("TIF", "*.tif")])
    return path_bg
    root.withdraw()


def message_dark_open():
    answer_darks = messagebox.askquestion("Darkframes", "Sollen Dark Dateien verwendet werden?")
    return answer_darks
    root.withdraw()


def open_dark_file_dialog():

    path_darks = filedialog.askopenfilenames(title="Select Dark Files", filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                                                      ("JPG", "*.JPG"), ("TIF", "*.tif")])
    return path_darks
    root.withdraw()

def message_dark_flats_open():
    answer_dark_flats = messagebox.askquestion("Dark_Flats", "Sollen Dark Flat Dateien verwendet werden?")
    return answer_dark_flats
    root.withdraw()


def open_dark_flat_file_dialog():
    path_dark_flats = filedialog.askopenfilenames(title="Select Dark Flat Files",
                                             filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                        ("JPG", "*.JPG"), ("TIF", "*.tif")])
    return path_dark_flats
    root.withdraw()

def message_bias_open():
        answer_bias = messagebox.askquestion("BiAS", "Sollen BIAS Dateien verwendet werden?")
        return answer_bias
        root.withdraw()

def open_bias_file_dialog():
        path_bias = filedialog.askopenfilenames(title="Select BIAS Files",
                                                      filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                                 ("JPG", "*.JPG"), ("TIF", "*.tif")])
        return path_bias
        root.withdraw()

def message_stack_lights_open():
    answer_stack_lights = messagebox.askquestion("Lights Mitteln", "Sollen die Lights Dateien gemittelt werden?")
    return answer_stack_lights

def message_lightdata_open(root):
    messagebox.showinfo("lightdata", "Light Dateien Öffnen")
    root.withdraw()

def open_multiplefile_dialog():

        filenames = filedialog.askopenfilenames(title="Select Light Files", filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                                                 ("JPG", "*.JPG"), ("TIF", "*.tif")])
        return filenames
        root.withdraw()