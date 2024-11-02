import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def select_video_with_audio():
    global video_with_audio_path
    video_with_audio_path = filedialog.askopenfilename(title="Select Video with Desired Audio")
    if video_with_audio_path:
        label_video_with_audio.config(text=f"Selected: {video_with_audio_path}")

def select_video_other():
    global video_other_path
    video_other_path = filedialog.askopenfilename(title="Select Video to Replace Audio")
    if video_other_path:
        label_video_other.config(text=f"Selected: {video_other_path}")

def select_output_directory():
    global output_directory
    output_directory = filedialog.askdirectory(title="Select Directory to Save Output Video")
    if output_directory:
        label_output_directory.config(text=f"Selected: {output_directory}")

def start_process():
    try:
        if not video_with_audio_path or not video_other_path or not output_directory:
            messagebox.showerror("Error", "Please select all required files and directory.")
            return

        output_video_path = os.path.join(output_directory, "output_video.mp4")

        spinner.start()

        def run_ffmpeg_commands():
            os.system(f"ffmpeg -i '{video_other_path}' -i '{video_with_audio_path}' -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_video_path}'")
            spinner.stop()
            messagebox.showinfo("Process Complete", "Audio replaced successfully!")

        app.after(100, run_ffmpeg_commands)
    except NameError as e:
        messagebox.showerror("Error", f"Variable not defined: {e}")

app = tk.Tk()
app.title("Audio Swop")

label_instruction = tk.Label(app, text="Select the video file with desired audio, the video to replace audio, and the directory to save the output.")
label_instruction.pack(pady=10)

button_video_with_audio = tk.Button(app, text="Select Video with Desired Audio", command=select_video_with_audio)
button_video_with_audio.pack(pady=5)

label_video_with_audio = tk.Label(app, text="No file selected")
label_video_with_audio.pack(pady=5)

button_video_other = tk.Button(app, text="Select Video to Replace Audio", command=select_video_other)
button_video_other.pack(pady=5)

label_video_other = tk.Label(app, text="No file selected")
label_video_other.pack(pady=5)

button_output_directory = tk.Button(app, text="Select Directory to Save Output Video", command=select_output_directory)
button_output_directory.pack(pady=5)

label_output_directory = tk.Label(app, text="No directory selected")
label_output_directory.pack(pady=5)

start_button = tk.Button(app, text="Start Process", command=start_process, bg="green", fg="white")
start_button.pack(pady=5)

spinner = ttk.Progressbar(app, mode='indeterminate')
spinner.pack(pady=5)

app.geometry("500x400")
app.mainloop()