import whisper
import json
import os
import time


VIDEO_PATH = "input/video.mp4"
OUTPUT_PATH = "transcript.json"


print()
print("======================================")
print("        AI VIDEO TRANSCRIBER")
print("======================================")
print()

# ======================================
# CEK FILE
# ======================================

if not os.path.exists(VIDEO_PATH):
    print("ERROR: Video tidak ditemukan!")
    print("File:", VIDEO_PATH)
    exit()


# ======================================
# LOAD MODEL
# ======================================

print("Memuat model Whisper...")
start_time = time.time()

model = whisper.load_model("base")

model_time = time.time() - start_time

print(f"Model siap ({model_time:.1f} detik)")
print()


# ======================================
# TRANSKRIPSI
# ======================================

print("======================================")
print("MULAI TRANSKRIPSI")
print("======================================")
print()

print("Video :", VIDEO_PATH)
print("Model : Whisper Base")
print("Bahasa: Indonesia")
print()

print("Whisper sedang memproses video...")
print("Mohon tunggu...")
print()


start_time = time.time()

result = model.transcribe(
    VIDEO_PATH,
    language="id",
    word_timestamps=True,
    fp16=False
)

transcription_time = time.time() - start_time


# ======================================
# PROSES HASIL
# ======================================

segments = []

for segment in result["segments"]:

    words = []

    for word in segment.get("words", []):

        words.append({
            "word": word["word"].strip(),
            "start": word["start"],
            "end": word["end"]
        })

    data = {
        "start": segment["start"],
        "end": segment["end"],
        "text": segment["text"].strip(),
        "words": words
    }

    segments.append(data)


# ======================================
# SAVE
# ======================================

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        segments,
        file,
        ensure_ascii=False,
        indent=4
    )


# ======================================
# STATISTIK
# ======================================

total_words = sum(
    len(segment["words"])
    for segment in segments
)

total_segments = len(segments)


# ======================================
# HASIL
# ======================================

print()
print("======================================")
print("TRANSKRIPSI SELESAI")
print("======================================")

print(f"Segment        : {total_segments}")
print(f"Word timestamp : {total_words}")
print(f"Waktu proses   : {transcription_time / 60:.1f} menit")
print(f"File           : {OUTPUT_PATH}")

print("======================================")
