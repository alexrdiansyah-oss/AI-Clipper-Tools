import json
import re


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
# SIGNAL WORDS
# =========================

curiosity_words = [
    "ternyata",
    "rahasia",
    "kenapa",
    "alasan",
    "fakta",
    "masalah",
    "solusi"
]

hook_words = [
    "jangan",
    "cara",
    "tips",
    "kesalahan",
    "paling",
    "terbesar",
    "penting"
]

emotional_words = [
    "gagal",
    "salah",
    "takut",
    "kaget",
    "bahaya",
    "parah",
    "menyesal",
    "untung"
]


# =========================
# CONFIGURATION
# =========================

MIN_DURATION = 20
TARGET_DURATION = 40
MAX_DURATION = 60


# =========================
# SCORE TEXT
# =========================

def calculate_text_score(text):

    text_lower = text.lower()

    score = 0
    signals = []


    # =========================
    # QUESTION
    # =========================

    if "?" in text:

        score += 1
        signals.append("question")


    # =========================
    # CURIOSITY
    # =========================

    matched_curiosity = []

    for word in curiosity_words:

        if word in text_lower:

            matched_curiosity.append(word)


    if matched_curiosity:

        score += 2
        signals.append("curiosity")


    # =========================
    # HOOK
    # =========================

    matched_hook = []

    for word in hook_words:

        if word in text_lower:

            matched_hook.append(word)


    if matched_hook:

        score += 2
        signals.append("hook")


    # =========================
    # NUMBER
    # =========================

    if re.search(r"\d+", text):

        score += 1
        signals.append("number")


    # =========================
    # EMOTION
    # =========================

    matched_emotional = []

    for word in emotional_words:

        if word in text_lower:

            matched_emotional.append(word)


    if matched_emotional:

        score += 2
        signals.append("emotion")


    # =========================
    # CONTENT DENSITY
    # =========================

    words = text_lower.split()

    if len(words) >= 20:

        score += 1
        signals.append("content_density")


    if len(words) >= 40:

        score += 1
        signals.append("rich_content")


    # =========================
    # FILLER PENALTY
    # =========================

    filler_words = [
        "iya",
        "oh",
        "apa tuh",
        "gak",
        "nggak",
        "coba",
        "udah",
        "mas",
        "guys"
    ]

    filler_count = 0

    for word in filler_words:

        filler_count += text_lower.count(
            word
        )


    # Banyak filler → kurangi score

    if filler_count >= 8:

        score -= 2
        signals.append("heavy_filler")

    elif filler_count >= 5:

        score -= 1
        signals.append("filler")


    return score, signals

# =========================
# FIND INTERESTING SEGMENTS
# =========================

interesting_segments = []


for i, segment in enumerate(segments):

    text = segment["text"].strip()

    score, signals = calculate_text_score(
        text
    )

    if score > 0:

        interesting_segments.append({

            "index": i,

            "score": score,

            "signals": signals

        })


# =========================
# BUILD CLIP WINDOW
# =========================

candidates = []


for item in interesting_segments:

    center_index = item["index"]

    center_segment = segments[
        center_index
    ]

    center_start = center_segment[
        "start"
    ]

    center_end = center_segment[
        "end"
    ]


    # --------------------------------
    # Start from the interesting segment
    # --------------------------------

    start_index = center_index

    end_index = center_index


    # --------------------------------
    # Expand backwards
    # --------------------------------

    while start_index > 0:

        current_duration = (
            segments[end_index]["end"]
            - segments[start_index]["start"]
        )

        if current_duration >= TARGET_DURATION:

            break

        start_index -= 1


    # --------------------------------
    # Expand forwards
    # --------------------------------

    while end_index < len(segments) - 1:

        current_duration = (
            segments[end_index]["end"]
            - segments[start_index]["start"]
        )

        if current_duration >= TARGET_DURATION:

            break

        end_index += 1


    # --------------------------------
    # Calculate final duration
    # --------------------------------

    start = segments[
        start_index
    ]["start"]

    end = segments[
        end_index
    ]["end"]

    duration = end - start


    # --------------------------------
    # Reject bad duration
    # --------------------------------

    if duration < MIN_DURATION:

        continue

    if duration > MAX_DURATION:

        end = start + MAX_DURATION

        duration = MAX_DURATION


    # --------------------------------
    # Combine text
    # --------------------------------

    clip_segments = segments[
        start_index:end_index + 1
    ]

    text_parts = []

    for segment in clip_segments:

        text_parts.append(
            segment["text"].strip()
        )


    text = " ".join(text_parts)


    # --------------------------------
    # Calculate total score
    # --------------------------------

    total_score, signals = calculate_text_score(
        text
    )


    # Give extra weight to the
    # original interesting segment

    total_score += item["score"]


    # --------------------------------
    # Create candidate
    # --------------------------------

    candidate = {

        "start": round(start, 2),

        "end": round(end, 2),

        "duration": round(
            duration,
            2
        ),

        "text": text,

        "score": total_score,

        "signals": signals,

        "trigger_segment": center_segment[
            "text"
        ].strip()

    }


    candidates.append(candidate)


# =========================
# REMOVE DUPLICATES
# =========================

unique_candidates = []


for candidate in candidates:

    is_duplicate = False


    for existing in unique_candidates:

        overlap_start = max(
            candidate["start"],
            existing["start"]
        )

        overlap_end = min(
            candidate["end"],
            existing["end"]
        )


        if overlap_end > overlap_start:

            overlap = (
                overlap_end
                - overlap_start
            )

            candidate_duration = (
                candidate["end"]
                - candidate["start"]
            )


            overlap_ratio = (
                overlap
                / candidate_duration
            )


            if overlap_ratio > 0.7:

                is_duplicate = True

                break


    if not is_duplicate:

        unique_candidates.append(
            candidate
        )


# =========================
# SORT BY SCORE
# =========================

unique_candidates.sort(
    key=lambda x: x["score"],
    reverse=True
)


# =========================
# SHOW RESULTS
# =========================

print()
print("==============================")
print("AI CLIP WINDOW BUILDER")
print("==============================")

print(
    "Interesting segments:",
    len(interesting_segments)
)

print(
    "Clip candidates:",
    len(unique_candidates)
)


for i, candidate in enumerate(
    unique_candidates[:10]
):

    print()
    print(
        "Clip",
        i + 1
    )

    print(
        "Start:",
        candidate["start"]
    )

    print(
        "End:",
        candidate["end"]
    )

    print(
        "Duration:",
        candidate["duration"],
        "detik"
    )

    print(
        "Score:",
        candidate["score"]
    )

    print(
        "Signals:",
        ", ".join(
            candidate["signals"]
        )
    )

    print(
        "Trigger:",
        candidate["trigger_segment"]
    )

    print(
        "Text:",
        candidate["text"]
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
        unique_candidates,
        file,
        ensure_ascii=False,
        indent=4
    )


print()
print(
    "Hasil disimpan ke "
    "clip_candidates.json"
)