import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk

class Modifier:
    def resolution(self, input_file, output_file, width, height):
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"scale={width}:{height}",
            "-y",
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Video resolution modified and saved to {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error while modifying resolution: {e}")

    # make sure to have the libvpx library installed
    # sudo apt-get install libvpx-dev
    # sudo apt-get install libx265-dev
    # sudo apt-get install libaom-dev
    # ./configure --enable-libvpx --enable-libx265 --enable-libaom --enable-gpl
    # make
    # sudo make install

    def encoder_modifier(self, input_file, output_file, encoder):
        if encoder == "vp8":
# ffmpeg -i BBB_Original.mp4 -c:v libvpx -b:v 2M -strict -2 output_vp8.webm
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libvpx",
                "-b:v", "2M",
                "-strict", "-2",
                "-y",
                f"{output_file}_vp8.webm"
            ]

        elif encoder == "vp9":
# ffmpeg -i BBB_Original.mp4 -c:v libvpx-vp9 -b:v 2M -strict -2 output_vp9.webm
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libvpx-vp9",
                "-b:v", "2M",
                "-strict", "-2",
                "-y",
                f"{output_file}_vp9.webm"
            ]

        elif encoder == "h265":
# ffmpeg -i BBB_Original.mp4 -c:v libx265 -c:a aac output_h265.mp4
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libx265",
                "-c:a", "aac",
                "-y",
                f"{output_file}_h265.mp4"
            ]

        elif encoder == "av1":
        # NOT WORKING (EXTREMELY SLOW)
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libaom-av1",
                "-b:v", "2M",
                "-c:a", "aac",
                "-y",
                f"{output_file}_av1.mp4"
            ]
            #return f"{output_file}_av1.mp4"

        try:
            subprocess.run(cmd, check=True)
            print(f"Encoder modified")
        except subprocess.CalledProcessError as e:
            print(f"Error while modifying encoder: {e}")

    def encoder_comparison(self, input_file, encoders, output_file):
        # ffmpeg -i left -i right -filter_complex hstack output.mp4
        vp8 = "BBB_encoder_vp8.webm"
        vp9 = "BBB_encoder_vp9.webm"
        h265 = "BBB_encoder_h265.mp4"

        if encoders == "vp8 & vp9":
            if not (os.path.exists(vp8)):
                print(f"No vp8 video found, convert using previous option first!")
            if not (os.path.exists(vp9)):
                print(f"No vp9 video found, convert using previous option first!")
            else:
                cmd = [
                    "ffmpeg",
                    "-i", vp8,
                    "-i", vp9,
                    "-filter_complex", "hstack",
                    "-y",
                    f"{output_file}_{encoders}.mp4"
                ]

        elif encoders == "vp8 & h265":
            if not (os.path.exists(vp8)):
                print(f"No vp8 video found, convert using previous option first!")
            if not (os.path.exists(h265)):
                print(f"No h265 video found, convert using previous option first!")
            else:
                cmd = [
                    "ffmpeg",
                    "-i", vp8,
                    "-i", h265,
                    "-filter_complex", "hstack",
                    "-y",
                    f"{output_file}_{encoders}.mp4"
                ]

        elif encoders == "vp9 & h265":
            if not (os.path.exists(vp9)):
                print(f"No vp9 video found, convert using previous option first!")
            if not (os.path.exists(h265)):
                print(f"No h265 video found, convert using previous option first!")
            else:
                cmd = [
                    "ffmpeg",
                    "-i", vp9,
                    "-i", h265,
                    "-filter_complex", "hstack",
                    "-y",
                    f"{output_file}_{encoders}.mp4"
                ]
        try:
            subprocess.run(cmd, check=True)
            print(f"Encoder comparison video saved to {output_file}_{encoders}.mp4")
        except subprocess.CalledProcessError as e:
            print(f"Error while creating encoder comparison video: {e}")


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Modifier GUI")
        self.modifier = Modifier()

        # Menu options
        resolutions = ["720p", "480p", "360x240", "160x120"]
        encoders = ["vp8", "vp9", "h265"]
        encoder_comparisons = ["vp8 & vp9", "vp8 & h265", "vp9 & h265"]

        self.resolution_label = ttk.Label(root, text="Resolution:")
        self.resolution_var = tk.StringVar(value=resolutions[0])
        self.resolution_dropdown = ttk.Combobox(root, textvariable=self.resolution_var, values=resolutions)

        self.encoder_label = ttk.Label(root, text="Encoder:")
        self.encoder_var = tk.StringVar(value=encoders[0])
        self.encoder_dropdown = ttk.Combobox(root, textvariable=self.encoder_var, values=encoders)

        self.encoder_comparison_label = ttk.Label(root, text="Encoders Comparison:")
        self.encoder_comparison_var = tk.StringVar(value=encoder_comparisons[0])
        self.encoder_comparison_dropdown = ttk.Combobox(root, textvariable=self.encoder_comparison_var, values=encoder_comparisons)

        self.resolution_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.resolution_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.encoder_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.encoder_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.encoder_comparison_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.encoder_comparison_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.resolution_button = ttk.Button(root, text="Execute", command=self.execute_resolution)
        self.resolution_button.grid(row=0, column=2, pady=10)

        self.encoder_button = ttk.Button(root, text="Execute", command=self.execute_encoder)
        self.encoder_button.grid(row=1, column=2, pady=10)

        self.encoder_comparison_button = ttk.Button(root, text="Execute",
                                                    command=self.execute_encoder_comparison)
        self.encoder_comparison_button.grid(row=2, column=2, pady=10)
    def execute_resolution(self):
        input_video = "BBB_Original.mp4"
        output_file = "BBB_resolution"
        resolution = self.resolution_var.get()
        if resolution:
            width, height = self.get_resolution_dimensions(resolution)
            output_video = f"{output_file}_{resolution}.mp4"
            self.modifier.resolution(input_video, output_video, width, height)

    def execute_encoder(self):
        input_video = "BBB_Original.mp4"
        output_file = "BBB_encoder"
        encoder = self.encoder_var.get()
        if encoder:
            output_encoder = f"{output_file}"
            self.modifier.encoder_modifier(input_video, output_encoder, encoder)

    def execute_encoder_comparison(self):
        input_video = "BBB_Original.mp4"
        output_file = "BBB_encoders"
        encoder_comparison = self.encoder_comparison_var.get()
        if encoder_comparison:
            output_comparison = f"{output_file}_comparison"
            self.modifier.encoder_comparison(input_video, encoder_comparison, output_comparison)

    def get_resolution_dimensions(self, resolution):
        if resolution == "720p":
            return 1280, 720
        elif resolution == "480p":
            return 640, 480
        elif resolution == "360x240":
            return 360, 240
        elif resolution == "160x120":
            return 160, 120
        else:
            return 0, 0

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
