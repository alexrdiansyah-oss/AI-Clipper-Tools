import json
import re


# =====================================
# LOAD CANDIDATES
# =====================================

with open(
    "clip_candidates.json",
    "r",
    encoding="utf-8"
) as file:

    candidates = json.load(file)


# =====================================
# CONFIGURATION
# =====================================

TOP_N = 10


# =====================================
# HELPER FUNCTIONS
# =====================================

def count_words(text):

    return len(
        text.split()
    )


def count_filler(text):

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

    text_lower = text.lower()

    count = 0

    for word in filler_words:

        count += text_lower.count(
            word
        )

    return count


def count_numbers(text):

    return len(
        re.findall(
            r"\d+",
            text
        )
    )


# =====================================
# CALCULATE RANKING SCORE
# =====================================

for candidate in candidates:

    text = candidate.get(
        "text",
        ""
    ).strip()

    signals = candidate.get(
        "signals",
        []
    )

    duration = candidate.get(
        "duration",
        0
    )


    # ---------------------------------
    # BASE SCORE
    # ---------------------------------

    detector_score = candidate.get(
        "score",
        0
    )

    score = detector_score


    # ---------------------------------
    # SIGNAL SCORE
    # ---------------------------------

    if "question" in signals:

        score += 1


    if "curiosity" in signals:

        score += 2


    if "hook" in signals:

        score += 2


    if "emotion" in signals:

        score += 2


    if "number" in signals:

        score += 1


    # ---------------------------------
    # CONTENT DENSITY
    # ---------------------------------

    word_count = count_words(
        text
    )

    candidate["word_count"] = word_count


    if word_count >= 40:

        score += 2

    elif word_count >= 20:

        score += 1

    # ---------------------------------
    # FILLER PENALTY
    # ---------------------------------

    filler_count = count_filler(
        text
    )

    candidate["filler_count"] = filler_count


    # ---------------------------------
    # FILLER RATIO
    # ---------------------------------

    if word_count > 0:

        filler_ratio = (
            filler_count
            / word_count
        )

    else:

        filler_ratio = 1


    candidate["filler_ratio"] = round(
        filler_ratio,
        3
    )


    # ---------------------------------
    # PENALTY BASED ON RATIO
    # ---------------------------------

    if filler_ratio >= 0.15:

        score -= 6

    elif filler_ratio >= 0.10:

        score -= 4

    elif filler_ratio >= 0.07:

        score -= 2

    elif filler_ratio >= 0.05:

        score -= 1


    # ---------------------------------
    # HEAVY FILLER PENALTY
    # ---------------------------------

    if filler_count >= 10:

        score -= 3

    elif filler_count >= 7:

        score -= 2


    # ---------------------------------
    # WEAK TRIGGER
    # ---------------------------------

    trigger = candidate.get(
        "trigger_segment",
        ""
    ).lower().strip()


    weak_triggers = [
        "apa tuh",
        "iya",
        "oh",
        "gak",
        "nggak",
        "coba",
        "udah",
        "mas",
        "guys",
        "jangan itu"
    ]


    if trigger in weak_triggers:

        score -= 4

    # ---------------------------------
    # NUMBER / INFORMATION BONUS
    # ---------------------------------

    number_count = count_numbers(
        text
    )

    candidate["number_count"] = number_count


    if number_count >= 2:

        score += 1


    # ---------------------------------
    # DURATION
    # ---------------------------------

    if 25 <= duration <= 45:

        score += 3

    elif 45 < duration <= 60:

        score += 2

    elif 20 <= duration < 25:

        score += 1

    elif duration < 15:

        score -= 2

    elif duration > 60:

        score -= 2


    # ---------------------------------
    # WEAK TRIGGER PENALTY
    # ---------------------------------

    trigger = candidate.get(
        "trigger_segment",
        ""
    ).lower()


    weak_triggers = [
        "apa tuh",
        "iya",
        "oh",
        "gak",
        "nggak",
        "coba",
        "udah",
        "mas"
    ]


    if trigger in weak_triggers:

        score -= 3


    # ---------------------------------
    # FINAL SCORE
    # ---------------------------------

    candidate["ranking_score"] = score


# =====================================
# SORT
# =====================================

candidates.sort(
    key=lambda x: x.get(
        "ranking_score",
        0
    ),
    reverse=True
)


# =====================================
# SMART DEDUPLICATION
# =====================================

selected = []


for candidate in candidates:

    candidate_start = candidate.get(
        "start",
        0
    )

    candidate_end = candidate.get(
        "end",
        0
    )

    is_overlap = False


    for existing in selected:

        existing_start = existing.get(
            "start",
            0
        )

        existing_end = existing.get(
            "end",
            0
        )


        # Calculate overlap

        overlap_start = max(
            candidate_start,
            existing_start
        )

        overlap_end = min(
            candidate_end,
            existing_end
        )


        if overlap_end > overlap_start:

            overlap_duration = (
                overlap_end
                - overlap_start
            )


            candidate_duration = (
                candidate_end
                - candidate_start
            )


            existing_duration = (
                existing_end
                - existing_start
            )


            smaller_duration = min(
                candidate_duration,
                existing_duration
            )


            if smaller_duration > 0:

                overlap_ratio = (
                    overlap_duration
                    / smaller_duration
                )


                if overlap_ratio >= 0.50:

                    is_overlap = True

                    break


    if not is_overlap:

        selected.append(
            candidate
        )


    if len(selected) >= TOP_N:

        break


# =====================================
# FINAL TOP CLIPS
# =====================================

top_candidates = selected


# =====================================
# DISPLAY
# =====================================

print()
print("======================================")
print("SMART CLIP RANKING")
print("======================================")

print(
    "Total candidates :",
    len(candidates)
)

print(
    "Selected clips   :",
    len(top_candidates)
)


for i, candidate in enumerate(
    top_candidates
):

    print()
    print(
        f"Rank {i + 1}"
    )

    print("--------------------------------------")

    print(
        "Ranking Score :",
        candidate.get(
            "ranking_score",
            0
        )
    )

    print(
        "Detector Score:",
        candidate.get(
            "score",
            0
        )
    )

    print(
        "Start         :",
        candidate.get(
            "start",
            0
        )
    )

    print(
        "End           :",
        candidate.get(
            "end",
            0
        )
    )

    print(
        "Duration      :",
        candidate.get(
            "duration",
            0
        ),
        "detik"
    )

    print(
        "Word Count    :",
        candidate.get(
            "word_count",
            0
        )
    )

    print(
        "Filler Count  :",
        candidate.get(
            "filler_count",
            0
        )
    )

    print(
    "Filler Ratio  :",
    candidate.get(
        "filler_ratio",
        0
        )
    )

    print(
        "Signals       :",
        ", ".join(
            candidate.get(
                "signals",
                []
            )
        )
    )

    print(
        "Trigger       :",
        candidate.get(
            "trigger_segment",
            ""
        )
    )

    print(
        "Text          :",
        candidate.get(
            "text",
            ""
        )
    )


# =====================================
# SAVE
# =====================================

with open(
    "top_clips.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        top_candidates,
        file,
        ensure_ascii=False,
        indent=4
    )


print()
print("======================================")
print("RANKING SELESAI")
print("======================================")

print(
    "Top clips:",
    len(top_candidates)
)

print(
    "File:",
    "top_clips.json"
)
