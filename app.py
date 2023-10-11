import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class ColorPaletteExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ektraksi Warna by ihgoyarp")
        self.root.geometry("600x450")  # Set the initial window size

        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=20)

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        self.palette_label = tk.Label(self.root)
        self.palette_label.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300))  # Resize the image for display
            img_tk = ImageTk.PhotoImage(image)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk

            palette = self.extract_palette(file_path, n_colors=10)
            self.display_palette(palette)

    def extract_palette(self, image_path, n_colors=10):
        image = Image.open(image_path)
        image_np = np.array(image)
        w, h, d = image_np.shape
        pixels = np.reshape(image_np, (w * h, d))

        model = KMeans(n_clusters=n_colors, random_state=42).fit(pixels)
        palette = np.uint8(model.cluster_centers_)
        return palette

    def display_palette(self, palette):
        # Create a palette image
        palette_img = np.zeros((50, 300, 3), dtype=np.uint8)
        step = int(300 / len(palette))
        for i in range(len(palette)):
            palette_img[:, i * step:(i + 1) * step, :] = palette[i]

        # Display the palette image
        palette_img = Image.fromarray(palette_img, 'RGB')
        palette_img_tk = ImageTk.PhotoImage(palette_img)
        self.palette_label.configure(image=palette_img_tk)
        self.palette_label.image = palette_img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPaletteExtractorApp(root)
    root.mainloop()
