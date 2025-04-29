import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=[("All Files", "*.*")]
    )
    if file_paths:
        files.clear()
        files.extend(file_paths)
        update_file_list()

def update_file_list():
    listbox.delete(0, tk.END)
    for file in files:
        listbox.insert(tk.END, os.path.basename(file))

def remove_selected_file():
    selected_file_index = listbox.curselection()
    if selected_file_index:
        files.pop(selected_file_index[0])
        update_file_list()

def select_destination_folder():
    global destination_folder
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if destination_folder:
        destination_folder_label.config(text=f"Destination Folder: {destination_folder}")

def update_file_size_preview():
    selected_file_index = listbox.curselection()
    if selected_file_index and destination_folder:
        file = files[selected_file_index[0]]
        output_file = os.path.join(destination_folder, os.path.splitext(os.path.basename(file))[0] + f'.{format_var.get()}')

        # Generar un archivo temporal para obtener su tamaño
        temp_output = os.path.join(destination_folder, "temp_preview_file.gif")

        # Ejecutar ffmpeg para generar una muestra corta (5 segundos) y obtener una estimación
        command = f'ffmpeg -i "{file}" -t 5 -vf "fps={fps_var.get()},scale={scale_var.get()}" -y "{temp_output}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            size_preview_label.config(text=f"Error: {result.stderr}")
        else:
            # Obtener el tamaño del archivo temporal
            estimated_size_bytes = os.path.getsize(temp_output)
            estimated_size_kb = estimated_size_bytes / 1024
            estimated_size_mb = estimated_size_kb / 1024

            # Mostrar el tamaño estimado
            size_preview_label.config(text=f"Estimated Size: {estimated_size_kb:.2f} KB ({estimated_size_mb:.2f} MB)")

            # Eliminar el archivo temporal después de la estimación
            os.remove(temp_output)

def convert_files():
    if not files:
        messagebox.showerror("Error", "No files selected.")
        return
    if not destination_folder:
        messagebox.showerror("Error", "No destination folder selected.")
        return

    file_format = format_var.get()
    fps = fps_var.get()
    scale = scale_var.get()

    progress_bar['value'] = 0
    app.update_idletasks()

    total_files = len(files)
    for i, file in enumerate(files):
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        output_file = os.path.join(destination_folder, os.path.splitext(os.path.basename(file))[0] + f'.{file_format}')

        if file_format == 'gif':
            command = f'ffmpeg -i "{file}" -vf "fps={fps},scale={scale}" -y "{output_file}"'
        elif file_format == 'jpg':
            command = f'ffmpeg -i "{file}" -vf "scale={scale}" -y "{output_file}"'
        elif file_format in ['mp4', 'avif']:
            command = f'ffmpeg -i "{file}" -vf "fps={fps},scale={scale}" -y "{output_file}"'
        else:
            command = f'ffmpeg -i "{file}" -y "{output_file}"'

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error processing file {file}: {result.stderr}")
        else:
            print(f"Successfully processed file {file}")

        progress_bar['value'] = (i + 1) / total_files * 100
        app.update_idletasks()

    messagebox.showinfo("Success", "Files converted successfully!")

# Setup GUI
app = tk.Tk()
app.title("File Converter")
app.geometry("600x400")

files = []
destination_folder = None

frame = tk.Frame(app)
frame.pack(pady=10)

listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50, height=10)
listbox.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

button_frame = tk.Frame(app)
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text="Select Files", command=select_files)
select_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(button_frame, text="Remove Selected", command=remove_selected_file)
remove_button.pack(side=tk.LEFT, padx=5)

preview_button = tk.Button(button_frame, text="Preview Size", command=update_file_size_preview)
preview_button.pack(side=tk.LEFT, padx=5)

convert_button = tk.Button(button_frame, text="Convert", command=convert_files)
convert_button.pack(side=tk.LEFT, padx=5)

destination_button = tk.Button(button_frame, text="Select Destination Folder", command=select_destination_folder)
destination_button.pack(side=tk.LEFT, padx=5)

destination_folder_label = tk.Label(button_frame, text="Destination Folder: Not Selected", bg="lightgray", width=50, height=2)
destination_folder_label.pack(side=tk.LEFT, padx=5)

format_var = tk.StringVar(value='gif')
format_frame = tk.Frame(app)
format_frame.pack(pady=10)

tk.Label(format_frame, text="Select Format:").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(format_frame, text="GIF", variable=format_var, value='gif').pack(side=tk.LEFT, padx=5)
tk.Radiobutton(format_frame, text="JPG", variable=format_var, value='jpg').pack(side=tk.LEFT, padx=5)
tk.Radiobutton(format_frame, text="MP4", variable=format_var, value='mp4').pack(side=tk.LEFT, padx=5)
tk.Radiobutton(format_frame, text="AVIF", variable=format_var, value='avif').pack(side=tk.LEFT, padx=5)

fps_var = tk.IntVar(value=30)
fps_frame = tk.Frame(app)
fps_frame.pack(pady=10)

tk.Label(fps_frame, text="FPS:").pack(side=tk.LEFT, padx=5)
fps_entry = tk.Entry(fps_frame, textvariable=fps_var, width=5)
fps_entry.pack(side=tk.LEFT, padx=5)

scale_var = tk.StringVar(value='360:640')
scale_frame = tk.Frame(app)
scale_frame.pack(pady=10)

tk.Label(scale_frame, text="Scale (WxH):").pack(side=tk.LEFT, padx=5)
scale_entry = tk.Entry(scale_frame, textvariable=scale_var, width=10)
scale_entry.pack(side=tk.LEFT, padx=5)

size_preview_frame = tk.Frame(app)
size_preview_frame.pack(pady=10)

size_preview_label = tk.Label(size_preview_frame, text="Estimated Size: N/A", bg="lightgray", width=50, height=2)
size_preview_label.pack()

progress_bar = Progressbar(app, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=10)

app.mainloop()
