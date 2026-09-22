import os
import subprocess


VIDEO_DIR = "output/shorts"
SUBTITLE_DIR = "output/subtitles"
OUTPUT_DIR = "output/final"

os.makedirs(OUTPUT_DIR, exist_ok=True)


videos = [
    file
    for file in os.listdir(VIDEO_DIR)
    if file.endswith(".mp4")
]


for video_file in videos:

    video_path = os.path.join(
        VIDEO_DIR,
        video_file
    )

    base_name = os.path.splitext(video_file)[0]

    subtitle_file = base_name + ".srt"

    subtitle_path = os.path.join(
        SUBTITLE_DIR,
        subtitle_file
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        video_file
    )


    # Jika subtitle tidak ditemukan
    if not os.path.exists(subtitle_path):
        print(f"Subtitle tidak ditemukan: {subtitle_file}")
        continue


    print()
    print("======================================")
    print(f"Processing: {video_file}")
    print("======================================")


    # Format path untuk FFmpeg
    subtitle_path_ffmpeg = (
        subtitle_path
        .replace("\\", "/")
        .replace(":", "\\:")
    )


    # ======================================
    # SUBTITLE STYLE
    # ======================================

    subtitle_style = (
        "FontName=Arial,"
        "FontSize=14,"
        "Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=2,"
        "Shadow=1,"
        "Alignment=2,"
        "MarginV=70"
    )


    # ======================================
    # FFMPEG
    # ======================================

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vf",
        f"subtitles={subtitle_path_ffmpeg}:force_style='{subtitle_style}'",
        "-c:a",
        "copy",
        output_path
    ]


    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )


    if result.returncode == 0:

        print("✓ Berhasil")
        print("Output:", output_path)

    else:

        print("✗ Gagal")
        print(result.stderr)


print()
print("======================================")
print("SEMUA SUBTITLE SELESAI")
print("======================================")
print("Folder:", OUTPUT_DIR)