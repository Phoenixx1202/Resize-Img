import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Redimensionamento de Imagens")

        # Configuração do Notebook (agora com apenas uma guia)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Guia para redimensionamento de imagens em lote
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Versão 1.1")

        # Label de informações do programa
        label_text = "Programa criado por: @Phoenixx1202"
        bold_font = ('Arial', 12, 'bold')
        label = tk.Label(root, text=label_text, background='light blue', font=bold_font)
        label.pack(side="bottom", pady=10)

        # Redimensionador de Imagens em Lote
        tk.Label(self.tab2, text="Redimensionador de Imagens", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.tab2, text="Tipos Suportados (PNG ou JPEG):").pack()
        self.file_listbox = tk.Listbox(self.tab2, selectmode=tk.MULTIPLE, height=5, width=80)
        self.file_listbox.pack(pady=5, padx=10)

        tk.Button(self.tab2, text="Adicionar Imagens", command=self.add_images).pack()

        # Checkbox para TrimuiSmartPro
        self.trimui_var = tk.BooleanVar()
        self.trimui_checkbox = tk.Checkbutton(self.tab2, text="Trimui Smart Pro", variable=self.trimui_var, command=self.toggle_trimui)
        self.trimui_checkbox.pack()

        # Widgets para entrada de largura e altura
        self.dimension_frame = tk.Frame(self.tab2)
        self.dimension_frame.pack()

        self.width_label = tk.Label(self.dimension_frame, text="Largura:")
        self.width_label.grid(row=0, column=0)

        self.width_entry = tk.Entry(self.dimension_frame)
        self.width_entry.grid(row=0, column=1)

        self.height_label = tk.Label(self.dimension_frame, text="Altura:")
        self.height_label.grid(row=1, column=0)

        self.height_entry = tk.Entry(self.dimension_frame)
        self.height_entry.grid(row=1, column=1)

        tk.Button(self.tab2, text="Selecionar Pasta de Destino", command=self.select_output_folder).pack()

        # Frame para os checkboxes de seleção do formato de saída
        output_format_frame = tk.Frame(self.tab2)
        output_format_frame.pack(pady=5)

        output_format_label = tk.Label(output_format_frame, text="Tipo de Saída:")
        output_format_label.pack(side=tk.LEFT)

        self.output_format_var = tk.StringVar(value='PNG')
        self.png_checkbox = tk.Radiobutton(output_format_frame, text=".PNG", variable=self.output_format_var, value='PNG')
        self.jpg_checkbox = tk.Radiobutton(output_format_frame, text=".JPG", variable=self.output_format_var, value='JPG')
        self.png_checkbox.pack(side=tk.LEFT, padx=5)
        self.jpg_checkbox.pack(side=tk.LEFT, padx=5)

        tk.Button(self.tab2, text="Redimensionar Imagens", command=self.resize_images).pack(pady=10)

        self.progress = ttk.Progressbar(self.tab2, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack()

        self.result_label = tk.Label(self.tab2, text="")
        self.result_label.pack(pady=10)

        self.save_path_label = tk.Label(self.tab2, text="")
        self.save_path_label.pack(pady=10)

        self.output_folder = ""

    def toggle_trimui(self):
        if self.trimui_var.get():
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, "268")
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, "391")
            self.width_entry.config(state='disabled')
            self.height_entry.config(state='disabled')
            self.output_format_var.set('PNG')  # Selecionar .PNG por padrão
        else:
            self.width_entry.config(state='normal')
            self.height_entry.config(state='normal')
            self.width_entry.delete(0, tk.END)
            self.height_entry.delete(0, tk.END)

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("JPEG Files", "*.jpg"),("PNG Files", "*.png")])
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.save_path_label.config(text=f"Pasta de destino selecionada: {self.output_folder}")
        else:
            self.save_path_label.config(text="Nenhuma pasta de destino selecionada.")

    def resize_images(self):
        if self.trimui_var.get():
            width = 268
            height = 391
        else:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())

        if not self.output_folder:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de destino.")
            return

        output_images_folder = os.path.join(self.output_folder, 'imagens_redimensionadas')
        if not os.path.exists(output_images_folder):
            os.makedirs(output_images_folder)

        total_files = self.file_listbox.size()
        if total_files == 0:
            messagebox.showerror("Erro", "Por favor, selecione pelo menos uma imagem.")
            return

        self.progress['value'] = 0
        self.progress['maximum'] = total_files

        output_format = self.output_format_var.get().lower()
        for index in range(total_files):
            file_path = self.file_listbox.get(index)
            file_name = os.path.splitext(os.path.basename(file_path))[0] + f'.{output_format}'

            img = Image.open(file_path)
            img_resized = img.resize((width, height))

            output_file_path = os.path.join(output_images_folder, file_name)
            img_resized.save(output_file_path, format=output_format.upper())

            self.progress['value'] += 1
            self.progress.update()

        self.result_label.config(text=f"Imagens redimensionadas e salvas em {output_images_folder}")
        self.save_path_label.config(text=f"Imagens salvas em {output_images_folder}")
        messagebox.showinfo("Concluído", "Redimensionamento de imagens concluído e salvo.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x720")
    root.configure(bg='white')
    icon_path = 'C:/Users/USER/OneDrive/Imagens/teste.ico'
    root.iconbitmap(icon_path)
    app = ImageResizerApp(root)
    
    # Imagem do criador do programa
    image_path = 'C:/Users/USER/OneDrive/Imagens/test.png'
    if os.path.exists(image_path):
        image = tk.PhotoImage(file=image_path)
        image_label = tk.Label(root, image=image, background='white')
        image_label.pack(pady=10)

    root.mainloop()
