import json


# =====================================
# LOAD CANDIDATES
# =====================================

with open("clip_candidates.json", "r", encoding="utf-8") as file:
    candidates = json.load(file)


# =====================================
# WORDS THAT CAN CREATE CURIOSITY
# =====================================

curiosity_words = [
    "ternyata",
    "kenapa",
    "jangan-jangan",
    "rahasia",
    "masalah",
    "turun",
    "naik",
    "gagal",
    "berhasil",
    "nggak",
    "tidak",
    "belum",
    "paling",
    "terbesar",
    "pertama",
    "seribu",
    "juta"
]


# =====================================
# CALCULATE SCORE
# =====================================

for candidate in candidates:

    score = 0

    title = candidate.get("title", "").lower()
    hook = candidate.get("hook", "").lower()
    reason = candidate.get("reason", "").lower()

    text = title + " " + hook + " " + reason


    # =================================
    # CURIOSITY SCORE
    # =================================

    for word in curiosity_words:

        if word in text:
            score += 1


    # =================================
    # QUESTION SCORE
    # =================================

    if "?" in candidate.get("hook", ""):
        score += 2


    # =================================
    # NUMBER SCORE
    # =================================

    numbers = [
        "seribu",
        "juta",
        "ribu",
        "100",
        "1000"
    ]

    for number in numbers:

        if number in text:
            score += 2
            break


    # =================================
    # DURATION
    # =================================

    start = candidate.get("start", 0)
    end = candidate.get("end", 0)

    duration = end - start

    candidate["duration"] = round(duration, 2)


    # Ideal short-form duration
    if 20 <= duration <= 45:
        score += 3

    elif 45 < duration <= 60:
        score += 2

    elif 10 <= duration < 20:
        score += 1

    else:
        score -= 1

    # =================================
    # SAVE SCORE
    # =================================

    candidate["score"] = score


# =====================================
# SORT
# =====================================

candidates = sorted(
    candidates,
    key=lambda x: x["score"],
    reverse=True
)


# =====================================
# TOP 10
# =====================================

top_candidates = candidates[:10]


# =====================================
# DISPLAY
# =====================================

print()
print("======================================")
print("TOP 10 CLIP CANDIDATES")
print("====================================")

for i, candidate in enumerate(top_candidates):

    print()
    print(f"Rank {i + 1}")
    print("--------------------------------------")

    print("Score    :", candidate["score"])
    print("Title    :", candidate.get("title", ""))
    print("Start    :", candidate.get("start", 0))
    print("End      :", candidate.get("end", 0))
    print("Duration :", candidate.get("duration", 0), "detik")
    print("Hook     :", candidate.get("hook", ""))
    print("Reason   :", candidate.get("reason", ""))


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

print("Jumlah kandidat :", len(candidates))
print("Top clips       :", len(top_candidates))
print("File             : top_clips.json")