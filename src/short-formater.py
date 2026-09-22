import os
from moviepy import VideoFileClip


# =====================================
# CONFIG
# =====================================

INPUT_DIR = "output"
OUTPUT_DIR = "output/shorts"

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920


# =====================================
# CREATE OUTPUT FOLDER
# =====================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =====================================
# FIND VIDEO FILES
# =====================================

files = [
    file
    for file in os.listdir(INPUT_DIR)
    if file.endswith(".mp4")
    and not file.startswith("shorts")
]


print()
print("======================================")
print("SHORTS FORMATTER")
print("======================================")

print("Jumlah video:", len(files))


# =====================================
# PROCESS VIDEOS
# =====================================

for file in files:

    input_path = os.path.join(
        INPUT_DIR,
        file
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        file
    )

    print()
    print("--------------------------------------")
    print("Processing:", file)


    # =================================
    # LOAD VIDEO
    # =================================

    video = VideoFileClip(input_path)


    # =================================
    # CALCULATE SCALE
    # =================================

    original_width = video.w
    original_height = video.h

    target_ratio = TARGET_WIDTH / TARGET_HEIGHT
    original_ratio = original_width / original_height


    # =================================
    # RESIZE
    # =================================

    if original_ratio > target_ratio:

        # Video terlalu lebar
        new_height = TARGET_HEIGHT
        new_width = int(
            original_width
            * TARGET_HEIGHT
            / original_height
        )

    else:

        # Video terlalu tinggi
        new_width = TARGET_WIDTH
        new_height = int(
            original_height
            * TARGET_WIDTH
            / original_width
        )


    video = video.resized(
        width=new_width,
        height=new_height
    )


    # =================================
    # CENTER CROP
    # =================================

    x_center = video.w / 2
    y_center = video.h / 2

    x1 = int(
        x_center - TARGET_WIDTH / 2
    )

    y1 = int(
        y_center - TARGET_HEIGHT / 2
    )

    x2 = x1 + TARGET_WIDTH
    y2 = y1 + TARGET_HEIGHT


    video = video.cropped(
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2
    )


    # =================================
    # EXPORT
    # =================================

    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )


    video.close()


print()
print("======================================")
print("SHORTS FORMAT SELESAI")
print("======================================")

print("Output:", OUTPUT_DIR)