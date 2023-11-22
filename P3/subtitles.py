import requests
import subprocess

class Subtitles:
    def download_subtitles(self, subtitle_url, output_file):
        try:
            response = requests.get(subtitle_url)
            response.raise_for_status()

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Subtitles downloaded successfully to {output_file}")
        except requests.RequestException as e:
            print(f"Error while downloading subtitles: {e}")

    def integrate_subtitles(self, video_file, subtitle_file, output_file):
        # need to have libass library installed
        # ffmpeg -i BBB_50.mp4 -vf subtitles=subtitles.srt output_srt.mp4
        cmd = [
            "ffmpeg",
            "-i", video_file,
            "-vf", f"subtitles={subtitle_file}",
            "-y",
            output_file
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Video with subtitles saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error while integrating subtitles: {e}")

def main():
    processor = Subtitles()
    #subtitle_url = "https://raw.githubusercontent.com/moust/MediaPlayer/master/demo/subtitles.srt"
    #subtitle = "subtitles.srt"
    #processor.download_subtitles(subtitle_url, subtitle)

    #input_video = "BBB_50.mp4"
    #output_video = "BBB_50_subtitles.mp4"
    #processor.integrate_subtitles(input_video, subtitle, output_video)

if __name__ == "__main__":
    main()
