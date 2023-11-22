import subprocess
import sys
import os

# change to the correct path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from P3.subtitles import Subtitles
from P3.yuv_histogram import YUVHistogram

class P3Main:
    # Task 1
    def motion_vectors(self, input_file, output_file):
        # ffmpeg -flags2 +export_mvs -i input.mp4 -vf codecview=mv=pf+bf+bb output.mp4
        cmd = [
            "ffmpeg",
            "-flags2",
            "+export_mvs",
            "-i", input_file,
            "-vf",
            "codecview=mv=pf+bf+bb",
            "-y",  # Overwrite output file if it exists
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Video showing motion vectors saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error while showing motion vectors: {e}")

    # Task 2 (we have to install libmp3lame encoder first)
    def container(self, input_file, output_file):
        # MP3 mono track
        mono_audio = "mono_audio.mp3"
        cmd_mono = [
            "ffmpeg",
            "-i", input_file,
            "-vn", "-ac", "1", "-ar", "44100",
            "-c:a", "libmp3lame",
            "-y",
            mono_audio
        ]

        # MP3 stereo lower bitrate
        stereo_audio = "stereo_audio.mp3"
        cmd_stereo = [
            "ffmpeg",
            "-i", input_file,
            "-vn", "-ac", "2", "-b:a", "64k",
            "-c:a", "libmp3lame",
            "-y",
            stereo_audio
        ]

        # audio in AAC codec
        aac_audio = "aac_audio.aac"
        cmd_aac = [
            "ffmpeg",
            "-i", input_file,
            "-vn", "-c:a", "aac", "-strict", "experimental",
            "-y",
            aac_audio
        ]

        # MP4 container
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-i", mono_audio,
            "-i", stereo_audio,
            "-i", aac_audio,
            "-filter_complex",
            "[1:a][2:a][3:a]concat=n=3:v=0:a=1[v]",
            "-map", "[v]",
            "-y",  # Overwrite output file if it exists
            output_file
        ]

        try:
            subprocess.run(cmd_mono, check=True)
            subprocess.run(cmd_stereo, check=True)
            subprocess.run(cmd_aac, check=True)
            subprocess.run(cmd, check=True)
            print(f"BBB container created and saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error while creating BBB container: {e}")

    # Task 3
    def count_tracks(self, input_file):
    # ffprobe -show_entries stream=channels -of compact=p=0:nk=1 -v 0 video.mp4
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_entries", "stream=channels:stream=codec_type",
            "-of", "compact=p=0:nk=1",
            "-v", "0",
            input_file
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            num_tracks = result.stdout.strip()
            print(f"Number of tracks: {num_tracks}")
        except subprocess.CalledProcessError as e:
            print(f"Error while printing information: {e}")


def main():
    # this lab needs to have both libass and libmp3lame enabled
    # ./configure --enable-libmp3lame --enable-libass
    # make
    # sudo make install
    processor = P3Main()
    print("########## Task 1 ##########")
    input_video = "BBB_Original.mp4"
    output_video = "BBB_motion_vectors.mp4"

    processor.motion_vectors(input_video, output_video)

    print("########## Task 2 ##########")
    input_video2 = "BBB_50.mp4"
    output_video2 = "BBB_Container.mp4"
    processor.container(input_video2, output_video2)

    print("########## Task 3 ##########")
    processor.count_tracks(output_video2)

    print("########## Task 4 & 5 ##########")
    processorSubtitles = Subtitles()
    subtitle_url = "https://raw.githubusercontent.com/moust/MediaPlayer/master/demo/subtitles.srt"
    subtitle = "subtitles.srt"
    processorSubtitles.download_subtitles(subtitle_url, subtitle)

    output_video3 = "BBB_50_subtitles.mp4"
    processorSubtitles.integrate_subtitles(input_video2, subtitle, output_video3)

    print("########## Task 6 ##########")
    processorHistogram = YUVHistogram()
    output_video4 = "BBB_50_Histogram.mp4"
    processorHistogram.yuv_histogram(input_video2, output_video4)

if __name__ == "__main__":
    main()
