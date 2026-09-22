import json
import requests
import time
from pathlib import Path


# ============================================
# AI CLIP RANKER
# Ollama + Qwen 2.5 7B
# ============================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

INPUT_FILE = "top_clips.json"
OUTPUT_FILE = "ranked_clips.json"

TOP_CANDIDATES = 50


def ask_ollama(clip):
    """
    Mengirim satu kandidat clip ke Qwen.
    """

    prompt = f"""
Kamu adalah AI Video Clip Editor.

Tugas kamu adalah menilai apakah sebuah potongan video cocok
dijadikan YouTube Shorts, TikTok, atau Instagram Reels.

Nilai berdasarkan:

1. Hook
   Apakah awal clip menarik perhatian?

2. Curiosity
   Apakah membuat penonton ingin terus menonton?

3. Emotion
   Apakah terdapat emosi, kejutan, konflik, humor, atau reaksi?

4. Story
   Apakah clip mempunyai cerita atau momen yang jelas?

5. Standalone
   Apakah clip masih masuk akal tanpa mengetahui video panjangnya?

6. Short Potential
   Apakah cocok dijadikan video pendek?

Berikan nilai 1-10 untuk setiap kategori.

PENTING:
- Jangan menilai berdasarkan panjang saja.
- Jangan memberikan nilai tinggi hanya karena ada kata seperti
  "jangan", "kenapa", "bahaya", atau angka.
- Perhatikan konteks percakapan.
- Transkrip mungkin memiliki kesalahan dari speech recognition.
- Tetap coba pahami maksud pembicara.
- Jika transkrip sangat kacau atau tidak mempunyai konteks,
  berikan nilai lebih rendah.

CLIP:

Start: {clip["start"]}
End: {clip["end"]}
Duration: {clip["duration"]} detik

Transcript:
{clip["text"]}

Balas HANYA dalam JSON valid dengan format:

{{
    "score": 0,
    "hook": 0,
    "curiosity": 0,
    "emotion": 0,
    "story": 0,
    "standalone": 0,
    "short_potential": 0,
    "reason": "alasan singkat",
    "title": "judul pendek yang menarik"
}}

Score adalah nilai keseluruhan 1-10.
"""


    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return json.loads(data["response"])

    except Exception as e:

        print(f"ERROR Ollama: {e}")

        return None


def main():

    print("=" * 60)
    print("        AI CLIP RANKER")
    print("        Ollama + Qwen 2.5 7B")
    print("=" * 60)

    # ----------------------------------------
    # Load candidates
    # ----------------------------------------

    if not Path(INPUT_FILE).exists():

        print(f"\nERROR: {INPUT_FILE} tidak ditemukan.")

        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    print(f"\nTotal candidates : {len(candidates)}")

    # ----------------------------------------
    # Ambil kandidat awal
    # ----------------------------------------

    candidates = candidates[:TOP_CANDIDATES]

    print(f"AI evaluation    : {len(candidates)}")
    print()

    ranked = []

    # ----------------------------------------
    # AI Evaluation
    # ----------------------------------------

    for i, clip in enumerate(candidates, 1):

        print("-" * 60)
        print(f"[{i}/{len(candidates)}] Evaluating clip")
        print(
            f"Start: {clip['start']:.2f} | "
            f"End: {clip['end']:.2f} | "
            f"Duration: {clip['duration']:.2f}s"
        )

        result = ask_ollama(clip)

        if result is None:

            print("AI evaluation gagal.")
            continue

        # Gabungkan data original + hasil AI

        ranked_clip = {
            **clip,
            "ai_score": result.get("score", 0),
            "hook_score": result.get("hook", 0),
            "curiosity_score": result.get("curiosity", 0),
            "emotion_score": result.get("emotion", 0),
            "story_score": result.get("story", 0),
            "standalone_score": result.get("standalone", 0),
            "short_potential_score": result.get(
                "short_potential", 0
            ),
            "ai_reason": result.get("reason", ""),
            "title": result.get("title", "")
        }

        ranked.append(ranked_clip)

        print(
            f"AI Score : {ranked_clip['ai_score']}/10"
        )

        print(
            f"Title    : {ranked_clip['title']}"
        )

        print(
            f"Reason   : {ranked_clip['ai_reason']}"
        )

        # Sedikit jeda supaya komputer tidak terlalu terbebani

        time.sleep(0.2)

    # ----------------------------------------
    # Sort berdasarkan AI score
    # ----------------------------------------

    ranked.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    # ----------------------------------------
    # Simpan hasil
    # ----------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            ranked,
            f,
            indent=2,
            ensure_ascii=False
        )

    # ----------------------------------------
    # Display Top 10
    # ----------------------------------------

    print("\n")
    print("=" * 60)
    print("             TOP 10 AI CLIPS")
    print("=" * 60)

    for i, clip in enumerate(ranked[:10], 1):

        print()
        print(f"Clip #{i}")
        print(
            f"AI Score : {clip['ai_score']}/10"
        )
        print(
            f"Start    : {clip['start']:.2f}"
        )
        print(
            f"End      : {clip['end']:.2f}"
        )
        print(
            f"Duration : {clip['duration']:.2f}s"
        )
        print(
            f"Title    : {clip['title']}"
        )
        print(
            f"Reason   : {clip['ai_reason']}"
        )

    print()
    print("=" * 60)
    print(f"Hasil disimpan ke: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()