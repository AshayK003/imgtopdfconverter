import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Canvas, Scrollbar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageTk
import os
import threading

class ImagetoPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.outputpdfname = tk.StringVar()
        self.output_pdf_path = None

        self.initialize_ui()

    def initialize_ui(self):
        self.root.configure(bg='#2E2E2E')

        # Main Frame
        main_frame = tk.Frame(self.root, bg='#2E2E2E')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="Image to PDF Converter", font=("Helvetica", 18, "bold"), bg='#2E2E2E', fg='#FFFFFF')
        title_label.pack(pady=10)

        # Select Images Button
        select_images_button = tk.Button(main_frame, text="Select Images", command=self.select_images, bg='#555555', fg='#FFFFFF', font=("Helvetica", 12))
        select_images_button.pack(pady=(0, 10))

        # Selected Images Treeview
        self.treeview_frame = tk.Frame(main_frame, bg='#2E2E2E')
        self.treeview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.treeview = ttk.Treeview(self.treeview_frame, columns=('Name', 'Path'), show='headings', selectmode='none')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Path', text='Path')
        self.treeview.column('Name', anchor='center')
        self.treeview.column('Path', anchor='center')
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Treeview Style
        style = ttk.Style()
        style.configure('Treeview', background='#333333', foreground='#FFFFFF', fieldbackground='#333333', font=('Helvetica', 10))
        style.configure('Treeview.Heading', background='#444444', foreground='#000000', font=('Helvetica', 12, 'bold'))

        # Preview Label
        preview_label = tk.Label(main_frame, text="Preview", bg='#2E2E2E', fg='#FFFFFF', font=("Helvetica", 12, "bold"))
        preview_label.pack()

        # Image Preview Canvas in a Scrollable Frame
        preview_frame = tk.Frame(main_frame, bg='#2E2E2E')
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = Canvas(preview_frame, bg='#333333', height=200)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(preview_frame, orient="vertical", command=self.canvas.xview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        self.preview_container = tk.Frame(self.canvas, bg='#333333')
        self.canvas.create_window((0, 0), window=self.preview_container, anchor="nw")

        # Output PDF Name
        label = tk.Label(main_frame, text="Enter output PDF name", bg='#2E2E2E', fg='#FFFFFF', font=("Helvetica", 12))
        label.pack()

        pdf_name_entry = tk.Entry(main_frame, textvariable=self.outputpdfname, width=40, justify='center', bg='#444444', fg='#FFFFFF', font=("Helvetica", 12), insertbackground='#FFFFFF')
        pdf_name_entry.pack(pady=(0, 10))

        # Convert Button
        convert_button = tk.Button(main_frame, text="Convert to PDF!", command=self.ask_save_location, bg='#555555', fg='#FFFFFF', font=("Helvetica", 12, "bold"))
        convert_button.pack(pady=(20, 10))

        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=(10, 20))

        # Status Label
        self.status_label = tk.Label(main_frame, text="", bg='#2E2E2E', fg='#FFFFFF', font=("Helvetica", 12))
        self.status_label.pack()

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()
        self.preview_images()

    def update_selected_images_listbox(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.treeview.insert('', 'end', values=(image_name, image_path))

    def preview_images(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()

        if self.image_paths:
            thumb_size = 100
            for idx, image_path in enumerate(self.image_paths):
                img = Image.open(image_path)
                img.thumbnail((thumb_size, thumb_size))
                img_tk = ImageTk.PhotoImage(img)

                thumb_label = tk.Label(self.preview_container, image=img_tk, bg='#333333')
                thumb_label.image = img_tk
                thumb_label.grid(row=0, column=idx, padx=5, pady=5)

    def ask_save_location(self):
        if not self.image_paths:
            messagebox.showerror("Error", "No images selected!")
            return
        
        default_name = self.outputpdfname.get() + ".pdf" if self.outputpdfname.get() else "output.pdf"
        save_location = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=default_name)
        if save_location:
            self.output_pdf_path = save_location
            self.start_conversion()

    def start_conversion(self):
        thread = threading.Thread(target=self.convert_images_to_pdf)
        thread.start()

    def convert_images_to_pdf(self):
        if not self.image_paths or not self.output_pdf_path:
            return

        pdf = canvas.Canvas(self.output_pdf_path, pagesize=letter)

        self.progress['value'] = 0
        total_images = len(self.image_paths)

        for idx, image_path in enumerate(self.image_paths):
            try:
                img = Image.open(image_path)
                available_width, available_height = letter
                scale_factor = min(available_width / img.width, available_height / img.height)
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)
                x_centered = (available_width - new_width) / 2
                y_centered = (available_height - new_height) / 2
                pdf.setFillColorRGB(1, 1, 1)
                pdf.rect(0, 0, available_width, available_height, fill=True)
                pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
                pdf.showPage()

                self.progress['value'] = (idx + 1) / total_images * 100
                self.status_label.config(text=f"Processing image {idx + 1} of {total_images}")
                self.root.update_idletasks()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image {image_path}: {e}")

        pdf.save()
        self.progress['value'] = 100
        self.status_label.config(text="Conversion completed!")
        messagebox.showinfo("Info", "PDF created successfully!")

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImagetoPDFConverter(root)
    root.geometry("600x800")
    root.mainloop()

if __name__ == "__main__":
    main()
