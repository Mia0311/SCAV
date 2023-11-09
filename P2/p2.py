import subprocess
import json
import sys
import os

# change to the correct path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from P1.rgb_yuv import rgb_to_yuv

# Task 1
def mp4_to_mp2(input_file, output_file):
    # ffmpeg -i input.mp4 -c:a mp2 output.mp2
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-c:a", "mp2",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Converted video saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error while converting video: {e}")

def parse_video_info(input_file):
    cmd = ["ffmpeg", "-i", input_file]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = result.stderr
        return info
    except subprocess.CalledProcessError as e:
        print(f"Error while parsing video info: {e}")
        return None

# Task 2
def resolution(input_file, output_file, width, height):
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
    except subprocess.CalledProcessError as e:
        print(f"Error while modifying resolution: {e}")

#Task 3
def chroma_subsampling(input_file, output_file, chroma_sub):
    # ffmpeg -i input.mp4 -c:v libx264 -vf format=yuv420p output.mp4
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"format=yuv{chroma_sub}p",
        "-y",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Chroma subsampling changed and video saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error while changing chroma subsampling: {e}")

#Task 4
def print_info(input_file):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-select_streams", "v:0",
        "-show_entries",
        "format=start_time,duration,size,bit_rate,probe_score,tags",
        input_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Information printed")
    except subprocess.CalledProcessError as e:
        print(f"Error while printing information: {e}")

def main():
    print("########## Task 1 ##########")
    input_video = "BBB_Original.mp4"
    output_video = "BBB.mp2"

    #mp4_to_mp2(input_video, output_video)
    #video_info = parse_video_info(output_video)
    #if video_info:
     #   print("Video Information:")
      #  print(video_info)

    print("########## Task 2 ##########")
    output_video2 = "BBB_resolution_modified.mp4"
    resolution(input_video, output_video2, 640, 680)

    print("########## Task 3 ##########")
    output_video3 = "BBB_chroma_sub.mp4"
    chroma_subsampling(input_video, output_video3, 420)

    print("########## Task 4 ##########")
    print_info(input_video)

    print("########## Task 5 ##########")
    r, g, b = 255, 0, 0
    y, u, v = rgb_to_yuv(r, g, b)
    print(f"RGB: ({r}, {g}, {b})")
    print(f"YUV: ({y}, {u}, {v})")

if __name__ == "__main__":
    main()
