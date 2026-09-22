import json
import os


TRANSCRIPT_PATH = "transcript.json"
CLIPS_PATH = "top_clips.json"
OUTPUT_DIR = "output/subtitles"

WORDS_PER_SUBTITLE = 4
MAX_GAP = 0.6
MAX_DURATION = 2.5


os.makedirs(OUTPUT_DIR, exist_ok=True)


def format_time(seconds):
    """
    Mengubah detik menjadi format SRT:
    HH:MM:SS,mmm
    """

    milliseconds = int(round(seconds * 1000))

    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000

    minutes = milliseconds // 60_000
    milliseconds %= 60_000

    secs = milliseconds // 1000
    milliseconds %= 1000

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


# =========================
# LOAD DATA
# =========================

with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as file:
    transcript = json.load(file)


with open(CLIPS_PATH, "r", encoding="utf-8") as file:
    clips = json.load(file)


# =========================
# PROSES SETIAP CLIP
# =========================

for clip_number, clip in enumerate(clips, start=1):

    clip_start = clip["start"]
    clip_end = clip["end"]
    clip_duration = clip_end - clip_start

    words = []

    # Ambil semua word yang masuk ke dalam clip
    for segment in transcript:

        for word in segment.get("words", []):

            word_start = word.get("start")
            word_end = word.get("end")
            word_text = word.get("word", "").strip()

            if word_start is None or word_end is None:
                continue

            if not word_text:
                continue

            # Word overlap dengan clip
            if word_end > clip_start and word_start < clip_end:

                relative_start = max(
                    word_start - clip_start,
                    0
                )

                relative_end = min(
                    word_end - clip_start,
                    clip_duration
                )

                words.append({
                    "word": word_text,
                    "start": relative_start,
                    "end": relative_end
                })


    # =========================
    # GROUP WORD
    # =========================

    subtitles = []

    current_words = []

    for word in words:

        if not current_words:
            current_words.append(word)
            continue

        first_start = current_words[0]["start"]
        last_end = current_words[-1]["end"]

        gap = word["start"] - last_end
        duration = word["end"] - first_start

        # Jika terlalu banyak kata,
        # gap terlalu panjang,
        # atau subtitle terlalu lama
        if (
            len(current_words) >= WORDS_PER_SUBTITLE
            or gap > MAX_GAP
            or duration > MAX_DURATION
        ):

            subtitles.append(current_words)

            current_words = [word]

        else:
            current_words.append(word)


    if current_words:
        subtitles.append(current_words)


    # =========================
    # BUAT FILE SRT
    # =========================

    srt_lines = []

    subtitle_index = 1

    for group in subtitles:

        text = " ".join(
            word["word"]
            for word in group
        )

        start = group[0]["start"]
        end = group[-1]["end"]

        # Pastikan tidak keluar dari durasi video
        start = max(start, 0)
        end = min(end, clip_duration)

        if end <= start:
            continue

        srt_lines.append(
            str(subtitle_index)
        )

        srt_lines.append(
            f"{format_time(start)} --> {format_time(end)}"
        )

        srt_lines.append(text)

        srt_lines.append("")

        subtitle_index += 1


    # =========================
    # SAVE
    # =========================

    output_path = os.path.join(
        OUTPUT_DIR,
        f"clip_{clip_number:02d}.srt"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(srt_lines)
        )


print()
print("======================================")
print("SUBTITLE WORD TIMESTAMP SELESAI")
print("======================================")
print("Output:", OUTPUT_DIR)