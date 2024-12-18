import os
from tkinter import Tk, Label, Entry, Button, filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip

def split_videos_in_folder(input_folder, output_folder, start_time, end_time):
    """
    :param input_folder:
    :param output_folder:
    :param start_time:
    :param end_time:
    """
    try:

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.endswith((".mp4", ".avi", ".mov", ".mkv")):
                input_path = os.path.join(input_folder, filename)
                
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_cropped{ext}"
                output_path = os.path.join(output_folder, output_filename)
                
                print(f"Runing: {filename}")
                video = VideoFileClip(input_path)
                
                video_duration = video.duration
                actual_end_time = min(end_time, video_duration)
                
                if start_time >= actual_end_time:
                    print(f"Error: Start time ({start_time}s) is set larger than the original video ({video_duration}s). Skip....")
                    continue
                
                trimmed_video = video.subclip(start_time, actual_end_time)
                trimmed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
                
        print("Done!")
    except Exception as e:
        print(f"Lỗi: {e}")

# Tkinter
def select_input_folder():
    folder = filedialog.askdirectory()
    input_folder_entry.delete(0, "end")
    input_folder_entry.insert(0, folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    output_folder_entry.delete(0, "end")
    output_folder_entry.insert(0, folder)

def process_videos():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    start_time = int(start_time_entry.get())
    end_time = int(end_time_entry.get())
    
    if not input_folder or not output_folder:
        print("Please select input and output foldert!")
        return
    
    split_videos_in_folder(input_folder, output_folder, start_time, end_time)

root = Tk()
root.title("Split Video - sharevina.com ")

Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_folder_entry = Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Open", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
Button(root, text="Open", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

Label(root, text="Start Time (Second):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
start_time_entry = Entry(root, width=20)
start_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

Label(root, text="End Time (Second):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
end_time_entry = Entry(root, width=20)
end_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

Button(root, text="Start", command=process_videos).grid(row=4, column=1, pady=10)

root.mainloop()
