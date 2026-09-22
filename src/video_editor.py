import json
import os
from moviepy import VideoFileClip


# =====================================
# CONFIG
# =====================================

VIDEO_PATH = "input/video.mp4"
CLIPS_PATH = "top_clips.json"
OUTPUT_DIR = "output"


# =====================================
# CREATE OUTPUT FOLDER
# =====================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =====================================
# LOAD CLIP DATA
# =====================================

with open(CLIPS_PATH, "r", encoding="utf-8") as file:
    clips = json.load(file)


print()
print("======================================")
print("AI VIDEO CLIPPER")
print("======================================")

print("Jumlah clip:", len(clips))


# =====================================
# LOAD VIDEO
# =====================================

print()
print("Memuat video...")

video = VideoFileClip(VIDEO_PATH)

print("Video berhasil dimuat.")
print("Durasi video:", round(video.duration, 2), "detik")


# =====================================
# CREATE CLIPS
# =====================================

for i, clip_data in enumerate(clips):

    start = clip_data["start"]
    end = clip_data["end"]

    title = clip_data.get(
        "title",
        f"Clip {i + 1}"
    )


    print()
    print("--------------------------------------")
    print(f"Clip {i + 1}")
    print("Title :", title)
    print("Start :", start)
    print("End   :", end)


    # =================================
    # CUT VIDEO
    # =================================

    clip = video.subclipped(
        start,
        end
    )


    # =================================
    # OUTPUT FILE
    # =================================

    output_path = os.path.join(
        OUTPUT_DIR,
        f"clip_{i + 1:02d}.mp4"
    )


    print("Menyimpan:", output_path)


    # =================================
    # EXPORT
    # =================================

    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )


    clip.close()


# =====================================
# CLOSE VIDEO
# =====================================

video.close()


print()
print("======================================")
print("SEMUA CLIP SELESAI")
print("======================================")

print("Folder:", OUTPUT_DIR)