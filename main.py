import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.axes_grid1 import make_axes_locatable
class ImageProcessingApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt1 Biometria")
        self.root.geometry("1500x800")

        self.original_image_pil = None
        self.processed_image_pil = None
    
        self.active_filters = {
            'grayscale': tk.BooleanVar(value=False),
            'negative': tk.BooleanVar(value=False),
            'brightness': tk.BooleanVar(value=False),
            'contrast': tk.BooleanVar(value=False),
            'gamma': tk.BooleanVar(value=False),
            'binarization': tk.BooleanVar(value=False),
            'blur': tk.BooleanVar(value=False),
            'gauss': tk.BooleanVar(value=False),
            'laplace': tk.BooleanVar(value=False),
            'roberts': tk.BooleanVar(value=False),
            'sobel': tk.BooleanVar(value=False)
        }
        
        self.filter_params = {
            'brightness': tk.DoubleVar(value=0.0),
            'contrast': tk.DoubleVar(value=1.0),
            'gamma': tk.DoubleVar(value=1.0),
            'binarization': tk.DoubleVar(value=128.0),
            'gauss': tk.IntVar(value=2),
            'laplace': tk.DoubleVar(value=1.0),
            'blur': tk.IntVar(value=1)
        }

        self.setup_menu()
        self.setup_layout()

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Wczytaj obraz", command=self.load_image)
        file_menu.add_command(label="Zapisz przetworzony", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjdź", command=self.root.quit)
        menubar.add_cascade(label="Plik", menu=file_menu)

        reset_menu = tk.Menu(menubar, tearoff=0)
        reset_menu.add_command(label="Resetuj wszystko", command=self.reset_to_original)
        menubar.add_cascade(label="Reset", menu=reset_menu)

        self.root.config(menu=menubar)

    def setup_layout(self):
        self.tools_wrapper = ttk.LabelFrame(self.root, text="Panel Narzędzi", padding=5)
        self.tools_wrapper.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.tools_canvas = tk.Canvas(self.tools_wrapper, width=280, highlightthickness=0)
        self.tools_scrollbar = ttk.Scrollbar(self.tools_wrapper, orient="vertical", command=self.tools_canvas.yview)
        self.tools_canvas.configure(yscrollcommand=self.tools_scrollbar.set)

        self.tools_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tools_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tools_frame = ttk.Frame(self.tools_canvas)
        self.canvas_window = self.tools_canvas.create_window((0, 0), window=self.tools_frame, anchor="nw")

        def on_frame_configure(event):
            self.tools_canvas.configure(scrollregion=self.tools_canvas.bbox("all"))
        self.tools_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            self.tools_canvas.itemconfig(self.canvas_window, width=event.width)
        self.tools_canvas.bind("<Configure>", on_canvas_configure)

        ttk.Label(self.tools_frame, text="Operacje Punktowe:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        self.create_tool_option("Odcienie Szarości", 'grayscale')
        self.create_tool_option("Negatyw", 'negative')
        
        ttk.Separator(self.tools_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        self.create_tool_option_with_slider("Korekta Jasności", 'brightness', -255, 255, 0)
        self.create_tool_option_with_slider("Korekta Kontrastu", 'contrast', 0.0, 3.0, 1.0, 0.1)
        self.create_tool_option_with_slider("Korekta Gamma", 'gamma', 0.1, 4.0, 1.0, 0.1)
        self.create_tool_option_with_slider("Binaryzacja", 'binarization', 0, 255, 128)
        self

        ttk.Separator(self.tools_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(self.tools_frame, text="Filtry Graficzne:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        self.create_tool_option_with_slider("Filtr Uśredniający (n-krotny blur)", 'blur', 1, 100, 1)
        self.create_tool_option_with_slider("Filtr Gaussa (b)", 'gauss', 1, 4, 2, 1)
        self.create_tool_option_with_slider("Filtr Laplace'a (c)", 'laplace', 0.1, 1.0, 1.0, 0.1)
        self.create_tool_option("Krzyż Robertsa", 'roberts')
        self.create_tool_option("Operator Sobela", 'sobel')

        self.images_frame = ttk.Frame(self.root)
        self.images_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.images_frame.columnconfigure(0, weight=1)
        self.images_frame.columnconfigure(1, weight=1)
        self.images_frame.columnconfigure(2, weight=2) 

        frame_original = ttk.LabelFrame(self.images_frame, text="Obraz Oryginalny")
        frame_original.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.lbl_original = tk.Label(frame_original, text="Brak obrazu")
        self.lbl_original.pack(expand=True)

        frame_processed = ttk.LabelFrame(self.images_frame, text="Obraz Przetworzony")
        frame_processed.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.lbl_processed = tk.Label(frame_processed, text="Brak obrazu")
        self.lbl_processed.pack(expand=True)

        frame_analysis = ttk.LabelFrame(self.images_frame, text="Analiza Obrazu")
        frame_analysis.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.lbl_analysis_placeholder = tk.Label(frame_analysis, text="Wczytaj obraz")
        self.lbl_analysis_placeholder.pack(expand=True)

        self.figure = Figure(figsize=(3, 4), dpi=100)
        
        self.ax_image = self.figure.add_subplot(2, 1, 1)
        
        divider = make_axes_locatable(self.ax_image)
        self.ax_proj_h = divider.append_axes("top", size="20%", pad=0.05)
        self.ax_proj_v = divider.append_axes("right", size="20%", pad=0.05)

        self.ax_hist = self.figure.add_subplot(2, 1, 2)
        
       
        self.figure.subplots_adjust(hspace=0.5, bottom=0.15, top=0.9, left=0.1, right=0.9)

        self.canvas = FigureCanvasTkAgg(self.figure, master=frame_analysis)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.analysis_is_packed = False
    def create_tool_option(self, text, dict_key):
        cb = ttk.Checkbutton(self.tools_frame, text=text, variable=self.active_filters[dict_key], command=self.trigger_update)
        cb.pack(anchor=tk.W, pady=2)

    def create_tool_option_with_slider(self, text, dict_key, min_val, max_val, default_val, resolution=1):
        frame = ttk.Frame(self.tools_frame)
        frame.pack(fill=tk.X, pady=5)
        
        cb = ttk.Checkbutton(frame, text=text, variable=self.active_filters[dict_key], command=self.trigger_update)
        cb.pack(anchor=tk.W)
        
        slider = tk.Scale(frame, from_=min_val, to=max_val, resolution=resolution, orient=tk.HORIZONTAL, 
                          variable=self.filter_params[dict_key], command=lambda _: self.trigger_update())
        slider.pack(fill=tk.X, padx=20)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.original_image_pil = Image.open(file_path)
            self.processed_image_pil = self.original_image_pil.copy()
            self.display_image(self.original_image_pil, self.lbl_original)
            self.display_image(self.processed_image_pil, self.lbl_processed)
            self.trigger_update()

    def display_image(self, img_pil, label_widget):
        img_copy = img_pil.copy()
        img_copy.thumbnail((400, 500)) 
        img_tk = ImageTk.PhotoImage(img_copy)
        label_widget.config(image=img_tk, text="")
        label_widget.image = img_tk 

    def save_image(self):
        if self.processed_image_pil is None: return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            self.processed_image_pil.save(file_path)

    def reset_to_original(self):
        for var in self.active_filters.values():
            var.set(False)
        self.filter_params['brightness'].set(0.0)
        self.filter_params['contrast'].set(1.0)
        self.filter_params['gamma'].set(1.0)
        self.filter_params['binarization'].set(128.0)
        self.filter_params['gauss'].set(2)
        self.filter_params['laplace'].set(1.0)
        self.filter_params['blur'].set(1)
        self.trigger_update()

    def get_image_array(self):
        if self.original_image_pil is None: return None
        img = self.original_image_pil.convert('RGB')
        return np.array(img, dtype=np.float32)
    

    
    
    def manual_3x3_blur(self, image_array,level):
        image=image_array.copy()
        for _ in range(level):
            result = np.zeros_like(image, dtype=np.float32)
            padded = np.pad(image, pad_width=((1, 1), (1, 1), (0, 0)), mode='edge')
            sum_array = (
                padded[0:-2, 0:-2] + padded[0:-2, 1:-1] + padded[0:-2, 2:] +
                padded[1:-1, 0:-2] + padded[1:-1, 1:-1] + padded[1:-1, 2:] +
                padded[2:,   0:-2] + padded[2:,   1:-1] + padded[2:,   2:]
            )
            result = sum_array / 9.0
            image= result
        return result
    
    def gaussian(self, image_array,b=2):
        result = np.zeros_like(image_array, dtype=np.float32)
        padded = np.pad(image_array, pad_width=((1, 1), (1, 1), (0, 0)), mode='edge')
        sum_array = (
            padded[0:-2, 0:-2] + b*padded[0:-2, 1:-1] + padded[0:-2, 2:] +
            b*padded[1:-1, 0:-2] + b*b*padded[1:-1, 1:-1] + b*padded[1:-1, 2:] +
            padded[2:,   0:-2] + b*padded[2:,   1:-1] + padded[2:,   2:]  
        )
        result=sum_array/(b+2)**2
        return result
    
    def laplace(self, image_array,c=1):
        result = np.zeros_like(image_array, dtype=np.float32)
        padded = np.pad(image_array, pad_width=((1, 1), (1, 1), (0, 0)), mode='edge')
        sum_array = (
            -1*padded[0:-2, 0:-2] + -1*padded[0:-2, 1:-1] + -1*padded[0:-2, 2:] +
            -1*padded[1:-1, 0:-2] + 8*padded[1:-1, 1:-1] + -1*padded[1:-1, 2:] +
            -1*padded[2:,   0:-2] + -1*padded[2:,   1:-1] + -1*padded[2:,   2:]
        )
        result = c*sum_array+image_array
        return result
    
    def roberts_cross(self, image_array):
        padded = np.pad(image_array, pad_width=((0, 1), (0, 1), (0, 0)), mode='edge')
        
        P_00 = padded[:-1, :-1]
        P_01 = padded[:-1, 1:]
        P_10 = padded[1:, :-1]
        P_11 = padded[1:, 1:]

        Gx = P_00 - P_11
        Gy = P_01 - P_10

        magnitude = np.sqrt(Gx**2 + Gy**2)
        return magnitude

    def sobel_operator(self, image_array):
        padded = np.pad(image_array, pad_width=((1, 1), (1, 1), (0, 0)), mode='edge')
        Gx = (
            -1.0 * padded[0:-2, 0:-2] + 0.0 + 1.0 * padded[0:-2, 2:] +
            -2.0 * padded[1:-1, 0:-2] + 0.0 + 2.0 * padded[1:-1, 2:] +
            -1.0 * padded[2:,   0:-2] + 0.0 + 1.0 * padded[2:,   2:]
        )
        
        Gy = (
            -1.0 * padded[0:-2, 0:-2] - 2.0 * padded[0:-2, 1:-1] - 1.0 * padded[0:-2, 2:] +
             0.0 + 0.0 + 0.0 +
             1.0 * padded[2:,   0:-2] + 2.0 * padded[2:,   1:-1] + 1.0 * padded[2:,   2:]
        )

        magnitude = np.sqrt(Gx**2 + Gy**2)
        return magnitude
    
    def update_analysis_layout(self, image_array):
        
        if not self.analysis_is_packed:
            self.lbl_analysis_placeholder.pack_forget() 
            self.canvas_widget.pack(fill=tk.BOTH, expand=True) 
            self.analysis_is_packed = True

        self.ax_image.clear()
        self.ax_proj_h.clear()
        self.ax_proj_v.clear()
        self.ax_hist.clear()

        img_uint8 = np.clip(image_array, 0, 255).astype(np.uint8)

        self.ax_image.imshow(img_uint8)
        self.ax_image.axis('off')

        if len(img_uint8.shape) == 3:
            gray = 0.299 * img_uint8[:,:,0] + 0.587 * img_uint8[:,:,1] + 0.114 * img_uint8[:,:,2]
        else:
            gray = img_uint8.astype(np.float32)

        inverted_gray = 255.0 - gray
        proj_h = np.sum(inverted_gray, axis=0) 
        proj_v = np.sum(inverted_gray, axis=1) 

        self.ax_proj_h.fill_between(range(len(proj_h)), proj_h, color='black')
        self.ax_proj_h.set_xlim(self.ax_image.get_xlim())
        self.ax_proj_h.axis('off') 
        self.ax_proj_h.set_title("Projekcja $P_h$", fontsize=9)

        self.ax_proj_v.fill_betweenx(range(len(proj_v)), proj_v, color='black')
        self.ax_proj_v.set_ylim(self.ax_image.get_ylim())
        self.ax_proj_v.axis('off')
        self.ax_proj_v.set_title("Projekcja $P_v$", fontsize=9, loc='left')

        bin_edges = np.arange(0, 260, 5) 
        colors = ('red', 'green', 'blue')
        
        for i, color in enumerate(colors):
            channel_data = img_uint8[:, :, i]
            counts, _ = np.histogram(channel_data, bins=bin_edges)
            self.ax_hist.bar(bin_edges[:-1], counts, width=5, color=color, alpha=0.5, align='edge', edgecolor='none')

        self.ax_hist.set_xlim([0, 255])
        self.ax_hist.set_title("Histogram RGB")
        self.ax_hist.set_xlabel("Wartość (0-255)", fontsize=8)
        self.ax_hist.set_ylabel("Piksele", fontsize=8)
        self.ax_hist.tick_params(axis='both', which='major', labelsize=8)
        self.ax_hist.grid(True, linestyle='--', alpha=0.3)

        self.canvas.draw()

    def trigger_update(self):
        img_array = self.get_image_array()
        if img_array is None: return

        work_array = np.copy(img_array)

        if self.active_filters['grayscale'].get():
            gray = 0.299 * work_array[:,:,0] + 0.587 * work_array[:,:,1] + 0.114 * work_array[:,:,2]
            work_array = np.stack([gray, gray, gray], axis=-1)

        if self.active_filters['blur'].get():
            level=self.filter_params['blur'].get()
            work_array = self.manual_3x3_blur(work_array, level)
            
        if self.active_filters['gauss'].get():
            b = self.filter_params['gauss'].get()
            work_array = self.gaussian(work_array, b)
            
        if self.active_filters['laplace'].get():
            c = self.filter_params['laplace'].get()
            work_array = self.laplace(work_array, c)
            
        if self.active_filters['roberts'].get():
            work_array = self.roberts_cross(work_array)
            
        if self.active_filters['sobel'].get():
            work_array = self.sobel_operator(work_array)

        if self.active_filters['brightness'].get():
            offset = self.filter_params['brightness'].get()
            work_array = work_array + offset

        if self.active_filters['contrast'].get():
            factor = self.filter_params['contrast'].get()
            work_array = factor * (work_array - 128.0) + 128.0

        if self.active_filters['gamma'].get():
            gamma_val = self.filter_params['gamma'].get()
            work_array = np.clip(work_array, 0, 255) 
            normalized = work_array / 255.0
            work_array = np.power(normalized, 1.0 / gamma_val) * 255.0

        if self.active_filters['negative'].get():
            work_array = np.clip(work_array, 0, 255) 
            work_array = 255.0 - work_array

        if self.active_filters['binarization'].get():
            threshold = self.filter_params['binarization'].get()
            temp_gray = 0.299 * work_array[:,:,0] + 0.587 * work_array[:,:,1] + 0.114 * work_array[:,:,2]
            binary_mask = np.where(temp_gray < threshold, 0.0, 255.0)
            work_array = np.stack([binary_mask, binary_mask, binary_mask], axis=-1)

        final_array = np.clip(work_array, 0, 255).astype(np.uint8)
        
        self.update_analysis_layout(final_array)
        
        self.processed_image_pil = Image.fromarray(final_array)
        self.display_image(self.processed_image_pil, self.lbl_processed)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()