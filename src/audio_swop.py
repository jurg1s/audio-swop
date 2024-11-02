import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from datetime import datetime


def select_video_with_audio():
    global video_with_audio_path
    video_with_audio_path = filedialog.askopenfilename(title="Select Video with Desired Audio", filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if video_with_audio_path:
        label_video_with_audio.config(text=f"Selected: {video_with_audio_path}", fg="gray")

def select_video_other():
    global video_other_path
    video_other_path = filedialog.askopenfilename(title="Select Video to Replace Audio", filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
    if video_other_path:
        label_video_other.config(text=f"Selected: {video_other_path}", fg="gray")

def select_output_directory():
    global output_directory
    output_directory = filedialog.askdirectory(title="Select Directory to Save Output Video")
    if output_directory:
        label_output_directory.config(text=f"Selected: {output_directory}", fg="gray")

def run_ffmpeg_commands():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_video_path = os.path.join(output_directory, f"output_video_{timestamp}.mp4")
        os.system(f"ffmpeg -i '{video_other_path}' -i '{video_with_audio_path}' -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_video_path}'")
        messagebox.showinfo("Process Complete", "Audio replaced successfully!")
    finally:
        spinner.pack_forget()

def start_process():
    try:
        if not video_with_audio_path or not video_other_path or not output_directory:
            messagebox.showerror("Error", "Please select all required files and directory.")
            return

        spinner.pack(pady=5)
        spinner.start()

        # Run the ffmpeg command in a separate thread
        threading.Thread(target=run_ffmpeg_commands).start()
    except NameError as e:
        messagebox.showerror("Error", f"Variable not defined: {e}")

app = tk.Tk()
app.title("Audio Swop")
# app.configure(bg="white")

label_instruction = tk.Label(app, text="Select the video file with desired audio, the video to replace audio, and the directory to save the output 📼.", font=("Helvetica", 12), wraplength=400)
label_instruction.pack(pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(app, bg="whitesmoke", bd=1, relief="sunken", padx=10, pady=10)
button_frame.pack(pady=10)

button_video_with_audio = tk.Button(button_frame, text="Select Video with Desired Audio 🔊", command=select_video_with_audio)
button_video_with_audio.pack(pady=5)

label_video_with_audio = tk.Label(button_frame, text="No file selected", fg="gray", wraplength=400, bg="whitesmoke")
label_video_with_audio.pack(pady=5)

button_video_other = tk.Button(button_frame, text="Select Video to Replace Audio 🎞️", command=select_video_other)
button_video_other.pack(pady=5)

label_video_other = tk.Label(button_frame, text="No file selected", fg="gray", wraplength=400, bg="whitesmoke")
label_video_other.pack(pady=5)

button_output_directory = tk.Button(button_frame, text="Select Directory to Save Output Video 📁", command=select_output_directory)
button_output_directory.pack(pady=5)

label_output_directory = tk.Label(button_frame, text="No directory selected", fg="darkgray", wraplength=400, bg="whitesmoke")
label_output_directory.pack(pady=5)

start_button = tk.Button(button_frame, text="Start Process", command=start_process, bg="green", fg="whitesmoke", cursor="hand2")
start_button.pack(pady=5)

spinner = ttk.Progressbar(app, mode='indeterminate')

app.geometry("500x430")
app.mainloop()