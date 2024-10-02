
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
def message_lightdata_open(root):
    messagebox.showinfo("lightdata", "Light Dateien Öffnen")
    root.withdraw()

def open_multiplefile_dialog():

        filenames = filedialog.askopenfilenames(title="Select Light Files", filetypes=[("Canon Raw", "*.CR2"), ("Nikon RAW", "*.NEF"),
                                                                                 ("JPG", "*.JPG"), ("TIF", "*.tif")])
        return filenames
        root.withdraw()