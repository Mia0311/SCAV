import subprocess

class YUVHistogram:
    def yuv_histogram(self, input_video, output_histogram):
        # ffplay BBB_50.mp4 -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay"
        cmd = [
            "ffmpeg",
            "-i", input_video,
            "-vf", "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay",
            "-y",  # Overwrite output file if it exists
            output_histogram
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"YUV histogram extracted and saved to {output_histogram}")
        except subprocess.CalledProcessError as e:
            print(f"Error while extracting YUV histogram: {e}")


