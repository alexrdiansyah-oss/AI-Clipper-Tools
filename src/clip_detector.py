import json


# =========================
# LOAD TRANSCRIPT
# =========================

with open(
    "transcript.json",
    "r",
    encoding="utf-8"
) as file:

    segments = json.load(file)


# =========================
# KEYWORDS
# =========================

keywords = [
    "kesalahan",
    "rahasia",
    "ternyata",
    "jangan",
    "cara",
    "kenapa",
    "tips",
    "paling",
    "terbesar",
    "penting",
    "masalah",
    "solusi"
]


# =========================
# FIND INTERESTING SEGMENTS
# =========================

candidates = []


for segment in segments:

    text = segment["text"].lower()

    matched_keywords = []

    for keyword in keywords:

        if keyword in text:
            matched_keywords.append(keyword)


    if matched_keywords:

        candidate = {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            "keywords": matched_keywords
        }

        candidates.append(candidate)


# =========================
# SHOW RESULTS
# =========================

print("\n==============================")
print("CANDIDATE CLIPS")
print("==============================")

print("Jumlah kandidat:", len(candidates))


for i, candidate in enumerate(candidates):

    print("\nClip", i + 1)

    print(
        "Start:",
        round(candidate["start"], 2)
    )

    print(
        "End:",
        round(candidate["end"], 2)
    )

    print(
        "Text:",
        candidate["text"]
    )

    print(
        "Keywords:",
        candidate["keywords"]
    )


# =========================
# SAVE RESULT
# =========================

with open(
    "clip_candidates.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        candidates,
        file,
        ensure_ascii=False,
        indent=4
    )


print("\nHasil disimpan ke clip_candidates.json")