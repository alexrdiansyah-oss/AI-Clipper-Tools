import os


# ======================================
# PROJECT PATH
# ======================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ======================================
# INPUT
# ======================================

INPUT_DIR = os.path.join(
    BASE_DIR,
    "input"
)

VIDEO_PATH = os.path.join(
    INPUT_DIR,
    "video.mp4"
)


# ======================================
# OUTPUT
# ======================================

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

SHORTS_DIR = os.path.join(
    OUTPUT_DIR,
    "shorts"
)

SUBTITLE_DIR = os.path.join(
    OUTPUT_DIR,
    "subtitles"
)

FINAL_DIR = os.path.join(
    OUTPUT_DIR,
    "final"
)


# ======================================
# DATA
# ======================================

TRANSCRIPT_PATH = os.path.join(
    BASE_DIR,
    "transcript.json"
)

CLIP_CANDIDATES_PATH = os.path.join(
    BASE_DIR,
    "clip_candidates.json"
)

TOP_CLIPS_PATH = os.path.join(
    BASE_DIR,
    "top_clips.json"
)


# ======================================
# CREATE FOLDERS
# ======================================

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SHORTS_DIR, exist_ok=True)
os.makedirs(SUBTITLE_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)