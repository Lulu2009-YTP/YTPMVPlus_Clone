import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, CompositeVideoClip
from pydub import AudioSegment
from moviepy.video.fx.all import rotate
from moviepy.video.fx.all import fadein, fadeout, mirror_x, mirror_y

class YTPMVCloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YTPMV+ Clone")
        
        # Browse and select source files
        self.label = tk.Label(root, text="Select Video File:")
        self.label.pack()
        
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(root, text="Browse Video", command=self.browse_video)
        self.browse_button.pack()

        # Browse audio
        self.audio_label = tk.Label(root, text="Select Audio File:")
        self.audio_label.pack()

        self.audio_entry = tk.Entry(root, width=50)
        self.audio_entry.pack()

        self.browse_audio_button = tk.Button(root, text="Browse Audio", command=self.browse_audio)
        self.browse_audio_button.pack()

        # Plugin Options (Checkbuttons)
        self.checkerboard_var = tk.IntVar()
        self.cylinder_var = tk.IntVar()
        self.flip_var = tk.IntVar()
        
        self.checkerboard_check = tk.Checkbutton(root, text="Checkerboard", variable=self.checkerboard_var)
        self.checkerboard_check.pack()

        self.cylinder_check = tk.Checkbutton(root, text="CC Cylinder", variable=self.cylinder_var)
        self.cylinder_check.pack()

        self.flip_check = tk.Checkbutton(root, text="Automatic Screen Flip", variable=self.flip_var)
        self.flip_check.pack()

        # Process Button
        self.process_button = tk.Button(root, text="Process", command=self.process_video)
        self.process_button.pack()

    def browse_video(self):
        video_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if video_file:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, video_file)
    
    def browse_audio(self):
        audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if audio_file:
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, audio_file)

    def process_video(self):
        video_path = self.file_entry.get()
        audio_path = self.audio_entry.get()

        if not video_path or not audio_path:
            messagebox.showerror("Error", "Please select both video and audio files")
            return

        try:
            # Load video and audio
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioSegment.from_file(audio_path)

            # Apply effects based on user input
            if self.checkerboard_var.get():
                video_clip = self.apply_checkerboard_effect(video_clip)
            
            if self.cylinder_var.get():
                video_clip = self.apply_cylinder_effect(video_clip)
            
            if self.flip_var.get():
                video_clip = self.apply_flip_effect(video_clip)

            # Export the final video
            output_path = "output_ytpmv.mp4"
            video_clip.write_videofile(output_path, audio=audio_path)
            
            messagebox.showinfo("Success", "Video processed successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def apply_checkerboard_effect(self, video_clip):
        # Example checkerboard effect using mirror
        return mirror_x(mirror_y(video_clip))

    def apply_cylinder_effect(self, video_clip):
        # Rotate the video to create a cylinder-like effect
        return rotate(video_clip, angle=45)

    def apply_flip_effect(self, video_clip):
        # Flip the video at intervals
        flipped = video_clip.fl_time(lambda t: -t, apply_to=['video'])
        return CompositeVideoClip([flipped])

if __name__ == "__main__":
    root = tk.Tk()
    app = YTPMVCloneApp(root)
    root.mainloop()
