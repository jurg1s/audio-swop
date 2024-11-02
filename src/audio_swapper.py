import os
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_audio():
    video_path = filedialog.askopenfilename(title="Select Video with Your Language")
    if not video_path:
        return

    audio_output_path = "audio_in_your_language.mp3"
    os.system(f"ffmpeg -i '{video_path}' -q:a 0 -map a '{audio_output_path}'")

    messagebox.showinfo("Extraction Complete", "Audio extracted successfully!")

def replace_audio():
    video_foreign_path = filedialog.askopenfilename(title="Select Foreign Language Video")
    if not video_foreign_path:
        return

    audio_input_path = "audio_in_your_language.mp3"
    output_video_path = "output_video.mp4"
    if not os.path.exists(audio_input_path):
        messagebox.showerror("Error", "Extracted audio file not found. Please extract audio first.")
        return

    os.system(f"ffmpeg -i '{video_foreign_path}' -i '{audio_input_path}' -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_video_path}'")

    messagebox.showinfo("Replacement Complete", "Audio replaced successfully!")

app = tk.Tk()
app.title("Audio Swop")

label = tk.Label(app, text="Select videos to replace foreign audio with your language")
label.pack(pady=10)

extract_button = tk.Button(app, text="Extract Audio", command=extract_audio)
extract_button.pack(pady=5)

replace_button = tk.Button(app, text="Replace Audio", command=replace_audio)
replace_button.pack(pady=5)

app.geometry("400x150")
app.mainloop()
